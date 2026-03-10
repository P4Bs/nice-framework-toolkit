from Helpers.team_capacities import compare_teams
from Models.team import Team
from Services.nice_service import NiceService
from Helpers.extract_json import load_json
from Models.risk_scenario import RiskScenario
from Models.role import Role
from Helpers.team_capacities import get_role_capacities


def main():
    nice = NiceService()

    ruta_risk = "Data/risk_scenarios.json"
    risk_scenarios = load_json(RiskScenario, ruta_risk)
    
    roles_risk_set = {rol for escenario in risk_scenarios for rol in escenario.critical_roles}

    ruta_roles = "Data/roles.json"
    roles_data = load_json(Role, ruta_roles)

    roles_json_set = {r.role_id for r in roles_data}

    print(f"Roles en Risk Scenarios: {len(roles_risk_set)}")
    print(f"Roles en roles.json: {len(roles_json_set)}")

    caps_risk = get_role_capacities(list(roles_risk_set))
    caps_roles = get_role_capacities(list(roles_json_set))

    interseccion_k = caps_risk.knowledge & caps_roles.knowledge
    interseccion_s = caps_risk.skills & caps_roles.skills
    interseccion_t = caps_risk.tasks & caps_roles.tasks

    print("\n--- REQUERIMIENTOS PARA ESCENARIOS DE RIESGO ---")
    print(f"Tasks (T): {caps_risk.tasks}")
    print(f"Skills (S): {caps_risk.skills}")
    print(f"Knowledge (K): {caps_risk.knowledge}")

    print("\n--- INTERSECCIÓN ENCONTRADA ---")
    print(f"Tareas comunes: {len(interseccion_t)}")
    print(f"Skills comunes: {len(interseccion_s)}")
    print(f"Knowledge común: {len(interseccion_k)}")

    porcentaje = lambda parte, total: (len(parte) / len(total) * 100) if len(total) > 0 else 0

    p_t = porcentaje(interseccion_t, caps_risk.tasks)
    p_s = porcentaje(interseccion_s, caps_risk.skills)
    p_k = porcentaje(interseccion_k, caps_risk.knowledge)

    print("\n--- COBERTURA RELATIVA (%) ---")
    print(f"Tareas cubiertas: {p_t:.2f}%")
    print(f"Skills cubiertas: {p_s:.2f}%")
    print(f"Knowledge cubierto: {p_k:.2f}%")


if __name__ == '__main__':
    main()