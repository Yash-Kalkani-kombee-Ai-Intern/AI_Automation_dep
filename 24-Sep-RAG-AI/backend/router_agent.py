import re
import requests
from datetime import datetime
from logger import logger
from router import classify_question
from sql_agent import (
    answer_database_question,
    get_reservation_for_customer,
)
from rag.rag_agent import answer_policy_question


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"


# ============================================================
# OLLAMA
# ============================================================

def ask_ollama(prompt: str):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0,
                "top_p": 0.1,
            },
        },
        timeout=120,
    )

    response.raise_for_status()

    return response.json()["response"].strip()


# ============================================================
# EXTRACT CUSTOMER ID
# ============================================================

def extract_customer_id(question: str):
    """
    Extract customer ID such as C005 from the question.
    """

    pattern = r"\bC\d+\b"

    match = re.search(
        pattern,
        question.upper()
    )

    if not match:
        return None

    return match.group(0)


# ============================================================
# EXTRACT CANCELLATION TIME
# ============================================================

def extract_cancellation_time(question: str):
    """
    Extract cancellation datetime from the user's question.

    Expected format:

    YYYY-MM-DD HH:MM

    or

    YYYY-MM-DD HH:MM:SS
    """

    pattern = (
        r"\b"
        r"(\d{4}-\d{2}-\d{2})"
        r"\s+"
        r"(\d{2}:\d{2}(?::\d{2})?)"
        r"\b"
    )

    match = re.search(
        pattern,
        question
    )

    if not match:
        return None

    date_part = match.group(1)
    time_part = match.group(2)

    if len(time_part) == 5:
        time_part += ":00"

    return f"{date_part} {time_part}"


# ============================================================
# CANCELLATION TIME CALCULATION
# ============================================================

def calculate_cancellation_status(
    reservation_date: str,
    reservation_time: str,
    cancellation_time: str,
):
    """
    Calculate how many hours remain before the reservation.

    Policy categories:

    >= 24 hours
        Free cancellation

    >= 2 hours and < 24 hours
        Late cancellation

    < 2 hours
        Very late cancellation / no-show
    """

    # Reservation date comes from the database after formatting.
    # Example:
    # September 25, 2026

    # Reservation time may be:
    # 18:30
    # or
    # 18:30:00

    if len(reservation_time) == 5:
        reservation_time += ":00"

    reservation_datetime = datetime.strptime(
        f"{reservation_date} {reservation_time}",
        "%B %d, %Y %H:%M:%S",
    )

    cancellation_datetime = datetime.strptime(
        cancellation_time,
        "%Y-%m-%d %H:%M:%S",
    )

    time_until_reservation = (
        reservation_datetime - cancellation_datetime
    )

    hours_until_reservation = (
        time_until_reservation.total_seconds() / 3600
    )

    if hours_until_reservation >= 24:

        return {
            "eligible_for_free_cancellation": True,
            "hours_remaining": hours_until_reservation,
            "policy_category": "free_cancellation",
        }

    if hours_until_reservation >= 2:

        return {
            "eligible_for_free_cancellation": False,
            "hours_remaining": hours_until_reservation,
            "policy_category": "late_cancellation",
        }

    return {
        "eligible_for_free_cancellation": False,
        "hours_remaining": hours_until_reservation,
        "policy_category": "very_late_cancellation",
    }


# ============================================================
# CALCULATE CANCELLATION FEE
# ============================================================

def calculate_cancellation_fee(
    policy_category: str,
    guests: int,
):
    """
    Calculate cancellation fee using the restaurant policy.

    Free cancellation:
        $0

    Late cancellation:
        $5 per guest, maximum $50

    Very late cancellation:
        $10 per guest, maximum $100
    """

    if policy_category == "free_cancellation":

        return {
            "fee": 0,
            "deposit_forfeited": False,
        }

    if policy_category == "late_cancellation":

        fee = min(
            guests * 5,
            50,
        )

        return {
            "fee": fee,
            "deposit_forfeited": False,
        }

    if policy_category == "very_late_cancellation":

        fee = min(
            guests * 10,
            100,
        )

        return {
            "fee": fee,
            "deposit_forfeited": True,
        }

    return {
        "fee": None,
        "deposit_forfeited": None,
    }


# ============================================================
# BOTH SYNTHESIS
# ============================================================

