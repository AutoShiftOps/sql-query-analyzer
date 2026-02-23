from huggingface_hub import InferenceClient
import os

class HuggingFaceAnalyzer:
    """Free Hugging Face Inference API (rate-limited)"""
    
    def __init__(self):
        # Users can set their own free HF token
        hf_token = os.getenv("HUGGINGFACE_TOKEN")
        self.client = InferenceClient(token=hf_token)
        self.model = "codellama/CodeLlama-7b-Instruct-hf"
    
    async def analyze_query(self, query: str, parsed_info: dict) -> str:
        prompt = f"""<s>[INST] You are a SQL expert. Analyze this query:

Query: {query}
Tables: {parsed_info.get('tables', [])}
Complexity: {parsed_info.get('complexity_score', 0)}/100

Provide:
1. Performance issues
2. Index recommendations (with CREATE INDEX DDL)
3. Optimized query rewrite

Be concise. [/INST]"""

        try:
            response = self.client.text_generation(
                prompt,
                model=self.model,
                max_new_tokens=512,
                temperature=0.1,
            )
            return response
        except Exception as e:
            return f"LLM unavailable (rate limit or token issue): {e}"
