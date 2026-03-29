import re
from typing import Optional

def clean_number(value_str: str) -> Optional[float]:
    if not value_str or not isinstance(value_str, str):
        if isinstance(value_str, (int, float)):
            return float(value_str)
        return None
    cleaned = re.sub(r'[^\d.-]', '', value_str)
    try:
        return float(cleaned)
    except ValueError:
        return None
