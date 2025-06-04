import sqlite3

DB_FILE = "database.db"


def connect_to_db():
    """Connect to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    return conn


def create_table_from_df(df, table_name):
    """Create a table in the database from a DataFrame."""
    conn = connect_to_db()
    # cursor = conn.cursor()

    # Create table with columns based on DataFrame
    df.to_sql(table_name, conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()
