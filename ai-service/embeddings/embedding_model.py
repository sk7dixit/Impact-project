import os
from typing import List, Optional, Union

import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from tenacity import retry, stop_after_attempt, wait_exponential

from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


class EmbeddingModel:
    _instance: Optional["EmbeddingModel"] = None

    def __new__(cls) -> "EmbeddingModel":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True
        self.model_name = os.getenv(
            "EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2"
        )
        self.device = os.getenv("EMBEDDING_DEVICE", "cpu")
        self.batch_size = int(os.getenv("EMBEDDING_BATCH_SIZE", "32"))
        self.max_seq_length = int(os.getenv("EMBEDDING_MAX_SEQUENCE_LENGTH", "512"))
        self._model: Optional[SentenceTransformer] = None
        self._dimension: int = int(os.getenv("VECTOR_DIMENSION", "384"))
        logger.info(
            f"EmbeddingModel configured: model={self.model_name}, "
            f"device={self.device}, dimension={self._dimension}"
        )

    def _load_model(self) -> SentenceTransformer:
        if self._model is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            self._model = SentenceTransformer(
                self.model_name,
                device=self.device,
            )
            self._model.max_seq_length = self.max_seq_length
            self._dimension = self._model.get_sentence_embedding_dimension()
            logger.info(
                f"Model loaded: {self.model_name}, "
                f"dimension={self._dimension}, "
                f"max_seq_length={self.max_seq_length}"
            )
        return self._model

    @property
    def dimension(self) -> int:
        if self._model is None:
            self._load_model()
        return self._dimension

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def encode(
        self,
        texts: Union[str, List[str]],
        normalize: bool = True,
        show_progress: bool = False,
    ) -> np.ndarray:
        model = self._load_model()

        if isinstance(texts, str):
            texts = [texts]

        if not texts:
            logger.warning("Empty text list provided for encoding")
            return np.array([])

        cleaned_texts = []
        for t in texts:
            if not t or not t.strip():
                cleaned_texts.append(" ")
            else:
                cleaned_texts.append(t.strip()[: self.max_seq_length * 4])

        logger.debug(f"Encoding {len(cleaned_texts)} texts, batch_size={self.batch_size}")

        embeddings = model.encode(
            cleaned_texts,
            batch_size=self.batch_size,
            show_progress_bar=show_progress,
            normalize_embeddings=normalize,
            convert_to_numpy=True,
        )

        logger.debug(f"Generated embeddings shape: {embeddings.shape}")
        return embeddings

    def encode_query(self, query: str) -> np.ndarray:
        return self.encode(query, normalize=True)

    def encode_batch(
        self, texts: List[str], show_progress: bool = True
    ) -> np.ndarray:
        return self.encode(texts, normalize=True, show_progress=show_progress)

    def compute_similarity(
        self, embedding1: np.ndarray, embedding2: np.ndarray
    ) -> float:
        return float(np.dot(embedding1, embedding2))

    def get_embedding_dimension(self) -> int:
        return self.dimension

    def to_list(self, embedding: np.ndarray) -> List[float]:
        return embedding.tolist() if hasattr(embedding, "tolist") else list(embedding)
