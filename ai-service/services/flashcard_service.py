from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from database.queries import FlashcardQueries, DocumentQueries, ChunkQueries
from database.schema import Flashcard
from models.flashcard_model import FlashcardGenerator
from utils.logger import get_logger

logger = get_logger(__name__)


class FlashcardService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.flashcard_queries = FlashcardQueries(session)
        self.document_queries = DocumentQueries(session)
        self.chunk_queries = ChunkQueries(session)
        self.flashcard_generator = FlashcardGenerator()

    async def generate_flashcards(
        self,
        user_id: str,
        document_id: int,
        num_cards: int = 10,
        topics: str = "general",
        difficulty: str = "medium",
        set_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        logger.info(
            f"Generating flashcards for document {document_id}: "
            f"cards={num_cards}, difficulty={difficulty}"
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

        result = await self.flashcard_generator.generate(
            context=context,
            num_cards=num_cards,
            topics=topics,
            difficulty=difficulty,
        )

        flashcard_set_name = set_name or f"Flashcards: {doc.filename}"

        db_flashcards = []
        for card in result.get("flashcards", []):
            db_flashcards.append(Flashcard(
                user_id=user_id,
                document_id=document_id,
                set_name=flashcard_set_name,
                subject=doc.subject,
                question=card.get("question", ""),
                answer=card.get("answer", ""),
                explanation=card.get("explanation", ""),
                difficulty=difficulty,
            ))

        if db_flashcards:
            await self.flashcard_queries.create_flashcards(db_flashcards)

        return {
            "set_name": flashcard_set_name,
            "total_cards": len(db_flashcards),
            "flashcards": [
                {
                    "question": c.question,
                    "answer": c.answer,
                    "explanation": c.explanation,
                }
                for c in db_flashcards
            ],
            "subject": doc.subject,
            "difficulty": difficulty,
        }

    async def get_user_flashcards(
        self,
        user_id: str,
        set_name: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Dict[str, Any]:
        cards = await self.flashcard_queries.get_user_flashcards(
            user_id=user_id, set_name=set_name, limit=limit, offset=offset
        )
        return {
            "total": len(cards),
            "flashcards": [
                {
                    "id": c.id,
                    "set_name": c.set_name,
                    "question": c.question,
                    "answer": c.answer,
                    "explanation": c.explanation,
                    "difficulty": c.difficulty,
                    "subject": c.subject,
                    "created_at": c.created_at.isoformat(),
                }
                for c in cards
            ],
        }

    async def get_flashcard_sets(self, user_id: str) -> List[Dict[str, Any]]:
        return await self.flashcard_queries.get_flashcard_sets(user_id=user_id)

    async def delete_set(self, user_id: str, set_name: str) -> int:
        return await self.flashcard_queries.delete_flashcard_set(
            user_id=user_id, set_name=set_name
        )
