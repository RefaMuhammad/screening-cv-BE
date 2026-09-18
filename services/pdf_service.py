import fitz  # PyMuPDF
import os
from typing import Tuple, List, Union
from PIL import Image
import io

class PDFService:
    def __init__(self):
        pass

    def extract_text_and_images(self, pdf_path: str) -> Tuple[str, List[Image.Image]]:
        """
        Tries to extract text. If text is too short (likely scanned),
        returns images for OCR instead.
        """
        text_content = ""
        images = []
        
        try:
            doc = fitz.open(pdf_path)
            
            for page in doc:
                text_content += page.get_text() + "\n"
                
            # If text is too short, consider it a scanned PDF and extract images
            if len(text_content.strip()) < 100:
                text_content = "" # clear it, we will use OCR
                for page in doc:
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # higher res for OCR
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    images.append(img)
            
            doc.close()
            return text_content.strip(), images
            
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return "", []
