import os
from dotenv import load_dotenv

load_dotenv()

print("LangSmith tracing:", os.getenv("LANGSMITH_TRACING"))
print("LangSmith project:", os.getenv("LANGSMITH_PROJECT"))

if os.getenv("LANGSMITH_API_KEY"):
    print("LangSmith API key: Loaded")
else:
    print("LangSmith API key: Missing")

if os.getenv("GOOGLE_API_KEY"):
    print("Gemini API key: Loaded")
else:
    print("Gemini API key: Missing")