import os
import numpy as np
from PIL import Image

class OCRService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OCRService, cls).__new__(cls)
            cls._instance._init_ocr()
        return cls._instance

    def _init_ocr(self):
        try:
            from paddleocr import PaddleOCR
            use_gpu = os.getenv("OCR_DEVICE", "gpu").lower() == "gpu"
            
            # Using mobile configuration to save VRAM
            self.ocr = PaddleOCR(
                use_angle_cls=True, 
                lang='en', 
                use_gpu=use_gpu,
                show_log=False,
                det_model_dir=None, # will download automatically
                rec_model_dir=None,
                cls_model_dir=None
            )
            self.device = "gpu" if use_gpu else "cpu"
            print(f"OCR initialized on {self.device.upper()}")
            self.available = True
        except Exception as e:
            print(f"Failed to initialize OCR: {e}")
            self.ocr = None
            self.available = False
            self.device = "unknown"

    def is_available(self):
        return self.available

    def extract_text_from_images(self, images: list) -> str:
        if not self.available:
            return ""
        
        full_text = []
        for img in images:
            # Convert PIL image to numpy array for PaddleOCR
            img_np = np.array(img)
            
            result = self.ocr.ocr(img_np, cls=True)
            
            if result and result[0]:
                for line in result[0]:
                    full_text.append(line[1][0])
                    
        return "\n".join(full_text)
