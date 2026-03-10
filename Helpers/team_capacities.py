import re
from typing import Tuple

from Models.team import Team, TeamCapacities
from Services.nice_service import NiceService

TASK_REGEX = re.compile("^T\d{4}$")
SKILL_REGEX = re.compile("^S\d{4}$")
KNOWLEDGE_REGEX = re.compile("^K\d{4}$")

def compare_teams(current_team: Team, target_team: Team) -> Tuple[float, set[str], set[str]]:
    preparation_ratio: float = 1.0
    skillset_match_set: set[str] = current_team.complete_skillset.intersection(target_team.complete_skillset)
    skillset_diff_set: set[str] = target_team.complete_skillset.difference(current_team.complete_skillset)
    if len(skillset_match_set) < len(target_team.complete_skillset):
        preparation_ratio = len(skillset_match_set) / len(target_team.complete_skillset)
    return preparation_ratio, skillset_match_set, skillset_diff_set

def get_role_capacities(roles: set[str] = None) -> TeamCapacities:
    nice = NiceService()
    team_capacities: TeamCapacities = TeamCapacities()

    for role in roles:
        role_relationships = nice.get_role_relationships(role)

        if not role_relationships:
            continue

        task_set = {
            r for r in role_relationships
            if TASK_REGEX.match(r)
        }

        skill_set = {
            r for r in role_relationships
            if SKILL_REGEX.match(r)
        }

        knowledge_set = {
            r for r in role_relationships
            if KNOWLEDGE_REGEX.match(r)
        }

        team_capacities.tasks.update(task_set)
        team_capacities.skills.update(skill_set)
        team_capacities.knowledge.update(knowledge_set)

    return team_capacities
