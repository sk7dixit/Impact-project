from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_async_session
from services.chat_service import ChatService
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("")
async def chat(
    user_id: str = Query(...),
    question: str = Query(...),
    session_id: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    document_ids: Optional[str] = Query(None),
    temperature: float = Query(0.3, ge=0.0, le=1.0),
    db_session: AsyncSession = Depends(get_async_session),
):
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question is required")

    doc_ids = None
    if document_ids:
        try:
            doc_ids = [int(did.strip()) for did in document_ids.split(",") if did.strip()]
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid document_ids format")

    service = ChatService(db_session)
    result = await service.chat(
        user_id=user_id,
        question=question,
        session_id=session_id,
        subject=subject,
        document_ids=doc_ids,
        temperature=temperature,
    )

    return {
        "success": True,
        "data": result,
    }


@router.get("/history")
async def get_chat_history(
    user_id: str = Query(...),
    session_id: str = Query(...),
    limit: int = Query(50, le=200),
    db_session: AsyncSession = Depends(get_async_session),
):
    service = ChatService(db_session)
    messages = await service.get_history(
        user_id=user_id, session_id=session_id, limit=limit
    )

    return {"success": True, "data": {"session_id": session_id, "messages": messages}}


@router.get("/sessions")
async def get_chat_sessions(
    user_id: str = Query(...),
    db_session: AsyncSession = Depends(get_async_session),
):
    service = ChatService(db_session)
    sessions = await service.get_sessions(user_id=user_id)

    return {"success": True, "data": sessions}


@router.delete("/sessions/{session_id}")
async def delete_chat_session(
    session_id: str,
    user_id: str = Query(...),
    db_session: AsyncSession = Depends(get_async_session),
):
    service = ChatService(db_session)
    deleted = await service.delete_session(
        user_id=user_id, session_id=session_id
    )

    return {
        "success": True,
        "message": f"Deleted {deleted} messages from session {session_id}",
    }
