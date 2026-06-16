from typing import Any, Dict, List, Optional, Sequence

from sqlalchemy import text, select, delete, update, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Select

from database.schema import (
    UploadedDocument,
    DocumentChunk,
    ChatHistory,
    GeneratedQuiz,
    Flashcard,
    GeneratedSummary,
)
from utils.logger import get_logger

logger = get_logger(__name__)


class QueryBuilder:
    @staticmethod
    def build_select(
        model,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        descending: bool = True,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Select:
        query = select(model)
        if filters:
            for key, value in filters.items():
                if hasattr(model, key):
                    if isinstance(value, (list, tuple)):
                        query = query.where(getattr(model, key).in_(value))
                    else:
                        query = query.where(getattr(model, key) == value)
        if order_by and hasattr(model, order_by):
            order_col = getattr(model, order_by)
            query = query.order_by(desc(order_col) if descending else order_col)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        return query


class DocumentQueries:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_document(self, **kwargs) -> UploadedDocument:
        doc = UploadedDocument(**kwargs)
        self.session.add(doc)
        await self.session.flush()
        logger.info(f"Document created: {doc.filename} (id={doc.id})")
        return doc

    async def get_document(self, document_id: int) -> Optional[UploadedDocument]:
        result = await self.session.execute(
            select(UploadedDocument).where(UploadedDocument.id == document_id)
        )
        return result.scalar_one_or_none()

    async def get_user_documents(
        self, user_id: str, status: Optional[str] = None, limit: int = 50, offset: int = 0
    ) -> List[UploadedDocument]:
        filters: Dict[str, Any] = {"user_id": user_id}
        if status:
            filters["status"] = status
        query = QueryBuilder.build_select(
            UploadedDocument, filters, order_by="created_at", descending=True, limit=limit, offset=offset
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update_document_status(
        self, document_id: int, status: str, **extra_fields
    ) -> Optional[UploadedDocument]:
        values = {"status": status, **extra_fields}
        await self.session.execute(
            update(UploadedDocument).where(UploadedDocument.id == document_id).values(**values)
        )
        await self.session.flush()
        logger.info(f"Document {document_id} status updated to '{status}'")
        return await self.get_document(document_id)

    async def delete_document(self, document_id: int) -> bool:
        result = await self.session.execute(
            delete(UploadedDocument).where(UploadedDocument.id == document_id)
        )
        await self.session.flush()
        return result.rowcount > 0

    async def count_user_documents(self, user_id: str) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(UploadedDocument).where(
                UploadedDocument.user_id == user_id
            )
        )
        return result.scalar() or 0


class ChunkQueries:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_chunks(self, chunks: List[DocumentChunk]) -> List[DocumentChunk]:
        self.session.add_all(chunks)
        await self.session.flush()
        logger.info(f"{len(chunks)} chunks created")
        return chunks

    async def get_document_chunks(self, document_id: int) -> List[DocumentChunk]:
        result = await self.session.execute(
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index)
        )
        return list(result.scalars().all())

    async def get_chunks_by_ids(self, chunk_ids: List[int]) -> List[DocumentChunk]:
        result = await self.session.execute(
            select(DocumentChunk).where(DocumentChunk.id.in_(chunk_ids))
        )
        return list(result.scalars().all())

    async def delete_document_chunks(self, document_id: int) -> int:
        result = await self.session.execute(
            delete(DocumentChunk).where(DocumentChunk.document_id == document_id)
        )
        await self.session.flush()
        return result.rowcount

    async def similarity_search(
        self, embedding: List[float], top_k: int = 5, document_ids: Optional[List[int]] = None
    ) -> List[tuple]:
        embedding_str = f"[{','.join(str(v) for v in embedding)}]"
        filters = ""
        if document_ids:
            ids_str = ",".join(str(did) for did in document_ids)
            filters = f"AND dc.document_id IN ({ids_str})"

        query = text(f"""
            SELECT
                dc.id,
                dc.document_id,
                dc.chunk_text,
                dc.chunk_index,
                dc.page_number,
                dc.heading,
                ud.filename,
                1 - (dc.embedding <=> :embedding) AS similarity_score
            FROM document_chunks dc
            JOIN uploaded_documents ud ON ud.id = dc.document_id
            WHERE dc.embedding IS NOT NULL {filters}
            ORDER BY dc.embedding <=> :embedding
            LIMIT :top_k
        """)

        result = await self.session.execute(
            query,
            {"embedding": embedding_str, "top_k": top_k},
        )
        rows = result.fetchall()
        logger.debug(f"Similarity search returned {len(rows)} results")
        return rows


class ChatQueries:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_message(self, **kwargs) -> ChatHistory:
        message = ChatHistory(**kwargs)
        self.session.add(message)
        await self.session.flush()
        return message

    async def get_session_history(
        self, user_id: str, session_id: str, limit: int = 50
    ) -> List[ChatHistory]:
        result = await self.session.execute(
            select(ChatHistory)
            .where(
                ChatHistory.user_id == user_id,
                ChatHistory.session_id == session_id,
            )
            .order_by(ChatHistory.created_at)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_user_sessions(self, user_id: str) -> List[dict]:
        result = await self.session.execute(
            select(
                ChatHistory.session_id,
                ChatHistory.subject,
                func.min(ChatHistory.created_at).label("started_at"),
                func.max(ChatHistory.created_at).label("last_message"),
                func.count().label("message_count"),
            )
            .where(ChatHistory.user_id == user_id)
            .group_by(ChatHistory.session_id, ChatHistory.subject)
            .order_by(desc(func.max(ChatHistory.created_at)))
        )
        rows = result.fetchall()
        return [
            {
                "session_id": row.session_id,
                "subject": row.subject,
                "started_at": row.started_at.isoformat() if row.started_at else None,
                "last_message": row.last_message.isoformat() if row.last_message else None,
                "message_count": row.message_count,
            }
            for row in rows
        ]

    async def delete_session(self, user_id: str, session_id: str) -> int:
        result = await self.session.execute(
            delete(ChatHistory).where(
                ChatHistory.user_id == user_id,
                ChatHistory.session_id == session_id,
            )
        )
        await self.session.flush()
        return result.rowcount


class QuizQueries:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_quiz(self, **kwargs) -> GeneratedQuiz:
        quiz = GeneratedQuiz(**kwargs)
        self.session.add(quiz)
        await self.session.flush()
        return quiz

    async def get_user_quizzes(
        self, user_id: str, limit: int = 20, offset: int = 0
    ) -> List[GeneratedQuiz]:
        query = QueryBuilder.build_select(
            GeneratedQuiz,
            {"user_id": user_id},
            order_by="created_at",
            limit=limit,
            offset=offset,
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_quiz(self, quiz_id: int) -> Optional[GeneratedQuiz]:
        result = await self.session.execute(
            select(GeneratedQuiz).where(GeneratedQuiz.id == quiz_id)
        )
        return result.scalar_one_or_none()

    async def delete_quiz(self, quiz_id: int) -> bool:
        result = await self.session.execute(
            delete(GeneratedQuiz).where(GeneratedQuiz.id == quiz_id)
        )
        await self.session.flush()
        return result.rowcount > 0


class FlashcardQueries:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_flashcards(self, flashcards: List[Flashcard]) -> List[Flashcard]:
        self.session.add_all(flashcards)
        await self.session.flush()
        return flashcards

    async def get_user_flashcards(
        self, user_id: str, set_name: Optional[str] = None, limit: int = 100, offset: int = 0
    ) -> List[Flashcard]:
        filters: Dict[str, Any] = {"user_id": user_id}
        if set_name:
            filters["set_name"] = set_name
        query = QueryBuilder.build_select(
            Flashcard, filters, order_by="created_at", limit=limit, offset=offset
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_flashcard_sets(self, user_id: str) -> List[dict]:
        result = await self.session.execute(
            select(
                Flashcard.set_name,
                Flashcard.subject,
                func.count().label("card_count"),
                func.min(Flashcard.created_at).label("created_at"),
            )
            .where(Flashcard.user_id == user_id)
            .group_by(Flashcard.set_name, Flashcard.subject)
        )
        rows = result.fetchall()
        return [
            {
                "set_name": row.set_name,
                "subject": row.subject,
                "card_count": row.card_count,
                "created_at": row.created_at.isoformat() if row.created_at else None,
            }
            for row in rows
        ]

    async def delete_flashcard_set(self, user_id: str, set_name: str) -> int:
        result = await self.session.execute(
            delete(Flashcard).where(
                Flashcard.user_id == user_id,
                Flashcard.set_name == set_name,
            )
        )
        await self.session.flush()
        return result.rowcount


class SummaryQueries:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_summary(self, **kwargs) -> GeneratedSummary:
        summary = GeneratedSummary(**kwargs)
        self.session.add(summary)
        await self.session.flush()
        return summary

    async def get_user_summaries(
        self, user_id: str, limit: int = 20, offset: int = 0
    ) -> List[GeneratedSummary]:
        query = QueryBuilder.build_select(
            GeneratedSummary,
            {"user_id": user_id},
            order_by="created_at",
            limit=limit,
            offset=offset,
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_summary(self, summary_id: int) -> Optional[GeneratedSummary]:
        result = await self.session.execute(
            select(GeneratedSummary).where(GeneratedSummary.id == summary_id)
        )
        return result.scalar_one_or_none()

    async def delete_summary(self, summary_id: int) -> bool:
        result = await self.session.execute(
            delete(GeneratedSummary).where(GeneratedSummary.id == summary_id)
        )
        await self.session.flush()
        return result.rowcount > 0
