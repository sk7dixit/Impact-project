from typing import Any, Dict, List, Optional

from utils.logger import get_logger
from models.llm import LLMFactory

logger = get_logger(__name__)

FLASHCARD_PROMPT = """You are an AI flashcard creator. Based on the study material, create effective flashcards for exam preparation.

Study Material:
{context}

Requirements:
- Number of Cards: {num_cards}
- Focus Topics: {topics}
- Difficulty Level: {difficulty}

Each flashcard should have:
1. A clear, specific question
2. A concise but complete answer
3. A brief explanation

Return a JSON array of flashcard objects:
[
  {{
    "question": "What is photosynthesis?",
    "answer": "The process by which plants convert light energy into chemical energy",
    "explanation": "Photosynthesis occurs in chloroplasts and produces glucose and oxygen",
    "difficulty": "{difficulty}"
  }}
]
"""


class FlashcardGenerator:
    def __init__(self):
        self.llm = LLMFactory.get_llm()

    async def generate(
        self,
        context: str,
        num_cards: int = 10,
        topics: str = "general",
        difficulty: str = "medium",
        temperature: float = 0.4,
    ) -> Dict[str, Any]:
        logger.info(
            f"Generating {num_cards} flashcards, difficulty={difficulty}, topics={topics}"
        )

        prompt = FLASHCARD_PROMPT.format(
            context=context[:12000],
            num_cards=num_cards,
            topics=topics,
            difficulty=difficulty,
        )

        messages = [
            {
                "role": "system",
                "content": "You are an AI flashcard generator. Return valid JSON only.",
            },
            {"role": "user", "content": prompt},
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=temperature,
            max_tokens=4096,
        )

        flashcards = self._parse_response(response, num_cards)

        return {
            "total_cards": len(flashcards),
            "flashcards": flashcards,
            "difficulty": difficulty,
            "topics": topics,
        }

    async def generate_batch(
        self,
        context: str,
        total_cards: int = 30,
        batch_size: int = 10,
        topics: str = "general",
        difficulty: str = "medium",
    ) -> Dict[str, Any]:
        all_flashcards = []
        remaining = total_cards

        while remaining > 0:
            current_batch = min(batch_size, remaining)
            result = await self.generate(
                context=context,
                num_cards=current_batch,
                topics=topics,
                difficulty=difficulty,
            )
            all_flashcards.extend(result["flashcards"])
            remaining -= current_batch

        return {
            "total_cards": len(all_flashcards),
            "flashcards": all_flashcards,
            "difficulty": difficulty,
            "topics": topics,
        }

    def _parse_response(self, response: str, expected_count: int) -> List[Dict]:
        import re
        import json

        json_match = re.search(r"\[.*\]", response, re.DOTALL)
        if json_match:
            try:
                cards = json.loads(json_match.group())
                if isinstance(cards, list):
                    return cards
            except json.JSONDecodeError:
                pass

        logger.warning("Could not parse flashcard response as JSON, returning raw")
        return [{"raw": response, "parsed": False}]
