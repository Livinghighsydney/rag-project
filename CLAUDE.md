# CLAUDE.md — Project Bible

> Read this before touching any file. Every architectural decision is documented here.
> If something is not documented here, ask before inventing.

---

## What This Project Is

A **RAG (Retrieval-Augmented Generation) system** that acts as a business growth knowledge base.
Users ask natural language questions about growing a business. The system retrieves relevant
passages from a library of 100+ business books and synthesizes a coached, actionable answer
using Claude (Anthropic). Answers are rewritten — never quoted — in the voice of a business advisor.

**The system must not hallucinate.** Every answer must be grounded in retrieved context.
A faithfulness checker runs after every generation to enforce this.

---

## Tech Stack

| Layer            | Tool                              |
|------------------|-----------------------------------|
| LLM              | Claude Sonnet via Anthropic API   |
| Embeddings       | sentence-transformers BAAI/bge-large-en-v1.5 (local, free) |
| Vector DB        | Pinecone free tier (dense search) |
| Reranker         | Claude (lightweight scoring call) |
| Orchestration    | LangGraph (stateful agentic loop) |
| Backend          | FastAPI + Python                  |
| Frontend         | React + TypeScript + Tailwind     |
| Build tool       | Vite                              |

---

## Architecture Overview

```
User Query (React UI)
        │
        ▼
[FastAPI Route]          ← thin: validates input, calls service, returns response
        │
        ▼
[Chat Service]           ← business logic: builds state, invokes graph, stores memory
        │
        ▼
[LangGraph RAG Graph]    ← agentic loop: retrieve → rerank → generate → check → retry
        │
   ┌────┴────┐
   │         │
[Retrieval  [Generation
 Services]   Services]
   │         │
[Pinecone] [Claude API]
```

**Rule:** Routes call Services. Services call Helpers or DB clients.
Helpers are pure functions — no API calls, no DB, no side effects.

---

## Folder Structure

```
backend/
├── app/
│   ├── main.py               # FastAPI app: registers routers, lifespan startup
│   ├── config.py             # All env vars via pydantic-settings. Import Settings here only.
│   │
│   ├── models/               # Pydantic schemas ONLY. No logic. No imports from services.
│   │   ├── chat.py           # ChatRequest, ChatResponse, Message
│   │   ├── chunk.py          # Chunk, QueryAnalysis, FaithfulnessResult
│   │   └── session.py        # Session, ConversationHistory
│   │
│   ├── routes/               # HTTP layer ONLY. One file per resource.
│   │   ├── chat.py           # POST /chat, DELETE /chat/{session_id}
│   │   └── health.py         # GET /health, GET /health/ready
│   │
│   ├── services/             # Business logic. One concern per file. Keep files short.
│   │   ├── ingestion/
│   │   │   ├── pdf_service.py       # PDF → clean text blocks
│   │   │   ├── md_service.py        # Markdown → clean text blocks
│   │   │   ├── chunk_service.py     # Text → parent/child chunk pairs
│   │   │   ├── embed_service.py     # Chunks → dense + sparse vectors
│   │   │   └── ingest_service.py    # Orchestrates: parse → chunk → embed → upsert
│   │   ├── retrieval/
│   │   │   ├── search_service.py    # Hybrid search on Pinecone
│   │   │   ├── rerank_service.py    # Cohere reranking
│   │   │   └── context_service.py   # Parent fetch + deduplicate + assemble context
│   │   ├── generation/
│   │   │   ├── llm_service.py            # All Claude API calls
│   │   │   ├── query_service.py          # Query analysis + multi-query expansion
│   │   │   └── faithfulness_service.py   # Post-generation hallucination check
│   │   └── memory/
│   │       ├── session_service.py   # Store/retrieve per-session message history
│   │       └── summary_service.py   # Summarize sessions > 10 turns
│   │
│   ├── helpers/              # Pure utility functions. No API calls. No DB. Testable in isolation.
│   │   ├── text.py           # clean_text(), count_tokens(), truncate_to_token_limit()
│   │   ├── hashing.py        # hash_file(), detect_duplicates()
│   │   ├── metadata.py       # get_book_category(), build_chunk_metadata()
│   │   └── prompt_builder.py # Assemble prompt strings from templates + variables
│   │
│   ├── prompts/              # Prompt templates as plain strings. No logic.
│   │   ├── system.py         # SYSTEM_PROMPT — advisor persona + grounding rules
│   │   ├── query_expansion.py  # QUERY_EXPANSION_PROMPT
│   │   ├── faithfulness.py     # FAITHFULNESS_CHECK_PROMPT
│   │   └── summarization.py    # SESSION_SUMMARY_PROMPT
│   │
│   ├── graph/                # LangGraph only. Nodes are thin — they call services.
│   │   ├── state.py          # RAGState TypedDict — the shared state bag
│   │   ├── nodes.py          # One function per node. Each calls a service.
│   │   └── rag_graph.py      # Wire nodes → edges → compiled graph singleton
│   │
│   └── db/                   # External client initialization ONLY. No queries here.
│       ├── pinecone_client.py  # Pinecone index singleton
│       └── api_clients.py      # Anthropic + OpenAI + Cohere client singletons
│
├── scripts/
│   ├── ingest.py             # CLI: runs full ingestion pipeline
│   └── eval_retrieval.py     # CLI: fires test queries, prints retrieval scores
│
└── tests/
    ├── unit/                 # Test helpers and services in isolation (no API calls)
    └── integration/          # Test full flows with real API calls (use sparingly)

frontend/
├── src/
│   ├── components/
│   │   ├── chat/             # ChatWindow, MessageBubble, InputBar, TypingIndicator
│   │   └── layout/           # Header, Sidebar
│   ├── hooks/
│   │   └── useChat.ts        # All chat state + API interaction
│   ├── services/
│   │   └── api.ts            # Raw fetch calls to backend. No state here.
│   └── types/
│       └── index.ts          # All shared TypeScript interfaces
```

