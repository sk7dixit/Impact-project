import os
import uuid
import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional


def generate_session_id() -> str:
    return str(uuid.uuid4())


def generate_document_hash(file_path: str) -> str:
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def count_words(text: str) -> int:
    return len(text.split())


def truncate_text(text: str, max_chars: int = 100, suffix: str = "...") -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + suffix


def format_file_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB"]
    unit_idx = 0
    size = float(size_bytes)
    while size >= 1024 and unit_idx < len(units) - 1:
        size /= 1024
        unit_idx += 1
    return f"{size:.1f} {units[unit_idx]}"


def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def current_timestamp() -> str:
    return datetime.utcnow().isoformat()


def safe_get(data: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        try:
            data = data[key]
        except (KeyError, TypeError, IndexError):
            return default
    return data


def merge_dicts(base: Dict, override: Dict) -> Dict:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def clean_filename(filename: str) -> str:
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename.strip().strip(".")


def generate_unique_filename(original_filename: str) -> str:
    name, ext = os.path.splitext(original_filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"{name}_{timestamp}_{unique_id}{ext}"


def extract_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()


def is_supported_pdf(filename: str) -> bool:
    return extract_file_extension(filename) == ".pdf"
