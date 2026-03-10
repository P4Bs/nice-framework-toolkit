from typing import Tuple

from Constants.constants import HIRE, TRAIN, OUTSOURCE
from Helpers.extract_csv import extract_csv
from Models.contract import RoleContract
from Models.role_cost import RoleCost

BUDGET = 100000
HIRING_COST = 6400


def calculate_role_contracts(role_list: list [RoleCost]) -> list[RoleContract]:
    role_contracts: list[RoleContract] = []

    for role in role_list:
        hiring_cost = role.bonus_cost + (role.time_to_hire_months * HIRING_COST)
        necessity_factor = role.criticality_score * role.risk_impact_score

        # Role_ID, cost, effectivity_ratio
        role_selection: Tuple[str, float, float]
        hiring_effectivity_ratio = necessity_factor / hiring_cost
        training_effectivity_ratio = necessity_factor / role.training_cost
        outsourcing_effectivity_ratio = necessity_factor / role.outsourcing_cost

        role_selection = (TRAIN, role.training_cost, training_effectivity_ratio) \
            if training_effectivity_ratio > hiring_effectivity_ratio \
            else (HIRE, hiring_cost, hiring_effectivity_ratio)
        role_selection = (OUTSOURCE, role.outsourcing_cost, outsourcing_effectivity_ratio) \
            if outsourcing_effectivity_ratio > role_selection[2] \
            else role_selection

        role_contracts.append(
            RoleContract(
                role_id=role.role_id,
                contract=role_selection[0],
                cost=role_selection[1],
                risk_impact=role.risk_impact_score,
                effectivity_ratio=role_selection[2]
            )
        )

    return sorted(role_contracts, key=lambda contract: contract.effectivity_ratio, reverse=True)

def optimize_team_composition(budget, ordered_role_contracts: list[RoleContract], total_cost=0):
    selected_contracts: list[RoleContract] = []

    for role_contract in ordered_role_contracts:
        # ¿Si compro este rol me paso del límite?
        if total_cost + role_contract.cost > budget:
            continue  # Me lo salto porque es muy caro, pero sigo mirando otros más baratos

        # Si me lo puedo permitir, lo compro
        total_cost += role_contract.cost
        selected_contracts.append(role_contract)

    return selected_contracts


lista_csv: list[RoleCost] = extract_csv("roles_costs_with_month_column.csv")
lista_greedy = calculate_role_contracts(lista_csv)
lista_greedy_ordenada = sorted(lista_greedy, key=lambda x: x.effectivity_ratio, reverse=True)

listado_optimo_1 = optimize_team_composition(BUDGET, lista_greedy_ordenada)

printedo = [item.risk_impact for item in listado_optimo_1]
print(sum(printedo))
printedo = [item.cost for item in listado_optimo_1]
print(sum(printedo))
printedo = [item.role_id for item in listado_optimo_1]
print(printedo)




