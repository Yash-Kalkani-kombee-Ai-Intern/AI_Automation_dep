import requests

from rag.retriever import retrieve_relevant_chunks


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"


def ask_ollama(prompt: str):
    system_instruction = """
You are a strict document question-answering assistant.

Your ONLY source of truth is the document context provided by the user.

Never use outside knowledge.
Never invent facts.
Never create booking counts.
Never create reservation statuses.
Never create customer information.
Never create database information.

If the answer is not explicitly supported by the document context,
say:

I could not find this information in the restaurant policy.

Answer the question directly and briefly.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "system": system_instruction,
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


def answer_policy_question(question: str):

    results = retrieve_relevant_chunks(
        question,
        top_k=2
    )

    documents = results["documents"][0]

    print("\n========== RAG QUESTION ==========")
    print(question)

    print("\n========== RETRIEVED DOCUMENTS ==========")

    for index, document in enumerate(documents, start=1):
        print(f"\n----- Chunk {index} -----")
        print(document)

    context = "\n\n".join(documents)

    prompt = f"""
DOCUMENT CONTEXT
================
{context}
================

QUESTION
================
{question}
================

Answer the QUESTION using ONLY the DOCUMENT CONTEXT.

For a cancellation-policy question, report the cancellation
time limits, fees, deposit rules, and exceptions that appear
in the document.

Do not talk about current bookings or reservation counts.

ANSWER:
"""

    return ask_ollama(prompt)


if __name__ == "__main__":

    question = "What is the cancellation policy?"

    answer = answer_policy_question(question)

    print("\n========== RAG ANSWER ==========")
    print(answer)