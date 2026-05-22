from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple


class VectorStore(ABC):
    @abstractmethod
    async def store_embedding(
        self,
        document_id: int,
        chunk_id: int,
        text: str,
        embedding: List[float],
        metadata: Optional[Dict] = None,
    ) -> Any:
        pass

    @abstractmethod
    async def store_embeddings_batch(
        self,
        embeddings_data: List[Dict],
    ) -> int:
        pass

    @abstractmethod
    async def similarity_search(
        self,
        embedding: List[float],
        top_k: int = 5,
        filters: Optional[Dict] = None,
    ) -> List[Dict]:
        pass

    @abstractmethod
    async def delete_document_embeddings(self, document_id: int) -> int:
        pass

    @abstractmethod
    async def get_embedding_count(self, document_id: Optional[int] = None) -> int:
        pass
