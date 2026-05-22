from typing import Any, Dict, List, Optional

from sqlalchemy import select, func, delete, text
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_async_session
from database.schema import DocumentChunk
from embeddings.vector_store import VectorStore
from utils.logger import get_logger

logger = get_logger(__name__)


class PgVectorStore(VectorStore):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def store_embedding(
        self,
        document_id: int,
        chunk_id: int,
        text: str,
        embedding: List[float],
        metadata: Optional[Dict] = None,
    ) -> DocumentChunk:
        embedding_str = f"[{','.join(str(v) for v in embedding)}]"
        await self.session.execute(
            text("""
                UPDATE document_chunks
                SET embedding = :embedding::vector
                WHERE id = :chunk_id AND document_id = :document_id
            """),
            {
                "embedding": embedding_str,
                "chunk_id": chunk_id,
                "document_id": document_id,
            },
        )
        await self.session.flush()
        logger.debug(f"Embedding stored for chunk {chunk_id}")
        return await self.session.get(DocumentChunk, chunk_id)

    async def store_embeddings_batch(
        self,
        embeddings_data: List[Dict],
    ) -> int:
        stored_count = 0
        for data in embeddings_data:
            await self.store_embedding(
                document_id=data["document_id"],
                chunk_id=data["chunk_id"],
                text=data["text"],
                embedding=data["embedding"],
                metadata=data.get("metadata"),
            )
            stored_count += 1

        await self.session.flush()
        logger.info(f"Stored {stored_count} embeddings in pgvector")
        return stored_count

    async def similarity_search(
        self,
        embedding: List[float],
        top_k: int = 5,
        filters: Optional[Dict] = None,
    ) -> List[Dict]:
        embedding_str = f"[{','.join(str(v) for v in embedding)}]"
        filter_clause = ""
        if filters:
            conditions = []
            if "document_id" in filters:
                doc_ids = filters["document_id"]
                if isinstance(doc_ids, list):
                    ids_str = ",".join(str(d) for d in doc_ids)
                    conditions.append(f"dc.document_id IN ({ids_str})")
                else:
                    conditions.append(f"dc.document_id = {doc_ids}")
            if conditions:
                filter_clause = " AND " + " AND ".join(conditions)

        query = text(f"""
            SELECT
                dc.id,
                dc.document_id,
                dc.chunk_text,
                dc.chunk_index,
                dc.page_number,
                dc.heading,
                ud.filename,
                ud.title,
                1 - (dc.embedding <=> :embedding) AS similarity_score
            FROM document_chunks dc
            JOIN uploaded_documents ud ON ud.id = dc.document_id
            WHERE dc.embedding IS NOT NULL {filter_clause}
            ORDER BY dc.embedding <=> :embedding
            LIMIT :top_k
        """)

        result = await self.session.execute(
            query,
            {"embedding": embedding_str, "top_k": top_k},
        )
        rows = result.fetchall()

        results = []
        for row in rows:
            results.append({
                "chunk_id": row.id,
                "document_id": row.document_id,
                "text": row.chunk_text,
                "chunk_index": row.chunk_index,
                "page_number": row.page_number,
                "heading": row.heading,
                "filename": row.filename,
                "title": row.title,
                "similarity_score": float(row.similarity_score),
            })

        logger.debug(f"Similarity search returned {len(results)} results")
        return results

    async def delete_document_embeddings(self, document_id: int) -> int:
        result = await self.session.execute(
            text("""
                UPDATE document_chunks
                SET embedding = NULL
                WHERE document_id = :document_id
            """),
            {"document_id": document_id},
        )
        await self.session.flush()
        count = result.rowcount
        logger.info(f"Deleted embeddings for document {document_id}: {count} chunks")
        return count

    async def get_embedding_count(self, document_id: Optional[int] = None) -> int:
        query = select(func.count()).select_from(DocumentChunk)
        if document_id:
            query = query.where(DocumentChunk.document_id == document_id)
        query = query.where(DocumentChunk.embedding.isnot(None))
        result = await self.session.execute(query)
        return result.scalar() or 0
