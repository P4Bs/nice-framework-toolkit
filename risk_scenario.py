class Weights:
    tasks: float
    skills: float
    knowledge: float

    def __init__(self, *args):
        if len(args) == 1:
            self.init_dict_arg(args[0])
        elif len(args) > 1:
            self.init_parameters_args(*args)

    def init_dict_arg(self, object_dict: dict):
        self.tasks = object_dict["tasks"]
        self.skills = object_dict["skills"]
        self.knowledge = object_dict["knowledge"]

    def init_parameters_args(self, tasks, skills, knowledge):
        self.tasks = tasks
        self.skills = skills
        self.knowledge = knowledge

class RiskScenario:
    risk_id: str
    scenario: str
    critical_roles: list[str]
    weights: Weights

    def __init__(self, *args):
        if len(args) == 1:
            self.init_dict_arg(args[0])
        elif len(args) > 1:
            self.init_parameters_args(*args)

    def init_dict_arg(self, object_dict: dict):
        self.risk_id = object_dict["risk_id"]
        self.scenario = object_dict["scenario"]
        self.critical_roles = object_dict["critical_roles"]

    def init_parameters_args(self, risk_id: str, scenario: str, critical_roles: list[str], weights: Weights):
        self.risk_id = risk_id
        self.scenario = scenario
        self.critical_roles = critical_roles
        self.weights = weights
