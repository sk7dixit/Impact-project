from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from database.queries import QuizQueries, DocumentQueries, ChunkQueries
from models.quiz_model import QuizGenerator
from rag.pipeline import RAGPipeline
from utils.logger import get_logger

logger = get_logger(__name__)


class QuizService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.quiz_queries = QuizQueries(session)
        self.document_queries = DocumentQueries(session)
        self.chunk_queries = ChunkQueries(session)
        self.quiz_generator = QuizGenerator()
        self.rag_pipeline = RAGPipeline(session)

    async def generate_quiz(
        self,
        user_id: str,
        document_id: int,
        quiz_type: str = "multiple_choice",
        difficulty: str = "medium",
        num_questions: int = 10,
        topics: str = "general",
        title: Optional[str] = None,
    ) -> Dict[str, Any]:
        logger.info(
            f"Generating quiz for document {document_id}: "
            f"type={quiz_type}, difficulty={difficulty}, "
            f"questions={num_questions}"
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

        result = await self.quiz_generator.generate(
            context=context,
            quiz_type=quiz_type,
            difficulty=difficulty,
            num_questions=num_questions,
            topics=topics,
        )

        quiz_title = title or f"Quiz: {doc.filename} ({quiz_type})"

        saved = await self.quiz_queries.create_quiz(
            user_id=user_id,
            document_id=document_id,
            title=quiz_title,
            subject=doc.subject,
            quiz_type=quiz_type,
            difficulty=difficulty,
            quiz_data=result,
            total_questions=len(result.get("questions", [])),
        )

        return {
            "quiz_id": saved.id,
            "title": saved.title,
            "quiz_type": quiz_type,
            "difficulty": difficulty,
            "total_questions": saved.total_questions,
            "questions": result.get("questions", []),
            "created_at": saved.created_at.isoformat(),
        }

    async def get_user_quizzes(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        quizzes = await self.quiz_queries.get_user_quizzes(
            user_id=user_id, limit=limit, offset=offset
        )
        return [
            {
                "id": q.id,
                "title": q.title,
                "quiz_type": q.quiz_type,
                "difficulty": q.difficulty,
                "total_questions": q.total_questions,
                "subject": q.subject,
                "created_at": q.created_at.isoformat(),
            }
            for q in quizzes
        ]

    async def get_quiz(self, quiz_id: int, user_id: str) -> Dict[str, Any]:
        quiz = await self.quiz_queries.get_quiz(quiz_id)
        if not quiz:
            raise ValueError(f"Quiz {quiz_id} not found")
        if quiz.user_id != user_id:
            raise PermissionError("Quiz does not belong to this user")

        return {
            "id": quiz.id,
            "title": quiz.title,
            "quiz_type": quiz.quiz_type,
            "difficulty": quiz.difficulty,
            "total_questions": quiz.total_questions,
            "subject": quiz.subject,
            "questions": quiz.quiz_data.get("questions", []),
            "created_at": quiz.created_at.isoformat(),
        }

    async def delete_quiz(self, quiz_id: int, user_id: str) -> bool:
        quiz = await self.quiz_queries.get_quiz(quiz_id)
        if not quiz:
            raise ValueError(f"Quiz {quiz_id} not found")
        if quiz.user_id != user_id:
            raise PermissionError("Quiz does not belong to this user")
        return await self.quiz_queries.delete_quiz(quiz_id)
