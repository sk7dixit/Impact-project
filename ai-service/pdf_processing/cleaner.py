import re
from typing import List, Optional

from utils.logger import get_logger

logger = get_logger(__name__)


class TextCleaner:
    def __init__(self):
        self._compiled_patterns = {
            "multiple_newlines": re.compile(r"\n{3,}"),
            "multiple_spaces": re.compile(r" {2,}"),
            "multiple_tabs": re.compile(r"\t{2,}"),
            "header_footer_numbers": re.compile(r"^\s*\d+\s*$", re.MULTILINE),
            "page_numbers": re.compile(r"\n\s*\d+\s*\n"),
            "urls": re.compile(r"https?://\S+|www\.\S+"),
            "email": re.compile(r"\S+@\S+\.\S+"),
            "special_chars": re.compile(r"[^\w\s\.\,\!\?\-\(\)\[\]\{\}\:\;\"\'\@\#\$\%\&\*\/\\\+\=\~\`\|<>]"),
            "control_chars": re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]"),
            "unicode_garbage": re.compile(r"[\u200b\u200c\u200d\u2060\u2061\u2062\u2063\u2064\ufeff]"),
            "bullet_chars": re.compile(r"[•●▪■◦‣⁃∙]"),
            "hyphens": re.compile(r"\u2010|\u2011|\u2012|\u2013|\u2014|\u2015"),
            "quotes": re.compile(r"[\u2018\u2019\u201a\u201b]"),
            "double_quotes": re.compile(r"[\u201c\u201d\u201e\u201f]"),
        }

    def clean(self, text: str, options: Optional[dict] = None) -> str:
        if not text:
            logger.warning("Empty text provided for cleaning")
            return ""

        defaults = {
            "remove_urls": True,
            "remove_emails": True,
            "remove_page_numbers": True,
            "remove_header_footers": True,
            "normalize_whitespace": True,
            "normalize_unicode": True,
            "remove_special_chars": False,
            "remove_control_chars": True,
            "preserve_paragraphs": True,
            "max_consecutive_newlines": 2,
            "strip_lines": True,
            "remove_empty_lines": True,
        }
        if options:
            defaults.update(options)
        opts = defaults

        original_length = len(text)

        if opts["normalize_unicode"]:
            text = self._compiled_patterns["hyphens"].sub("-", text)
            text = self._compiled_patterns["quotes"].sub("'", text)
            text = self._compiled_patterns["double_quotes"].sub('"', text)
            text = self._compiled_patterns["bullet_chars"].sub("*", text)
            text = self._compiled_patterns["unicode_garbage"].sub("", text)

        if opts["remove_control_chars"]:
            text = self._compiled_patterns["control_chars"].sub("", text)

        if opts["remove_urls"]:
            text = self._compiled_patterns["urls"].sub("[URL REMOVED]", text)

        if opts["remove_emails"]:
            text = self._compiled_patterns["email"].sub("[EMAIL REMOVED]", text)

        if opts["remove_page_numbers"]:
            text = self._compiled_patterns["page_numbers"].sub("\n", text)

        if opts["remove_header_footers"]:
            text = self._compiled_patterns["header_footer_numbers"].sub("", text)

        if opts["remove_special_chars"]:
            text = self._compiled_patterns["special_chars"].sub(" ", text)

        if opts["normalize_whitespace"]:
            text = self._compiled_patterns["multiple_tabs"].sub("\t", text)
            text = self._compiled_patterns["multiple_spaces"].sub(" ", text)

        if opts["preserve_paragraphs"]:
            max_nl = opts["max_consecutive_newlines"]
            pattern = re.compile(r"\n{" + str(max_nl + 1) + r",}")
            text = pattern.sub("\n" * max_nl, text)

        if opts["strip_lines"]:
            lines = text.split("\n")
            lines = [line.strip() for line in lines]
            text = "\n".join(lines)

        if opts["remove_empty_lines"]:
            lines = [line for line in text.split("\n") if line.strip()]
            text = "\n".join(lines)

        text = text.strip()

        cleaned_length = len(text)
        reduction = ((original_length - cleaned_length) / max(original_length, 1)) * 100

        logger.debug(
            f"Text cleaned: {original_length} -> {cleaned_length} chars "
            f"({reduction:.1f}% reduction)"
        )

        return text

    def clean_pages(self, pages: List[str], options: Optional[dict] = None) -> List[str]:
        return [self.clean(page, options) for page in pages]

    def extract_clean_sentences(self, text: str, min_length: int = 10) -> List[str]:
        cleaned = self.clean(text, {"preserve_paragraphs": False})
        sentences = re.split(r'(?<=[.!?])\s+', cleaned)
        return [s.strip() for s in sentences if len(s.strip()) >= min_length]

    def remove_references_section(self, text: str) -> str:
        patterns = [
            r"\n(?:References|Bibliography|Works Cited|Citations)\s*\n",
            r"\n(?:REFERENCES|BIBLIOGRAPHY|WORKS CITED)\s*\n",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                text = text[: match.start()]
        return text.strip()
