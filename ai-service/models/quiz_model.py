from typing import Any, Dict, List, Optional

from utils.logger import get_logger
from models.llm import LLMFactory

logger = get_logger(__name__)

QUIZ_GENERATION_PROMPT = """You are an expert quiz generator. Based on the following study material, generate a quiz.

Study Material:
{context}

Requirements:
- Quiz Type: {quiz_type}
- Difficulty Level: {difficulty}
- Number of Questions: {num_questions}
- Topics to Cover: {topics}

Return the response as a JSON array of question objects. Each object must follow this structure:
{response_format}
"""

RESPONSE_FORMATS = {
    "multiple_choice": """{
  "question": "What is...?",
  "type": "multiple_choice",
  "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
  "correct_answer": "A) ...",
  "explanation": "Explanation of why this is correct"
}""",
    "true_false": """{
  "question": "Statement...",
  "type": "true_false",
  "options": ["True", "False"],
  "correct_answer": "True",
  "explanation": "Explanation"
}""",
    "fill_blank": """{
  "question": "The capital of France is ___.",
  "type": "fill_blank",
  "correct_answer": "Paris",
  "explanation": "Paris is the capital of France"
}""",
    "short_answer": """{
  "question": "Explain the concept of...",
  "type": "short_answer",
  "correct_answer": "Brief model answer...",
  "explanation": "Key points that should be covered"
}""",
}


class QuizGenerator:
    def __init__(self):
        self.llm = LLMFactory.get_llm()

    async def generate(
        self,
        context: str,
        quiz_type: str = "multiple_choice",
        difficulty: str = "medium",
        num_questions: int = 10,
        topics: str = "general",
        temperature: float = 0.4,
    ) -> Dict[str, Any]:
        logger.info(
            f"Generating {quiz_type} quiz: {num_questions} questions, "
            f"difficulty={difficulty}"
        )

        response_format = RESPONSE_FORMATS.get(quiz_type, RESPONSE_FORMATS["multiple_choice"])

        prompt = QUIZ_GENERATION_PROMPT.format(
            context=context[:12000],
            quiz_type=quiz_type.replace("_", " ").title(),
            difficulty=difficulty.title(),
            num_questions=num_questions,
            topics=topics,
            response_format=response_format,
        )

        messages = [
            {
                "role": "system",
                "content": "You are an AI quiz generator. Always return valid JSON arrays.",
            },
            {"role": "user", "content": prompt},
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=temperature,
            max_tokens=4096,
        )

        questions = self._parse_response(response, num_questions)

        return {
            "quiz_type": quiz_type,
            "difficulty": difficulty,
            "total_questions": len(questions),
            "questions": questions,
            "raw_response": response,
        }

    async def generate_mixed(
        self,
        context: str,
        num_questions: int = 10,
        difficulty: str = "medium",
        topics: str = "general",
    ) -> Dict[str, Any]:
        quiz_types = ["multiple_choice", "true_false", "fill_blank", "short_answer"]
        questions_per_type = max(1, num_questions // len(quiz_types))

        all_questions = []
        for qt in quiz_types:
            result = await self.generate(
                context=context,
                quiz_type=qt,
                difficulty=difficulty,
                num_questions=questions_per_type,
                topics=topics,
            )
            all_questions.extend(result["questions"])

        import random
        random.shuffle(all_questions)

        return {
            "quiz_type": "mixed",
            "difficulty": difficulty,
            "total_questions": len(all_questions),
            "questions": all_questions[:num_questions],
        }

    def _parse_response(self, response: str, expected_count: int) -> List[Dict]:
        import re
        import json

        json_match = re.search(r"\[.*\]", response, re.DOTALL)
        if json_match:
            try:
                questions = json.loads(json_match.group())
                if isinstance(questions, list):
                    return questions
            except json.JSONDecodeError:
                pass

        json_match = re.search(r"\{[^}]+\}", response)
        if json_match:
            try:
                single = json.loads(json_match.group())
                if isinstance(single, dict) and "question" in single:
                    return [single]
            except json.JSONDecodeError:
                pass

        logger.warning("Could not parse quiz response as JSON, returning raw")
        return [{"raw": response, "parsed": False}]
