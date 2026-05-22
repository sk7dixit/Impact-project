import os
from typing import List, Optional, Tuple

from utils.logger import get_logger

logger = get_logger(__name__)

MAX_FILE_SIZE_MB = int(os.getenv("MAX_PDF_SIZE_MB", "50"))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
SUPPORTED_EXTENSIONS = {".pdf"}


class ValidationError(Exception):
    pass


def validate_pdf_file(file_path: str) -> None:
    if not os.path.exists(file_path):
        raise ValidationError(f"File not found: {file_path}")

    if not os.path.isfile(file_path):
        raise ValidationError(f"Path is not a file: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValidationError(
            f"Unsupported file type '{ext}'. Only {SUPPORTED_EXTENSIONS} files are supported."
        )

    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE_BYTES:
        raise ValidationError(
            f"File size ({file_size / 1024 / 1024:.1f} MB) exceeds maximum "
            f"allowed size ({MAX_FILE_SIZE_MB} MB)"
        )

    if file_size == 0:
        raise ValidationError("File is empty")

    try:
        with open(file_path, "rb") as f:
            header = f.read(5)
        if header[:4] != b"%PDF":
            raise ValidationError("File does not appear to be a valid PDF")
    except Exception as e:
        raise ValidationError(f"Cannot read file: {e}")


def validate_file_size(file_size: int, max_mb: Optional[int] = None) -> Tuple[bool, str]:
    max_size = (max_mb or MAX_FILE_SIZE_MB) * 1024 * 1024
    if file_size > max_size:
        size_mb = file_size / (1024 * 1024)
        max_size_mb = max_mb or MAX_FILE_SIZE_MB
        return False, f"File size ({size_mb:.1f} MB) exceeds limit ({max_size_mb} MB)"
    if file_size <= 0:
        return False, "File is empty"
    return True, ""


def validate_file_extension(filename: str) -> Tuple[bool, str]:
    ext = os.path.splitext(filename)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        return False, f"Unsupported extension '{ext}'. Only PDF files are allowed."
    return True, ""


def validate_api_key(api_key: Optional[str]) -> Tuple[bool, str]:
    if not api_key:
        return False, "API key is required"
    if len(api_key) < 10:
        return False, "API key is too short"
    return True, ""


def validate_text_input(text: Optional[str], min_length: int = 1, max_length: int = 50000) -> Tuple[bool, str]:
    if not text:
        return False, "Text input is required"
    if not text.strip():
        return False, "Text input cannot be empty"
    if len(text) < min_length:
        return False, f"Text is too short (minimum {min_length} characters)"
    if len(text) > max_length:
        return False, f"Text is too long (maximum {max_length} characters)"
    return True, ""


def validate_quiz_parameters(
    quiz_type: str,
    difficulty: str,
    num_questions: int,
) -> Tuple[bool, str]:
    valid_types = {"multiple_choice", "true_false", "fill_blank", "short_answer", "mixed"}
    if quiz_type not in valid_types:
        return False, f"Invalid quiz type. Must be one of: {valid_types}"

    valid_difficulties = {"easy", "medium", "hard"}
    if difficulty not in valid_difficulties:
        return False, f"Invalid difficulty. Must be one of: {valid_difficulties}"

    if num_questions < 1 or num_questions > 100:
        return False, "Number of questions must be between 1 and 100"

    return True, ""


def sanitize_filename(filename: str) -> str:
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    filename = "".join(c for c in filename if c.isprintable())
    return filename.strip() or "document"
