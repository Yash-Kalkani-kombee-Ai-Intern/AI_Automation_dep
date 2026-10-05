import os

from pathlib import Path

from dotenv import load_dotenv

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


# Load .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


# Read MySQL configuration
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "restaurant_ai")


from urllib.parse import quote_plus

# Escape special characters in password (such as '@')
ENCODED_PASSWORD = quote_plus(MYSQL_PASSWORD)

# Create database URL
DATABASE_URL = (
    f"mysql+pymysql://"
    f"{MYSQL_USER}:{ENCODED_PASSWORD}@"
    f"{MYSQL_HOST}:{MYSQL_PORT}/"
    f"{MYSQL_DATABASE}"
)


# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


def test_connection():
    """Test whether the database connection works."""

    try:
        with engine.connect() as connection:

            result = connection.execute(
                text("SELECT DATABASE();")
            )

            database_name = result.scalar()

            print("[SUCCESS] Database connection successful!")
            print(f"Active database: {database_name}")

    except SQLAlchemyError as e:
        print(f"[ERROR] Database connection failed: {e}")


if __name__ == "__main__":
    test_connection()