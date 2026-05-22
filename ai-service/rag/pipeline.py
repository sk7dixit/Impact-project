from typing import Any, AsyncGenerator, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from rag.retriever import Retriever
from rag.generator import Generator
from rag.prompt_builder import PromptBuilder
from rag.context_manager import ContextManager
from utils.logger import get_logger

logger = get_logger(__name__)


class RAGPipeline:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.retriever = Retriever(session)
        self.generator = Generator()
        self.prompt_builder = PromptBuilder()
        self.context_manager = ContextManager()

    async def run(
        self,
        question: str,
        top_k: int = 5,
        document_ids: Optional[List[int]] = None,
        temperature: float = 0.3,
        use_hybrid_search: bool = False,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        logger.info(f"RAG Pipeline: question='{question[:50]}...'")

        retrieval_result = await self.retriever.retrieve(
            query=question,
            top_k=top_k,
            document_ids=document_ids,
            use_hybrid=use_hybrid_search,
        )

        context = self.context_manager.build_context(retrieval_result)
        sources = self.context_manager.extract_sources(retrieval_result)

        messages = self.prompt_builder.build_chat_prompt(
            context=context,
            question=question,
            chat_history=chat_history,
        )

        response = await self.generator.generate(
            messages=messages,
            temperature=temperature,
        )

        logger.info(
            f"RAG response generated: {len(response)} chars, "
            f"{len(sources)} sources, "
            f"retrieval: {retrieval_result.retrieval_time_ms}ms"
        )

        return {
            "answer": response,
            "sources": sources,
            "context_chunks": [c.to_dict() for c in retrieval_result.chunks],
            "retrieval_time_ms": retrieval_result.retrieval_time_ms,
            "total_chunks_retrieved": retrieval_result.total_chunks,
        }

    async def run_stream(
        self,
        question: str,
        top_k: int = 5,
        document_ids: Optional[List[int]] = None,
        temperature: float = 0.3,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> AsyncGenerator[str, None]:
        retrieval_result = await self.retriever.retrieve(
            query=question,
            top_k=top_k,
            document_ids=document_ids,
        )

        context = self.context_manager.build_context(retrieval_result)

        messages = self.prompt_builder.build_chat_prompt(
            context=context,
            question=question,
            chat_history=chat_history,
        )

        async for chunk in self.generator.generate_stream(
            messages=messages,
            temperature=temperature,
        ):
            yield chunk

    async def run_with_citations(
        self,
        question: str,
        top_k: int = 5,
        document_ids: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        result = await self.run(
            question=question,
            top_k=top_k,
            document_ids=document_ids,
        )

        citations = []
        for source in result["sources"]:
            citations.append(
                f"[{source['filename']}"
                + (f", p.{source['page_number']}" if source.get("page_number") else "")
                + "]"
            )

        result["citations"] = citations
        result["answer_with_citations"] = (
            f"{result['answer']}\n\n---\nSources: " + "; ".join(citations)
        )

        return result

    async def generate_summary(
        self,
        context: str,
        summary_type: str = "chapter",
        focus_area: str = "general",
        temperature: float = 0.3,
    ) -> Dict[str, Any]:
        messages = self.prompt_builder.build_summary_prompt(
            context=context,
            summary_type=summary_type,
            focus_area=focus_area,
        )

        response = await self.generator.generate(
            messages=messages,
            temperature=temperature,
        )

        return {
            "summary": response,
            "summary_type": summary_type,
            "word_count": len(response.split()),
        }

    async def generate_quiz(
        self,
        context: str,
        quiz_type: str = "multiple_choice",
        difficulty: str = "medium",
        num_questions: int = 10,
        topics: str = "general",
        temperature: float = 0.4,
    ) -> Dict[str, Any]:
        messages = self.prompt_builder.build_quiz_prompt(
            context=context,
            quiz_type=quiz_type,
            difficulty=difficulty,
            num_questions=num_questions,
            topics=topics,
        )

        response = await self.generator.generate(
            messages=messages,
            temperature=temperature,
        )

        import json
        try:
            quiz_data = json.loads(response)
        except json.JSONDecodeError:
            quiz_data = {"raw": response, "format": "text"}

        return {
            "quiz_data": quiz_data,
            "quiz_type": quiz_type,
            "difficulty": difficulty,
            "total_questions": num_questions,
        }

    async def generate_flashcards(
        self,
        context: str,
        num_cards: int = 10,
        topics: str = "general",
        difficulty: str = "medium",
        temperature: float = 0.4,
    ) -> Dict[str, Any]:
        messages = self.prompt_builder.build_flashcard_prompt(
            context=context,
            num_cards=num_cards,
            topics=topics,
            difficulty=difficulty,
        )

        response = await self.generator.generate(
            messages=messages,
            temperature=temperature,
        )

        import json
        try:
            flashcard_data = json.loads(response)
        except json.JSONDecodeError:
            flashcard_data = {"raw": response, "format": "text"}

        return {
            "flashcards": flashcard_data,
            "total_cards": num_cards,
            "difficulty": difficulty,
        }
