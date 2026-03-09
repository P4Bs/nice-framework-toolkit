import re

from Models.initial_team import Team
from Models.relationship import Relationship
from Services.nice_service import load_nice_framework_relationships

TASK_REGEX = re.compile("^T\\d{4}$")
SKILLS_REGEX = re.compile("^S\\d{4}$")
KNOWLEDGE_REGEX = re.compile("^K\\d{4}$")

def extract_team_tasks_skills_knowledge(team_roles: list[str] = ["DD-WRL-002"]) -> tuple[list[str], list[str], list[str]]:
    team_tasks: list[str] = []
    team_skills: list[str] = []
    team_knowledge: list[str] = []
    nice_framework_relationships: list[Relationship] = load_nice_framework_relationships()
    for role in team_roles:
        capacities_filtered_by_role: list[str] = [relationship["dest_element_identifier"] for relationship in nice_framework_relationships if relationship["source_element_identifier"] == role]

        team_tasks += filter(TASK_REGEX.match, capacities_filtered_by_role)
        team_skills += filter(SKILLS_REGEX.match, capacities_filtered_by_role)
        team_knowledge += filter(KNOWLEDGE_REGEX.match, capacities_filtered_by_role)

    return team_tasks, team_skills, team_knowledge

# TODO: WRITE THIS FUNCTION
def compare_teams(current_team: Team, target_team: Team):
    print("")