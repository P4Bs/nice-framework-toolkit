import json
import logging

from risk_scenario import RiskScenario, Weights


def load_json(json_file: str) -> list[RiskScenario]:
    try:
        with json.load(open(json_file, "r")) as object_list:
            if not isinstance(type(object_list), list):
                logging.info(f"The file {json_file} does not contain a list")
                return []

            if not isinstance(object_list[0], RiskScenario):
                logging.info(f"The JSON file {json_file} does not contain a RiskScenario object definition")
                return []

            return [RiskScenario(risk_scenario) for risk_scenario in object_list]
    except Exception as e:
        logging.error(e)
        raise
