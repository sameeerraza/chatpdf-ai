import pdfplumber
import pytesseract
from PIL import Image
from pathlib import Path
from typing import Optional
import logging
from .scoring import TextQualityScorer

class PDFExtractor:
    def __init__(self, use_ocr: bool = True, ocr_threshold: float = 0.1):
        self.use_ocr = use_ocr
        self.ocr_threshold = ocr_threshold
        self.scorer = TextQualityScorer()

    def extract_text(self, pdf_path: Path) -> str:
        """Extract text from PDF with optional OCR fallback."""
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        extracted_text = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                
                for i, page in enumerate(pdf.pages, 1):
                    print(f"Processing page {i}/{total_pages}")
                    page_text = self._extract_page_text(page)
                    extracted_text.append(f"Page {i}:\n{page_text}\n")
                    
        except Exception as e:
            raise RuntimeError(f"Error processing PDF: {e}")
            
        return "".join(extracted_text)
    
    def _extract_page_text(self, page) -> str:
        """Extract text from a single page with OCR fallback."""
        # Try text extraction first
        text = page.extract_text() or ""
        
        # Use OCR if text quality is poor and OCR is enabled
        if self.use_ocr and self.scorer.score_text_quality(text) < self.ocr_threshold:
            try:
                pil_image = page.to_image(resolution=200).original  # Reduced resolution
                ocr_text = pytesseract.image_to_string(pil_image, lang='eng')
                
                if self.scorer.score_text_quality(ocr_text) > self.scorer.score_text_quality(text):
                    return ocr_text
            except Exception as e:
                logging.warning(f"OCR failed: {e}")
                
        return text