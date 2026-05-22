from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_async_session
from services.quiz_service import QuizService
from utils.logger import get_logger
from utils.validators import validate_quiz_parameters

logger = get_logger(__name__)

router = APIRouter(prefix="/api/quiz", tags=["Quiz"])


@router.post("/generate")
async def generate_quiz(
    user_id: str = Query(...),
    document_id: int = Query(...),
    quiz_type: str = Query("multiple_choice"),
    difficulty: str = Query("medium"),
    num_questions: int = Query(10, ge=1, le=100),
    topics: str = Query("general"),
    title: Optional[str] = Query(None),
    db_session: AsyncSession = Depends(get_async_session),
):
    valid, error = validate_quiz_parameters(quiz_type, difficulty, num_questions)
    if not valid:
        raise HTTPException(status_code=400, detail=error)

    service = QuizService(db_session)
    try:
        result = await service.generate_quiz(
            user_id=user_id,
            document_id=document_id,
            quiz_type=quiz_type,
            difficulty=difficulty,
            num_questions=num_questions,
            topics=topics,
            title=title,
        )
        return {"success": True, "data": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Quiz generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Quiz generation failed: {str(e)}")


@router.get("/list")
async def list_quizzes(
    user_id: str = Query(...),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    db_session: AsyncSession = Depends(get_async_session),
):
    service = QuizService(db_session)
    quizzes = await service.get_user_quizzes(
        user_id=user_id, limit=limit, offset=offset
    )
    return {"success": True, "data": quizzes}


@router.get("/{quiz_id}")
async def get_quiz(
    quiz_id: int,
    user_id: str = Query(...),
    db_session: AsyncSession = Depends(get_async_session),
):
    service = QuizService(db_session)
    try:
        quiz = await service.get_quiz(quiz_id=quiz_id, user_id=user_id)
        return {"success": True, "data": quiz}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/{quiz_id}")
async def delete_quiz(
    quiz_id: int,
    user_id: str = Query(...),
    db_session: AsyncSession = Depends(get_async_session),
):
    service = QuizService(db_session)
    try:
        deleted = await service.delete_quiz(quiz_id=quiz_id, user_id=user_id)
        return {"success": True, "message": "Quiz deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
