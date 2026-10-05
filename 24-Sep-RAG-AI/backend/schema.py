from database import engine
from sqlalchemy import inspect


def get_database_schema():
    """
    Get all tables and their columns from the database.
    """

    inspector = inspect(engine)

    schema = {}

    # Get all table names
    tables = inspector.get_table_names()

    for table in tables:
        columns = inspector.get_columns(table)

        schema[table] = []

        for column in columns:
            schema[table].append({
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column["nullable"],
            })

    return schema


def print_database_schema():
    """
    Print the database schema in a readable format.
    """

    schema = get_database_schema()

    print("\n========== DATABASE SCHEMA ==========\n")

    for table, columns in schema.items():

        print(f"Table: {table}")

        for column in columns:
            print(
                f"  - {column['name']} "
                f"({column['type']}) "
                f"nullable={column['nullable']}"
            )

        print()


if __name__ == "__main__":
    print_database_schema()