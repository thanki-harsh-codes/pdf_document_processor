"""
confidence.py

Calculates confidence score for extracted products.
"""


def calculate_confidence(product):
    score = 0.0

    if product.get("sku"):
        score += 0.4

    if product.get("name"):
        score += 0.3

    if product.get("mrp"):
        score += 0.2

    if product.get("images"):
        score += 0.1

    return round(score, 2)
