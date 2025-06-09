from sqlalchemy import create_engine
from sqlalchemy.sql import text

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


def connect_to_db():
    """Connect to the external database."""
    db = db_config()
    engine = create_engine(f"mysql+pymysql://{db.USER}:{db.PASSWORD}@{db.HOST}:{db.PORT}/{db.NAME}")
    return engine.connect()


def create_table_from_df(df, table_name):
    """Create a table in the database from a DataFrame."""
    db = connect_to_db()
    df.to_sql(table_name, db, if_exists="replace", index=False)

    db.commit()
    db.close()


def get_db_schema():
    """Extract database schema with tables and columns."""
    db = connect_to_db()
    tables = db.execute(text("SHOW TABLES")).fetchall()
    schema = {}

    for table in tables:
        table_name = table[0]
        columns = db.execute(text(f"DESCRIBE {table_name}")).fetchall()
        schema[table_name] = columns

    db.close()
    return schema


if __name__ == "__main__":
    print("Database schema:")
    db_schema = get_db_schema()

    for table_name, columns in db_schema.items():
        print(f"\nTable: {table_name}")
        print("-" * 80)
        for column in columns:
            print(f"Field: {column[0]}, Type: {column[1]}, Null: {column[2]}, Key: {column[3]}, Default: {column[4]}")
