class Coverage:
    role_id: str
    covered_abilities: int
    amount_target_abilities: int
    total_coverage: float

    def __init__(self, role_id: str, covered_abilities: int, amount_target_abilities: int):
        self.role_id = role_id
        self.covered_abilities = covered_abilities
        self.amount_target_abilities = amount_target_abilities
        self.total_coverage = self.covered_abilities / self.amount_target_abilities
