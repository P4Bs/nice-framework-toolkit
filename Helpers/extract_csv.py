import csv
import logging

from Models.role_cost import RoleCost

def extract_csv(csv_file: str) -> list[RoleCost]:
    try:
        with open(csv_file, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            next(reader)
            return [RoleCost(row) for row in reader]
    except Exception as e:
        logging.error(e)
        raise