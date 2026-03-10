import json
import logging

from Constants.constants import T
from Models.risk_scenario import RiskScenario

def load_json(cls: type[T], json_file: str) -> list[T]:
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            object_list = json.load(file)

        if not isinstance(object_list, list):
            logging.info(f"The file {json_file} does not contain a list")
            return []

        if not object_list:
            return []

        if not isinstance(object_list[0], dict):
            logging.info(f"The JSON file {json_file} does not contain valid object definitions")
            return []

        return [cls(**item) for item in object_list]

    except Exception as e:
        logging.error(f"Error loading {json_file}: {e}")
        raise