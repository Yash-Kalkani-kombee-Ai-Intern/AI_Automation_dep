import sqlite3
from datetime import datetime, timezone
from pathlib import Path


# ============================================================
# Database configuration
# ============================================================

DB_PATH = Path(__file__).parent / "feedback.db"


# ============================================================
# Default system prompt
# ============================================================

DEFAULT_SYSTEM_PROMPT = """
You are a helpful AI assistant.

Explain technical topics in simple language.
Start with the basic concept.
Explain why it is used.
Give a practical example when useful.
Keep answers clear, structured, and easy to understand.
"""


# ============================================================
# Database connection
# ============================================================

def get_connection():
    return sqlite3.connect(DB_PATH)


# ============================================================
# Initialize database
# ============================================================

def init_db():
    with get_connection() as conn:

        # ----------------------------------------------------
        # Feedback table
        # ----------------------------------------------------

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                response_id TEXT NOT NULL UNIQUE,
                user_prompt TEXT,
                model_response TEXT,
                rating INTEGER,
                comment TEXT,
                response_latency REAL,
                turn_number INTEGER,
                created_at TEXT NOT NULL
            )
            """
        )

        # ----------------------------------------------------
        # Settings table
        # ----------------------------------------------------

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )

        # ----------------------------------------------------
        # Prompt version history
        # ----------------------------------------------------

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS prompt_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT NOT NULL,
                reason TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        # ----------------------------------------------------
        # Create initial prompt only once
        # ----------------------------------------------------

        existing_prompt = conn.execute(
            """
            SELECT value
            FROM settings
            WHERE key = 'active_prompt'
            """
        ).fetchone()

        if existing_prompt is None:

            conn.execute(
                """
                INSERT INTO settings (
                    key,
                    value
                )
                VALUES (
                    'active_prompt',
                    ?
                )
                """,
                (DEFAULT_SYSTEM_PROMPT,),
            )

            conn.execute(
                """
                INSERT INTO prompt_versions (
                    prompt,
                    reason,
                    created_at
                )
                VALUES (
                    ?,
                    ?,
                    ?
                )
                """,
                (
                    DEFAULT_SYSTEM_PROMPT,
                    "Initial system prompt",
                    datetime.now(timezone.utc).isoformat(),
                ),
            )

        conn.commit()


# ============================================================
# Save user feedback
# ============================================================

def save_feedback(
    session_id,
    response_id,
    user_prompt,
    model_response,
    rating,
    comment,
    response_latency,
    turn_number,
):

    with get_connection() as conn:

        conn.execute(
            """
            INSERT OR IGNORE INTO feedback (
                session_id,
                response_id,
                user_prompt,
                model_response,
                rating,
                comment,
                response_latency,
                turn_number,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                response_id,
                user_prompt,
                model_response,
                rating,
                comment,
                response_latency,
                turn_number,
                datetime.now(timezone.utc).isoformat(),
            ),
        )

        conn.commit()


# ============================================================
# Get current active system prompt
# ============================================================

def get_active_prompt():

    with get_connection() as conn:

        row = conn.execute(
            """
            SELECT value
            FROM settings
            WHERE key = 'active_prompt'
            """
        ).fetchone()

    if row:
        return row[0]

    return DEFAULT_SYSTEM_PROMPT


# ============================================================
# Update active system prompt
# ============================================================

def set_active_prompt(
    new_prompt,
    reason,
):

    with get_connection() as conn:

        # Update current active prompt
        conn.execute(
            """
            UPDATE settings
            SET value = ?
            WHERE key = 'active_prompt'
            """,
            (new_prompt,),
        )

        # Store prompt version history
        conn.execute(
            """
            INSERT INTO prompt_versions (
                prompt,
                reason,
                created_at
            )
            VALUES (?, ?, ?)
            """,
            (
                new_prompt,
                reason,
                datetime.now(timezone.utc).isoformat(),
            ),
        )

        conn.commit()


# ============================================================
# Get negative feedback
# ============================================================

def get_negative_feedback():

    with get_connection() as conn:

        rows = conn.execute(
            """
            SELECT
                user_prompt,
                model_response,
                comment,
                response_latency,
                created_at
            FROM feedback
            WHERE rating = 0
            ORDER BY id DESC
            LIMIT 20
            """
        ).fetchall()

    return rows


# ============================================================
# Count negative feedback
# ============================================================

def get_negative_feedback_count():

    with get_connection() as conn:

        row = conn.execute(
            """
            SELECT COUNT(*)
            FROM feedback
            WHERE rating = 0
            """
        ).fetchone()

    return row[0]


# ============================================================
# Get all feedback
# ============================================================

def get_all_feedback():

    with get_connection() as conn:

        rows = conn.execute(
            """
            SELECT
                id,
                session_id,
                response_id,
                user_prompt,
                model_response,
                rating,
                comment,
                response_latency,
                turn_number,
                created_at
            FROM feedback
            ORDER BY id DESC
            """
        ).fetchall()

    return rows


# ============================================================
# Get prompt history
# ============================================================

def get_prompt_versions():

    with get_connection() as conn:

        rows = conn.execute(
            """
            SELECT
                id,
                prompt,
                reason,
                created_at
            FROM prompt_versions
            ORDER BY id DESC
            """
        ).fetchall()

    return rows