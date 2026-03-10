import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import json
import time

from Models.risk_scenario import RiskScenario
from Models.role import Role
from Helpers.team_capacities import get_role_capacities
from analyzer import calculate_role_contracts
from analyzer import optimize_team_composition
from Models.role_cost import RoleCost

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA Y CONSTANTES
# ==========================================
st.set_page_config(page_title="CISO DSS - NICE Framework", layout="wide")

PRESUPUESTO_MAXIMO = 250000

st.title("🛡️ CISO Decision Support System (DSS)")
st.subheader("Optimización de Fuerza de Trabajo y Mitigación de Riesgos")

# ==========================================
# INTERFAZ: CONTENEDORES PARA CARGA PROGRESIVA
# ==========================================
st.divider()
placeholder_capacidades = st.empty()
st.divider()
placeholder_optimizacion = st.empty()

# ==========================================
# EJECUCIÓN DEL PASO 1: CAPACIDADES NICE
# ==========================================
with placeholder_capacidades.container():
    with st.spinner("Analizando requerimientos de capacidades (Tasks, Skills, Knowledge)..."):
        time.sleep(1.5) # Simulación de carga visual
        
        try:
           # 1. Carga de JSONs 
            with open("../Data/risk_scenarios.json", "r", encoding="utf-8") as f:
                scenarios_raw = json.load(f)
            with open("../Data/roles.json", "r", encoding="utf-8") as f:
                roles_raw = json.load(f)

            # --- NUEVO: PARCHE PARA DESEMPAQUETAR EL JSON ---
            # Si el JSON es un diccionario (empieza por '{'), sacamos la lista que hay dentro
            if isinstance(scenarios_raw, dict):
                scenarios_raw = next(iter(scenarios_raw.values()))
                
            if isinstance(roles_raw, dict):
                roles_raw = next(iter(roles_raw.values()))
            # ------------------------------------------------

            # 2. Instanciar los objetos (y aplicar el parche de 'risk_id' que vimos antes si elegiste la opción A)
            for s in scenarios_raw:
                if "id" in s and "risk_id" not in s:
                    s["risk_id"] = s["id"]

            escenarios_obj = [RiskScenario(s) for s in scenarios_raw]
            roles_obj = [Role(r["role_id"], r["name"]) for r in roles_raw]
            escenarios_obj = [RiskScenario(s) for s in scenarios_raw]
            roles_obj = [Role(r["role_id"], r["name"]) for r in roles_raw] 

            # 3. Extraer los roles en estructuras `set` separadas
            roles_escenarios_set = set()
            for escenario in escenarios_obj:
                roles_escenarios_set.update(escenario.critical_roles)
                
            roles_json_set = set(r.role_id for r in roles_obj)

            req_capacities = get_role_capacities(roles_escenarios_set)
            disp_capacities = get_role_capacities(roles_json_set)

            T_req = req_capacities.tasks
            S_req = req_capacities.skills
            K_req = req_capacities.knowledge

            T_disp = disp_capacities.tasks
            S_disp = disp_capacities.skills
            K_disp = disp_capacities.knowledge
            

            # 5. Calcular intersecciones
            T_intersect = T_req.intersection(T_disp)
            S_intersect = S_req.intersection(S_disp)
            K_intersect = K_req.intersection(K_disp)
            
            # 6. Cálculos de porcentajes
            pct_T = (len(T_intersect) / len(T_req) * 100) if T_req else 100
            pct_S = (len(S_intersect) / len(S_req) * 100) if S_req else 100
            pct_K = (len(K_intersect) / len(K_req) * 100) if K_req else 100

            # 7. Mostrar resultados por pantalla
            st.write("### 🎯 Cobertura de Capacidades (Intersección)")
            col_t, col_s, col_k = st.columns(3)
            col_t.metric("Tasks (T) Cubiertas", f"{pct_T:.1f}%", f"{len(T_intersect)} de {len(T_req)}")
            col_s.metric("Skills (S) Cubiertas", f"{pct_S:.1f}%", f"{len(S_intersect)} de {len(S_req)}")
            col_k.metric("Knowledge (K) Cubiertos", f"{pct_K:.1f}%", f"{len(K_intersect)} de {len(K_req)}")
            
            with st.expander("Ver detalle de requisitos vs cobertura"):
                st.write("**Tasks comunes:**", ", ".join(T_intersect) or "Ninguna")
                st.write("**Skills comunes:**", ", ".join(S_intersect) or "Ninguna")
                st.write("**Knowledge comunes:**", ", ".join(K_intersect) or "Ninguna")

        except Exception as e:
            st.error(f"Error en el Paso 1: {e}")

