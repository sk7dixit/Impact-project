import json
import os
from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, List, Optional

from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


class BaseLLM(ABC):
    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
    ) -> str:
        pass

    @abstractmethod
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[str, None]:
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        pass


class GeminiLLM(BaseLLM):
    def __init__(self):
        import google.genai as genai
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set")
        self.client = genai.Client(api_key=self.api_key)
        logger.info(f"GeminiLLM initialized with model: {self.model_name}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
    ) -> str:
        system_prompt = ""
        contents = []
        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            else:
                contents.append({"role": msg["role"], "parts": [{"text": msg["content"]}]})

        config = {
            "temperature": temperature,
            "system_instruction": system_prompt or None,
        }
        if max_tokens:
            config["max_output_tokens"] = max_tokens

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=contents,
            config=config,
        )
        return response.text

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[str, None]:
        system_prompt = ""
        contents = []
        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            else:
                contents.append({"role": msg["role"], "parts": [{"text": msg["content"]}]})

        config = {
            "temperature": temperature,
            "system_instruction": system_prompt or None,
        }
        if max_tokens:
            config["max_output_tokens"] = max_tokens

        response = self.client.models.generate_content_stream(
            model=self.model_name,
            contents=contents,
            config=config,
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text

    def get_model_name(self) -> str:
        return f"gemini/{self.model_name}"


class OpenAILLM(BaseLLM):
    def __init__(self):
        from openai import AsyncOpenAI
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not set")
        self.client = AsyncOpenAI(api_key=self.api_key)
        logger.info(f"OpenAILLM initialized with model: {self.model_name}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
    ) -> str:
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[str, None]:
        stream = await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def get_model_name(self) -> str:
        return f"openai/{self.model_name}"


class LLMFactory:
    _instance: Optional[BaseLLM] = None

    @classmethod
    def get_llm(cls) -> BaseLLM:
        if cls._instance is not None:
            return cls._instance

        provider = os.getenv("LLM_PROVIDER", "gemini").lower()

        if provider == "openai":
            cls._instance = OpenAILLM()
        elif provider == "gemini":
            cls._instance = GeminiLLM()
        else:
            logger.warning(f"Unknown LLM provider '{provider}', falling back to Gemini")
            cls._instance = GeminiLLM()

        logger.info(f"LLM Factory created: {cls._instance.get_model_name()}")
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        cls._instance = None
        logger.info("LLM Factory reset")
