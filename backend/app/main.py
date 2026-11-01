import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat import router as chat_router
from app.routes.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    from app.db.pinecone_client import get_index
    from app.db.api_clients import get_anthropic_client
    from app.graph.rag_graph import get_graph
    get_index()
    get_anthropic_client()
    get_graph()
    yield


app = FastAPI(title="RAG Business Knowledge Base", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(health_router)
