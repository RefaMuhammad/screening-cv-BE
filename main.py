from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
import os
import shutil
from dotenv import load_dotenv

from models.schemas import JobRequirement, ScreeningResponse
from services.screening_service import process_batch
from services.ocr_service import OCRService
from services.deepseek_service import DeepSeekService

load_dotenv()

app = FastAPI(title="Winmaker CV Screening POC")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Winmaker CV Screening API is running"}

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/ocr/status")
def ocr_status():
    ocr = OCRService()
    return {
        "available": ocr.is_available(),
        "device": ocr.device,
        "engine": "PaddleOCR",
        "model": os.getenv("OCR_MODEL", "PP-OCRv4_mobile")
    }

@app.post("/api/job/polish")
def polish_job_description(content: dict):
    # Endpoint to polish role description using AI
    ds = DeepSeekService()
    polished = ds.polish_role_description(content.get("text", ""))
    return {"polished_text": polished}

@app.post("/api/screen/batch", response_model=ScreeningResponse)
async def screen_batch(
    job_requirement: str = Form(...),
    files: List[UploadFile] = File(...)
):
    try:
        job_req_dict = json.loads(job_requirement)
        job_req = JobRequirement(**job_req_dict)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Job Requirement JSON: {str(e)}")

    if not files:
        raise HTTPException(status_code=400, detail="No CV files provided")

    # Save uploaded files
    saved_files = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file_path)

    try:
        # Process batch
        results = await process_batch(job_req, saved_files)
        return ScreeningResponse(
            job_title=job_req.job_info.job_title,
            results=results
        )
    finally:
        # Cleanup files if not keeping them
        if os.getenv("KEEP_UPLOADED_FILES", "false").lower() != "true":
            for file_path in saved_files:
                if os.path.exists(file_path):
                    os.remove(file_path)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
