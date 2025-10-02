import spacy
import subprocess
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_spacy_model(model_name="en_core_web_md"):
    try:
        return spacy.load(model_name)
    except OSError:
        logger.warning(f"Model '{model_name}' not found. Attempting to install fallback model 'en_core_web_sm'.")
        try:
            subprocess.run(
                ["python", "-m", "spacy", "download", "en_core_web_sm"], check=True
            )
            logger.info("Fallback model 'en_core_web_sm' installed successfully.")
            return spacy.load("en_core_web_sm")
        except Exception as e:
            logger.error("Could not load or install the required spaCy models.")
            logger.error("Please install the 'en_core_web_md' model using:")
            logger.error("    python -m spacy download en_core_web_md")
            logger.error("Or install the fallback 'en_core_web_sm' model using:")
            logger.error("    python -m spacy download en_core_web_sm")
            raise e

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()
