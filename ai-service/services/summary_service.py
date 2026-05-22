from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from database.queries import SummaryQueries, DocumentQueries, ChunkQueries
from models.summary_model import SummaryGenerator
from rag.pipeline import RAGPipeline
from utils.logger import get_logger
from utils.helpers import count_words

logger = get_logger(__name__)


class SummaryService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.summary_queries = SummaryQueries(session)
        self.document_queries = DocumentQueries(session)
        self.chunk_queries = ChunkQueries(session)
        self.summary_generator = SummaryGenerator()
        self.rag_pipeline = RAGPipeline(session)

    async def generate_summary(
        self,
        user_id: str,
        document_id: int,
        summary_type: str = "chapter",
        focus_area: str = "general",
        title: Optional[str] = None,
    ) -> Dict[str, Any]:
        logger.info(
            f"Generating {summary_type} summary for document {document_id}"
        )

        doc = await self.document_queries.get_document(document_id)
        if not doc:
            raise ValueError(f"Document {document_id} not found")
        if doc.user_id != user_id:
            raise PermissionError("Document does not belong to this user")

        chunks = await self.chunk_queries.get_document_chunks(document_id)
        context = "\n\n".join([c.chunk_text for c in chunks])

        if not context.strip():
            raise ValueError("No content found in document")

        result = await self.summary_generator.generate(
            context=context,
            summary_type=summary_type,
            focus_area=focus_area,
        )

        summary_title = title or f"Summary: {doc.filename} ({summary_type})"

        saved = await self.summary_queries.create_summary(
            user_id=user_id,
            document_id=document_id,
            title=summary_title,
            subject=doc.subject,
            summary_type=summary_type,
            summary_text=result["summary"],
            word_count=result["word_count"],
        )

        return {
            "summary_id": saved.id,
            "title": saved.title,
            "summary_type": summary_type,
            "summary": result["summary"],
            "word_count": result["word_count"],
            "subject": doc.subject,
            "created_at": saved.created_at.isoformat(),
        }

    async def get_user_summaries(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        summaries = await self.summary_queries.get_user_summaries(
            user_id=user_id, limit=limit, offset=offset
        )
        return [
            {
                "id": s.id,
                "title": s.title,
                "summary_type": s.summary_type,
                "subject": s.subject,
                "word_count": s.word_count,
                "created_at": s.created_at.isoformat(),
            }
            for s in summaries
        ]

    async def get_summary(self, summary_id: int, user_id: str) -> Dict[str, Any]:
        summary = await self.summary_queries.get_summary(summary_id)
        if not summary:
            raise ValueError(f"Summary {summary_id} not found")
        if summary.user_id != user_id:
            raise PermissionError("Summary does not belong to this user")

        return {
            "id": summary.id,
            "title": summary.title,
            "summary_type": summary.summary_type,
            "subject": summary.subject,
            "summary": summary.summary_text,
            "word_count": summary.word_count,
            "created_at": summary.created_at.isoformat(),
        }

    async def delete_summary(self, summary_id: int, user_id: str) -> bool:
        summary = await self.summary_queries.get_summary(summary_id)
        if not summary:
            raise ValueError(f"Summary {summary_id} not found")
        if summary.user_id != user_id:
            raise PermissionError("Summary does not belong to this user")
        return await self.summary_queries.delete_summary(summary_id)
