class RoleScoring:
    role_id: str
    contract_scheme: str
    cost: float
    risk_impact: float
    ratio: float

    def __init__(self, role_id, contract_scheme, cost, risk_impact, ratio):
        self.role_id = role_id
        self.contract_scheme = contract_scheme
        self.cost = cost
        self.risk_impact = risk_impact