---

## Data Flow — Step by Step

### Ingestion (run once)
```
1. scripts/ingest.py
2. → ingest_service.py: discovers all files, deduplicates
3.   → pdf_service.py or md_service.py: file → raw text blocks
4.   → metadata.py helper: assigns book category, author, chapter
5.   → chunk_service.py: text → parent chunks (1500 tok) + child chunks (300 tok)
6.   → embed_service.py: child chunks → dense vector + sparse BM25 vector
7.   → pinecone_client.py: upsert child vectors; store parent text as metadata
```

### Query (per user message)
```
1. POST /chat route receives ChatRequest
2. → chat_service.py: loads session history, builds initial RAGState
3. → rag_graph.py (LangGraph) invokes compiled graph:

   Node 1: analyze_query
     → query_service.py: detect intent, expand to 3-5 rephrasings

   Node 2: retrieve
     → search_service.py: hybrid search for each expanded query, merge with RRF

   Node 3: rerank
     → rerank_service.py: Cohere scores chunks, drops low-relevance ones

   Node 4: assemble_context
     → context_service.py: fetch parents, deduplicate, trim to token budget

   Node 5: generate_answer
     → llm_service.py: Claude generates answer from context + history

   Node 6: check_faithfulness
     → faithfulness_service.py: second Claude call verifies answer is grounded
     → If FAIL and retries < 2: go back to Node 2 with refined query
     → If FAIL and retries >= 2: return graceful "not enough info" message

   Node 7: finalize
     → Returns final answer

4. → session_service.py: stores user message + answer in session history
5. → Route returns ChatResponse
```

---

## Key Design Decisions

### Why parent-child chunking?
Small chunks (300 tok) are embedded for precise semantic matching.
When retrieved, the parent (1500 tok) is returned for full context.
This prevents answers that miss surrounding explanation.

### Why hybrid search (dense + sparse)?
Dense = semantic meaning ("how to grow revenue")
Sparse = exact keywords ("Hormozi", "Profit First", specific terms)
RRF merge = best of both. Neither alone is sufficient.

### Why a faithfulness checker?
Claude can fill gaps when context is thin. The checker makes a second
pass and flags any claim not supported by the retrieved context.
This is the primary hallucination firewall.

### Why LangGraph?
The retry loop (retrieve → generate → check → retry) requires stateful
orchestration. LangGraph manages state across nodes cleanly.

### Why prompts/ is a separate folder?
Prompts change frequently. Keeping them isolated means you tune wording
without touching service logic. Never hardcode prompts inside service files.

