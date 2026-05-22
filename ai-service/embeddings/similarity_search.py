from typing import Any, Dict, List, Optional

import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession

from database.queries import ChunkQueries
from embeddings.embedding_model import EmbeddingModel
from embeddings.pgvector_store import PgVectorStore
from utils.logger import get_logger

logger = get_logger(__name__)


class SimilarityResult:
    def __init__(
        self,
        chunk_id: int,
        document_id: int,
        text: str,
        chunk_index: int,
        page_number: Optional[int],
        heading: Optional[str],
        filename: str,
        similarity_score: float,
    ):
        self.chunk_id = chunk_id
        self.document_id = document_id
        self.text = text
        self.chunk_index = chunk_index
        self.page_number = page_number
        self.heading = heading
        self.filename = filename
        self.similarity_score = similarity_score

    def to_dict(self) -> Dict:
        return {
            "chunk_id": self.chunk_id,
            "document_id": self.document_id,
            "text": self.text,
            "chunk_index": self.chunk_index,
            "page_number": self.page_number,
            "heading": self.heading,
            "filename": self.filename,
            "similarity_score": self.similarity_score,
        }


class SimilaritySearcher:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.embedding_model = EmbeddingModel()
        self.vector_store = PgVectorStore(session)
        self.chunk_queries = ChunkQueries(session)

    async def search(
        self,
        query: str,
        top_k: int = 5,
        document_ids: Optional[List[int]] = None,
        min_score: float = 0.0,
    ) -> List[SimilarityResult]:
        logger.info(f"Similarity search: query='{query[:50]}...', top_k={top_k}")

        query_embedding = self.embedding_model.encode_query(query)
        query_embedding_list = query_embedding.tolist()

        filters = {}
        if document_ids:
            filters["document_id"] = document_ids

        results = await self.vector_store.similarity_search(
            embedding=query_embedding_list,
            top_k=top_k,
            filters=filters if filters else None,
        )

        filtered_results = [
            SimilarityResult(
                chunk_id=r["chunk_id"],
                document_id=r["document_id"],
                text=r["text"],
                chunk_index=r["chunk_index"],
                page_number=r["page_number"],
                heading=r["heading"],
                filename=r["filename"],
                similarity_score=r["similarity_score"],
            )
            for r in results
            if r["similarity_score"] >= min_score
        ]

        logger.debug(
            f"Search returned {len(filtered_results)} results "
            f"(filtered from {len(results)})"
        )
        return filtered_results

    async def hybrid_search(
        self,
        query: str,
        top_k: int = 5,
        document_ids: Optional[List[int]] = None,
        keyword_boost: float = 0.3,
    ) -> List[SimilarityResult]:
        semantic_results = await self.search(
            query, top_k=top_k * 2, document_ids=document_ids
        )

        query_lower = query.lower()
        query_terms = set(query_lower.split())

        for result in semantic_results:
            text_lower = result.text.lower()
            term_matches = sum(1 for term in query_terms if term in text_lower)
            keyword_score = term_matches / max(len(query_terms), 1)
            result.similarity_score = (
                result.similarity_score * (1 - keyword_boost)
                + keyword_score * keyword_boost
            )

        semantic_results.sort(key=lambda r: r.similarity_score, reverse=True)
        return semantic_results[:top_k]

    async def search_across_documents(
        self,
        query: str,
        top_k_per_doc: int = 3,
        document_ids: Optional[List[int]] = None,
    ) -> Dict[int, List[SimilarityResult]]:
        results = await self.search(
            query, top_k=top_k_per_doc * 10, document_ids=document_ids
        )

        grouped: Dict[int, List[SimilarityResult]] = {}
        for result in results:
            if result.document_id not in grouped:
                grouped[result.document_id] = []
            if len(grouped[result.document_id]) < top_k_per_doc:
                grouped[result.document_id].append(result)

        return grouped
