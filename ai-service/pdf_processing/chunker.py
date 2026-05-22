import os
import re
from typing import Dict, List, Optional

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    TokenTextSplitter,
)
from utils.logger import get_logger

logger = get_logger(__name__)


class TextChunk:
    def __init__(
        self,
        text: str,
        chunk_index: int,
        page_number: Optional[int] = None,
        heading: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ):
        self.text = text
        self.chunk_index = chunk_index
        self.page_number = page_number
        self.heading = heading
        self.metadata = metadata or {}

    def to_dict(self) -> Dict:
        return {
            "text": self.text,
            "chunk_index": self.chunk_index,
            "page_number": self.page_number,
            "heading": self.heading,
            "metadata": self.metadata,
            "char_count": len(self.text),
            "word_count": len(self.text.split()),
        }


class TextChunker:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        strategy: str = "recursive",
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.strategy = strategy
        logger.info(
            f"TextChunker initialized: size={chunk_size}, "
            f"overlap={chunk_overlap}, strategy={strategy}"
        )

    def chunk_text(
        self,
        text: str,
        pages: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> List[TextChunk]:
        if not text or not text.strip():
            logger.warning("Empty text provided for chunking")
            return []

        if self.strategy == "recursive":
            chunks = self._recursive_split(text)
        elif self.strategy == "token":
            chunks = self._token_split(text)
        elif self.strategy == "semantic":
            chunks = self._semantic_split(text, pages)
        else:
            chunks = self._recursive_split(text)

        enriched_chunks = self._enrich_chunks(chunks, pages, metadata)
        logger.info(f"Text chunked into {len(enriched_chunks)} chunks")
        return enriched_chunks

    def _recursive_split(self, text: str) -> List[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len,
        )
        return splitter.split_text(text)

    def _token_split(self, text: str) -> List[str]:
        splitter = TokenTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        return splitter.split_text(text)

    def _semantic_split(self, text: str, pages: Optional[List[str]] = None) -> List[str]:
        paragraphs = re.split(r"\n\s*\n", text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        chunks = []
        current_chunk = []
        current_size = 0

        for para in paragraphs:
            para_size = len(para)
            if current_size + para_size > self.chunk_size and current_chunk:
                chunks.append("\n\n".join(current_chunk))
                overlap_text = current_chunk
                current_chunk = []
                current_size = 0
                overlap_size = 0
                for old_para in reversed(overlap_text):
                    if overlap_size + len(old_para) <= self.chunk_overlap:
                        current_chunk.insert(0, old_para)
                        overlap_size += len(old_para)
                    else:
                        break
                current_chunk.append(para)
                current_size = sum(len(p) for p in current_chunk)
            else:
                current_chunk.append(para)
                current_size += para_size

        if current_chunk:
            chunks.append("\n\n".join(current_chunk))

        return chunks if chunks else [text]

    def _enrich_chunks(
        self,
        chunks: List[str],
        pages: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> List[TextChunk]:
        enriched = []
        running_char_count = 0

        for idx, chunk_text in enumerate(chunks):
            page_number = self._estimate_page_number(
                chunk_text, pages, running_char_count
            )
            heading = self._extract_heading(chunk_text)

            enriched.append(TextChunk(
                text=chunk_text,
                chunk_index=idx,
                page_number=page_number,
                heading=heading,
                metadata={
                    **(metadata or {}),
                    "chunk_strategy": self.strategy,
                    "chunk_size": len(chunk_text),
                },
            ))
            running_char_count += len(chunk_text)

        return enriched

    def _estimate_page_number(
        self,
        chunk_text: str,
        pages: Optional[List[str]],
        running_char_count: int,
    ) -> Optional[int]:
        if not pages:
            return None
        chars_per_page = sum(len(p) for p in pages) / max(len(pages), 1)
        estimated_page = int(running_char_count / max(chars_per_page, 1)) + 1
        return min(estimated_page, len(pages))

    def _extract_heading(self, chunk_text: str) -> Optional[str]:
        lines = chunk_text.strip().split("\n")
        for line in lines[:3]:
            stripped = line.strip()
            if stripped and len(stripped) < 100 and (
                stripped.isupper() or
                stripped.endswith(":") or
                re.match(r"^(?:Chapter|Section|\d+\.)\s", stripped)
            ):
                return stripped[:100]
        return None

    def chunk_by_pages(self, pages: List[str], metadata: Optional[Dict] = None) -> List[TextChunk]:
        chunks = []
        for page_num, page_text in enumerate(pages):
            page_chunks = self.chunk_text(page_text, metadata=metadata)
            for chunk in page_chunks:
                chunk.page_number = page_num + 1
            chunks.extend(page_chunks)
        return chunks
