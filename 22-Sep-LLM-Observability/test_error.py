import os

from dotenv import load_dotenv
from google import genai
from langsmith import traceable

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


@traceable(
    name="Gemini Error Test",
    run_type="llm",
    metadata={
        "ls_provider": "google",
        "ls_model_name": "invalid-model-test",
    },
)
def test_invalid_model():

    print("Calling invalid Gemini model...")

    response = client.models.generate_content(
        model="invalid-model-test",
        contents="Say hello",
    )

    return response.text


if __name__ == "__main__":
    test_invalid_model()