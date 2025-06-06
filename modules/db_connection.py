import sqlite3

from sqlalchemy import create_engine

DB_FILE = "database.db"


class db_config:
    # def __init__(self):
    import os

    from dotenv import load_dotenv

    load_dotenv()
    HOST = os.getenv("db_host")
    NAME = os.getenv("db_name")
    USER = os.getenv("db_user")
    PASSWORD = os.getenv("db_password")
    PORT = os.getenv("db_port")


# def connect_to_db():
#     """Connect to the SQLite database."""
#     conn = sqlite3.connect(DB_FILE)
#     return conn


def connect_to_db():
    """Connect to the external database."""
    db = db_config()
    engine = create_engine(f"mysql+pymysql://{db.USER}:{db.PASSWORD}@{db.HOST}:{db.PORT}/{db.NAME}")
    return engine.connect()


def create_table_from_df(df, table_name):
    """Create a table in the database from a DataFrame."""
    conn = connect_to_db()
    # cursor = conn.cursor()

    # Create table with columns based on DataFrame
    df.to_sql(table_name, conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Example usage
    conn = connect_to_db()
    print("Connected to the database successfully.")
    conn.close()
    print("Connection closed.")
