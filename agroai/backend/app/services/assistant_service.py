"""
RAG-based AI assistant using Google Gemini (gemini-2.0-flash).
Location: backend/app/services/assistant_service.py
"""

from typing import Optional
from app.config import settings
from app.schemas.assistant import ALLOWED_CATEGORIES


# ─── Gemini client cache ───────────────────────────────────────────────────
_gemini_model = None


def _load_gemini():
    """Lazily load and cache the Gemini model. Returns None if unavailable."""
    global _gemini_model
    if _gemini_model is not None:
        return _gemini_model
    if not settings.llm_api_key:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.llm_api_key)
        _gemini_model = genai.GenerativeModel("gemini-2.5-flash")
        print("[AI] Gemini model loaded: gemini-2.5-flash")
        return _gemini_model
    except Exception as e:
        print(f"[WARN] Gemini load failed: {e}")
        return None


# ─── NO cache — every question gets a live Gemini answer ──────────────────


# ─── Main entry point ──────────────────────────────────────────────────────
def ask_assistant(question: str, category: str, language: str = "en", context: Optional[dict] = None) -> dict:
    """
    Sends question to Gemini with an agricultural system context.
    Returns a live AI-generated answer.
    """
    # Validate category
    if category not in ALLOWED_CATEGORIES:
        return {
            "answer": f"Category not supported. Choose from: {', '.join(ALLOWED_CATEGORIES)}",
            "sources": [],
            "related_questions": [],
        }

    if not settings.llm_api_key:
        return {
            "answer": "AI assistant is not configured. Please add a Gemini API key in backend/.env (LLM_API_KEY=...).",
            "sources": [],
            "related_questions": [],
        }

    # System instructions — sets personality and domain
    if language == "hi":
        system_prompt = """You are an AgroAI assistant helping Indian farmers convert crop waste into valuable products.

Your responses MUST follow these strict rules:

1. उत्तर केवल सरल हिंदी में दें। अंग्रेज़ी अनुवाद बिल्कुल न दें।
2. छोटे, स्पष्ट, और व्यावहारिक वाक्यों का उपयोग करें। एक बार में अधिकतम 6-8 लाइनें लिखें।
3. हमेशा इस संरचना और नीचे दिए गए इमोजी का पालन करें:

🌱 क्या है:
[संक्षिप्त व्याख्या]

⚙️ प्रक्रिया (Steps):
1. [कदम]
2. [कदम]
...

💰 खर्च (Cost):
[संभावित खर्च या मेहनत]

⚠️ सुझाव (Tips):
[व्यावहारिक सुझाव या चेतावनी]

4. किसान के प्रति सम्मानजनक और मित्रवत रहें।
5. उत्तर अधूरा न छोड़ें।
6. बात को न दोहराएं।"""

    else:
        system_prompt = """You are an AgroAI assistant helping Indian farmers convert crop waste into valuable products.

Your responses MUST follow these strict rules:

1. Answer only in simple English. Do not include Hindi translation.
2. Keep sentences very short, practical, and actionable. Max 6-8 lines visible at once.
3. ALWAYS structure your answer EXACTLY like this using the following emojis and sections:

🌱 What it is:
[Short concise explanation]

⚙️ Steps:
1. [step]
2. [step]
...

💰 Cost:
[Cost or effort details]

⚠️ Tips:
[Practical tips or warnings]

4. Keep tone friendly and respectful.
5. Do NOT give incomplete sentences. Never cut off midway.
6. Do NOT repeat the same greetings or intro lines. Get straight to the point.
7. Focus on farmer-friendly clarity. Avoid dense paragraphs."""

    # Category-specific context hint
    category_hints = {
        "how_to_convert": "The farmer is asking about converting crop waste into a value-added product.",
        "equipment": "The farmer wants equipment guidance — costs, types, where to buy.",
        "quality_tips": "The farmer wants practical tips on waste quality, drying, and storage.",
        "general_policy": "The farmer is asking about government schemes, subsidies, or policy.",
    }
    hint = category_hints.get(category, "")

    full_prompt = f"{system_prompt}\n\nContext: {hint}\n\nFarmer's question: {question}"

    try:
        model = _load_gemini()
        if not model:
            return {
                "answer": "AI service is temporarily unavailable. Please check your API key configuration.",
                "sources": [],
                "related_questions": _get_related_questions(category),
            }

        response = model.generate_content(
            full_prompt,
            generation_config={
                "max_output_tokens": 1500,
                "temperature": 0.5,  # Slightly lower temperature to encourage the structured format rigidly
            }
        )
        answer = response.text.strip()
        print(f"[AI] Gemini answered: {answer[:80]}...")

    except Exception as e:
        err = str(e)
        print(f"[ERROR] Gemini call failed: {err[:200]}")
        if "RESOURCE_EXHAUSTED" in err or "quota" in err.lower():
            # Using 2.5 flash, we just fail fast if limit is hit
            answer = "The AI is currently at maximum capacity (free tier quota). Please wait a few seconds and try sending again!"
        elif "API_KEY_INVALID" in err:
            answer = "AI key is invalid. Please update LLM_API_KEY in backend/.env."
        else:
            answer = "I couldn't process that request right now. Please try again."

    return {
        "answer": answer,
        "sources": [],
        "related_questions": _get_related_questions(category),
    }


def _get_related_questions(category: str) -> list:
    """Return predefined related questions based on category."""
    related = {
        "how_to_convert": [
            "What equipment do I need for biochar?",
            "How long does the conversion process take?",
            "What moisture level is needed?",
        ],
        "equipment": [
            "How much does a briquette machine cost?",
            "Where can I buy a pyrolysis kiln?",
            "Is there government subsidy on equipment?",
        ],
        "quality_tips": [
            "How to dry straw quickly?",
            "How to store crop waste safely?",
            "Does moisture affect briquette quality?",
        ],
        "general_policy": [
            "What is the penalty for burning stubble?",
            "Which government schemes help farmers?",
            "How do carbon credits work for farmers?",
        ],
    }
    return related.get(category, [])
