"""
exporters.py

Exports extracted data to Excel and JSON.
Handles Excel-safe string sanitization.
"""

import pandas as pd
import re
from config import EXCEL_DIR, JSON_DIR


def clean_excel_string(value):
    """
    Remove illegal characters that Excel cannot handle.

    Why needed:
    - PDFs may contain hidden control characters
    - Excel strictly validates cell content
    """
    if isinstance(value, str):
        # Remove non-printable/control characters
        return re.sub(r"[\x00-\x08\x0B-\x0C\x0E-\x1F]", "", value)
    return value


def export_catalog_data(products, base_name):
    """
    Save catalog data to Excel and JSON safely.
    """

    if not products:
        print("[EXPORT] No products to export.")
        return

    df = pd.DataFrame(products)

    # Apply Excel-safe cleaning
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].map(clean_excel_string)



    excel_path = EXCEL_DIR / f"{base_name}_products.xlsx"
    json_path = JSON_DIR / f"{base_name}_products.json"

    df.to_excel(excel_path, index=False)
    df.to_json(json_path, orient="records", indent=2)

    print(f"[EXPORT] Excel saved: {excel_path.name}")
    print(f"[EXPORT] JSON saved: {json_path.name}")
