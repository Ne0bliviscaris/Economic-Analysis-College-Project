import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))  # for imports
from modules.tables_metadata import tables_metadata


def extract_filename_parts(filename):
    """Extract parts from the filename."""
    four_letters = r"([A-Z]{4})"
    group = r"(\d+)"
    date = r"(\d{8})"
    table_id = r"(\d{6})"
    pattern = f"^{four_letters}_{group}_{four_letters}_{date}{table_id}.csv$"
    match = re.match(pattern, filename)

    if match:
        category = match.group(1)
        group = match.group(2)
        table_type = match.group(3)
        date = match.group(4)
        table_id = match.group(5)

        return {
            "category": category,
            "group": group,
            "table_type": table_type,
            "date": date,
            "table_id": table_id,
        }
    return None
