from database import engine
from sqlalchemy import text


def validate_read_only_query(query: str):
    """
    Validate that the query is a single read-only SELECT query.
    """

    query = query.strip()

    if not query:
        raise ValueError("Query cannot be empty.")

    # Remove trailing semicolon for validation
    clean_query = query.rstrip(";").strip()

    # Only SELECT statements are allowed
    if not clean_query.lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    # Prevent multiple SQL statements
    if ";" in clean_query:
        raise ValueError("Multiple SQL statements are not allowed.")

    # Block dangerous SQL keywords
    forbidden_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "replace",
    ]

    lower_query = clean_query.lower()

    for keyword in forbidden_keywords:

        if keyword in lower_query:
            raise ValueError(
                f"Unsafe SQL detected: {keyword}"
            )

    return clean_query


def run_read_only_query(query: str):
    """
    Validate and execute a read-only SQL query.
    """

    query = validate_read_only_query(query)

    try:

        with engine.connect() as connection:

            result = connection.execute(text(query))

            records = [
                dict(row)
                for row in result.mappings()
            ]

            return records

    except Exception as e:

        raise RuntimeError(
            f"Query execution failed: {e}"
        )


if __name__ == "__main__":

    query = """
    SELECT *
    FROM reservations
    WHERE customer_id = 'C005'
    """

    records = run_read_only_query(query)

    print("\nQuery Result:")

    for record in records:
        print(record)