# ==========================================
# EJECUCIÓN DEL PASO 3: OPTIMIZACIÓN
# ==========================================
with placeholder_optimizacion.container():
    with st.spinner("Ejecutando algoritmo de optimización de contratos..."):
        
        try:
            # 1. Extraer contenido del CSV
            df_costs = pd.read_csv("../Data/roles_costs_with_month_column.csv")
            
            # 2. Filtrar por los roles recogidos en el conjunto roles_json_set (Paso 1)
            df_filtrado = df_costs[df_costs['role_id'].isin(roles_json_set)]
            
            # 3. Proporcionar lista a la función calculate_role_contracts
            lista_diccionarios = df_filtrado.to_dict('records')
            lista_roles_filtrados = []
            
            for d in lista_diccionarios:
                # Extraemos los datos del CSV mapeando los nombres reales de tus columnas
                # Usamos .get() con un valor por defecto para que no falle si falta alguna
                role_id = str(d.get("role_id", ""))
                name = str(d.get("role", d.get("name", ""))) # En tu CSV original se llamaba 'role'
                category = str(d.get("category", "General"))
                
                # Buscamos los costes (quitando el _usd si tu CSV lo tiene así)
                training_cost = int(d.get("training_cost_usd", d.get("training_cost", 0)))
                outsourcing_cost = int(d.get("outsourcing_cost_usd", d.get("outsourcing_cost", 0)))
                time_to_hire = float(d.get("time_to_hire_months", 0.0))
                bonus_cost = int(d.get("bonus_cost_usd", d.get("bonus_cost", 0)))
                
                # Scores
                criticality = float(d.get("role_criticality", d.get("criticality_score", 0.0)))
                risk_impact = float(d.get("risk_impact", d.get("risk_impact_score", 0.0)))

                # 🪄 Creamos el objeto pasándole los parámetros en el ORDEN EXACTO
                # que pide el init_parameters_args de Fran:
                nuevo_rol = RoleCost(
                    role_id, 
                    name, 
                    category, 
                    training_cost, 
                    outsourcing_cost, 
                    time_to_hire, 
                    bonus_cost, 
                    criticality, 
                    risk_impact
                )
                
                lista_roles_filtrados.append(nuevo_rol)
            
            # LLAMADAS REALES A LAS FUNCIONES DE FRAN
            contratos = calculate_role_contracts(lista_roles_filtrados)
            
            # Ordenamos la lista por el ratio
            contratos_ordenados = sorted(contratos, key=lambda x: x.effectivity_ratio, reverse=True)
            
            # ¡PARÁMETROS EN EL ORDEN CORRECTO! (Primero Presupuesto, luego la Lista)
            resultados_optimizacion = optimize_team_composition(PRESUPUESTO_MAXIMO, contratos_ordenados)
            
            # 4. Mostrar resultados formateados por pantalla
            st.write("### 💼 Resultados de Contratación Optimizada")
            
            # ⚠️ ATENCIÓN AQUÍ: Extraemos el coste y la lista de roles
            coste_total = sum(rol.cost for rol in resultados_optimizacion)
            
            # Formateo visual del presupuesto
            if coste_total <= PRESUPUESTO_MAXIMO:
                st.success(f"**✅ Presupuesto Consumido:** ${coste_total:,.2f} / Límite: ${PRESUPUESTO_MAXIMO:,.2f}")
            else:
                st.error(f"**⚠️ Presupuesto Excedido:** ${coste_total:,.2f} / Límite: ${PRESUPUESTO_MAXIMO:,.2f}")
                
            st.write("#### Roles Seleccionados para Contratación:")
            for rol in resultados_optimizacion:
           
                st.markdown(f"- 🧑‍💻 **Rol ID: {rol.role_id}** | Modalidad: `{rol.contract}` | Inversión: ${rol.cost:,.2f} | Impacto mitigado: {rol.risk_impact:.2f}")
        except Exception as e:
            st.error(f"Error en el Paso 3: {e}")
        