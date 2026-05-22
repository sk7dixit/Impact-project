from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_async_session
from services.flashcard_service import FlashcardService
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/flashcards", tags=["Flashcards"])


@router.post("/generate")
async def generate_flashcards(
    user_id: str = Query(...),
    document_id: int = Query(...),
    num_cards: int = Query(10, ge=1, le=100),
    topics: str = Query("general"),
    difficulty: str = Query("medium"),
    set_name: Optional[str] = Query(None),
    db_session: AsyncSession = Depends(get_async_session),
):
    service = FlashcardService(db_session)
    try:
        result = await service.generate_flashcards(
            user_id=user_id,
            document_id=document_id,
            num_cards=num_cards,
            topics=topics,
            difficulty=difficulty,
            set_name=set_name,
        )
        return {"success": True, "data": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Flashcard generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Flashcard generation failed: {str(e)}")


@router.get("/list")
async def list_flashcards(
    user_id: str = Query(...),
    set_name: Optional[str] = Query(None),
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0),
    db_session: AsyncSession = Depends(get_async_session),
):
    service = FlashcardService(db_session)
    result = await service.get_user_flashcards(
        user_id=user_id, set_name=set_name, limit=limit, offset=offset
    )
    return {"success": True, "data": result}


@router.get("/sets")
async def list_flashcard_sets(
    user_id: str = Query(...),
    db_session: AsyncSession = Depends(get_async_session),
):
    service = FlashcardService(db_session)
    sets = await service.get_flashcard_sets(user_id=user_id)
    return {"success": True, "data": sets}


@router.delete("/sets/{set_name}")
async def delete_flashcard_set(
    set_name: str,
    user_id: str = Query(...),
    db_session: AsyncSession = Depends(get_async_session),
):
    service = FlashcardService(db_session)
    deleted = await service.delete_set(user_id=user_id, set_name=set_name)
    return {
        "success": True,
        "message": f"Deleted {deleted} flashcards from set '{set_name}'",
    }
