import os
from typing import Dict, List, Optional

from huggingface_hub import AsyncInferenceClient


class HFLLM:
    """
    Hugging Face Serverless Inference (Chat Completions) client.

    Uses the HF Inference router with an OpenAI-compatible chat interface. [page:7]
    Requires a Hugging Face user token (HF_API_KEY) passed as a Bearer token. [page:8]
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        provider: str = "hf-inference",
    ):
        self.api_key = (api_key or os.getenv("HF_API_KEY", "")).strip()
        if not self.api_key:
            raise ValueError("HF_API_KEY is missing")

        self.model = (model or os.getenv("HF_MODEL", "google/gemma-2-2b-it")).strip()
        self.provider = provider

        # Async client for HF Inference routing
        self.client = AsyncInferenceClient(provider=self.provider, api_key=self.api_key)

    async def chat(
        self,
        messages: List[Dict[str, str]],
        *,
        max_tokens: int = 700,
        temperature: float = 0.2,
    ) -> str:
        """
        messages format: [{"role":"user","content":"..."}, ...] [page:7]
        """
        resp = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=False,
        )
        return resp.choices[0].message.content
