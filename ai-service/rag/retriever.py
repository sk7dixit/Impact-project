from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from database.queries import ChunkQueries
from embeddings.embedding_model import EmbeddingModel
from embeddings.similarity_search import SimilarityResult, SimilaritySearcher
from utils.logger import get_logger

logger = get_logger(__name__)


class RetrievalResult:
    def __init__(
        self,
        chunks: List[SimilarityResult],
        query: str,
        total_chunks: int,
        retrieval_time_ms: float,
    ):
        self.chunks = chunks
        self.query = query
        self.total_chunks = total_chunks
        self.retrieval_time_ms = retrieval_time_ms

    def to_dict(self) -> Dict:
        return {
            "query": self.query,
            "total_chunks": self.total_chunks,
            "retrieval_time_ms": self.retrieval_time_ms,
            "chunks": [c.to_dict() for c in self.chunks],
        }

    def get_context_text(self, separator: str = "\n\n---\n\n") -> str:
        texts = []
        for chunk in self.chunks:
            source = f"[Source: {chunk.filename}"
            if chunk.page_number:
                source += f", Page {chunk.page_number}"
            if chunk.heading:
                source += f", {chunk.heading}"
            source += "]"
            texts.append(f"{chunk.text}\n{source}")
        return separator.join(texts)


class Retriever:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.embedding_model = EmbeddingModel()
        self.searcher = SimilaritySearcher(session)
        self.chunk_queries = ChunkQueries(session)

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        document_ids: Optional[List[int]] = None,
        min_score: float = 0.0,
        use_hybrid: bool = False,
    ) -> RetrievalResult:
        import time
        start_time = time.time()

        logger.info(
            f"Retrieving for query: '{query[:50]}...', "
            f"top_k={top_k}, hybrid={use_hybrid}"
        )

        if use_hybrid:
            results = await self.searcher.hybrid_search(
                query, top_k=top_k, document_ids=document_ids
            )
        else:
            results = await self.searcher.search(
                query, top_k=top_k, document_ids=document_ids, min_score=min_score
            )

        elapsed_ms = (time.time() - start_time) * 1000

        return RetrievalResult(
            chunks=results,
            query=query,
            total_chunks=len(results),
            retrieval_time_ms=round(elapsed_ms, 2),
        )

    async def retrieve_with_scores(
        self,
        query: str,
        top_k: int = 5,
        document_ids: Optional[List[int]] = None,
    ) -> RetrievalResult:
        return await self.retrieve(
            query, top_k=top_k, document_ids=document_ids, use_hybrid=True
        )

    async def retrieve_multiple_queries(
        self,
        queries: List[str],
        top_k: int = 3,
        document_ids: Optional[List[int]] = None,
    ) -> RetrievalResult:
        all_chunks: Dict[int, SimilarityResult] = {}
        total_time_ms = 0.0
        for query in queries:
            result = await self.retrieve(
                query, top_k=top_k, document_ids=document_ids
            )
            total_time_ms += result.retrieval_time_ms
            for chunk in result.chunks:
                if chunk.chunk_id not in all_chunks:
                    all_chunks[chunk.chunk_id] = chunk

        sorted_chunks = sorted(
            all_chunks.values(),
            key=lambda c: c.similarity_score,
            reverse=True,
        )

        return RetrievalResult(
            chunks=sorted_chunks,
            query=" | ".join(queries),
            total_chunks=len(sorted_chunks),
            retrieval_time_ms=round(total_time_ms, 2),
        )
