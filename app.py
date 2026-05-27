import streamlit as st
import requests
import tempfile
import os
import json

st.set_page_config(
    page_title="Receipt Information Extractor",
    page_icon="📄",
    layout="wide"
)

FASTAPI_URL = "http://127.0.0.1:8000/extract-receipt"

st.title("📄 AI Financial Document Intelligence System")

st.markdown(
    """
Upload a receipt or invoice image to extract structured financial data using Gemini Vision AI.
"""
)

# Sidebar settings
with st.sidebar:

    st.header("Extraction Settings")

    output_fields_input = st.text_area(
        "Fields To Extract",
        height=220,
        placeholder="""
store_name
store_address
date
time
member_id
transaction_id
payment_method
subtotal
tax
total
items
"""
    )

    st.markdown("---")

    st.caption(
        "Powered by Gemini Vision • FastAPI • Streamlit"
    )

# File upload
uploaded_file = st.file_uploader(
    "Upload Receipt / Invoice",
    type=["jpg", "jpeg", "png"]
)

# Run extraction button
run_button = st.button(
    "Run AI Extraction",
    use_container_width=True
)

# Main workflow
if run_button:

    if uploaded_file is None:

        st.error(
            "Please upload a receipt image."
        )

    else:

        # Convert fields into list
        output_fields = [

            field.strip()

            for field in output_fields_input.split("\n")

            if field.strip()
        ]

        # Save temp image
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jpg"
        ) as temp_file:

            temp_file.write(
                uploaded_file.read()
            )

            temp_image_path = temp_file.name

        # Layout columns
        left_col, right_col = st.columns([1, 1])

        # Image preview
        with left_col:

            st.subheader("Uploaded Receipt")

            st.image(
                temp_image_path,
                use_container_width=True
            )

        # API call
        with st.spinner(
            "Running AI Extraction..."
        ):

            try:

                with open(
                    temp_image_path,
                    "rb"
                ) as image_file:

                    files = {

                        "file": image_file
                    }

                    data = {

                        "output_fields": json.dumps(
                            output_fields
                        )
                    }

                    response = requests.post(
                        FASTAPI_URL,
                        files=files,
                        data=data
                    )

                result = response.json()

            except Exception as e:

                st.error(
                    "Failed to connect to FastAPI backend."
                )

                st.code(str(e))

                st.stop()

        # Right side results
        with right_col:

            # Validation failure
            if "error" in result:

                st.error(
                    "Validation Failed"
                )

                st.warning(
                    result["error"]
                )

                # Quality analysis
                if "quality_result" in result:

                    quality_result = result[
                        "quality_result"
                    ]

                    st.subheader(
                        "Receipt Quality Analysis"
                    )

                    st.metric(
                        "Quality Score",
                        f"{quality_result['score']}%"
                    )

                    if quality_result["issues"]:

                        for issue in quality_result["issues"]:

                            st.write(
                                f"• {issue}"
                            )

            else:

                st.success(
                    "Validation Passed"
                )

                # Quality analysis
                quality_result = result.get(
                    "quality_result",
                    {}
                )

                st.subheader(
                    "Receipt Quality"
                )

                st.metric(
                    "Quality Score",
                    f"{quality_result.get('score', 0)}%"
                )

                if quality_result.get("issues"):

                    st.warning(
                        "Detected Issues"
                    )

                    for issue in quality_result["issues"]:

                        st.write(
                            f"• {issue}"
                        )

                else:

                    st.success(
                        "No major quality issues detected."
                    )

                # Vendor info
                vendor_name = result.get(
                    "vendor",
                    "UNKNOWN"
                )

                st.subheader(
                    "Vendor Detection"
                )

                st.info(
                    f"Detected Vendor: {vendor_name}"
                )

                # Vendor prompt
                vendor_prompt = result.get(
                    "vendor_prompt",
                    "No vendor-specific rules found."
                )

                with st.expander(
                    "Vendor-Specific Prompt"
                ):

                    st.code(
                        vendor_prompt
                    )

        # Structured extraction
        st.markdown("---")

        st.subheader(
            "Structured Financial Extraction"
        )

        gemini_result = result.get(
            "gemini_result"
        )

        try:

            # Clean response
            cleaned_result = gemini_result.strip()

            cleaned_result = cleaned_result.replace(
                "```json",
                ""
            )

            cleaned_result = cleaned_result.replace(
                "```",
                ""
            ).strip()

            # Parse JSON
            parsed_json = json.loads(
                cleaned_result
            )

            # Show JSON
            st.json(
                parsed_json
            )

            # Items table
            if (
                "items" in parsed_json
                and
                parsed_json["items"]
            ):

                st.subheader(
                    "Extracted Items"
                )

                st.dataframe(
                    parsed_json["items"],
                    use_container_width=True
                )

        except Exception as e:

            st.error(
                "Failed to parse Gemini JSON output."
            )

            st.code(
                gemini_result
            )

            print(e)

        # Delete temp image
        if os.path.exists(
            temp_image_path
        ):

            os.remove(
                temp_image_path
            )