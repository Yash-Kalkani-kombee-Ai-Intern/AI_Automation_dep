import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chat_history import save_chat, get_chat_history
from logger import logger
from router_agent import answer_question
from rag.rag_agent import answer_policy_question

app = FastAPI(
    title="LocalAI API",
    description="Private AI Database and RAG Assistant",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST / RESPONSE MODELS
# ============================================================

class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


class RAGRequest(BaseModel):
    question: str


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "LocalAI API is running",
        "status": "success",
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


# ============================================================
# UNIFIED CHAT
# ============================================================

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    start_time = time.perf_counter()

    try:
        question = request.question.strip()

        if not question:
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty.",
            )

        logger.info(f"QUESTION | {question}")

        answer = answer_question(question)

        save_chat(question, answer)

        elapsed_time = time.perf_counter() - start_time

        logger.info(f"ANSWER | {answer}")
        logger.info(
            f"RESPONSE_TIME | {elapsed_time:.2f} seconds"
        )

        return ChatResponse(answer=answer)

    except HTTPException:
        raise

    except Exception as e:
        elapsed_time = time.perf_counter() - start_time

        logger.error(f"ERROR | {str(e)}")
        logger.error(
            f"RESPONSE_TIME | {elapsed_time:.2f} seconds"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

@app.get("/history")
def history():
    try:
        return {
            "history": get_chat_history()
        }

    except Exception as e:
        logger.error(f"HISTORY_ERROR | {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
# ============================================================
# DIRECT RAG ENDPOINT
# ============================================================

@app.post("/rag", response_model=ChatResponse)
def rag_chat(request: RAGRequest):

    try:

        question = request.question.strip()

        if not question:
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty.",
            )

        answer = answer_policy_question(question)

        return ChatResponse(
            answer=answer
        )

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )