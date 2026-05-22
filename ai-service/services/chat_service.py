from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from database.queries import ChatQueries, DocumentQueries
from rag.pipeline import RAGPipeline
from utils.logger import get_logger
from utils.helpers import generate_session_id

logger = get_logger(__name__)


class ChatService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.chat_queries = ChatQueries(session)
        self.document_queries = DocumentQueries(session)
        self.rag_pipeline = RAGPipeline(session)

    async def chat(
        self,
        user_id: str,
        question: str,
        session_id: Optional[str] = None,
        subject: Optional[str] = None,
        document_ids: Optional[List[int]] = None,
        temperature: float = 0.3,
    ) -> Dict[str, Any]:
        if not session_id:
            session_id = generate_session_id()

        logger.info(
            f"Chat: user={user_id}, session={session_id}, "
            f"question='{question[:50]}...'"
        )

        chat_history = await self.chat_queries.get_session_history(
            user_id=user_id, session_id=session_id
        )

        history_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in chat_history[-10:]
        ]

        if document_ids:
            valid_docs = []
            for doc_id in document_ids:
                doc = await self.document_queries.get_document(doc_id)
                if doc and doc.user_id == user_id:
                    valid_docs.append(doc_id)
            document_ids = valid_docs if valid_docs else None
            if not document_ids:
                logger.warning(f"No valid documents found for user {user_id}")

        result = await self.rag_pipeline.run(
            question=question,
            document_ids=document_ids,
            chat_history=history_messages,
            temperature=temperature,
        )

        await self.chat_queries.add_message(
            user_id=user_id,
            session_id=session_id,
            subject=subject,
            document_ids=document_ids or [],
            role="user",
            content=question,
        )

        await self.chat_queries.add_message(
            user_id=user_id,
            session_id=session_id,
            subject=subject,
            document_ids=document_ids or [],
            role="assistant",
            content=result["answer"],
            source_chunks=[
                {
                    "chunk_id": c["chunk_id"],
                    "document_id": c["document_id"],
                    "filename": c["filename"],
                    "page_number": c["page_number"],
                    "similarity_score": c["similarity_score"],
                }
                for c in result["context_chunks"]
            ],
        )

        return {
            "session_id": session_id,
            "answer": result["answer"],
            "sources": result["sources"],
            "retrieval_time_ms": result["retrieval_time_ms"],
        }

    async def get_history(
        self,
        user_id: str,
        session_id: str,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        messages = await self.chat_queries.get_session_history(
            user_id=user_id, session_id=session_id, limit=limit
        )
        return [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
                "sources": msg.source_chunks,
            }
            for msg in messages
        ]

    async def get_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        return await self.chat_queries.get_user_sessions(user_id=user_id)

    async def delete_session(self, user_id: str, session_id: str) -> int:
        return await self.chat_queries.delete_session(
            user_id=user_id, session_id=session_id
        )
