"""
image_mapper.py

Groups images by page number and attaches them to products.
"""

from pathlib import Path
import re


def map_images_to_products(products, pdf_stem):
    """
    Attach images to products using page number matching.
    """

    images_dir = Path("data/output/images")
    if not images_dir.exists():
        return products

    # Build page → images mapping
    page_images = {}

    for img in images_dir.glob(f"{pdf_stem}_page_*_img_*.jpeg"):
        match = re.search(r"_page_(\d+)_", img.name)
        if not match:
            continue

        page_no = int(match.group(1))
        page_images.setdefault(page_no, []).append(img.name)

    # Attach images to products
    for product in products:
        page = product.get("page")
        product["images"] = page_images.get(page, [])

    return products
