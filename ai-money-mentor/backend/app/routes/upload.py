"""
Upload route — implements parsing logic:
  LAYER 1: pdfplumber structured parsing
  LAYER 2: LLM extraction from raw text
  (If both fail, it returns an error rather than sample data)
"""
import os
import shutil
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.api_models import UploadResponse
from app.parsers.csv_parser import parse_csv
from app.parsers.pdf_parser import parse_pdf
from app.parsers.llm_fallback_parser import extract_with_llm
from app.services.portfolio_normalizer import normalize_portfolio

router = APIRouter()

MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".csv", ".pdf"]:
        return UploadResponse(
            success=False,
            error="unsupported_file_type",
            message="Please upload a PDF or CSV file.",
            suggestion="Download your CAMS statement as PDF or export as CSV."
        )

    # Write to temp file
    temp = NamedTemporaryFile(delete=False, suffix=ext)
    try:
        content = await file.read()
        if len(content) > MAX_SIZE_BYTES:
            return UploadResponse(
                success=False,
                error="file_too_large",
                message="File exceeds the 10MB limit.",
                suggestion="Try compressing the PDF or using a CSV export."
            )
        temp.write(content)
        temp.close()

        warnings = []

        # ── CSV PATH ──────────────────────────────────────────────────────────
        if ext == ".csv":
            raw_records = parse_csv(temp.name)
            if raw_records:
                portfolio = normalize_portfolio(raw_records, source="csv")
                return UploadResponse(success=True, source="csv", portfolio=portfolio, warnings=warnings)
            # CSV with no usable data
            return UploadResponse(
                success=False,
                error="parse_failed",
                message="We couldn't extract any funds from this CSV.",
                suggestion="Please try entering your funds manually using the 'Enter Manually' tab."
            )

        # ── PDF PATH ─────────────────────────────────────────────────────────
        # LAYER 1: pdfplumber
        result, raw_text = parse_pdf(temp.name)

        if result and len(result.get("funds", [])) >= 2:
            portfolio = normalize_portfolio(result["funds"], source="pdf")
            if result.get("investor_name"):
                portfolio.investor_name = result["investor_name"]
            return UploadResponse(success=True, source="pdf", portfolio=portfolio, warnings=warnings)

        warnings.append("Standard parsing extracted insufficient data from your PDF.")

        # LAYER 2: LLM extraction
        if raw_text.strip():
            try:
                llm_result = await extract_with_llm(raw_text)
                llm_funds = llm_result.get("funds", [])
                if len(llm_funds) >= 1:
                    portfolio = normalize_portfolio(llm_funds, source="pdf_llm_fallback")
                    if llm_result.get("investor_name"):
                        portfolio.investor_name = llm_result["investor_name"]
                    warnings.append(
                        "We couldn't fully parse your file. Showing an intelligent estimate from your statement."
                    )
                    return UploadResponse(
                        success=True,
                        source="pdf_llm_fallback",
                        portfolio=portfolio,
                        warnings=warnings
                    )
            except Exception:
                pass

        # If we got here, parsing completely failed
        return UploadResponse(
            success=False,
            error="parse_failed",
            message="We couldn't extract your data from this document.",
            suggestion="Please try entering your funds manually using the 'Enter Manually' tab."
        )

    finally:
        if os.path.exists(temp.name):
            os.remove(temp.name)

