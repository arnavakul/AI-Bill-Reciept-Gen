from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

client = genai.Client(
    api_key=GEMINI_API_KEY
)


def extract_receipt_data(image_path, output_fields, document_rules):
    uploaded_file = client.files.upload(
        file=image_path
    )
    

    prompt = """
    You are an advanced receipt extraction engine.

    Analyze the uploaded receipt image carefully.

    Extract ALL possible structured information.

    Return ONLY valid JSON.

    Do not explain anything.

    Rules:

    1. Do not hallucinate missing values.
    2. If value missing return null.
    3. Preserve exact numeric values.
    4. Extract item list carefully.
    5. Group item names with correct prices.
    6. Ignore random OCR noise.

    Required JSON structure:

    {
    "store_name": "",
    "store_address": "",
    "date": "",
    "time": "",
    "member_id": "",
    "transaction_id": "",
    "payment_method": "",

    "items": [
        {
        "item_name": "",
        "quantity": null,
        "price": null
        }
    ],

    "subtotal": null,
    "tax": null,
    "total": null
    }
    """

    response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=[prompt, uploaded_file],
    config={
        "response_mime_type": "application/json"
    }
    )
    
    
    return response.text

