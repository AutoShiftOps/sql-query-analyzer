import os
from typing import Optional, Tuple


async def run_llm(provider: str, prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Route LLM requests to the specified provider.
    
    Returns: (ai_insights, model_name)
    If provider not configured, returns (None, None)
    """
    provider = (provider or "huggingface").lower().strip()

    if provider == "huggingface":
        if not os.getenv("HF_API_KEY", "").strip():
            return None, None
        
        from app.llm.hf_client import HFLLM
        llm = HFLLM()
        model = os.getenv("HF_MODEL", "google/gemma-2-2b-it")
        text = await llm.chat([{"role": "user", "content": prompt}])
        return text, model

    if provider == "openai":
        # Enabled when OPENAI_API_KEY is set on server (Render env vars)
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            return None, None
        
        # OpenAI async client (server-side only, never expose key to client)
        try:
            from openai import AsyncOpenAI
        except ImportError:
            # If openai package not installed yet, return None
            return None, None
        
        client = AsyncOpenAI(api_key=api_key)
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=800,
                timeout=30.0,
            )
            return response.choices[0].message.content, model
        except Exception as e:
            # Log error but don't crash the API
            print(f"OpenAI API error: {e}")
            return None, model

    return None, None
