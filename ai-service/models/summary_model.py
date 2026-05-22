from typing import Any, Dict, List, Optional

from utils.logger import get_logger
from models.llm import LLMFactory

logger = get_logger(__name__)

SUMMARY_PROMPTS = {
    "chapter": """Create a comprehensive chapter summary from the following study material. Focus on the main concepts, key definitions, important formulas, and critical points that are likely to appear in exams.

Study Material:
{context}

Format the summary with:
- Main topics covered
- Key definitions and concepts
- Important formulas (if applicable)
- Key takeaways
- Exam tips""",

    "short_notes": """Create concise short notes from the following study material for quick revision. Use bullet points, abbreviations, and brief explanations.

Study Material:
{context}

Format as:
- Brief bullet points
- Key terms highlighted
- Quick facts
- One-line definitions""",

    "key_points": """Extract only the most important key points from the following study material. Focus on what is absolutely essential for exam preparation.

Study Material:
{context}

List the top key points with:
- Each point should be 1-2 sentences
- Cover the most critical concepts
- Include any must-remember facts or formulas""",

    "detailed": """Create a detailed, comprehensive summary of the following study material. Include explanations, examples, and thorough coverage of all topics.

Study Material:
{context}

Include:
- Detailed topic explanations
- Examples and applications
- Important derivations
- Comprehensive coverage
- Connections between concepts""",
}


class SummaryGenerator:
    def __init__(self):
        self.llm = LLMFactory.get_llm()

    async def generate(
        self,
        context: str,
        summary_type: str = "chapter",
        focus_area: str = "general",
        temperature: float = 0.3,
    ) -> Dict[str, Any]:
        logger.info(f"Generating {summary_type} summary, focus={focus_area}")

        prompt_template = SUMMARY_PROMPTS.get(
            summary_type, SUMMARY_PROMPTS["chapter"]
        )

        prompt = prompt_template.format(
            context=context[:12000],
        )

        if focus_area and focus_area != "general":
            prompt += f"\n\nSpecial focus area: {focus_area}"

        messages = [
            {
                "role": "system",
                "content": "You are an AI study assistant specializing in creating educational summaries.",
            },
            {"role": "user", "content": prompt},
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=temperature,
            max_tokens=4096,
        )

        return {
            "summary": response,
            "summary_type": summary_type,
            "focus_area": focus_area,
            "word_count": len(response.split()),
            "char_count": len(response),
        }

    async def generate_multi_type(
        self,
        context: str,
        types: List[str] = None,
        focus_area: str = "general",
    ) -> Dict[str, Any]:
        if types is None:
            types = ["short_notes", "key_points"]

        results = {}
        for st in types:
            result = await self.generate(
                context=context,
                summary_type=st,
                focus_area=focus_area,
            )
            results[st] = result

        return {
            "summaries": results,
            "types_generated": types,
        }
