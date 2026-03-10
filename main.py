from Helpers.team_capacities import get_role_capacities
from Services.nice_service import NiceService
from Helpers.extract_json import load_json
from Models.risk_scenario import RiskScenario
from Models.role import Role
from Models.contract import RoleContract
from analyzer import calculate_role_contracts, optimize_team_composition
from Helpers.extract_csv import extract_csv


def calculate_realist_security_score(team_caps, risk_scenarios) -> float:
    """
    Calcula el Score de Seguridad evaluando la cobertura escenario por escenario.
    Devuelve un valor de 0 a 100 (Media de mitigación de todos los riesgos).
    """
    if not risk_scenarios:
        return 100.0

    total_score_acumulado = 0.0
    
    # Evaluamos riesgo a riesgo
    for escenario in risk_scenarios:
        # 1. ¿Qué exige ESTE escenario en concreto?
        caps_requeridas = get_role_capacities(escenario.critical_roles)
        
        req_t = len(caps_requeridas.tasks)
        req_s = len(caps_requeridas.skills)
        req_k = len(caps_requeridas.knowledge)
        total_req = req_t + req_s + req_k
        
        # Si el escenario no requiere nada, asumimos que está cubierto al 100%
        if total_req == 0:
            total_score_acumulado += 100.0
            continue
            
        # 2. ¿Qué puede aportar mi equipo a ESTE escenario? (Intersección)
        cov_t = len(team_caps.tasks & caps_requeridas.tasks)
        cov_s = len(team_caps.skills & caps_requeridas.skills)
        cov_k = len(team_caps.knowledge & caps_requeridas.knowledge)
        total_cov = cov_t + cov_s + cov_k
        
        # 3. Calculamos la cobertura de este escenario (0 a 100)
        cobertura_escenario = (total_cov / total_req) * 100

        
        # 4. Sumamos al acumulado global
        total_score_acumulado += cobertura_escenario

    # La nota final es la media de todos los escenarios
    score_final = total_score_acumulado / len(risk_scenarios)
    
    return round(score_final, 2)


def main():
    nice = NiceService()

    ruta_risk = "Data/risk_scenarios.json"
    risk_scenarios = load_json(RiskScenario, ruta_risk)
    
    roles_risk_set = {rol for escenario in risk_scenarios for rol in escenario.critical_roles}

    ruta_roles = "Data/roles.json"
    roles_data = load_json(Role, ruta_roles)

    roles_json_set = {r.role_id for r in roles_data}

    caps_risk = get_role_capacities(list(roles_risk_set)) #Roles relacionados con los escenarios de riesgo
    caps_roles = get_role_capacities(list(roles_json_set))  #Roles del equipo actual

    score_actual = calculate_realist_security_score(caps_roles, risk_scenarios)

    print(f"El score de seguridad actual del equipo es: {score_actual}%")

    # 1. Extraer el CSV 
    lista_csv = extract_csv("roles_costs_with_month_column.csv")
    lista_greedy = calculate_role_contracts(lista_csv)
    
    listado_optimo = optimize_team_composition(250000, lista_greedy)

    # 4. RESULTADOS DE LA OPTIMIZACIÓN
    coste_total = sum(item.cost for item in listado_optimo)
    roles_adquiridos = [item.role_id for item in listado_optimo]

    # 5. ESTADO FINAL (Después de la optimización)
    equipo_actual = list(roles_json_set)
    
    # Unimos los roles que ya teníamos con los nuevos que hemos comprado
    equipo_final = equipo_actual + roles_adquiridos
    
    # Sacamos las capacidades del nuevo súper-equipo y calculamos el score
    caps_finales = get_role_capacities(equipo_final)
    score_final = calculate_realist_security_score(caps_finales, risk_scenarios)
    
    # Añadimos unos prints para que veas el resultado mágico por consola:
    print(f"💰 Presupuesto gastado: ${coste_total} / $250000")
    print(f"👥 Nuevos roles adquiridos: {len(roles_adquiridos)}")
    print(f"🚀 SCORE DE SEGURIDAD FINAL: {score_final}%")
    print(f"📈 Mejora de seguridad: +{score_final - score_actual:.2f} %")
    

if __name__ == '__main__':
    main()