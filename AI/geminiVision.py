from google import genai
from dotenv import load_dotenv
import os

from AI.vendorDetector import (
    detect_vendor
)

load_dotenv()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

client = genai.Client(
    api_key=GEMINI_API_KEY
)

# Vendor rules
vendor_rules = {

    "COSTCO": """

    Costco receipts usually contain:
    - MEMBER ID
    - TRANSACTION ID
    - warehouse/store number

    Total appears near TAX.
    """,

    "WALMART": """

    Walmart receipts usually contain:
    - TC#
    - OP#
    - itemized tax
    """,

    "TARGET": """

    Target receipts may contain:
    - REDCard
    - payment section
    """
}


def extract_receipt_data(

    image_path,

    output_fields,

    document_rules
):

    # Upload image
    uploaded_file = client.files.upload(
        file=image_path
    )

    # Detect vendor
    vendor = detect_vendor(
        image_path
    )

    # Get vendor-specific rules
    vendor_prompt = vendor_rules.get(
        vendor,
        "Generic receipt extraction."
    )

    # Convert fields into text
    fields_text = "\n".join(
        [f"- {field}" for field in output_fields]
    )

    # Convert rules into text
    rules_text = "\n".join(
        document_rules
    )

    # Main extraction prompt
    prompt = f"""

    You are an advanced receipt extraction engine.

    Analyze the uploaded receipt image carefully.

    Extract ALL possible structured information.

    Return ONLY valid JSON.

    Do not explain anything.


    General Rules:

    1. Do not hallucinate values blindly.

    2. If a value is clearly visible:
       - mark source as "EXTRACTED"
       - give high confidence

    3. If a value is not clearly visible but can be logically inferred:
       - mark source as "AI_INFERRED"
       - provide confidence score
       - provide inference reason

    4. If inference impossible:
       - return null

    5. Never infer:
       - transaction IDs
       - member IDs
       - payment IDs

    6. You may infer:
       - subtotal
       - tax
       - total

    7. Preserve exact visible numeric values.

    8. Extract item list carefully.

    9. Group item names with correct prices.

    10. Ignore random OCR noise.


    Vendor Detected:

    {vendor}


    Vendor-Specific Rules:

    {vendor_prompt}


    User Requested Fields:

    {fields_text}


    Additional Document Rules:

    {rules_text}


    Required JSON Structure:

    {{
        "store_name": "",
        "store_address": "",
        "date": "",
        "time": "",
        "member_id": "",
        "transaction_id": "",
        "payment_method": "",

        "items": [
            {{
                "item_name": "",
                "quantity": null,
                "price": null
            }}
        ],

        "subtotal": {{
            "value": null,
            "source": "",
            "confidence": 0,
            "reason": ""
        }},

        "tax": {{
            "value": null,
            "source": "",
            "confidence": 0,
            "reason": ""
        }},

        "total": {{
            "value": null,
            "source": "",
            "confidence": 0,
            "reason": ""
        }}
    }}
    """

    # Gemini response
    response = client.models.generate_content(

        model="gemini-3.1-flash-lite",

        contents=[
            prompt,
            uploaded_file
        ],

        config={
            "response_mime_type": "application/json"
        }
    )

    return {

        "vendor": vendor,

        "vendor_prompt": vendor_prompt,

        "gemini_result": response.text
    }