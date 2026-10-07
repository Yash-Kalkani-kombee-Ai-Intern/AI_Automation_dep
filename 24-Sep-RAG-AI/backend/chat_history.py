import sqlite3
from pathlib import Path


DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "chat_history.db"
)


def create_history_table():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_chat(question: str, answer: str):
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO chat_history (question, answer)
            VALUES (?, ?)
            """,
            (question, answer),
        )


def get_chat_history():
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute(
            """
            SELECT id, question, answer, created_at
            FROM chat_history
            ORDER BY id ASC
            """
        ).fetchall()

        return [dict(row) for row in rows]


create_history_table()