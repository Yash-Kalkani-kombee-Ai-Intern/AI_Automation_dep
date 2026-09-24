import os
import time

from dotenv import load_dotenv
from google import genai
from langsmith import traceable
from langsmith.run_helpers import get_current_run_tree

load_dotenv()

# --------------------------------------------------
# Configuration
# --------------------------------------------------

GEMINI_MODEL = "gemini-3.6-flash"

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def call_gemini_with_retry(prompt: str, max_retries: int = 3, delay: float = 2.0):
    for attempt in range(1, max_retries + 1):
        try:
            return client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )
        except Exception as e:
            if attempt == max_retries:
                raise
            print(f"\n[Warning] API call failed ({e}). Retrying in {delay}s (Attempt {attempt}/{max_retries})...")
            time.sleep(delay)
            delay *= 2


# --------------------------------------------------
# Step 1: Gemini Analysis
# --------------------------------------------------

@traceable(
    name="Gemini Analysis",
    run_type="llm",
    metadata={
        "ls_provider": "google",
        "ls_model_name": GEMINI_MODEL,
    },
)
def analyze_topic(topic):

    prompt = f"""
Analyze the following topic in simple terms:

Topic: {topic}

Give:
1. Definition
2. Main purpose
3. One real-world example
"""

    start_time = time.time()

    response = call_gemini_with_retry(prompt)

    latency = time.time() - start_time

    # ----------------------------------------------
    # Capture Gemini token usage
    # ----------------------------------------------

    usage = response.usage_metadata

    if usage:
        usage_data = {
            "input_tokens": usage.prompt_token_count,
            "output_tokens": usage.candidates_token_count,
            "total_tokens": usage.total_token_count,
        }

        # Attach token usage to LangSmith trace
        current_run = get_current_run_tree()

        if current_run:
            current_run.set(
                usage_metadata=usage_data
            )

        print("\n--- Gemini Analysis Telemetry ---")
        print(f"Latency: {latency:.2f}s")
        print(f"Input tokens: {usage.prompt_token_count}")
        print(f"Output tokens: {usage.candidates_token_count}")
        print(f"Total tokens: {usage.total_token_count}")

    return response.text


# --------------------------------------------------
# Step 2: Gemini Final Answer
# --------------------------------------------------

@traceable(
    name="Gemini Final Answer",
    run_type="llm",
    metadata={
        "ls_provider": "google",
        "ls_model_name": GEMINI_MODEL,
    },
)
def generate_final_answer(topic, analysis):

    prompt = f"""
Create a concise final answer about this topic.

Topic:
{topic}

Analysis:
{analysis}

Explain it clearly for a beginner.
"""

    start_time = time.time()

    response = call_gemini_with_retry(prompt)

    latency = time.time() - start_time

    # ----------------------------------------------
    # Capture Gemini token usage
    # ----------------------------------------------

    usage = response.usage_metadata

    if usage:
        usage_data = {
            "input_tokens": usage.prompt_token_count,
            "output_tokens": usage.candidates_token_count,
            "total_tokens": usage.total_token_count,
        }

        # Attach token usage to LangSmith trace
        current_run = get_current_run_tree()

        if current_run:
            current_run.set(
                usage_metadata=usage_data
            )

        print("\n--- Gemini Final Answer Telemetry ---")
        print(f"Latency: {latency:.2f}s")
        print(f"Input tokens: {usage.prompt_token_count}")
        print(f"Output tokens: {usage.candidates_token_count}")
        print(f"Total tokens: {usage.total_token_count}")

    return response.text


# --------------------------------------------------
# Main Application
# --------------------------------------------------

def main():

    topic = input("Enter a topic: ")

    print("\nStep 1: Analyzing topic...")

    analysis = analyze_topic(topic)

    print("\nStep 2: Generating final answer...")

    final_answer = generate_final_answer(
        topic,
        analysis,
    )

    print("\n========================================")
    print("           FINAL ANSWER")
    print("========================================")

    print(final_answer)


# --------------------------------------------------
# Application Entry Point
# --------------------------------------------------

if __name__ == "__main__":
    main()

