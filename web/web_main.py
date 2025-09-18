import os
import sys
import uuid
from pathlib import Path
from typing import Dict, Any
import shutil

# parent directory to the path so we can import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from src.pdf.extractor import PDFExtractor
from src.chat.gemini_setup import ChatClient
from src.utils.logging_config import setup_logging
from contextlib import asynccontextmanager

# Setup logging
setup_logging()

# Initialize FastAPI app
app = FastAPI(title="ChatPDF", description="Chat with your PDF documents")

# Create necessary directories
UPLOAD_DIR = Path("../data/uploads")
STATIC_DIR = Path("static")
TEMPLATES_DIR = Path("templates")

for dir_path in [UPLOAD_DIR, STATIC_DIR, TEMPLATES_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Mount static files and templates
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# In-memory session storage
sessions: Dict[str, Dict[str, Any]] = {}

# Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".pdf"}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with file upload."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Handle PDF file upload and processing."""
    
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")
    
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Check file size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"File size exceeds {MAX_FILE_SIZE // (1024*1024)}MB limit")
    
    try:
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Save uploaded file
        file_path = UPLOAD_DIR / f"{session_id}.pdf"
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        # Extract text using your existing extractor
        extractor = PDFExtractor()
        document_text = extractor.extract_text(file_path)
        
        # Initialize chat client
        chat_client = ChatClient()
        
        # Store session data
        sessions[session_id] = {
            "file_path": file_path,
            "document_text": document_text,
            "chat_client": chat_client,
            "filename": file.filename,
            "messages": []
        }
        
        # Initialize chat client with document
        chat_client._init_chat_session(document_text)
        
        return JSONResponse({
            "success": True,
            "session_id": session_id,
            "filename": file.filename,
            "redirect_url": f"/chat/{session_id}"
        })
        
    except Exception as e:
        # Clean up file if processing failed
        if 'file_path' in locals() and file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.get("/chat/{session_id}", response_class=HTMLResponse)
async def chat_page(request: Request, session_id: str):
    """Chat interface page."""
    if session_id not in sessions:
        return RedirectResponse(url="/", status_code=302)
    
    session_data = sessions[session_id]
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "session_id": session_id,
        "filename": session_data["filename"],
        "messages": session_data["messages"]
    })

@app.post("/chat/{session_id}")
async def send_message(session_id: str, message: str = Form(...)):
    """Handle chat messages."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if not message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        session_data = sessions[session_id]
        chat_client = session_data["chat_client"]
        
        # Get response from chat client
        response = chat_client._get_response(message)
        
        # Store messages in session
        session_data["messages"].extend([
            {"role": "user", "content": message},
            {"role": "assistant", "content": response}
        ])
        
        return JSONResponse({
            "success": True,
            "response": response
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.delete("/session/{session_id}")
async def cleanup_session(session_id: str):
    """Clean up session and associated files."""
    if session_id in sessions:
        session_data = sessions[session_id]
        
        # Remove uploaded file
        if session_data["file_path"].exists():
            session_data["file_path"].unlink()
        
        # Remove session from memory
        del sessions[session_id]
        
        return JSONResponse({"success": True, "message": "Session cleaned up"})
    
    raise HTTPException(status_code=404, detail="Session not found")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "active_sessions": len(sessions)}

#Cleanup function for server shutdown
@app.on_event("shutdown")
async def cleanup_on_shutdown():
    """Clean up all sessions and files on server shutdown."""
    for session_id, session_data in sessions.items():
        if session_data["file_path"].exists():
            session_data["file_path"].unlink()
    
    # Clean up uploads directory
    if UPLOAD_DIR.exists():
        shutil.rmtree(UPLOAD_DIR)
        UPLOAD_DIR.mkdir(exist_ok=True)

# if __name__ == "__main__":
#     uvicorn.run(
#         "web_main:app",
#         host="127.0.0.1",
#         port=8000,
#         reload=True,
#         log_level="info"
#     )
if __name__ == "__main__":
    # Get port from environment variable for deployment
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")  # Changed from 127.0.0.1
    
    uvicorn.run(
        "web_main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )