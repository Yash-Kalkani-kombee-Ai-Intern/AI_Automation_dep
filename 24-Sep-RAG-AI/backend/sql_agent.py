import requests

from schema import get_database_schema
from query_tool import run_read_only_query
from datetime import date, datetime, time, timedelta


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"


def ask_ollama(prompt: str):
    """Send a prompt to the local Ollama model."""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["response"].strip()


def generate_sql(question: str):
    """Convert a natural-language question into SQL."""

    schema = get_database_schema()

    schema_text = ""

    for table, columns in schema.items():

        schema_text += f"\nTable: {table}\n"

        for column in columns:
            schema_text += (
                f"- {column['name']} ({column['type']})\n"
            )

    prompt = f"""
You are a SQL assistant.

Convert the user's question into a MySQL SELECT query.

DATABASE SCHEMA:
{schema_text}

RULES:
1. Generate ONLY a SELECT query.
2. Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, or CREATE.
3. Use only tables and columns from the provided schema.
4. If the user provides an ID such as C005, R105, T07, etc., match it against the corresponding ID column, not a name column.
5. customer IDs must be matched using customers.customer_id.
6. reservation IDs must be matched using reservations.reservation_id.
7. table IDs must be matched using restaurant_tables.table_id.
8. Do not guess names when the user provides an ID.
9. Do not explain the SQL.
10. Return only the SQL query.

USER QUESTION:
{question}
"""

    sql = ask_ollama(prompt)

    # Remove Markdown formatting
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql

def format_database_records(records):
    """
    Convert Python date/time values into readable strings.
    """

    formatted_records = []

    for record in records:

        formatted_record = {}

        for key, value in record.items():

            if isinstance(value, datetime):
                formatted_record[key] = value.strftime(
                    "%B %d, %Y at %I:%M %p"
                )

            elif isinstance(value, date):
                formatted_record[key] = value.strftime(
                    "%B %d, %Y"
                )

            elif isinstance(value, timedelta):
                total_seconds = int(value.total_seconds())

                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60

                formatted_record[key] = (
                    f"{hours:02d}:{minutes:02d}"
                )

            else:
                formatted_record[key] = value

        formatted_records.append(formatted_record)

    return formatted_records

def answer_database_question(question: str):
    """Generate SQL, retrieve database records, and create the final answer."""

    # Step 1: Generate SQL
    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)

    # Step 2: Execute SQL using the read-only query tool
    records = run_read_only_query(sql)

    # Step 3: Format database values
    records = format_database_records(records)

    print("\nDatabase Result:")
    print(records)

    # Step 4: Handle empty result directly
    if not records:
        return "No matching record was found."

    # Step 5: Ask LLM to explain the result
    answer_prompt = f"""
You are a helpful restaurant assistant.

Answer the user's question using the database result below.

USER QUESTION:
{question}

DATABASE RESULT:
{records}

IMPORTANT RULES:
1. Use ONLY the database result.
2. Do NOT invent information.
3. Include EVERY record.
4. Do NOT remove, skip, summarize, or merge records.
5. If there are multiple records, mention ALL of them.
6. Return a natural human-readable answer.
7. Do NOT output Python dictionaries.
8. Do NOT say "Here is the database result".
"""

    final_answer = ask_ollama(answer_prompt)

    return final_answer

if __name__ == "__main__":

    question = "What did customer C999 order?"

    answer = answer_database_question(question)

    print("\nFinal Answer:")
    print(answer)