def synthesize_cancellation_answer(
    question: str,
    reservation: dict,
    cancellation_status: dict,
    cancellation_fee: dict,
    rag_answer: str,
):
    """
    Generate the final natural-language answer.

    Important:
    Python has already calculated the cancellation result.

    The LLM only explains the result.
    """

    prompt = f"""
You are the final answer generator for a restaurant AI assistant.

USER QUESTION:
{question}

RESERVATION DATA:
{reservation}

CANCELLATION CALCULATION:
{cancellation_status}

CANCELLATION FEE:
{cancellation_fee}

RESTAURANT POLICY:
{rag_answer}

IMPORTANT RULES:

1. Use ONLY the provided information.

2. Do NOT invent information.

3. Do NOT recalculate the cancellation result.

4. The Python calculation is authoritative.

5. If eligible_for_free_cancellation is True,
   clearly say the customer can cancel without a fee.

6. If the policy category is "late_cancellation",
   explain that a $5 per guest fee applies,
   with a maximum of $50.

7. If the policy category is "very_late_cancellation",
   explain that a $10 per guest fee applies,
   with a maximum of $100,
   and the deposit is forfeited.

8. Mention the reservation date and time when useful.

9. Mention the number of guests when useful.

10. Never say that you personally cancelled,
    modified, updated, or changed the reservation.

11. The system is read-only and only provides
    cancellation eligibility and fee information.

12. Use wording such as:
    "You can cancel..."
    or
    "A cancellation fee of..."
    instead of:
    "I can cancel..."

13. Do not mention SQL, RAG, router, Python,
    database implementation, or internal systems.

14. Give a short, natural answer.

FINAL ANSWER:
"""

    return ask_ollama(prompt)


# ============================================================
# BOTH — CANCELLATION HANDLER
# ============================================================

def handle_cancellation_question(question: str):

    customer_id = extract_customer_id(
        question
    )

    if not customer_id:

        return (
            "Please provide the customer ID so I can "
            "check the reservation."
        )

    cancellation_time = extract_cancellation_time(
        question
    )

    if not cancellation_time:

        return (
            "I found the customer's reservation, but the "
            "cancellation date and time were not provided. "
            "Please provide the cancellation date and time "
            "in the format YYYY-MM-DD HH:MM so I can "
            "determine the applicable cancellation fee."
        )

    # --------------------------------------------------------
    # Get actual reservation from database
    # --------------------------------------------------------

    reservations = get_reservation_for_customer(
        customer_id
    )

    if not reservations:

        return (
            f"No reservation was found for customer "
            f"{customer_id}."
        )

    reservation = reservations[0]

    # --------------------------------------------------------
    # Get policy information
    # --------------------------------------------------------

    rag_answer = answer_policy_question(
        question
    )

    # --------------------------------------------------------
    # Calculate cancellation status
    # --------------------------------------------------------

    cancellation_status = calculate_cancellation_status(
        reservation_date=reservation[
            "reservation_date"
        ],
        reservation_time=reservation[
            "reservation_time"
        ],
        cancellation_time=cancellation_time,
    )

    # --------------------------------------------------------
    # Calculate fee
    # --------------------------------------------------------

    cancellation_fee = calculate_cancellation_fee(
        policy_category=cancellation_status[
            "policy_category"
        ],
        guests=reservation["guests"],
    )

    # --------------------------------------------------------
    # Generate final explanation
    # --------------------------------------------------------

    return synthesize_cancellation_answer(
        question=question,
        reservation=reservation,
        cancellation_status=cancellation_status,
        cancellation_fee=cancellation_fee,
        rag_answer=rag_answer,
    )


# ============================================================
# MAIN ROUTER
# ============================================================

def answer_question(question: str):

    question = question.strip()
    
    if not question:

        return "Please provide a question."

    route = classify_question(
        question
    )

    logger.info(f"ROUTE | {route}")

    print("\n========== AI ROUTER ==========")
    print(f"Question: {question}")
    print(f"Route: {route}")

    # ========================================================
    # SQL
    # ========================================================

    if route == "SQL":

        print("\nUsing SQL Agent...")

        return answer_database_question(
            question
        )

    # ========================================================
    # RAG
    # ========================================================

    if route == "RAG":

        print("\nUsing RAG Agent...")

        return answer_policy_question(
            question
        )

    # ========================================================
    # BOTH
    # ========================================================

    if route == "BOTH":

        print("\nUsing SQL + RAG...")

        return handle_cancellation_question(
            question
        )

    # ========================================================
    # UNKNOWN
    # ========================================================

    return (
        "I could not determine how to answer "
        "this question."
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    question = input(
        "\nAsk a question: "
    )

    answer = answer_question(
        question
    )

    print(
        "\n========== FINAL ANSWER =========="
    )

    print(answer)

