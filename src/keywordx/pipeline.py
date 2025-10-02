from .extractor import KeywordExtractor

def extract(text, keywords):
    ke = KeywordExtractor()
    return ke.extract(text, keywords)
