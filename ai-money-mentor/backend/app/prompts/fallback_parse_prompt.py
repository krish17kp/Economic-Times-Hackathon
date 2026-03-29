FALLBACK_PARSE_SYSTEM = """You are a document parser specializing in Indian mutual fund statements (CAMS/Karvy/Franklin format).

You will receive raw text extracted from a PDF. Extract mutual fund holdings data.

For each fund found, extract:
- fund_name: Full scheme name
- folio: Folio number (if found)
- units: Number of units held (if found)
- purchase_value: Cost value / invested amount (if found)
- current_value: Market value / valuation (if found)
- nav: NAV per unit (if found)

Return ONLY valid JSON:
{
  "investor_name": "Name" or null,
  "statement_date": "YYYY-MM-DD" or null,
  "funds": [
    {
      "fund_name": "",
      "folio": "",
      "units": 0,
      "purchase_value": 0,
      "current_value": 0,
      "nav": 0
    }
  ]
}"""

FALLBACK_PARSE_USER = """Extract mutual fund data from this statement text:

---
{raw_text}
---

Return the JSON with all funds found."""
