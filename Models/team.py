import re
from typing import Tuple

from Models.relationship import Relationship
from Services.nice_service import load_nice_framework_relationships


FILTER_REGEX = re.compile("^[TSK]\d{4}$")


class Capacities:
    role_id: str
    # Aggregation of tasks, skills and knowledge
    abilities: set[str]

    def __init__(self, *args):
        if len(args) == 2:
            self.role_id = args[0]
            self.abilities = args[1]

class Team:
    team_coverage: set[Capacities]
    complete_skillset: set[str]

    def __init__(self, *args):
        # If it is only one argument then it takes the list of roles
        if len(args) == 1:
            self.team_coverage, self.complete_skillset = extract_roles_capacities(args[0])

def extract_roles_capacities(roles: set[str] = None) -> Tuple[set[Capacities], set[str]]:
    team_abilities: set[Capacities] = set()
    abilities_set: set[str] = set()
    nice_framework_relationships: list[Relationship] = load_nice_framework_relationships()

    for role in roles:
        role_relationships: list[str] = \
            [relationship["dest_element_identifier"]
             for relationship in nice_framework_relationships
                if relationship["source_element_identifier"] == role]

        if len(role_relationships) == 0:
            # The role specified does not exist
            continue

        role_abilities_set = {role for role in role_relationships if FILTER_REGEX.match(role)}
        abilities_set = abilities_set.union(role_abilities_set)
        team_abilities.add(Capacities(role, role_abilities_set))

    return team_abilities, abilities_set