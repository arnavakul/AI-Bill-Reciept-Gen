# AI-Powered Financial Document Intelligence System

## Overview

AI-Powered Financial Document Intelligence System is a multimodal AI application designed to automate receipt and invoice understanding using Gemini Vision (`gemini-3.1-flash-lite`).

The system validates uploaded receipts, analyzes document quality, detects vendors, extracts structured financial information, and returns standardized JSON responses through a FastAPI backend and Streamlit frontend.

---

## Features

### Receipt Validation

- Determines whether an uploaded image is a valid receipt or invoice
- Rejects unrelated or unsupported documents

---

### Receipt Quality Analysis

Analyzes:
- Blur
- Lighting
- Readability
- Cropping issues
- Visibility of important financial information

Returns:
- Quality score
- Validation status
- Identified issues

---

### Vendor Detection

Automatically detects receipt vendors and applies vendor-specific extraction strategies.

Supported vendors include:
- Costco
- Walmart
- Target

Additional vendors can be easily configured.

---

### AI-Powered Data Extraction

Extracts:

- Store Name
- Store Address
- Date
- Time
- Member ID
- Transaction ID
- Payment Method
- Itemized Purchases
- Subtotal
- Tax
- Total

---

### Intelligent Inference Layer

When financial values are partially missing:

- Clearly extracted values are marked as `EXTRACTED`
- Logically inferred values are marked as `AI_INFERRED`
- Confidence scores and reasoning are provided
- Critical identifiers such as transaction IDs are never inferred

---

### JSON-Based Responses

All extraction results are returned in structured JSON format, making integration with other systems straightforward.

---

### FastAPI Backend

Provides REST APIs for:

- Receipt upload
- Validation
- Quality analysis
- AI extraction

---

### Streamlit Frontend

Provides:

- Receipt upload interface
- Image preview
- Vendor information display
- Quality analysis visualization
- JSON response viewer
- Itemized table display

---

## Architecture

```text
Upload Receipt
        ↓
Receipt Validation
        ↓
Receipt Quality Analysis
        ↓
Vendor Detection
        ↓
Vendor-Specific Prompt Routing
        ↓
Gemini Vision Extraction
        ↓
Intelligent Inference Layer
        ↓
Structured JSON Output
        ↓
Frontend Visualization
```

---

## Tech Stack

### AI / ML

- Gemini Vision (gemini-3.1-flash-lite)
- Generative AI
- Multimodal AI
- Prompt Engineering

### Backend

- Python
- FastAPI

### Frontend

- Streamlit

### Computer Vision

- OpenCV

### OCR

- Tesseract OCR

### Data Processing

- JSON
- Regex

---

## Project Structure

```text
AI Bill Receipt Gen/
│
├── AI/
│   ├── geminiVision.py
│   ├── receiptEngine.py
│   ├── vendorDetector.py
│   ├── documentValidator.py
│   └── documentAnalyzer.py
│
├── api/
│   └── main.py
│
├── app.py
├── requirements.txt
├── .env
└── README.md
```

---

## Installation

```bash
git clone <repository-url>

cd AI-Bill-Receipt-Gen

pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## Running FastAPI Backend

```bash
uvicorn api.main:app --reload
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Running Streamlit Frontend

```bash
streamlit run app.py
```

---

## Future Enhancements

- Multi-receipt batch processing
- Multi-language receipt support
- Database integration
- CSV/Excel export
- Fraud detection
- Cloud deployment
- Enterprise document workflows
- Agentic AI orchestration

---

## Disclaimer

This project is intended for educational, research, and AI system prototyping purposes.

AI-generated inferences are explicitly marked and should be reviewed before use in financial workflows.
