# MVP - build sqlite db from a folder of CSV files
import os

import pandas as pd

from csv_processing import filename_processing
from modules.db_connection import connect_to_db

INPUTS_FOLDER = "data"


def list_csv_files(folder):
    """List all CSV files in the specified folder."""
    return [file for file in os.listdir(folder) if file.endswith(".csv")]


def open_file_as_df(file_path):
    """Open a CSV file and return it as a DataFrame."""
    file_path = os.path.join(INPUTS_FOLDER, file_path)
    return pd.read_csv(file_path, sep=";")


def build_db_from_folder():
    """Process all CSV files in the specified folder."""
    csv_list = list_csv_files(INPUTS_FOLDER)

    for file in csv_list:
        file_df = open_file_as_df(file)
        filename_parts = filename_processing.extract_filename_parts(file)
        if filename_parts:
            first = filename_parts["first_four_letters"]
            subgroup = filename_parts["subgroup"]
            table_id = f"{filename_parts['table_id']}"
            table_name = f"{first}_{subgroup}_{table_id}"
            file_df.to_sql(table_name, con=connect_to_db(), if_exists="replace", index=False)
            # print(f"Table {table_name} created from {file}")
            print(f"Table {table_name} added to the database from {file}")
        else:
            print(f"Filename {file} does not match expected format.")


if __name__ == "__main__":
    build_db_from_folder()
    print("Database has been built from the CSV files in the folder.")
