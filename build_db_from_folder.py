# MVP - build sqlite db from a folder of CSV files
import os
import re
import unicodedata

import pandas as pd

from modules.db_connection import connect_to_db
from modules.filename_processing import extract_filename_parts
from modules.tables_metadata import tables_metadata

INPUTS_FOLDER = "data"
TABLE_FORMAT = "CREL"  # relational CSV
# TABLE_FORMAT = "CTAB"  # tabular CSV (multi-dimensional)


def list_csv_files(folder):
    """List CSV files in folder."""
    return [file for file in os.listdir(folder) if file.endswith(".csv")]


def get_table_alias(file):
    """Return table alias for file."""
    parts = extract_filename_parts(file, table_format=TABLE_FORMAT)
    if parts and parts["group"] in tables_metadata:
        table_alias = tables_metadata[parts["group"]]["alias"]
        return f"{table_alias}"
    return None


def open_file_as_df(file_path):
    """Open a CSV file and return it as a DataFrame."""
    file_path = os.path.join(INPUTS_FOLDER, file_path)
    return pd.read_csv(file_path, sep=";")


def clean_column_names(df):
    """Remove special characters and Polish diacritics from column names."""

    def clean(col):
        """Clean a single column name."""
        col = col.replace("ł", "l").replace("Ł", "L")
        col = "".join(c for c in unicodedata.normalize("NFKD", col) if not unicodedata.combining(c))
        col = re.sub(r"[^a-zA-Z0-9_]", "_", col)
        return col

    df.columns = [clean(col) for col in df.columns]
    return df


def build_db_from_folder():
    """Build database from CSV files in folder."""
    for file in list_csv_files(INPUTS_FOLDER):
        alias = get_table_alias(file)
        if not alias:
            # print(f"Skipping file {file}: no table metadata found.")
            continue
        df = open_file_as_df(file)
        df = clean_column_names(df)
        df.to_sql(alias, con=connect_to_db(), if_exists="replace", index=False)
        print(f"Table {alias} added to the database from {file}")


if __name__ == "__main__":
    build_db_from_folder()
    print("Database has been built from the CSV files in the folder.")
