import argparse
import sys
import os
from pathlib import Path

# parent directory to the path so we can import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.pdf.extractor import PDFExtractor
from src.chat.gemini_setup import ChatClient

def main():
    parser = argparse.ArgumentParser(description='ChatPDF - Chat with your PDF documents')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('--model', default='gemini-1.5-flash', help='Model to use')
    
    args = parser.parse_args()
    
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"Error: File {pdf_path} not found")
        sys.exit(1)
        
    try:
        extractor = PDFExtractor()
        text = extractor.extract_text(pdf_path)
        
        chat_client = ChatClient(model=args.model)
        chat_client.start_chat(text)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()