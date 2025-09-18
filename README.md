# ChatPDF AI 🤖📄

An intelligent PDF chat application that allows you to have natural conversations with your PDF documents. Upload any PDF and ask questions about its content using the power of Google's Gemini AI through OpenAI's API interface.

## 🌐 Live Demo
Try it now: https://chatpdf-ai-dcvo.onrender.com/
Upload any PDF and start chatting with your document instantly!

## ✨ Features

- **Interactive PDF Chat**: Ask questions about your PDF content in natural language
- **Dual Interface**: Choose between a modern FastAPI web interface or convenient CLI tool
- **Smart Text Extraction**: Advanced PDF processing with pdfplumber and intelligent content scoring
- **OCR Fallback**: Automatic OCR using Tesseract for scanned or low-quality PDFs
- **Text Quality Assessment**: NLTK-powered text quality scoring for optimal extraction method selection
- **AI-Powered Responses**: Leverages Google Gemini 1.5 Flash for accurate, context-aware answers
- **Session Management**: Secure file handling with automatic cleanup
- **Comprehensive Logging**: Detailed logs for debugging and monitoring

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key
- Tesseract OCR (optional, for scanned PDFs)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/chatpdf-ai.git
   cd chatpdf-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Create config directory if it doesn't exist
   mkdir -p config
   
   # Create your .env file
   echo "GEMINI_API_KEY=your_gemini_api_key_here" > config/.env
   ```

4. **Run the application**
   
   **Web Interface:**
   ```bash
   cd web
   python web_main.py
   ```
   Then open `http://localhost:8000` in your browser
   
   **CLI Interface:**
   ```bash
   python cli/main.py
   ```

## 📁 Project Structure

```
chatPDF/
├── src/                          # Core source code
│   ├── pdf/                      # PDF processing modules
│   │   ├── extractor.py          # PDF text extraction
│   │   └── scoring.py            # Content relevance scoring
│   ├── chat/                     # Chat functionality
│   │   └── gemini_setup.py       # Gemini AI integration
│   └── utils/                    # Utility modules
│       ├── config.py             # Configuration management
│       └── logging_config.py     # Logging setup
├── web/                          # Web interface
│   ├── templates/                # HTML templates
│   ├── static/                   # CSS and static files
│   └── web_main.py               # FastAPI web application
├── cli/                          # Command-line interface
│   └── main.py                   # CLI application
├── data/                         # Data directories
│   ├── uploads/                  # Uploaded PDF files
│   └── logs/                     # Application logs
└── config/                       # Configuration files
    └── .env                      # Environment variables
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `config/` directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Application Settings

The application includes several configurable parameters:

- **Max File Size**: 10MB limit for uploaded PDFs
- **OCR Settings**: Automatic OCR fallback for scanned documents
- **Text Quality Threshold**: 0.1 (documents below this score trigger OCR)
- **Model**: Uses Gemini 1.5 Flash for optimal performance
- **Session Management**: Automatic cleanup on server shutdown

### Tesseract OCR Setup (Optional)

For better handling of scanned PDFs:

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

## 🖥️ Usage

### Web Interface

1. Start the web server:
   ```bash
   cd web
   python web_main.py
   ```

2. Open your browser to `http://localhost:8000`

3. Upload a PDF file using the interface

4. Start asking questions about your document!

### CLI Interface

1. Run the CLI tool:
   ```bash
   python cli/main.py
   ```

2. Follow the prompts to upload your PDF and start chatting

### Example Interactions

```
You: "What is the main topic of this document?"
AI: "Based on the content, this document primarily discusses..."

You: "Can you summarize the key findings?"
AI: "The key findings include: 1) ... 2) ... 3) ..."

You: "What does it say about methodology?"
AI: "The document describes the methodology as..."
```

## 🏗️ Architecture

### Core Components

- **PDF Processing (`src/pdf/`)**:
  - `extractor.py`: Multi-method text extraction with pdfplumber and Tesseract OCR
  - `scoring.py`: NLTK-based text quality assessment using dictionary validation, character variety, and linguistic patterns

- **AI Integration (`src/chat/`)**:
  - `gemini_setup.py`: OpenAI-compatible client for Google Gemini API
  - Conversation management with context-aware responses
  - Document-specific assistant with strict content boundaries

- **Web Interface (`web/`)**:
  - FastAPI-based REST API with async file handling
  - Session-based file management with automatic cleanup
  - Real-time chat interface with message history

- **Utilities (`src/utils/`)**:
  - `config.py`: Environment and application configuration
  - `logging_config.py`: Structured logging setup

### Key Features

- **Intelligent Text Extraction**: Automatically selects between direct text extraction and OCR based on content quality
- **Quality Scoring**: Uses multiple metrics including dictionary validation, character variety, and linguistic patterns
- **Session Management**: Secure file handling with UUID-based sessions and automatic cleanup
- **Error Handling**: Comprehensive error handling with detailed logging and user feedback

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📋 Dependencies

Key packages (see `requirements.txt` for complete list):

### Core Dependencies
- `fastapi==0.116.2` - Modern web framework for the API
- `uvicorn==0.35.0` - ASGI server for FastAPI
- `openai==1.107.3` - OpenAI client (used for Gemini API access)
- `python-dotenv==1.1.1` - Environment variable management

### PDF Processing
- `pdfplumber==0.11.7` - Primary PDF text extraction
- `pdfminer-six==20250506` - Low-level PDF processing
- `pytesseract==0.3.13` - OCR for scanned documents
- `pillow==11.3.0` - Image processing for OCR

### Natural Language Processing
- `nltk==3.9.1` - Text quality assessment and linguistic analysis

### Additional Utilities
- `aiofiles==24.1.0` - Async file operations
- `jinja2==3.1.6` - Template rendering
- `httpx==0.28.1` - HTTP client for API calls

## 🐛 Troubleshooting

### Common Issues

**PDF Upload Fails**
- Check file size limits in configuration
- Ensure the PDF is not password protected or corrupted

**AI Responses Are Poor**
- Verify your Gemini API key is correct
- Check if the PDF text extraction was successful
- Ensure sufficient context is being provided

**Web Interface Won't Load**
- Check if port 8000 is available
- Verify all dependencies are installed correctly
- Check the logs in `data/logs/` for detailed errors
- Ensure the config/.env file exists with your API key

**OCR Not Working**
- Install Tesseract OCR on your system
- Verify Tesseract is accessible from command line: `tesseract --version`
- Check if PIL/Pillow can process your PDF images

**Session Errors**
- Sessions are stored in memory and cleared on server restart
- Check that the uploads directory has proper write permissions
- Verify the data/uploads directory structure exists

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for providing the powerful language model
- The FastAPI team for the excellent async web framework
- pdfplumber and pdfminer developers for robust PDF processing
- Tesseract OCR project for optical character recognition
- NLTK project for natural language processing tools
- Contributors and testers who helped improve this project
