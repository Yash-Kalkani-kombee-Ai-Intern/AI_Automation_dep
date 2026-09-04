from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="LLM Chatbot API")


# --------------------------------------------------
# Gemini Client
# --------------------------------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


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

chat_sessions = {}

chat_history = {}


# --------------------------------------------------
# Request Model
# --------------------------------------------------

class ChatRequest(BaseModel):
    session_id: str
    message: str


# --------------------------------------------------
# Serve Frontend
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


@app.get("/", response_class=HTMLResponse)
def home():

    with open("templates/index.html", "r", encoding="utf-8") as file:
        return file.read()


# --------------------------------------------------
# Chat API
# --------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    # Create new session
    if request.session_id not in chat_sessions:

        chat_sessions[request.session_id] = client.chats.create(
            model="gemini-3.6-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            )
        )

        chat_history[request.session_id] = []


    # Get existing chat
    chat = chat_sessions[request.session_id]


    # Send message to Gemini
    response = chat.send_message(
        message=request.message
    )


    # Save user message
    chat_history[request.session_id].append({
        "role": "user",
        "message": request.message
    })


    # Save AI response
    chat_history[request.session_id].append({
        "role": "assistant",
        "message": response.text
    })


    return {
        "session_id": request.session_id,
        "response": response.text
    }


# --------------------------------------------------
# Get Chat History
# --------------------------------------------------

@app.get("/chat/{session_id}/history")
def get_chat_history(session_id: str):

    if session_id not in chat_history:

        return {
            "session_id": session_id,
            "history": []
        }


    return {
        "session_id": session_id,
        "history": chat_history[session_id]
    }


# --------------------------------------------------
# Delete Chat History
# --------------------------------------------------

@app.delete("/chat/{session_id}")
def delete_chat(session_id: str):

    if session_id in chat_sessions:
        del chat_sessions[session_id]


    if session_id in chat_history:
        del chat_history[session_id]


    return {
        "message": "Chat history deleted",
        "session_id": session_id
    }