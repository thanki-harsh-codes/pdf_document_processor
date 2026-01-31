"""
catalog_parser.py

Extracts structured product data from catalog-style PDFs.
Handles real-world PDF failures gracefully.
Supports multiple SKUs per line with inline MRP extraction.
Adds image grouping, confidence scoring, and explainability.
"""

import pdfplumber
import re

from exporters import export_catalog_data
from image_mapper import map_images_to_products
from confidence import calculate_confidence
from explainability import explain_product


# ---------------- REGEX PATTERNS ----------------

# Strict SKU pattern
SKU_PATTERN = re.compile(r"\b[A-Z]{2,4}-[A-Z]{2,4}-\d{4,6}\b")

# SKU + MRP on same line (most important fix)
SKU_MRP_PATTERN = re.compile(
    r"(?P<sku>[A-Z]{2,4}-[A-Z]{2,4}-\d{4,6})\s*MRP\s*[:\-]?\s*(?P<mrp>\d+)",
    re.IGNORECASE
)

# Standalone MRP
PRICE_PATTERN = re.compile(r"MRP\s*[:\-]?\s*(\d+)", re.IGNORECASE)


# ---------------- MAIN FUNCTION ----------------

def process_catalog(pdf_path):
    """
    Main catalog processing function.

    Strategy:
    - Read PDF page by page
    - Extract SKU+MRP pairs first (highest accuracy)
    - Fallback to standalone SKU extraction
    - Attach names/descriptions when present
    - Skip pages that fail parsing
    - Add image grouping, confidence, explainability
    """

    print(f"[CATALOG] Extracting data from: {pdf_path.name}")

    products = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):

            # -------- SAFE PAGE EXTRACTION --------
            try:
                text = page.extract_text()
            except Exception as e:
                print(f"[WARN] Text extraction failed on page {page_number}: {e}")
                continue

            if not text:
                continue
            # -------------------------------------

            lines = [line.strip() for line in text.split("\n") if line.strip()]

            for line in lines:

                # 1️ BEST CASE: SKU + MRP pairs on same line
                pairs = SKU_MRP_PATTERN.findall(line)
                if pairs:
                    for sku, mrp in pairs:
                        products.append({
                            "sku": sku,
                            "name": "",
                            "description": "",
                            "mrp": mrp,
                            "page": page_number,
                            "source_pdf": pdf_path.name,
                        })
                    continue

                # 2️ FALLBACK: SKU(s) without inline price
                skus_found = SKU_PATTERN.findall(line)
                if skus_found:
                    for sku in skus_found:
                        products.append({
                            "sku": sku,
                            "name": "",
                            "description": "",
                            "mrp": "",
                            "page": page_number,
                            "source_pdf": pdf_path.name,
                        })
                    continue

                # 3️ CONTEXTUAL DATA (name / description / price)
                if products:
                    last_product = products[-1]

                    # Price on separate line
                    price_match = PRICE_PATTERN.search(line)
                    if price_match and not last_product["mrp"]:
                        last_product["mrp"] = price_match.group(1)
                        continue

                    # Product name (first meaningful text)
                    if not last_product["name"]:
                        last_product["name"] = line
                        continue

                    # Description (remaining text)
                    last_product["description"] += " " + line

    print(f"[CATALOG] Products extracted: {len(products)}")

    # ---------------- IMAGE GROUPING ----------------
    products = map_images_to_products(products, pdf_path.stem)

    # ---------------- CONFIDENCE & EXPLANATION ------
    for product in products:
        product["confidence"] = calculate_confidence(product)
        product["explanation"] = explain_product(product)

    # ---------------- EXPORT ------------------------
    export_catalog_data(products, pdf_path.stem)

    return products
