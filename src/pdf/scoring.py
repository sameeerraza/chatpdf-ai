import re
from functools import lru_cache
from typing import Set
import string

class TextQualityScorer:
    def __init__(self):
        self._word_list: Set[str] | None = None
        
    @property
    def word_list(self) -> Set[str]:
        """Lazy load word list."""
        if self._word_list is None:
            self._word_list = self._load_word_list()
        return self._word_list
    
    def _load_word_list(self) -> Set[str]:
        """Load NLTK word list with error handling."""
        try:
            import nltk
            from nltk.corpus import words
            return set(word.lower() for word in words.words())
        except LookupError:
            import nltk
            nltk.download("words", quiet=True)
            from nltk.corpus import words
            return set(word.lower() for word in words.words())
        except Exception:
            # Fallback to basic scoring without dictionary
            return set()
    
    @lru_cache(maxsize=1000)
    def score_text_quality(self, text: str) -> float:
        """Score text quality based on multiple factors."""
        if not text or not text.strip():
            return 0.0
            
        # Clean and tokenize
        clean_text = text.lower().translate(str.maketrans('', '', string.punctuation))
        tokens = re.findall(r'\b[a-z]{2,}\b', clean_text)
        
        if not tokens:
            return 0.0
            
        # Multiple scoring factors
        scores = []
        
        # Dictionary word ratio
        if self.word_list:
            valid_words = sum(1 for token in tokens if token in self.word_list)
            scores.append(valid_words / len(tokens))
        
        # Character variety (not just repeated characters)
        unique_chars = len(set(text.lower()))
        char_variety_score = min(unique_chars / 26, 1.0)  # Normalize to alphabet size
        scores.append(char_variety_score)
        
        # Average word length (reasonable words)
        avg_word_length = sum(len(token) for token in tokens) / len(tokens)
        length_score = min(avg_word_length / 6, 1.0)  # Normalize around 6 chars
        scores.append(length_score)
        
        # Whitespace ratio (good text has reasonable spacing)
        whitespace_ratio = text.count(' ') / len(text) if text else 0
        space_score = min(whitespace_ratio * 5, 1.0)  # Reasonable spacing
        scores.append(space_score)
        
        return sum(scores) / len(scores) if scores else 0.0