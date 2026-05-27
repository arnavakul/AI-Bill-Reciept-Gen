import streamlit as st
from AI.receiptEngine import run_engine
import tempfile
import os
import json

st.set_page_config(
    page_title="AI Receipt Extraction",
    layout="wide"
)

st.title("AI Bill Receipt Extraction")

st.write(
    "Upload a receipt image and extract structured data using Gemini Vision."
)

# Upload image
uploaded_file = st.file_uploader(
    "Upload Receipt Image",
    type=["jpg", "jpeg", "png"]
)

# Fields input
output_fields_input = st.text_area(
    "Fields To Extract (one per line)",
    height=200,
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

# Run extraction
if st.button("Run Extraction"):

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

        # Show uploaded image
        st.subheader("Uploaded Receipt")

        st.image(
            temp_image_path,
            use_container_width=True
        )

        # Run engine
        with st.spinner(
            "Running AI Receipt Engine..."
        ):

            result = run_engine(
                temp_image_path,
                output_fields,
                []
            )

        # Validation failure
        if "error" in result:

            st.error(
                "Validation Failed"
            )

            st.warning(
                result["error"]
            )

            # Show image type if available
            if "image_type" in result:

                st.info(
                    f"Image Type: {result['image_type']}"
                )

            # Show quality details if available
            if "quality_result" in result:

                quality_result = result["quality_result"]

                st.subheader(
                    "Receipt Quality Analysis"
                )

                st.metric(
                    "Quality Score",
                    f"{quality_result['score']}%"
                )

                if quality_result["issues"]:

                    st.warning(
                        "Issues Detected:"
                    )

                    for issue in quality_result["issues"]:

                        st.write(
                            f"- {issue}"
                        )

        else:

            st.success(
                "Validation Passed"
            )

            # Show image type
            image_type = result.get(
                "image_type",
                "UNKNOWN"
            )

            st.info(
                f"Image Type: {image_type}"
            )

            # Show quality result
            quality_result = result.get(
                "quality_result",
                {}
            )

            st.subheader(
                "Receipt Quality Analysis"
            )

            st.metric(
                "Quality Score",
                f"{quality_result.get('score', 0)}%"
            )

            if quality_result.get("issues"):

                st.warning(
                    "Issues Detected:"
                )

                for issue in quality_result["issues"]:

                    st.write(
                        f"- {issue}"
                    )

            else:

                st.success(
                    "No quality issues detected."
                )

            # Vendor info
            vendor_name = result.get(
                "vendor",
                "UNKNOWN"
            )

            vendor_prompt = result.get(
                "vendor_prompt",
                "No vendor-specific rules found."
            )

            st.info(
                f"Detected Vendor: {vendor_name}"
            )

            # Vendor rules
            st.subheader(
                "Vendor-Specific Prompt"
            )

            st.text_area(
                "Vendor Rules",
                vendor_prompt,
                height=150
            )

            # Gemini result
            gemini_result = result.get(
                "gemini_result"
            )

            st.subheader(
                "Gemini Extraction"
            )

            try:

                # Clean Gemini response
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

                # Show extracted items
                if (
                    "items" in parsed_json
                    and
                    parsed_json["items"]
                ):

                    st.subheader(
                        "Extracted Items"
                    )

                    st.table(
                        parsed_json["items"]
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