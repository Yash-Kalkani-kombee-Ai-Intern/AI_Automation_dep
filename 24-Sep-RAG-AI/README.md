# Private AI Business Assistant

A privacy-first, local AI assistant capable of answering complex business questions by reasoning across **live structured databases (SQL)** and **unstructured business documents (RAG)** using **local open-source LLMs (Ollama)** with full conversation memory.

---

## 🎯 Core Concept

Traditional chatbots either rely solely on static model weights or basic document search (RAG). Real-world business queries, however, often require correlating **live operational records** (e.g., reservation times, order status, inventory) with **unstructured company policies** (e.g., cancellation rules, refund terms, service guidelines).

The **Private AI Business Assistant** solves this by combining:
1. **Live Structured Data (SQL Database):** Accurate, transactional real-time state.
2. **Private Documents (Vector DB / RAG):** Policies, guides, manuals, and FAQs.
3. **Intelligent Router:** Analyzes user intent to fetch data via SQL, RAG, or both.
4. **Local LLM Execution (Ollama):** 100% on-premise/local execution — zero business data leaks to external APIs.
5. **Conversational Memory:** Context-aware multi-turn conversations.

> **Reusable AI Engine:** The core reasoning engine is domain-agnostic. We build it once using a **Restaurant domain** (reservations + dining policies), and it can be ported to **Airlines, Hotels, E-commerce, Healthcare, or Enterprise IT** simply by swapping the database schema and document store.

---

## 🏗️ Architecture Overview

```text
                               ┌──────────────────┐
                               │       USER       │
                               └────────┬─────────┘
                                        │
                                        ▼
                               ┌──────────────────┐
                               │  Custom Web UI   │
                               │  (HTML/CSS/JS)   │
                               └────────┬─────────┘
                                        │
                                        ▼
                               ┌──────────────────┐
                               │ FastAPI Backend  │
                               └────────┬─────────┘
                                        │
                                        ▼
                               ┌──────────────────┐
                               │ AI Router Agent  │
                               └────────┬─────────┘
                                        │
                 ┌──────────────────────┼──────────────────────┐
                 │                      │                      │
                 ▼                      ▼                      ▼
        ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
        │    SQL Agent    │    │    RAG Agent    │    │   Both Tools    │
        │   (Read-Only)   │    │  (ChromaDB +    │    │ (SQL + Policy)  │
        │                 │    │   Embeddings)   │    │                 │
        └────────┬────────┘    └────────┬────────┘    └────────┬────────┘
                 │                      │                      │
                 ▼                      ▼                      │
        ┌─────────────────┐    ┌─────────────────┐             │
        │  Business DB    │    │  Policy Docs    │             │
        │ (SQLite/Postgres│    │ (PDF/TXT/MD)    │             │
        └────────┬────────┘    └────────┬────────┘             │
                 │                      │                      │
                 └──────────────────────┼──────────────────────┘
                                        │
                                        ▼
                               ┌──────────────────┐
                               │    Local LLM     │
                               │ (Ollama Engine)  │
                               └────────┬─────────┘
                                        │
                                        ▼
                               ┌──────────────────┐
                               │ Synthesized Resp │
                               └──────────────────┘
```

---

## ⚡ Key Differentiator: RAG vs SQL vs Hybrid

| Query Type | Example | Mechanism |
| :--- | :--- | :--- |
| **Structured Only (SQL)** | *"What is the status of reservation R102?"* | Queries SQL tables (`reservations`, `customers`). |
| **Unstructured Only (RAG)** | *"What is your reservation cancellation policy?"* | Vector search in ChromaDB across policy documents. |
| **Hybrid (SQL + RAG)** | *"Can I cancel reservation R102 without a fee?"* | **1.** SQL fetches R102's time (8:00 PM).<br>**2.** RAG fetches cancellation cutoff (2 hours prior).<br>**3.** LLM evaluates current time vs 8 PM and generates a context-aware answer. |

---

## 🛠️ Technology Stack

| Component | Technology | Responsibility |
| :--- | :--- | :--- |
| **Backend & API** | FastAPI (Python) | High-performance async REST API, request orchestration |
| **Frontend UI** | HTML5, CSS3, Vanilla JS | Clean, responsive, interactive custom web chat interface |
| **Local LLM Runtime** | Ollama | Runs open-source LLMs locally (e.g., Llama 3, Mistral, Qwen) |
| **Database & ORM** | SQLite / SQLAlchemy | Structured business records with strict Read-Only constraints |
| **Vector DB** | ChromaDB | Local vector store for document chunk embeddings |
| **Embedding Model** | FastEmbed / HuggingFace Local | Converts document chunks & queries into dense vectors |
| **Agent / Orchestrator** | Custom Python Engine / LangChain | Query routing, SQL generation, synthesis, and memory |
| **Memory** | Session Buffer / Sliding Window | Multi-turn conversational context tracking |
| **Containerization** | Docker & Docker Compose | Self-contained, zero-leak private deployment |

---

## 🔒 Security & Privacy Guarantees

- **100% Local Inference:** No prompts or business data sent to external cloud APIs.
- **Strict Read-Only SQL:** Only `SELECT` statements are executed; write/destructive operations (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`) are blocked at both validation and database connection levels.
- **Credential & Secret Protection:** Zero credentials exposed to the LLM context or frontend; strictly managed via environment variables (`.env`).
- **Input Sanitization:** Guardrails on document uploads and query syntax.

---

## 📁 Target Project Structure

```text
24-Sep-RAG-AI/
│
├── backend/
│   ├── main.py                  # FastAPI application entry point
│   │
│   ├── agents/
│   │   ├── router.py            # Intent classification (SQL / RAG / Both)
│   │   ├── sql_agent.py         # Read-only SQL generation & execution
│   │   └── rag_agent.py         # Vector similarity search & context injection
│   │
│   ├── database/
│   │   ├── connection.py        # SQLAlchemy engine & session setup
│   │   ├── schema.py            # Table models & metadata
│   │   └── query.py             # Safe SQL executor
│   │
│   ├── rag/
│   │   ├── ingest.py            # Document parsing (PDF, TXT, MD) & chunking
│   │   ├── embeddings.py        # Local embedding generator
│   │   └── retriever.py         # ChromaDB retrieval interface
│   │
│   ├── memory/
│   │   └── conversation.py      # Multi-turn history manager
│   │
│   └── security/
│       └── validation.py        # SQL validator & guardrails
│
├── frontend/
│   ├── index.html               # Custom chat interface
│   ├── style.css                # Premium styling & dark mode
│   └── app.js                   # WebSocket / REST client logic
│
├── documents/                   # Business policy documents (PDF, TXT, MD)
├── data/
│   └── restaurant.db            # Initial domain SQLite database
├── chroma_db/                   # Persistent vector store directory
├── tests/                       # Unit and integration test suites
│
├── README.md                    # Project documentation
├── PLANNING.md                  # Development roadmap & phase tracker
├── requirements.txt             # Python dependencies
├── .env.example                 # Template for environment variables
└── .gitignore                   # Ignored files & secrets
```
