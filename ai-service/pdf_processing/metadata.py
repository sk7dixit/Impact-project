import os
from datetime import datetime
from typing import Dict, Optional

from utils.logger import get_logger

logger = get_logger(__name__)


class MetadataExtractor:
    def extract_file_metadata(self, file_path: str, filename: str) -> Dict:
        stat = os.stat(file_path)
        return {
            "filename": filename,
            "file_path": file_path,
            "file_size_bytes": stat.st_size,
            "file_size_mb": round(stat.st_size / (1024 * 1024), 2),
            "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "extension": os.path.splitext(filename)[1].lower(),
        }

    def extract_subject_from_filename(self, filename: str) -> Optional[str]:
        name_without_ext = os.path.splitext(filename)[0]
        subject_keywords = {
            "mathematics": ["math", "mathematics", "algebra", "calculus", "geometry", "trigonometry"],
            "physics": ["physics", "mechanics", "thermodynamics", "optics", "electromagnetism"],
            "chemistry": ["chemistry", "organic", "inorganic", "biochemistry"],
            "biology": ["biology", "botany", "zoology", "genetics", "ecology"],
            "computer_science": ["computer", "programming", "algorithm", "data structure", "software"],
            "history": ["history", "world war", "civilization", "ancient"],
            "literature": ["literature", "english", "poetry", "prose", "grammar"],
            "economics": ["economics", "economy", "microeconomics", "macroeconomics"],
            "geography": ["geography", "geology", "map", "cartography"],
        }

        name_lower = name_without_ext.lower().replace("_", " ").replace("-", " ")
        for subject, keywords in subject_keywords.items():
            for keyword in keywords:
                if keyword in name_lower:
                    return subject
        return None

    def extract_chapter_info(self, text: str) -> Dict:
        import re
        chapter_info = {
            "chapters_found": [],
            "total_chapters": 0,
            "has_chapters": False,
        }

        chapter_patterns = [
            r"(?:Chapter|CHAPTER|Ch\.|ch\.)\s*(\d+|[IVXLCDM]+)",
            r"(?:Section|SECTION|Sec\.|sec\.)\s*(\d+(?:\.\d+)*)",
            r"(?:Unit|UNIT)\s*(\d+)",
            r"(?:Lesson|LESSON)\s*(\d+)",
            r"^\s*(\d+)\.\s+[A-Z]",
        ]

        for pattern in chapter_patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            if matches:
                chapter_info["chapters_found"] = list(set(matches))
                chapter_info["total_chapters"] = len(chapter_info["chapters_found"])
                chapter_info["has_chapters"] = True
                break

        return chapter_info

    def build_document_metadata(
        self,
        file_path: str,
        filename: str,
        extraction_result: Optional[Dict] = None,
        subject: Optional[str] = None,
    ) -> Dict:
        file_meta = self.extract_file_metadata(file_path, filename)
        subject_guess = subject or self.extract_subject_from_filename(filename)

        metadata = {
            **file_meta,
            "subject": subject_guess,
            "processing_timestamp": datetime.utcnow().isoformat(),
        }

        if extraction_result:
            metadata.update({
                "page_count": extraction_result.get("page_count", 0),
                "total_characters": extraction_result.get("total_characters", 0),
                "document_metadata": extraction_result.get("metadata", {}),
            })

        return metadata
