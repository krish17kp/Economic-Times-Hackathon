import pdfplumber
import re
from typing import Dict, Any, List, Optional, Tuple
from app.parsers.parser_utils import clean_number


def extract_full_text(file_path: str) -> str:
    """Extract all raw text from every page."""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        pass
    return text


def parse_with_pdfplumber(file_path: str) -> Dict[str, Any]:
    """
    Try to extract structured fund data from CAMS PDF using tables and regex.
    Returns dict with 'funds', 'investor_name', 'statement_date'.
    """
    funds = []
    investor_name = None
    statement_date = None

    try:
        with pdfplumber.open(file_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                full_text += page_text + "\n"

            # Try to extract investor name
            name_match = re.search(r"(?:Name|Investor Name)\s*[:\-]?\s*([A-Za-z\s]+?)(?:\n|PAN|Folio)", full_text)
            if name_match:
                investor_name = name_match.group(1).strip()

            # Try to extract statement date
            date_match = re.search(r"(?:Statement|Valuation) (?:as on|date|on)\s*[:\-]?\s*(\d{2}[\-/]\w+[\-/]\d{4})", full_text, re.IGNORECASE)
            if date_match:
                statement_date = date_match.group(1).strip()

            # Regex patterns for fund entries in CAMS format
            # Pattern: fund name followed by valuation data
            fund_patterns = [
                # Pattern 1: Name followed by cost/market value on same/next line
                r"([A-Za-z][\w\s\-&()]+(?:Fund|Scheme|Plan|Growth|Dividend|Option)[\w\s\-]*)\s+[\n\s]*"
                r"(?:Folio[:\s]+[\w\d]+\s+)?(?:\d+[\.,\d]*\s+){1,2}"
                r"([\d,]+\.?\d*)\s+([\d,]+\.?\d*)",
            ]

            for pattern in fund_patterns:
                matches = re.finditer(pattern, full_text, re.IGNORECASE | re.MULTILINE)
                for m in matches:
                    try:
                        fund_name = m.group(1).strip()
                        purchase_val = clean_number(m.group(2))
                        current_val = clean_number(m.group(3))
                        if fund_name and purchase_val and current_val and current_val > 0:
                            funds.append({
                                "fund_name": fund_name,
                                "purchase_value": purchase_val,
                                "current_value": current_val,
                            })
                    except (IndexError, TypeError):
                        continue

            # Fallback regex: Look for "Cost Value" and "Market Value" pairs
            if len(funds) < 2:
                cost_matches = re.findall(r"Cost\s+Value\s*[:\-]?\s*([\d,]+\.?\d*)", full_text, re.IGNORECASE)
                mkt_matches = re.findall(r"(?:Market|Current)\s+Value\s*[:\-]?\s*([\d,]+\.?\d*)", full_text, re.IGNORECASE)
                names = re.findall(r"([A-Za-z][\w\s\-&()]+(?:Fund|Scheme)[\w\s\-]*)", full_text)

                for i, (cost, mkt) in enumerate(zip(cost_matches, mkt_matches)):
                    name = names[i] if i < len(names) else f"Fund {i+1}"
                    pv = clean_number(cost)
                    cv = clean_number(mkt)
                    if pv and cv:
                        funds.append({
                            "fund_name": name.strip(),
                            "purchase_value": pv,
                            "current_value": cv,
                        })

    except Exception:
        pass

    return {
        "funds": funds,
        "investor_name": investor_name,
        "statement_date": statement_date,
        "confidence": "high" if len(funds) >= 3 else ("medium" if len(funds) >= 1 else "low")
    }


def parse_pdf(file_path: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """
    LAYER 1: Try structured parsing.
    Returns (result, raw_text).
    result is None if parsing was insufficient.
    """
    raw_text = extract_full_text(file_path)

    try:
        data = parse_with_pdfplumber(file_path)
        if len(data.get("funds", [])) >= 2:
            data["raw_text"] = raw_text
            return data, raw_text
        # Not enough funds extracted
        raise Exception(f"Only found {len(data.get('funds', []))} fund(s) — insufficient")
    except Exception:
        return None, raw_text


# Keep backwards-compatible alias
def parse_cams_pdf(file_path: str) -> Dict[str, Any]:
    result, raw_text = parse_pdf(file_path)
    if result:
        return result
    return {"funds": [], "confidence": "low", "raw_text": raw_text}


# Keep backwards-compatible alias
extract_raw_text = extract_full_text
