class Role:
    name: str
    category_id: str
    category: str
    training_cost: int
    outsourcing_cost: int
    time_to_hire_months: float
    bonus_cost: int
    criticality_score: float
    risk_impact_score: float

    def __init__(self, *args):
        if isinstance(args[0], list):
            self.init_row_arg(*args)
        elif len(args) > 1:
            self.init_parameters_args(*args)

    def init_row_arg(self, row: list[str]):
        self.category_id = row[0]
        self.name = row[1]
        self.category = row[2]
        self.training_cost = int(row[3])
        self.outsourcing_cost = int(row[4])
        self.time_to_hire_months = float(row[5])
        self.bonus_cost = int(row[6])
        self.criticality_score = float(row[7])
        self.risk_impact_score = float(row[8])

    def init_parameters_args(self, category_id: str, name: str = "", category: str = "", training_cost = 0, outsourcing_cost = 0, time_to_hire_months = 0.0, bonus_cost = 0, criticality_score = 0.0, risk_impact_score = 0.0):
        self.category_id = category_id
        self.name = name
        self.category = category
        self.training_cost = training_cost
        self.outsourcing_cost = outsourcing_cost
        self.time_to_hire_months = time_to_hire_months
        self.bonus_cost = bonus_cost
        self.criticality_score = criticality_score
        self.risk_impact_score = risk_impact_score
