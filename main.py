from build_db_from_folder import build_db_from_folder


def main():
    """Main function to build the database from CSV files."""
    build_db_from_folder()
    print("Database built successfully from CSV files.")


if __name__ == "__main__":
    main()
    print("Database has been built from the CSV files in the folder.")
