from fastapi import (
    FastAPI,
    UploadFile,
)

from fastapi import File

import tempfile

import os

from AI.receiptEngine import run_engine

app=FastAPI()

@app.post("/extract-receipt")
async def extract_receipt(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix="jpg") as temp_file:
        
        content = await file.read()
        temp_file.write(content)
        
        temp_image_path = temp_file.name
        
        result = run_engine(
            temp_image_path,
            [],
            []
        )
        
        try:

                os.remove(
                    temp_image_path
                )

        except:

            pass
                
        return result

