import pdfplumber
from config import DOCUMENT_TYPES


def detect_document_type(pdf_path):
    """
    Detect document type using business-level keywords.
    """

    with pdfplumber.open(pdf_path) as pdf:
        first_page_text = pdf.pages[0].extract_text() or ""
        first_page_text = first_page_text.lower()

    # Product catalog indicators
    catalog_keywords = [
        "faucet",
        "sanitary",
        "bath",
        "mrp",
        "catalog",
        "product"
    ]

    # Company profile indicators
    profile_keywords = [
        "company profile",
        "who we are",
        "about us",
        "our values",
        "mission",
        "vision"
    ]

    if any(word in first_page_text for word in catalog_keywords):
        return DOCUMENT_TYPES["catalog"]

    if any(word in first_page_text for word in profile_keywords):
        return DOCUMENT_TYPES["profile"]

    return "UNKNOWN"
