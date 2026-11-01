from app.models.session import Session, ConversationHistory

_sessions: dict[str, Session] = {}

SHORT_TERM_LIMIT = 5
SUMMARY_TRIGGER = 10


def get_history(session_id: str) -> ConversationHistory:
    session = _sessions.get(session_id)
    if not session:
        return ConversationHistory(messages=[], summary="")
    return ConversationHistory(
        messages=session.messages[-SHORT_TERM_LIMIT:],
        summary=session.summary,
    )


def add_message(session_id: str, role: str, content: str) -> None:
    if session_id not in _sessions:
        _sessions[session_id] = Session(session_id=session_id, messages=[], summary="", turn_count=0)

    session = _sessions[session_id]
    session.messages.append({"role": role, "content": content})
    session.turn_count += 1

    if session.turn_count >= SUMMARY_TRIGGER:
        _compress_session(session)


def clear_session(session_id: str) -> None:
    _sessions.pop(session_id, None)


def _compress_session(session: Session) -> None:
    from app.services.memory.summary_service import summarize_session

    older = session.messages[:-SHORT_TERM_LIMIT]
    if not older:
        return
    session.summary = summarize_session(older)
    session.messages = session.messages[-SHORT_TERM_LIMIT:]
    session.turn_count = SHORT_TERM_LIMIT
