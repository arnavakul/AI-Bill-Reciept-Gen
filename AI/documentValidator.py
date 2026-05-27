# from google import genai
# from dotenv import load_dotenv
# import os

# load_dotenv()

# client = genai.Client(
#     api_key = os.getenv(
#         "GEMINI_API_KEY"
#     )
# )

# def validate_receipt(image_path):
#     uploaded_file = client.files.upload(
#         file=image_path
#     )

#     prompt = """
    
#     Analyze the uploaded image.

#     Determine whether this image is a valid shopping receipt, invoice, or bill.

#     Return ONLY one word:

#     YES
#     or
#     NO

#     Rules:

#     - YES if image contains:
#       - receipt-like structure
#       - line items
#       - totals
#       - prices
#       - store/vendor information

#     - NO if image is:
#       - selfie
#       - random object
#       - meme
#       - unrelated photo
#       - blank image
#       - non-financial document
#     """
    
#     response = client.models.generate_content(
#     model="gemini-3.1-flash-lite",
#     contents=[prompt, uploaded_file],
#     )
    
#     result = response.text.strip().upper()
    
#     return result =="YES"