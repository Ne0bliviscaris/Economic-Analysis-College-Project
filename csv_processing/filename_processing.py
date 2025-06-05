import os
import re


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


def get_table_ids_from_folder(folder, table_format=None):
    """Get a list of table names from CSV files in the specified folder.\n
    **Available formats:**\n
    **'CTAB'** - (tabular)\n
    **'CREL'** - (relational)."""
    table_ids = []
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            filename_parts = extract_filename_parts(file, table_format=table_format)
            if filename_parts:
                group = filename_parts["group"]
                table_type = filename_parts["table_type"]
                table_id = f"{filename_parts['table_id']}"

                table_ids.append(f"{group}_{table_type}_{table_id}")
    return table_ids


if __name__ == "__main__":
    folder_path = ".\\data"
    table_ids = get_table_ids_from_folder(folder_path)
    print("Table IDs found in the folder:")
    for table_id in table_ids:
        print(table_id)
