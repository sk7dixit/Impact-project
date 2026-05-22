from typing import Any, AsyncGenerator, Dict, List, Optional

from models.llm import LLMFactory
from utils.logger import get_logger

logger = get_logger(__name__)


class Generator:
    def __init__(self):
        self.llm = LLMFactory.get_llm()

    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
    ) -> str:
        logger.debug(f"Generating response with {len(messages)} messages")
        response = await self.llm.generate(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response

    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[str, None]:
        async for chunk in self.llm.generate_stream(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        ):
            yield chunk

    async def generate_with_retry(
        self,
        messages: List[Dict[str, str]],
        max_retries: int = 3,
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
    ) -> str:
        last_error = None
        for attempt in range(max_retries):
            try:
                return await self.generate(
                    messages=messages,
                    temperature=temperature + (attempt * 0.1),
                    max_tokens=max_tokens,
                )
            except Exception as e:
                last_error = e
                logger.warning(
                    f"Generation attempt {attempt + 1} failed: {e}"
                )

        raise last_error or RuntimeError("Generation failed after retries")

    async def generate_structured(
        self,
        messages: List[Dict[str, str]],
        output_schema: Dict[str, Any],
        temperature: float = 0.3,
    ) -> Dict[str, Any]:
        response = await self.generate(
            messages=messages,
            temperature=temperature,
        )
        import json
        try:
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            logger.warning("Failed to parse structured output, returning raw text")
            return {"raw_response": response, "parsed": False}
