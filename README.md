# PDF Document Processor – Automated Catalog Data & Image Extraction

## Overview

This project is a production-style Python tool that automatically processes PDF documents (such as product catalogs) and converts unstructured PDF content into clean, structured, and explainable data.

It is designed to handle real-world PDFs, not ideal or perfectly formatted ones.

The system:

- Extracts product information (SKU, price, page number, etc.)
- Extracts all images from PDFs
- Groups images to products using page-based logic
- Outputs structured data in Excel and JSON
- Adds confidence scores and explanations for transparency
- Supports multiple PDFs automatically without code changes

This project is built with robustness, explainability, and scalability in mind.

---

## Key Features

- Batch Processing  
  Place one or many PDFs into the input folder.  
  No configuration or code change is required.

- Structured Data Extraction  
  - SKU (one product per SKU)
  - MRP / Price
  - Page number
  - Source PDF name

- Image Extraction  
  - Extracts all embedded images from each PDF
  - Handles large, image-heavy catalogs

- Page-Based Image Grouping  
  - Images are linked to products found on the same page
  - This reflects how real PDFs store content

- Confidence Scoring  
  - Each product includes a confidence score based on available signals
  - Helps downstream users judge data reliability

- Explainability  
  - Each product includes a clear explanation of why it was extracted
  - No hidden or black-box logic

- Fault-Tolerant Design  
  - Corrupted or complex pages are skipped safely
  - One bad page never crashes the pipeline

---

## Project Structure

pdf_document_processor/
│
├── data/
│   ├── input/            # Place PDFs here
│   ├── output/
│   │   ├── excel/        # Generated Excel files
│   │   ├── json/         # Generated JSON files
│   │   └── images/       # Extracted images
│
├── src/
│   ├── main.py
│   ├── catalog_parser.py
│   ├── image_extractor.py
│   ├── image_mapper.py
│   ├── exporters.py
│   ├── confidence.py
│   ├── explainability.py
│   ├── detector.py
│   └── config.py
│
├── requirements.txt
├── README.md
└── python_env_pdf/        # Virtual environment (optional)

---

## How the Pipeline Works (Simple Explanation)

1. Input PDFs  
   You place one or more PDF files into data/input/

2. Document Detection  
   Each PDF is inspected to detect whether it is a product catalog  
   Unsupported document types are skipped safely

3. Catalog Parsing  
   - The PDF is read page by page  
   - SKU patterns are detected  
   - Inline prices (MRP) are extracted correctly  
   - Multiple SKUs on the same line are handled properly  

4. Image Extraction  
   - All images are extracted from the PDF  
   - Images are named using page numbers for traceability  

5. Image Grouping  
   - Images are associated with products based on page number  
   - This reflects real-world PDF limitations  

6. Confidence & Explainability  
   - Each product is scored based on extracted signals  
   - A human-readable explanation is added  

7. Export  
   - Final output is saved as Excel (.xlsx) and JSON (.json)

---

## Input Instructions (Very Important)

### Adding One PDF

Place the PDF inside:
data/input/

### Adding Multiple PDFs

You can add 2, 5, or 100 PDFs to the same folder:
data/input/
├── Catalog_2023.pdf
├── Catalog_2024.pdf
├── New_Collection.pdf

No code change is required.  
The pipeline automatically processes all PDFs.

---

## How to Run the Project

### Option 1: Standard Run

python src/main.py

### Option 2: CLI Mode (Recommended)

python -m pdf_document_processor data/input

Both commands produce the same result.

---

## Output Files

For each processed PDF, the system generates:

### Excel

data/output/excel/<PDF_NAME>_products.xlsx

### JSON

data/output/json/<PDF_NAME>_products.json

### Images

Files are never overwritten, even when multiple PDFs are processed.

---

## Example Output (JSON)

{
  "sku": "GO-LEG-29001",
  "mrp": "3300",
  "page": 6,
  "images": [
    "Catalog_page_6_img_1.jpeg",
    "Catalog_page_6_img_2.jpeg"
  ],
  "confidence": 0.7,
  "explanation": "SKU pattern detected; Price (MRP) detected; Images found on same page"
}

---

## Why Some Fields May Be Empty

In real-world catalogs:

- Product names may be embedded in images
- Text layers may be incomplete or inconsistent

This project does not guess or hallucinate data.

If a value cannot be extracted reliably:

- The field is left empty
- The confidence score reflects this
- The explanation clearly states what was detected

This is intentional and professional behavior.

---

## Technologies Used

- Python 3
- pdfplumber & pdfminer
- PyMuPDF
- Pandas & OpenPyXL
- Regular Expressions

---

## Design Principles

- Reliability over assumptions
- Explainability over black-box logic
- Batch-friendly architecture
- Easy extensibility for future improvements
- Clean separation of concerns

---

## Possible Future Improvements

- Layout-based image-text matching
- OCR for image-only PDFs
- Database storage
- API interface
- Parallel processing for very large batches

---

## Summary

This project demonstrates:

- Real-world PDF processing
- Robust error handling
- Clean data extraction
- Explainable outputs
- Scalable, reusable design

You can add new PDFs, rerun the pipeline, and get consistent results without touching the code.

---

## Final Note

This tool is intentionally designed to behave like a real production system, not a demo script.

If you are reviewing this project:

- Please check the Excel and JSON outputs
- Review the confidence and explanation fields
- Note that the system favors correctness and transparency

---

End of README
