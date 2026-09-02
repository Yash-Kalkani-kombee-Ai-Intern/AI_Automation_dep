import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_text(topic, content_type, tone, length):

    prompt = f"""
    Generate {content_type} about the following topic:

    Topic: {topic}

    Tone: {tone}

    Length: {length}

    Make the content clear, useful, and well-structured.
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text