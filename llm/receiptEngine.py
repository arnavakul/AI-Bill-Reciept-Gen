from llm.geminiVision import (
    extract_receipt_data
)

def run_engine(
    image_path, output_fields, document_rules
):
    gemini_result = extract_receipt_data(
        image_path,output_fields,document_rules
    )
    
    final_result = {
        "gemini_result": gemini_result
    }
    
    return final_result