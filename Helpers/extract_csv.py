import csv
import logging

from Models.role import Role

def extract_csv(csv_file: str) -> list[Role]:
    try:
        with open(csv_file, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            return [Role(row) for row in reader]
    except Exception as e:
        logging.error(e)
        raise