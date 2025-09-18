import logging
from pathlib import Path
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def setup_logging(level=logging.INFO):
    """Configure logging for the application."""
    log_dir = Path("../data/logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "chatpdf.log"),
            logging.StreamHandler()
        ]
    )