import json
import logging

from Constants.constants import T
from Models.risk_scenario import RiskScenario

def load_json(cls: type[T], json_file: str) -> list[T]:
    try:
        with json.load(open(json_file, "r")) as object_list:
            if not isinstance(type(object_list), list):
                logging.info(f"The file {json_file} does not contain a list")
                return []

            if not isinstance(object_list[0], RiskScenario):
                logging.info(f"The JSON file {json_file} does not contain a RiskScenario object definition")
                return []

            return [cls(object) for object in object_list]
    except Exception as e:
        logging.error(e)
        raise
