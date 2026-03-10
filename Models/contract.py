class RoleContract:
    role_id: str
    contract: str
    cost: float
    risk_impact: float
    effectivity_ratio: float

    def __init__(self, role_id, contract, cost, risk_impact, effectivity_ratio):
        self.role_id = role_id
        self.contract = contract
        self.cost = cost
        self.risk_impact = risk_impact
        self.effectivity_ratio = effectivity_ratio
