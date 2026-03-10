from typing import Tuple

import json
import Helpers.team_capacities as tc

def calcularDiferencia(risk_tsk_list, tsk_hire):
     
    #tsk_risk = tc.get_role_capacities(risk_tsk_list)    
    tsk_roles = tc.get_role_capacities(tsk_hire)
    
    print(tsk_roles.knowledge)

    with open('Data/risk_scenarios.json', 'r') as f:
        data = json.load(f)

    buscador_pesos = {escenario['id']: escenario['weights'] for escenario in data}
    score = []

    for risk in risk_tsk_list:

        tsk_risk = tc.get_role_capacities(risk)

        print(tsk_risk.knowledge)
        task_diff = tsk_risk.tasks - tsk_roles.tasks 
        knowledge_diff = tsk_risk.knowledge - tsk_roles.knowledge
        skills_diff = tsk_risk.skills - tsk_roles.skills

        pesos = buscador_pesos.get(risk)

        score_diff = len(task_diff)*pesos["tasks"] + len(knowledge_diff)*pesos["knowledge"] + len(skills_diff)*pesos["skills"]

        score.append(score_diff)
    
    print(score)
    return sum(score)



ids_escenarios = ["RS-01", "RS-02", "RS-03", "RS-04"]

# 1 Rol
roles_1 = ["DD-WRL-005"]

# 5 Roles
roles_5 = ["PD-WRL-001", "OG-WRL-013", "IO-WRL-005", "DD-WRL-001", "PD-WRL-007"]

# 10 Roles
roles_10 = [
    "DD-WRL-003", "PD-WRL-003", "OG-WRL-002", "DD-WRL-007", 
    "IO-WRL-004", "DD-WRL-002", "OG-WRL-008", "PD-WRL-005", 
    "DD-WRL-004", "IO-WRL-006"
]

score = calcularDiferencia(ids_escenarios,roles_1)

print(score)




        




    



    