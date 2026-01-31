"""
image_extractor.py

What this module does:
- Extracts all embedded images from a PDF
- Saves them as individual image files

Why this is needed:
- Product catalogs store images inside PDFs
- We need them as separate files for reuse (web, ERP, ML, etc.)
"""

import fitz  # PyMuPDF
from pathlib import Path
from config import IMAGE_DIR


def extract_images(pdf_path):
    """
    Extract images from a PDF and save them to output/images.

    Naming convention (temporary, Phase 2):
    <pdf_name>_page_<page_number>_img_<index>.png
    """

    print(f"[IMAGES] Extracting images from: {pdf_path.name}")

    doc = fitz.open(pdf_path)
    pdf_name = pdf_path.stem

    image_count = 0

    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image_filename = (
                f"{pdf_name}_page_{page_index+1}_img_{img_index+1}.{image_ext}"
            )

            image_path = IMAGE_DIR / image_filename

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            image_count += 1

    print(f"[IMAGES] Total images extracted: {image_count}")
