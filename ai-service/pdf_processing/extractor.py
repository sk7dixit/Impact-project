import os
from typing import Dict, List, Optional, Tuple

import fitz

from utils.logger import get_logger
from utils.validators import validate_pdf_file

logger = get_logger(__name__)


class PDFExtractionResult:
    def __init__(
        self,
        text: str,
        pages: List[str],
        page_count: int,
        metadata: Dict,
        file_path: str,
        filename: str,
    ):
        self.text = text
        self.pages = pages
        self.page_count = page_count
        self.metadata = metadata
        self.file_path = file_path
        self.filename = filename

    def to_dict(self) -> Dict:
        return {
            "filename": self.filename,
            "page_count": self.page_count,
            "total_characters": len(self.text),
            "total_pages": len(self.pages),
            "metadata": self.metadata,
        }


class PDFExtractor:
    def __init__(self):
        self.supported_extensions = {".pdf", ".PDF"}

    def extract(self, file_path: str) -> PDFExtractionResult:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        validate_pdf_file(file_path)

        filename = os.path.basename(file_path)
        logger.info(f"Starting PDF extraction: {filename}")

        doc = fitz.open(file_path)
        try:
            page_count = doc.page_count
            pages = []
            full_text = []

            doc_metadata = self._extract_document_metadata(doc)

            for page_num in range(page_count):
                page = doc[page_num]
                page_text = page.get_text("text")
                pages.append(page_text)
                full_text.append(page_text)

            combined_text = "\n\n".join(full_text)

            logger.info(
                f"PDF extracted: {filename}, "
                f"pages={page_count}, "
                f"chars={len(combined_text)}"
            )

            return PDFExtractionResult(
                text=combined_text,
                pages=pages,
                page_count=page_count,
                metadata=doc_metadata,
                file_path=file_path,
                filename=filename,
            )
        finally:
            doc.close()

    def extract_page(self, file_path: str, page_number: int) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        doc = fitz.open(file_path)
        try:
            if page_number < 0 or page_number >= doc.page_count:
                raise ValueError(
                    f"Page number {page_number} out of range. Document has {doc.page_count} pages."
                )
            page = doc[page_number]
            return page.get_text("text")
        finally:
            doc.close()

    def extract_with_images(self, file_path: str) -> Tuple[str, List[bytes]]:
        result = self.extract(file_path)
        images = []

        doc = fitz.open(file_path)
        try:
            for page_num in range(doc.page_count):
                page = doc[page_num]
                image_list = page.get_images()
                for img_idx, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    images.append(image_bytes)
        finally:
            doc.close()

        return result.text, images

    def _extract_document_metadata(self, doc: fitz.Document) -> Dict:
        raw_metadata = doc.metadata or {}
        return {
            "title": raw_metadata.get("title", ""),
            "author": raw_metadata.get("author", ""),
            "subject": raw_metadata.get("subject", ""),
            "keywords": raw_metadata.get("keywords", ""),
            "producer": raw_metadata.get("producer", ""),
            "creator": raw_metadata.get("creator", ""),
            "creation_date": raw_metadata.get("creationDate", ""),
            "modification_date": raw_metadata.get("modDate", ""),
        }
