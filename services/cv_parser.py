import os
from services.pdf_service import PDFService
from services.ocr_service import OCRService
from services.deepseek_service import DeepSeekService
from models.schemas import CandidateInfo

class CVParser:
    def __init__(self):
        self.pdf_service = PDFService()
        self.ocr_service = OCRService()
        self.ds_service = DeepSeekService()

    def process_cv(self, filepath: str, job_desc: str = "") -> dict:
        filename = os.path.basename(filepath)
        
        # 1. Extract text or images
        text, images = self.pdf_service.extract_text_and_images(filepath)
        
        source_type = "pdf_text"
        
        # 2. OCR if needed
        if not text and images:
            print(f"[INFO] No text found in {filename}. Falling back to local OCR processing ({len(images)} pages)...")
            source_type = "ocr"
            text = self.ocr_service.extract_text_from_images(images)
            if text:
                print(f"[SUCCESS] OCR completed successfully for {filename}")
            else:
                print(f"[ERROR] OCR failed to extract any text from {filename}")
        elif text:
            print(f"[SUCCESS] Text extracted directly from PDF for {filename}")
            
        if not text:
            raise Exception(f"Could not extract any text from CV {filename} (both PDF text & OCR failed)")
            
        # 3. Extract info via DeepSeek
        print(f"[INFO] Extracting structured data via DeepSeek AI for {filename}...")
        candidate_info = self.ds_service.extract_candidate_info(text, job_desc)
        
        if candidate_info.candidate_name and candidate_info.candidate_name != "Unknown":
            print(f"[SUCCESS] AI extraction successful for {filename} (Name: {candidate_info.candidate_name})")
        else:
            print(f"[WARNING] AI extraction might have failed or degraded for {filename}")
        
        return {
            "filename": filename,
            "source_type": source_type,
            "candidate_info": candidate_info,
            "raw_text": text
        }
