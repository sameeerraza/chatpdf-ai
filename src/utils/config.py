import os
from pathlib import Path

class Config:
    # PDF Processing
    OCR_RESOLUTION = int(os.getenv("OCR_RESOLUTION", "200"))
    OCR_LANGUAGE = os.getenv("OCR_LANGUAGE", "eng")
    TEXT_QUALITY_THRESHOLD = float(os.getenv("TEXT_QUALITY_THRESHOLD", "0.1"))
    
    # Chat Settings
    MAX_CONVERSATION_HISTORY = int(os.getenv("MAX_CONVERSATION_HISTORY", "20"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # API Settings
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_BASE_URL = os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
    
    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent
    CACHE_DIR = PROJECT_ROOT / "cache"