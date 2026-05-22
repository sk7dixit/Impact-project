from typing import Dict, List, Optional, Tuple

from rag.retriever import RetrievalResult
from utils.logger import get_logger

logger = get_logger(__name__)


class ContextManager:
    def __init__(self, max_context_length: int = 8000):
        self.max_context_length = max_context_length

    def build_context(
        self,
        retrieval_result: RetrievalResult,
        max_chars: Optional[int] = None,
        include_sources: bool = True,
    ) -> str:
        limit = max_chars or self.max_context_length
        context_parts = []
        total_chars = 0

        for chunk in retrieval_result.chunks:
            source_info = ""
            if include_sources:
                source_info = f"[Source: {chunk.filename}"
                if chunk.page_number:
                    source_info += f" - Page {chunk.page_number}"
                if chunk.heading:
                    source_info += f" - {chunk.heading}"
                source_info += "]\n"

            entry = f"{source_info}{chunk.text}"
            entry_chars = len(entry)

            if total_chars + entry_chars > limit:
                remaining = limit - total_chars
                if remaining > 200:
                    context_parts.append(entry[:remaining])
                break

            context_parts.append(entry)
            total_chars += entry_chars

        context = "\n\n---\n\n".join(context_parts)

        logger.debug(
            f"Context built: {len(context_parts)} chunks, "
            f"{len(context)} characters"
        )

        return context

    def build_multi_document_context(
        self,
        retrieval_results: Dict[int, RetrievalResult],
        max_chars: Optional[int] = None,
    ) -> str:
        limit = max_chars or self.max_context_length
        all_contexts = []

        for doc_id, result in retrieval_results.items():
            context = self.build_context(
                result,
                max_chars=limit // max(len(retrieval_results), 1),
                include_sources=True,
            )
            if context:
                all_contexts.append(f"=== Document {doc_id} ===\n{context}")

        return "\n\n".join(all_contexts)

    def truncate_context(self, context: str, max_chars: int = 8000) -> str:
        if len(context) <= max_chars:
            return context
        truncated = context[:max_chars]
        last_period = truncated.rfind(".")
        last_newline = truncated.rfind("\n")
        split_point = max(last_period + 1, last_newline, max_chars - 500)
        return truncated[:split_point] + "\n\n[Context truncated due to length...]"

    def extract_sources(self, retrieval_result: RetrievalResult) -> List[Dict]:
        seen = set()
        sources = []
        for chunk in retrieval_result.chunks:
            source_key = f"{chunk.filename}-{chunk.page_number}"
            if source_key not in seen:
                seen.add(source_key)
                sources.append({
                    "filename": chunk.filename,
                    "page_number": chunk.page_number,
                    "heading": chunk.heading,
                    "similarity_score": chunk.similarity_score,
                })
        return sources

    def format_for_llm(
        self,
        context: str,
        question: str,
        max_context_chars: int = 6000,
    ) -> Tuple[str, str]:
        truncated_context = self.truncate_context(context, max_context_chars)
        return truncated_context, question
