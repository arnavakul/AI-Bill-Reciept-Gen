import os
import json

from google import genai

from dotenv import load_dotenv


load_dotenv()


client = genai.Client(

    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)

#Image Validator to check if the uploaded image is validated or not 

def validate_receipt(image_path):
    
    uploaded_file = client.files.upload(

        file=image_path,

        config={
            "mime_type": "image/jpeg"
        }
    )

    prompt = """
    
    Analyze the uploaded image.

    Determine whether this image is a valid shopping receipt, invoice, or bill.

    Return ONLY one word:

    YES
    or
    NO

    Rules:

    - YES if image contains:
      - receipt-like structure
      - line items
      - totals
      - prices
      - store/vendor information

    - NO if image is:
      - selfie
      - random object
      - meme
      - unrelated photo
      - blank image
      - non-financial document
    """
    
    response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=[prompt, uploaded_file],
    )
    
    result = response.text.strip().upper()
    
    return result =="YES"


# # Detect screenshot or camera image

# def detect_image_type(image_path):

#     uploaded_file = client.files.upload(
#         file=image_path
#     )


#     prompt = """
#     Determine whether this receipt image is:

#     - CAMERA_IMAGE
#     - SCREENSHOT

#     Rules:
#     - screenshots are digitally captured
#     - camera images contain lighting, shadows,
#       hands, perspective distortion or backgrounds

#     Return ONLY one label.
#     """


#     response = client.models.generate_content(

#         model="gemini-3.1-flash-lite",

#         contents=[
#             prompt,
#             uploaded_file
#         ]
#     )


#     return response.text.strip()



# Validate receipt quality

def validate_receipt_quality(image_path):

    uploaded_file = client.files.upload(

    file=image_path,

        config={
            "mime_type": "image/jpeg"
        }
    )


    prompt = """
    Analyze this receipt image.

    Check:
    - blur
    - crop
    - readability
    - lighting
    - skew
    - visibility of totals

    Return ONLY valid JSON.

    Example:

    {
        "quality_passed": true,
        "score": 92,
        "issues": []
    }
    """


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


    cleaned_result = response.text.strip()


    cleaned_result = cleaned_result.replace(
        "```json",
        ""
    )


    cleaned_result = cleaned_result.replace(
        "```",
        ""
    ).strip()


    return json.loads(
        cleaned_result
    )

