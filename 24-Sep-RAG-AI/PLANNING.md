# Project Planning & Roadmap: Private AI Business Assistant

This document outlines the step-by-step development roadmap, milestone criteria, and execution rules for building the **Private AI Business Assistant**.

---

## 🧭 Development Methodology

We follow a disciplined, iterative workflow:

```text
CONCEPT  ──►  DESIGN  ──►  IMPLEMENT  ──►  TEST  ──►  IMPROVE  ──►  NEXT PHASE
```

### Core Rules:
1. **Never dump unverified, bloated code all at once.**
2. **Each component must be individually tested and understood before moving to the next phase.**
3. **Keep the engine domain-agnostic; test initially with the Restaurant domain.**
4. **Enforce Read-Only database access by default.**

---

## 📊 Phase Roadmap & Status

| Phase | Description | Status |
| :--- | :--- | :---: |
| **Phase 1** | Project Foundation, Environment & Folder Structure | ✅ Completed |
| **Phase 2** | Local LLM Integration (Ollama Connection & Validation) | ✅ Completed |
| **Phase 3** | Domain Database Setup (SQLite + SQLAlchemy, Read-Only) | ⏳ Ready to Start |
| **Phase 4** | Document Ingestion & Local Embeddings (PDF, TXT, MD) | ⚪ Planned |
| **Phase 5** | RAG Pipeline & ChromaDB Vector Search | ⚪ Planned |
| **Phase 6** | Read-Only SQL Agent & Safe Query Execution | ⚪ Planned |
| **Phase 7** | Intelligent Query Router (SQL vs RAG vs Both) | ⚪ Planned |
| **Phase 8** | Multi-Source Synthesis Engine (Hybrid SQL + RAG Reasoning) | ⚪ Planned |
| **Phase 9** | Conversational Memory & Context Tracking | ⚪ Planned |
| **Phase 10** | Custom Web UI (Vanilla HTML/CSS/JS Chat Interface) | ⚪ Planned |
| **Phase 11** | Security Guardrails & Input Validation | ⚪ Planned |
| **Phase 12** | Evaluation & Test Suite (Correctness & Latency Benchmarks) | ⚪ Planned |
| **Phase 13** | Containerization (Docker Compose Deployment) | ⚪ Planned |
| **Phase 14** | Monitoring, Logging & Observability | ⚪ Planned |

---

## 📋 Detailed Phase Breakdown

### Phase 1: Project Foundation & Setup
- [x] Create project documentation (`README.md` and `PLANNING.md`).
- [x] Create standardized `.gitignore` (ignore venv, SQLite db files, chroma_db, .env).
- [x] Create `.env.example` with environment variable templates (Ollama endpoint, DB URI, model names).
- [x] Create `requirements.txt` with locked/compatible dependencies (`fastapi`, `uvicorn`, `sqlalchemy`, `chromadb`, `requests`, `pypdf`, etc.).
- [x] Set up base directory structure (`backend/`, `frontend/`, `documents/`, `data/`, `tests/`).

### Phase 2: Local LLM Setup (Ollama)
- [x] Create `.env` configuration loader with `pydantic-settings` (`backend/config.py`).
- [x] Build async Python interface / wrapper to interact with local Ollama API (`backend/llm.py`).
- [x] Support text generation, multi-turn chat, JSON mode, and token streaming.
- [x] Implement automated test suite (`tests/test_llm.py`) with graceful reachability checks.

### Phase 3: Domain Database Setup (Restaurant Domain)
- [ ] Create SQLite schema (`customers`, `reservations`, `tables`, `menu_items`, `orders`).
- [ ] Seed realistic sample restaurant data (sample reservations, customer IDs, statuses).
- [ ] Implement SQLAlchemy connection layer with strict **read-only** execution mode.
- [ ] Write integration test to ensure `SELECT` queries succeed while `INSERT`/`UPDATE`/`DELETE` are strictly blocked.

### Phase 4: Document Knowledge Base Ingestion
- [ ] Create sample policy documents in `documents/`:
  - `cancellation_policy.md`
  - `reservation_rules.pdf`
  - `refund_and_deposit_policy.txt`
- [ ] Implement document loader supporting PDF, TXT, and Markdown formats.
- [ ] Implement text chunking strategy with appropriate chunk size and overlap.
- [ ] Connect local embeddings model to generate dense vector embeddings.

### Phase 5: RAG Vector Store & Retrieval Pipeline
- [ ] Initialize persistent ChromaDB vector store.
- [ ] Ingest chunked documents and index embeddings with metadata (source file, section, page).
- [ ] Build retrieval module with cosine similarity / MMR search.
- [ ] Build RAG answer generator with citation of source documents.

### Phase 6: Read-Only SQL Agent
- [ ] Develop database schema introspection tool (providing schema metadata to LLM).
- [ ] Design LLM prompt for converting natural language queries into valid SQLite queries.
- [ ] Build SQL safety sanitizer:
  - Verify AST / query starts with `SELECT`.
  - Block SQL injection patterns, system tables, and write keywords.
- [ ] Execute query and format tabular output for natural language explanation.

### Phase 7: Intelligent Query Router
- [ ] Design classification prompt and heuristics to categorize incoming queries:
  - `SQL` (Structured record lookup)
  - `RAG` (Policy / general knowledge question)
  - `HYBRID` (Requires structured records + policy reasoning)
  - `GENERAL` (Chitchat / greeting / out of scope)
- [ ] Write automated tests verifying routing precision across test question batches.

### Phase 8: Multi-Source Synthesis Engine (Hybrid Reasoning)
- [ ] Orchestrate execution flow for `HYBRID` queries:
  1. Trigger SQL Agent to retrieve live database record.
  2. Trigger RAG Agent with query + entity context to retrieve relevant policy chunks.
  3. Feed both context streams into local LLM synthesis prompt.
- [ ] Generate unified, context-aware answer (e.g., *"Reservation R102 is at 8:00 PM. According to our 2-hour policy, you can cancel until 6:00 PM without fee."*).

### Phase 9: Conversational Memory & Context
- [ ] Implement session-based conversation buffer.
- [ ] Support coreference resolution (e.g., *"Tell me about R102"* -> *"Can I cancel **it**?"*).
- [ ] Maintain token-efficient sliding window history.

### Phase 10: Custom Web Frontend
- [ ] Build clean, responsive single-page chat UI using HTML5, CSS3, and JavaScript.
- [ ] Include collapsible inspection panels:
  - Router classification badge (`SQL` / `RAG` / `Hybrid`)
  - Retrieved policy citations
  - Executed SQL query & raw result table
- [ ] Add loading indicators and real-time response rendering.

### Phase 11: Security & Guardrails
- [ ] Validate and sanitize all user inputs.
- [ ] Prevent prompt injection and sensitive schema leaks.
- [ ] Ensure all secrets reside solely in `.env`.

### Phase 12: Evaluation & Benchmarking
- [ ] Construct evaluation dataset covering SQL, RAG, and Hybrid questions.
- [ ] Measure retrieval precision, SQL generation accuracy, end-to-end latency, and hallucination rate.

### Phase 13 & 14: Containerization & Observability
- [ ] Build `Dockerfile` and `docker-compose.yml`.
- [ ] Add execution latency tracking, request counters, and query logging.

---

## 🎯 Verification Strategy

For each phase, we will execute automated test scripts before marking tasks complete:
1. **Unit Tests:** Verify individual agents (Router, SQL Validator, Chunk Parser).
2. **Integration Tests:** End-to-end query execution with verified expected answers.
3. **Security Audits:** Probing read-only restrictions and invalid inputs.
