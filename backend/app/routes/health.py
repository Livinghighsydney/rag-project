from fastapi import APIRouter
from app.db.pinecone_client import get_index
from app.db.api_clients import get_anthropic_client

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def liveness():
    return {"status": "ok"}


@router.get("/ready")
async def readiness():
    checks = {}
    try:
        get_index()
        checks["pinecone"] = "ok"
    except Exception as e:
        checks["pinecone"] = f"error: {e}"

    try:
        get_anthropic_client()
        checks["anthropic"] = "ok"
    except Exception as e:
        checks["anthropic"] = f"error: {e}"

    all_ok = all(v == "ok" for v in checks.values())
    return {"status": "ready" if all_ok else "degraded", "checks": checks}
