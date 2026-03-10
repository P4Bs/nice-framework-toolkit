import re
from typing import Tuple
from Services.nice_service import NiceService


FILTER_TSK_REGEX = re.compile("^[TSK]\d{4}$")


class Capacities:
    def __init__(self, role_id: str, abilities: set[str]):
        self.role_id = role_id
        self.abilities = abilities
        self.nice = NiceService()

class Team:
    team_coverage: set[Capacities]
    complete_skillset: set[str]

    def __init__(self, roles: set[str]):
        self.team_coverage, self.complete_skillset = extract_roles_capacities(roles)

def extract_roles_capacities(roles: set[str] = None) -> Tuple[set[Capacities], set[str]]:
    nice = NiceService()
    team_abilities: set[Capacities] = set()
    abilities_set: set[str] = set()

    for rol in roles:
        role_relationships = nice.get_role_relationships(rol)

        if not role_relationships:
            continue

        role_abilities_set = {
            r for r in role_relationships
            if FILTER_TSK_REGEX.match(r)
        }

        abilities_set |= role_abilities_set
        team_abilities.add(Capacities(rol, role_abilities_set))

    return team_abilities, abilities_set