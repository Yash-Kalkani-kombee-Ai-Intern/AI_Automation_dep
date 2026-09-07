import os
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from google import genai
from google.genai import types
from pydantic import BaseModel

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="LLM Chatbot API")

# --------------------------------------------------
# Gemini Client
# --------------------------------------------------

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Fallback to prevent crash if not set, or let genai find it from env
    api_key = ""

client = genai.Client(api_key=api_key) if api_key else genai.Client()


# --------------------------------------------------
# System Prompt
# --------------------------------------------------

SYSTEM_PROMPT = """
You are a helpful and professional AI assistant.

Rules:
- Answer clearly and accurately.
- Use simple and easy-to-understand language.
- Maintain context from previous messages.
- If you do not know something, clearly say that you do not know.
- Do not invent or make up facts.
- Stay within your knowledge boundaries.
- Be polite and professional.
- Keep responses concise unless the user asks for more detail.
"""


# --------------------------------------------------
# Conversation Memory
# --------------------------------------------------

chat_sessions: Dict[str, Any] = {}
chat_history: Dict[str, List[Dict[str, str]]] = {}


# --------------------------------------------------
# Request Model
# --------------------------------------------------

class ChatRequest(BaseModel):
    session_id: str
    message: str


# --------------------------------------------------
# Serve Frontend
# --------------------------------------------------

static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(static_dir)),
        name="static",
    )


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    index_file = BASE_DIR / "templates" / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Template not found")
    return HTMLResponse(content=index_file.read_text(encoding="utf-8"))


# --------------------------------------------------
# Chat API
# --------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest) -> Dict[str, Any]:
    # Create new session if not existing
    if request.session_id not in chat_sessions:
        chat_sessions[request.session_id] = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            ),
        )
        chat_history[request.session_id] = []

    # Get existing chat session
    session_chat = chat_sessions[request.session_id]

    # Send message to Gemini
    response = session_chat.send_message(
        message=request.message
    )

    response_text = response.text or ""

    # Save user message
    chat_history[request.session_id].append({
        "role": "user",
        "message": request.message,
    })

    # Save AI response
    chat_history[request.session_id].append({
        "role": "assistant",
        "message": response_text,
    })

    return {
        "session_id": request.session_id,
        "response": response_text,
    }


# --------------------------------------------------
# Get Chat History
# --------------------------------------------------

@app.get("/chat/{session_id}/history")
def get_chat_history(session_id: str) -> Dict[str, Any]:
    if session_id not in chat_history:
        return {
            "session_id": session_id,
            "history": [],
        }

    return {
        "session_id": session_id,
        "history": chat_history[session_id],
    }


# --------------------------------------------------
# Delete Chat History
# --------------------------------------------------

@app.delete("/chat/{session_id}")
def delete_chat(session_id: str) -> Dict[str, Any]:
    if session_id in chat_sessions:
        del chat_sessions[session_id]

    if session_id in chat_history:
        del chat_history[session_id]

    return {
        "message": "Chat history deleted",
        "session_id": session_id,
    }