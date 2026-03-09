from Helpers.team_capacities import compare_teams
from Models.team import Team


def main():
    print("Hello World")
    current_team = Team(["IO-WRL-005", "PD-WRL-006"])
    target_team = Team(["PD-WRL-001"])
    coverage, matched_skills, difference_skill = compare_teams(current_team, target_team)
    print(f"Coverage: {coverage}")


if __name__ == '__main__':
    main()