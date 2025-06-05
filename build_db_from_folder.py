# MVP - build sqlite db from a folder of CSV files
import os

import pandas as pd

from modules.db_connection import connect_to_db
from modules.filename_processing import extract_filename_parts
from modules.tables_metadata import tables_metadata

INPUTS_FOLDER = "data"
# TABLE_FORMAT = "CREL"  # relational CSV
# TABLE_FORMAT = "CTAB"  # tabular CSV (multi-dimensional)


def list_csv_files(folder):
    """List CSV files in folder."""
    return [file for file in os.listdir(folder) if file.endswith(".csv")]


def get_table_alias(file, table_format):
    """Return table alias for file."""
    parts = extract_filename_parts(file, table_format=table_format)
    if parts and parts["group"] in tables_metadata:
        table_type = parts["table_type"]
        table_alias = tables_metadata[parts["group"]]["alias"]
        return f"{table_type}_{table_alias}"
    return None


def open_file_as_df(file_path):
    """Open a CSV file and return it as a DataFrame."""
    file_path = os.path.join(INPUTS_FOLDER, file_path)
    return pd.read_csv(file_path, sep=";")


def build_db_from_folder(table_format=None):
    """Build database from CSV files in folder."""
    for file in list_csv_files(INPUTS_FOLDER):
        alias = get_table_alias(file, table_format)
        if not alias:
            print(f"Skipping file {file}: no table metadata found.")
            continue
        df = open_file_as_df(file)
        df.to_sql(alias, con=connect_to_db(), if_exists="replace", index=False)
        print(f"Table {alias} added to the database from {file}")


if __name__ == "__main__":
    build_db_from_folder()
    print("Database has been built from the CSV files in the folder.")
