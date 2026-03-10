class RoleRequirements:
    role_id: str
    required_tasks: set[str]
    required_skills: set[str]
    required_knowledge: set[str]

    def __init__(self, role_id: str, required_tasks: set[str], required_skills: set[str], required_knowledge: set[str]):
        self.role_id = role_id
        self.required_tasks = required_tasks
        self.required_skills = required_skills
        self.required_knowledge = required_knowledge
