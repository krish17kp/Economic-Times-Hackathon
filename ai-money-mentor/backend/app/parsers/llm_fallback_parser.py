"""
LAYER 2: LLM-based extraction from raw PDF text.
Called when pdfplumber extraction returns < 2 funds.
"""
import json
import re
from typing import Dict, Any, Optional
from app.parsers.pdf_parser import extract_full_text
from app.config import get_settings


def _call_llm_sync(raw_text: str) -> str:
    """Synchronous LLM call — works inside async via run_in_executor or direct."""
    settings = get_settings()

    prompt = f"""Extract mutual fund data from this CAMS/financial statement text.

Return JSON ONLY, no explanations:
{{
  "investor_name": "string or null",
  "statement_date": "YYYY-MM-DD or null",
  "funds": [
    {{
      "fund_name": "exact fund name",
      "purchase_value": number,
      "current_value": number,
      "units": number_or_null,
      "nav": number_or_null,
      "folio": "string_or_null"
    }}
  ]
}}

Rules:
- Numbers use Indian format like 1,23,456.78 — remove commas when returning
- Extract ALL funds that have both purchase_value and current_value
- If only current_value is visible, use it as purchase_value too
- Return empty funds array if no fund data found

TEXT:
{raw_text[:12000]}"""

    # Try Anthropic Claude first
    if settings.ANTHROPIC_API_KEY:
        try:
            import httpx
            resp = httpx.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": settings.ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json={
                    "model": "claude-3-5-sonnet-20241022",
                    "max_tokens": 4096,
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=60.0
            )
            if resp.status_code == 200:
                return resp.json()["content"][0]["text"]
        except Exception:
            pass

    # Try OpenAI as backup
    if settings.OPENAI_API_KEY:
        try:
            import httpx
            resp = httpx.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You are a financial document parser. Return only valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 4096,
                    "temperature": 0.1
                },
                timeout=60.0
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
        except Exception:
            pass

    return ""


def _parse_json_safely(text: str) -> Optional[dict]:
    """Try multiple strategies to extract JSON from LLM response."""
    if not text:
        return None

    # Strategy 1: direct parse
    try:
        return json.loads(text)
    except Exception:
        pass

    # Strategy 2: extract from markdown code block
    match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if match:
        try:
            return json.loads(match.group(1))
        except Exception:
            pass

    # Strategy 3: find first { to last }
    first = text.find('{')
    last = text.rfind('}')
    if first != -1 and last != -1:
        try:
            return json.loads(text[first:last + 1])
        except Exception:
            pass

    return None


async def extract_with_llm(raw_text: str) -> Dict[str, Any]:
    """
    LAYER 2: Send raw text to LLM to extract structured fund data.
    Returns dict with 'funds' list. Never raises — returns empty funds on failure.
    """
    try:
        import asyncio
        loop = asyncio.get_event_loop()
        llm_text = await loop.run_in_executor(None, _call_llm_sync, raw_text)

        if not llm_text:
            return {"funds": [], "confidence": "llm_no_key"}

        parsed = _parse_json_safely(llm_text)
        if not parsed or "funds" not in parsed:
            return {"funds": [], "confidence": "llm_parse_fail"}

        # Validate and clean each fund
        clean_funds = []
        for f in parsed.get("funds", []):
            if not f.get("fund_name"):
                continue
            pv = f.get("purchase_value") or f.get("current_value") or 0
            cv = f.get("current_value") or pv
            if cv > 0:
                clean_funds.append({
                    "fund_name": str(f["fund_name"]).strip(),
                    "purchase_value": float(pv),
                    "current_value": float(cv),
                    "units": f.get("units"),
                    "nav": f.get("nav"),
                    "folio": f.get("folio"),
                    "category": "Uncategorized"
                })

        return {
            "funds": clean_funds,
            "investor_name": parsed.get("investor_name"),
            "statement_date": parsed.get("statement_date"),
            "confidence": "llm_high" if len(clean_funds) >= 2 else "llm_low"
        }

    except Exception:
        return {"funds": [], "confidence": "llm_error"}


async def parse_with_llm(file_path: str) -> Dict[str, Any]:
    """Convenience wrapper that extracts text then calls LLM."""
    raw_text = extract_full_text(file_path)
    result = await extract_with_llm(raw_text)
    result["raw_text"] = raw_text
    return result
