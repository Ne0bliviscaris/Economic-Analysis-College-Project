import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))  # for imports
from modules.tables_metadata import tables_metadata


def extract_filename_parts(filename, table_format=None):
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

        table_format_mismatch = table_format and table_type != table_format
        if table_format_mismatch:
            return None

        return {
            "category": category,
            "group": group,
            "table_type": table_type,
            "date": date,
            "table_id": table_id,
        }
    return None


def get_table_names_from_folder(folder, table_format=None):
    """Get a list of table names from CSV files in the specified folder.\n
    **Available formats:**\n
    **'CTAB'** - (tabular)\n
    **'CREL'** - (relational)."""
    if table_format and table_format not in ("CREL", "CTAB"):
        raise ValueError('table_format must be "CREL" or "CTAB"')

    table_names = []
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            filename_parts = extract_filename_parts(file, table_format=table_format)
            if filename_parts:
                group = filename_parts["group"]
                table_type = filename_parts["table_type"]
                if group in tables_metadata:
                    alias = tables_metadata[group]["alias"]
                    table_name = f"{table_type}_{alias}"
                    table_names.append(table_name)
    return table_names


if __name__ == "__main__":

    folder_path = "data"
    table_ids = get_table_names_from_folder(folder_path)

    print("Table IDs found in the folder:")
    for table_id in table_ids:
        print(table_id)
