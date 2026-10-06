import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"


def ask_ollama(prompt: str):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0,
            },
        },
        timeout=120,
    )

    response.raise_for_status()

    return response.json()["response"].strip()


def classify_question(question: str):
    prompt = f"""
You are an AI router for a restaurant assistant.

Classify the user's question into exactly ONE category:

SQL
RAG
BOTH

SQL:
Use SQL when the question requires live information from the
restaurant database.

Examples:
- What did customer C005 order?
- What is customer C005's reservation?
- Which table is assigned to C005?
- What is the status of order O007?

RAG:
Use RAG when the question requires information from restaurant
policies, rules, manuals, FAQs, or documents.

Examples:
- What is the cancellation policy?
- How much is the late cancellation fee?
- What is the no-show policy?
- How can I cancel a reservation?

BOTH:
Use BOTH when the question requires BOTH:
1. live database information
2. restaurant policy information

Examples:
- Can customer C005 cancel their reservation without paying a fee?
- Does C005's reservation qualify for a free cancellation?
- Based on C005's reservation and the cancellation policy, can they cancel for free?

IMPORTANT:
Return ONLY one word:

SQL
RAG
BOTH

USER QUESTION:
{question}
"""

    result = ask_ollama(prompt)

    result = result.strip().upper()

    if "BOTH" in result:
        return "BOTH"

    if "RAG" in result:
        return "RAG"

    if "SQL" in result:
        return "SQL"

    return "RAG"