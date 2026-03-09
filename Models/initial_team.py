from Helpers.team_capacities import extract_team_tasks_skills_knowledge


class Team:
    roles: list[str]
    tasks: list[str]
    skills: list[str]
    knowledge: list[str]

    def __init__(self, *args):
        # If it is only one argument then it takes the list of roles
        if len(args) == 1:
            self.roles = args[0]
            self.extract_team_capacities()
        elif len(args) == 4:
            self.roles = args[0]
            self.tasks = args[1]
            self.skills = args[3]
            self.knowledge = args[2]

    def extract_team_capacities(self):
        self.tasks, self.skills, self.knowledge = extract_team_tasks_skills_knowledge()
