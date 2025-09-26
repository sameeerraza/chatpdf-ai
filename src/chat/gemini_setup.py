import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict
import logging

class ChatClient:
    def __init__(self, model: str = "gemini-2.5-flash", max_history: int = 20):
        load_dotenv(dotenv_path="../config/.env")
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        self.model = model
        self.max_history = max_history
        self.messages: List[Dict[str, str]] = []
        
    def _init_chat_session(self, document_text: str):
        """Initialize chat session with document context (for web interface)."""
        system_prompt = """You are a specialized PDF document assistant. Your role is STRICTLY LIMITED to answering questions about the provided PDF document only.

IMPORTANT RULES:
1. ONLY answer questions that can be answered using information from the provided PDF document
2. If a question is about topics NOT covered in the PDF, politely decline and redirect the user back to the document content
3. If asked about unrelated topics (like movies, games, general knowledge, etc.), respond with: "I can only answer questions about the content of the provided PDF document. Please ask me something related to the document."
4. Always base your answers on the specific content, data, and information present in the PDF
5. If you're unsure whether information is in the document, clearly state your uncertainty
6. You can help clarify, summarize, or explain concepts that are mentioned in the PDF document

Remember: You are a document-specific assistant, not a general knowledge AI."""
        
        self.messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Document content:\n{document_text[:10000]}..."}  # Limit initial context
        ]
        
    def start_chat(self, document_text: str):
        """Start interactive chat session (for CLI interface)."""
        self._init_chat_session(document_text)
        
        print("ChatPDF is ready! Type your question or 'exit' to quit.")
        
        while True:
            try:
                question = input("\nYou: ").strip()
                if question.lower() in ["exit", "quit", "q"]:
                    print("Goodbye!")
                    break
                    
                if not question:
                    continue
                    
                response = self._get_response(question)
                print(f"Bot: {response}")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                logging.error(f"Chat error: {e}")
                
    def _get_response(self, question: str) -> str:
        """Get response from the AI model."""
        self.messages.append({"role": "user", "content": question})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages[-self.max_history:],  # Limit conversation history
                max_tokens=1000,
                temperature=0.3  # Lower temperature for more focused responses
            )
            
            answer = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": answer})
            
            return answer
            
        except Exception as e:
            raise RuntimeError(f"API call failed: {e}")
