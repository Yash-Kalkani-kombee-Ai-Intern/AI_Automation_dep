import os

from dotenv import load_dotenv
from google import genai
from langsmith import Client
from langsmith.evaluation import evaluate

load_dotenv()

# --------------------------------------------------
# Configuration
# --------------------------------------------------

MODEL = "gemini-3.6-flash"

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

langsmith_client = Client()

DATASET_NAME = "LLM-Observability-Evaluation"


# --------------------------------------------------
# Create Gemini application
# --------------------------------------------------

def answer_question(inputs):
    question = inputs["question"]

    prompt = f"""
Answer the following question clearly and accurately.

Question:
{question}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    return {
        "answer": response.text
    }


# --------------------------------------------------
# Evaluation dataset
# --------------------------------------------------

examples = [
    {
        "inputs": {
            "question": "What does RAG stand for?"
        },
        "outputs": {
            "answer": "Retrieval-Augmented Generation"
        },
    },
    {
        "inputs": {
            "question": "What is FastAPI?"
        },
        "outputs": {
            "answer": "A Python web framework for building APIs"
        },
    },
    {
        "inputs": {
            "question": "What is Docker?"
        },
        "outputs": {
            "answer": "A platform for building and running applications in containers"
        },
    },
]


# --------------------------------------------------
# Create dataset
# --------------------------------------------------

existing_datasets = list(
    langsmith_client.list_datasets(
        dataset_name=DATASET_NAME
    )
)

if existing_datasets:
    dataset = existing_datasets[0]
    print(f"Using existing dataset: {DATASET_NAME}")

else:
    dataset = langsmith_client.create_dataset(
        dataset_name=DATASET_NAME,
        description="Basic LLM observability evaluation dataset",
    )

    langsmith_client.create_examples(
        inputs=[example["inputs"] for example in examples],
        outputs=[example["outputs"] for example in examples],
        dataset_id=dataset.id,
    )

    print(f"Created dataset: {DATASET_NAME}")


# --------------------------------------------------
# Simple evaluator
# --------------------------------------------------

def correctness_evaluator(inputs, outputs, reference_outputs):

    expected = reference_outputs["answer"].lower()
    actual = outputs["answer"].lower()

    if expected in actual:
        score = 1
    else:
        score = 0

    return {
        "key": "correctness",
        "score": score,
    }


# --------------------------------------------------
# Run evaluation
# --------------------------------------------------

print("\nRunning evaluation...\n")

results = evaluate(
    answer_question,
    data=DATASET_NAME,
    evaluators=[correctness_evaluator],
    experiment_prefix="Gemini-Evaluation",
)

print("\nEvaluation completed.")
print(results)

