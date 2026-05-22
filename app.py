import streamlit as st

from llm.receiptEngine import (
    
    run_engine
)

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


# Upload receipt image

uploaded_file = st.file_uploader(

    "Upload Receipt Image",

    type=["jpg", "jpeg", "png"]
)


# Dynamic output fields

default_fields = """

subtotal
tax
total
member_id
transaction_id
"""


output_fields_input = st.text_area(

    "Fields To Extract (one per line)",

    value=default_fields,

    height=150
)


# Document rules

default_rules = """

Transaction ID usually appears near TRAN ID.
Member ID appears near MEMBER.
Total amount appears near TOTAL.
Tax appears near TAX.
Do not guess missing values.
"""


document_rules_input = st.text_area(

    "Document Rules",

    value=default_rules,

    height=200
)


# Run extraction button

if st.button("Run Extraction"):

    if uploaded_file is None:

        st.error("Please upload a receipt image.")

    else:

        # Convert user input into list

        output_fields = [

            field.strip()

            for field in output_fields_input.split("\n")

            if field.strip()
        ]


        document_rules = [

            rule.strip()

            for rule in document_rules_input.split("\n")

            if rule.strip()
        ]


        # Save uploaded image temporarily

        with tempfile.NamedTemporaryFile(

            delete=False,

            suffix=".jpg"
        ) as temp_file:

            temp_file.write(

                uploaded_file.read()
            )

            temp_image_path = temp_file.name


        # Show uploaded image

        st.image(

            temp_image_path,

            caption="Uploaded Receipt",

            use_container_width=True
        )


        # Run AI extraction

        with st.spinner("Running Gemini Vision Extraction..."):

            result = run_engine(

                temp_image_path,

                output_fields,

                document_rules
            )


        st.success("Extraction Completed")


        # Parse Gemini JSON safely

        gemini_result = result.get(
            "gemini_result"
        )


        st.subheader("Gemini Extraction")


        try:

            parsed_json = json.loads(
                gemini_result
            )

            st.json(parsed_json)
            
            #table format 
            
            if "items" in parsed_json:
                
                st.subheader("Extracted Items")
                
                st.table(
                    parsed_json["items"]
                )

        except:

            st.code(gemini_result)


        # Delete temp image

        if os.path.exists(temp_image_path):

            os.remove(temp_image_path)
            