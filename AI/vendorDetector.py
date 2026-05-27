import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key = os.getenv(
        "GEMINI_API_KEY"
    )
)

def detect_vendor(image_path):
    
    uploaded_file = client.files.upload(file = image_path)
    
    prompt = """
    
    Identify the store/vendor name from this receipt.

    Return ONLY the vendor/store name.

    Examples:
    - Costco
    - Walmart
    - Target
    - Starbucks

    If unclear return:
    UNKNOWN
    """
    
    response = client.models.generate_content(

        model="gemini-3.1-flash-lite",

        contents=[
            prompt,
            uploaded_file
        ]
    )
    
    vendor = response.text.strip()
    
    return vendor.upper()