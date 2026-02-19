import csv
import logging

logger = logging.getLogger(__name__)

def read_csv(file_path):
    try:
        with open(file_path, newline='') as csvfile:
            return list(csv.DictReader(csvfile))
    except Exception as e:
        logger.error(f"Failed to read CSV {file_path}: {e}")
        return []
