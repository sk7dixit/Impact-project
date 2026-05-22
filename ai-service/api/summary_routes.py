from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_async_session
from services.summary_service import SummaryService
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/summaries", tags=["Summaries"])


@router.post("/generate")
async def generate_summary(
    user_id: str = Query(...),
    document_id: int = Query(...),
    summary_type: str = Query("chapter"),
    focus_area: str = Query("general"),
    title: Optional[str] = Query(None),
    db_session: AsyncSession = Depends(get_async_session),
):
    valid_types = {"chapter", "short_notes", "key_points", "detailed"}
    if summary_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid summary type. Must be one of: {valid_types}",
        )

    service = SummaryService(db_session)
    try:
        result = await service.generate_summary(
            user_id=user_id,
            document_id=document_id,
            summary_type=summary_type,
            focus_area=focus_area,
            title=title,
        )
        return {"success": True, "data": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Summary generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Summary generation failed: {str(e)}")


@router.get("/list")
async def list_summaries(
    user_id: str = Query(...),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    db_session: AsyncSession = Depends(get_async_session),
):
    service = SummaryService(db_session)
    summaries = await service.get_user_summaries(
        user_id=user_id, limit=limit, offset=offset
    )
    return {"success": True, "data": summaries}


@router.get("/{summary_id}")
async def get_summary(
    summary_id: int,
    user_id: str = Query(...),
    db_session: AsyncSession = Depends(get_async_session),
):
    service = SummaryService(db_session)
    try:
        summary = await service.get_summary(
            summary_id=summary_id, user_id=user_id
        )
        return {"success": True, "data": summary}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/{summary_id}")
async def delete_summary(
    summary_id: int,
    user_id: str = Query(...),
    db_session: AsyncSession = Depends(get_async_session),
):
    service = SummaryService(db_session)
    try:
        deleted = await service.delete_summary(
            summary_id=summary_id, user_id=user_id
        )
        return {"success": True, "message": "Summary deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
