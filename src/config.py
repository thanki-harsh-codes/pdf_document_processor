"""
config.py

Why this file exists:
- Centralizes all configuration
- Avoids hardcoding paths in logic
- Makes the project reusable for any PDF set
"""

from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Input PDFs
INPUT_DIR = BASE_DIR / "data" / "input"

# Output directories
OUTPUT_DIR = BASE_DIR / "data" / "output"
EXCEL_DIR = OUTPUT_DIR / "excel"
JSON_DIR = OUTPUT_DIR / "json"
IMAGE_DIR = OUTPUT_DIR / "images"

# Ensure output folders exist
for directory in [EXCEL_DIR, JSON_DIR, IMAGE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Supported document types
DOCUMENT_TYPES = {
    "catalog": "PRODUCT_CATALOG",
    "profile": "COMPANY_PROFILE"
}
