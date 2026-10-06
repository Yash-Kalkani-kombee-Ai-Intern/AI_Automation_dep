from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

    try:

        question = request.question.strip()

        if not question:
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty.",
            )

        print("\n========== CHAT REQUEST ==========")
        print(f"Question: {question}")

        # AI Router decides:
        # SQL / RAG / BOTH
        answer = answer_question(question)

        print("\n========== CHAT ANSWER ==========")
        print(answer)
        print("==================================\n")

        return ChatResponse(
            answer=answer
        )

    except HTTPException:
        raise

    except Exception as e:

        print("\n========== CHAT ERROR ==========")
        print(str(e))
        print("================================\n")

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