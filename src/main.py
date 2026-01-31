"""
main.py

Pipeline entry point.
This is the only file users need to run.
"""

from config import INPUT_DIR
from detector import detect_document_type
from catalog_parser import process_catalog
from profile_parser import process_profile
from image_extractor import extract_images
from explainability import explain_product


def run_pipeline():
    for pdf_file in INPUT_DIR.glob("*.pdf"):
        print(f"\nProcessing: {pdf_file.name}")

        doc_type = detect_document_type(pdf_file)
        print(f"Detected type: {doc_type}")

        if doc_type == "PRODUCT_CATALOG":
            process_catalog(pdf_file)

        elif doc_type == "COMPANY_PROFILE":
            process_profile(pdf_file)

        else:
            print("Unknown document type. Skipping.")

        extract_images(pdf_file)


if __name__ == "__main__":
    run_pipeline()
