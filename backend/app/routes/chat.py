import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.chat import ChatRequest, ChatResponse
from app.services.generation.chat_service import handle_message, handle_message_stream
from app.services.memory.session_service import get_history, clear_session

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest):
    answer = handle_message(req.session_id, req.message, req.content_type)
    return ChatResponse(session_id=req.session_id, answer=answer, content_type=req.content_type)


@router.post("/stream")
def chat_stream(req: ChatRequest):
    def generate():
        try:
            for chunk in handle_message_stream(req.session_id, req.message, req.content_type):
                yield f"data: {json.dumps({'c': chunk})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/history/{session_id}")
async def get_session_history(session_id: str):
    history = get_history(session_id)
    return {"session_id": session_id, "messages": history.messages, "summary": history.summary}


@router.delete("/history/{session_id}")
async def delete_session_history(session_id: str):
    clear_session(session_id)
    return {"session_id": session_id, "cleared": True}
