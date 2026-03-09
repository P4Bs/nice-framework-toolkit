from typing import Tuple
from Models.team import Team


def compare_teams(current_team: Team, target_team: Team) -> Tuple[float, set[str], set[str]]:
    preparation_ratio: float = 1.0
    skillset_match_set: set[str] = current_team.complete_skillset.intersection(target_team.complete_skillset)
    skillset_diff_set: set[str] = target_team.complete_skillset.difference(current_team.complete_skillset)
    if len(skillset_match_set) < len(target_team.complete_skillset):
        preparation_ratio = len(skillset_match_set) / len(target_team.complete_skillset)
    return preparation_ratio, skillset_match_set, skillset_diff_set