### Why helpers/ are pure functions?
Testable without mocking. A junior developer can test `count_tokens("hello")`
with zero setup. Keeps services focused on orchestration, not string math.

---

## Coding Conventions

### File length
- Routes: max ~40 lines
- Services: max ~60 lines
- Helpers: max ~50 lines
- If a file grows beyond this, split it.

### Function length
- Max 20 lines per function. If longer, extract a helper.

### Naming
- Services: verb_noun pattern → `search_chunks()`, `rerank_results()`, `build_context()`
- Helpers: pure verb → `clean_text()`, `count_tokens()`, `hash_file()`
- Routes: REST nouns → `/chat`, `/health`
- LangGraph nodes: verb phrase → `analyze_query`, `check_faithfulness`

### Imports
- Never import a service from a route file directly — use FastAPI Depends()
- Never import a route from a service
- Helpers can be imported anywhere
- Models can be imported anywhere
- DB clients are imported only inside services (not in routes)

### Error handling
- Routes catch exceptions and return proper HTTP status codes
- Services raise specific exceptions (not generic Exception)
- Helpers never raise — they return None or empty on failure

### Environment variables
- No config.py. Load with `python-dotenv` — call `load_dotenv()` once in `main.py`
- Every file that needs an env var does: `import os` then `os.getenv("KEY_NAME")`
- All keys must have an entry in `.env`

---

## Anti-Patterns — Never Do These

| Anti-pattern | Why |
|---|---|
| Business logic in routes | Routes become untestable, logic is hidden |
| Prompts hardcoded in services | Impossible to tune without reading service code |
| One giant service file | Junior developers cannot find the bug |
| Using `os.environ["KEY"]` instead of `os.getenv("KEY")` | Hard crash if key missing; getenv returns None gracefully |
| Calling Claude inside a helper | Helpers must be pure and fast |
| Skipping the faithfulness check | Hallucinations reach the user |
| Fixed-size flat chunking | Destroys sentence and idea boundaries |
| Mocking Pinecone in retrieval tests | Masks real vector quality issues |

---

## Book Categories (used in metadata tagging)

| Category key       | Books |
|--------------------|-------|
| business_systems   | E-Myth Revisited, Systemology, Traction, Get Scalable |
| lead_generation    | 100M Leads, Instant Leads |
| cashflow_finance   | Profit First, Instant Cashflow, Instant Profit |
| team_leadership    | High Output Management, The Advantage, Instant Team Building |
| scaling            | Rockefeller Habits, Good to Great, Buy Back Your Time, 4-Hour Workweek |
| strategy_power     | 48 Laws of Power, Art of War, The Prince, Mastery, 33 Strategies of War |
| psychology         | All Gabor Maté books |
| politics_history   | Robert Caro series, Asian Godfathers, Party Politics in SE Asia |

---

## Environment Variables (all required)

```
ANTHROPIC_API_KEY       Claude LLM
OPENAI_API_KEY          Embeddings (text-embedding-3-large)
PINECONE_API_KEY        Vector DB
PINECONE_INDEX_NAME     Pinecone index name
PINECONE_ENVIRONMENT    e.g. us-east-1-aws
COHERE_API_KEY          Reranker
CORS_ORIGINS            Frontend URL (default: http://localhost:5173)
PARENT_CHUNK_SIZE       Default 1500 tokens
CHILD_CHUNK_SIZE        Default 300 tokens
RETRIEVAL_TOP_K         Candidates before reranking (default 20)
RERANKER_TOP_K          Chunks passed to LLM (default 6)
MAX_FAITHFULNESS_RETRIES Default 2
```

---

## How to Add a New Feature

1. Define the data shape in `models/`
2. Write helper functions in `helpers/` (pure, testable)
3. Write the service in `services/` (calls helpers + DB clients)
4. If it fits in the RAG loop, add a node in `graph/nodes.py` and wire it in `graph/rag_graph.py`
5. If it needs an API endpoint, add a route in `routes/`
6. Write a unit test for the helper, integration test for the service

---

## Running the Project

```bash
# Backend
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # fill in keys
uvicorn app.main:app --reload

# Ingestion (run once after filling .env)
python scripts/ingest.py --corpus-path ../corpus-20261101T082003Z-1-001/corpus

# Frontend
cd frontend
npm install
npm run dev
```
