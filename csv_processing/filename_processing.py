import re


def extract_filename_parts(filename):
    """Extract parts from the filename."""
    four_letters = r"([A-Z]{4})"
    subgroup = r"(\d+)"
    date = r"(\d{8})"
    table_id = r"(\d{6})"
    pattern = f"^{four_letters}_{subgroup}_{four_letters}_{date}{table_id}.csv$"
    match = re.match(pattern, filename)

    if match:
        first_four_letters = match.group(1)
        subgroup = match.group(2)
        second_four_letters = match.group(3)
        date = match.group(4)
        table_id = match.group(5)

        return {
            "first_four_letters": first_four_letters,
            "subgroup": subgroup,
            "second_four_letters": second_four_letters,
            "date": date,
            "table_id": table_id,
        }
    return None
