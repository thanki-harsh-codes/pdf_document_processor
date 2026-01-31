"""
explainability.py

Generates human-readable explanations for extracted products.
"""


def explain_product(product):
    """
    Explain why a product was extracted.
    """

    reasons = []

    if product.get("sku"):
        reasons.append("SKU pattern detected")

    if product.get("name"):
        reasons.append("Product name detected")

    if product.get("mrp"):
        reasons.append("Price (MRP) detected")

    if product.get("images"):
        reasons.append("Images found on same page")

    return "; ".join(reasons)
