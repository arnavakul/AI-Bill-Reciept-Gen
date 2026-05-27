from AI.geminiVision import (

    extract_receipt_data
)


from AI.documentAnalyzer import (

    validate_receipt_quality,
    validate_receipt,
    detect_image_type
)


def run_engine(

    image_path,

    output_fields,

    document_rules
):

    # Detect image type
    image_type = detect_image_type(
        image_path
    )


    # Validate receipt quality
    quality_result = validate_receipt_quality(
        image_path
    )


    # Reject poor quality receipts
    if not quality_result["quality_passed"]:

        return {

            "error": "Poor receipt quality.",

            "quality_result": quality_result,

            "image_type": image_type
        }


    # Validate receipt document
    is_valid_receipt = validate_receipt(
        image_path
    )


    # Reject invalid receipts
    if not is_valid_receipt:

        return {

            "error": "Uploaded image is not a valid receipt.",

            "image_type": image_type,

            "quality_result": quality_result
        }


    # Run Gemini extraction
    extraction_result = extract_receipt_data(

        image_path,

        output_fields,

        document_rules
    )


    # Final response
    final_result = {

        "image_type": image_type,

        "quality_result": quality_result,

        "vendor": extraction_result["vendor"],

        "vendor_prompt": extraction_result["vendor_prompt"],

        "gemini_result": extraction_result["gemini_result"]
    }


    return final_result