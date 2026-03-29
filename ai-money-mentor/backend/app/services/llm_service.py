import json
import re

import httpx
from app.config import get_settings

class LLMService:
    def __init__(self, provider: str = None):
        settings = get_settings()
        self.provider = provider or settings.LLM_PROVIDER
        self.anthropic_key = settings.ANTHROPIC_API_KEY
        self.openai_key = settings.OPENAI_API_KEY
        
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        if self.provider == "claude" and self.anthropic_key:
            return await self._call_claude(system_prompt, user_prompt)
        elif self.provider == "openai" and self.openai_key:
            return await self._call_openai(system_prompt, user_prompt)
        
        # Fallback empty string if no keys provided
        return "{}"

    async def _call_claude(self, system: str, user: str) -> str:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.anthropic_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        data = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 4096,
            "system": system,
            "messages": [{"role": "user", "content": user}]
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, headers=headers, json=data)
            if resp.status_code != 200:
                raise Exception(f"Anthropic API Error: {resp.text}")
            return resp.json()["content"][0]["text"]

    async def _call_openai(self, system: str, user: str) -> str:
        # Simplified mock for openai call
        return "{}"

    async def generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        text = await self.generate(system_prompt, user_prompt)
        return self._extract_json(text)
        
    def _extract_json(self, response_text: str) -> dict:
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass
        
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', response_text)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        first_brace = response_text.find('{')
        last_brace = response_text.rfind('}')
        if first_brace != -1 and last_brace != -1:
            try:
                return json.loads(response_text[first_brace:last_brace + 1])
            except json.JSONDecodeError:
                pass
        
        raise ValueError("Could not extract valid JSON from LLM response")
