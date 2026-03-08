import streamlit as st
import pandas as pd
import json
import plotly.express as px
import os

# Configuración de la página
st.set_page_config(page_title="CISO DSS - NICE Framework", layout="wide")

# --- FUNCIONES DE CARGA DE DATOS ---
def load_local_data():
    """Carga los archivos CSV y JSON proporcionados por el usuario"""
    try:
        # Cargar CSV de costes y scores
        df_costs = pd.read_csv("roles_costs.csv")
        
        # Cargar JSON de escenarios de riesgo
        with open("risk_scenarios.json", "r", encoding='utf-8') as f:
            scenarios = json.load(f)
            
        return df_costs, scenarios
    except Exception as e:
        st.error(f"Error al cargar archivos: {e}. Asegúrate de que 'roles_costs.csv' y 'risk_scenarios.json' estén en la misma carpeta.")
        return None, None

df_costs, scenarios_data = load_local_data()

# --- INTERFAZ PRINCIPAL ---
st.title("🛡️ CISO Decision Support System (DSS)")
st.subheader("Optimización de Fuerza de Trabajo y Mitigación de Riesgos")

if df_costs is not None and scenarios_data is not None:
    
    # --- BARRA LATERAL: CONFIGURACIÓN ESTRATÉGICA ---
    with st.sidebar:
        st.header("⚙️ Configuración")
        presupuesto_limite = 250000
        
        # Selector de Escenario (desde tu JSON)
        nombres_escenarios = [s['scenario'] for s in scenarios_data]
        seleccion_escenario = st.selectbox("🎯 Seleccionar Escenario de Riesgo", nombres_escenarios)
        
        # Obtener datos del escenario seleccionado
        escenario_info = next(s for s in scenarios_data if s['scenario'] == seleccion_escenario)
        
        st.divider()
        st.write(f"**Escenario ID:** {escenario_info['id']}")

    # --- LÓGICA DE FILTRADO ---
    # Mapeo de IDs: Tu JSON usa "RS-01" pero tu CSV usa "RS-001"
    # Esta línea ajusta el ID para que coincidan perfectamente
    id_csv = escenario_info['id'].replace("RS-0", "RS-00")
    
    # Filtrar el CSV por el escenario seleccionado
    df_escenario = df_costs[df_costs['risk_scenario_id'] == id_csv]

    # --- DASHBOARD: MÉTRICAS CLAVE (KPIs) ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        coste_total = df_escenario['training_cost_usd'].sum() + df_escenario['bonus_cost_usd'].sum()
        st.metric("Inversión Estimada", f"${coste_total:,}", f"{((coste_total/presupuesto_limite)*100):.1f}% del presupuesto")
        
    with col2:
        # Heurística de riesgo: media del risk_impact en el escenario
        mitigacion = df_escenario['risk_impact'].mean() * 100
        st.metric("Reducción de Riesgo", f"{mitigacion:.1f}%", "Postura Proactiva")
        
    with col3:
        # Score total de cobertura según los pesos aplicados
        score_total = df_escenario['score'].sum()
        st.metric("Puntuación Cobertura TKS", f"{score_total:.1f} pts")

    st.divider()

    # --- ANÁLISIS VISUAL ---
    left_col, right_col = st.columns(2)

    with left_col:
        st.write("### 📊 Eficacia por Rol (NICE Score)")
        # Gráfico con los scores reales de tu CSV 
        fig_score = px.bar(df_escenario, x="role_id", y="score", color="role_criticality",
                           title="Contribución al Score por Rol Crítico",
                           labels={"score": "Puntuación TKS", "role_id": "ID de Rol NICE"})
        st.plotly_chart(fig_score, use_container_width=True)

    with right_col:
        st.write("### 💰 Análisis de Costes (Training vs Outsourcing)")
        # Comparativa de costes para el CISO 
        fig_cost = px.scatter(df_escenario, x="training_cost_usd", y="outsourcing_cost_usd", 
                              size="risk_impact", hover_name="role",
                              title="Inversión Interna vs Externalización")
        st.plotly_chart(fig_cost, use_container_width=True)

    st.divider()

    # --- TABLA DE DATOS REALES (roles_costs.csv) ---
    st.write("### 📅 Plan Maestro de 2 Años: Detalle de Roles")
    # Mostramos los campos estratégicos que pide el PDF
    st.dataframe(df_escenario[['role', 'role_id', 'time_to_hire_months', 'training_cost_usd', 'role_criticality', 'risk_impact', 'score']], 
                 use_container_width=True)

    # Validación presupuestaria final
    if coste_total <= presupuesto_limite:
        st.success(f"✅ Presupuesto validado: Quedan ${(presupuesto_limite - coste_total):,} disponibles.")
    else:
        st.error(f"⚠️ Alerta: Se ha excedido el presupuesto por ${(coste_total - presupuesto_limite):,}.")

else:
    st.warning("Esperando archivos de configuración para mostrar el Dashboard...")