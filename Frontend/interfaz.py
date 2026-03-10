import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import json
import time

# --- IMPORTACIONES DE TUS CLASES Y MÓDULOS ---
# ⚠️ CAMBIA 'models' POR EL NOMBRE DEL ARCHIVO DONDE TIENES TUS CLASES

from Models.risk_scenario import RiskScenario
from Models.role import Role
from Helpers.team_capacities import get_role_capacities

# ⚠️ DESCOMENTA ESTO CUANDO FRAN TERMINE SUS MÓDULOS
# from team_capacities import get_role_capacities
# from analyzer import calculate_role_contracts, optimize_team_composition

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA Y CONSTANTES
# ==========================================
st.set_page_config(page_title="CISO DSS - NICE Framework", layout="wide")

PRESUPUESTO_MAXIMO = 250000

st.title("🛡️ CISO Decision Support System (DSS)")
st.subheader("Optimización de Fuerza de Trabajo y Mitigación de Riesgos")
st.write("Cargando módulos de análisis de forma progresiva...")

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

            # 4. Llamadas a las funciones
            T_req, S_req, K_req = get_role_capacities(roles_escenarios_set)
            T_disp, S_disp, K_disp = get_role_capacities(roles_json_set)
            

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
        time.sleep(2.5) # Simulación de carga visual
        
        try:
            # 1. Extraer contenido del CSV
            df_costs = pd.read_csv("../Data/roles_costs_with_month_column.csv")
            
            # 2. Filtrar por los roles recogidos en el conjunto roles_json_set (Paso 1)
            df_filtrado = df_costs[df_costs['role_id'].isin(roles_json_set)]
            
            # 3. Proporcionar lista a la función calculate_role_contracts
            lista_roles_filtrados = df_filtrado.to_dict('records')
            
            # LLAMADAS A LAS FUNCIONES DE FRAN (Descomentar cuando existan)
            # contratos = calculate_role_contracts(lista_roles_filtrados)
            # resultados_optimizacion = optimize_team_composition(contratos, PRESUPUESTO_MAXIMO)
            
            # --- DATOS SIMULADOS TEMPORALES ---
            resultados_optimizacion = {
                "roles_contratados": ["Analista de Inteligencia de Amenazas (PR-TIA-001)", 
                                      "Ingeniero de Seguridad Cloud (PR-INF-002)", 
                                      "Especialista en Respuesta a Incidentes (PR-CIR-001)"],
                "coste_total": 234500.50
            }
            # -----------------------------------
            
            # 4. Mostrar resultados formateados por pantalla
            st.write("### 💼 Resultados de Contratación Optimizada")
            
            coste = resultados_optimizacion['coste_total']
            
            # Formateo visual del presupuesto
            if coste <= PRESUPUESTO_MAXIMO:
                st.success(f"**✅ Presupuesto Consumido:** ${coste:,.2f} / Límite: ${PRESUPUESTO_MAXIMO:,.2f}")
            else:
                st.error(f"**⚠️ Presupuesto Excedido:** ${coste:,.2f} / Límite: ${PRESUPUESTO_MAXIMO:,.2f}")
                
            st.write("#### Roles Seleccionados para Contratación:")
            for rol in resultados_optimizacion['roles_contratados']:
                st.markdown(f"- 🧑‍💻 **{rol}**")
                
        except Exception as e:
            st.error(f"Error en el Paso 3: {e}")