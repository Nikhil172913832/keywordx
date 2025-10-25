import time
import subprocess
import sys
import logging
import numpy as np
from keywordx import KeywordExtractor

logging.getLogger('summa').setLevel(logging.WARNING)

try:
    import spacy
    try:
        spacy.load('en_core_web_md')
    except OSError:
        print("Downloading required spaCy model 'en_core_web_md'...")
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_md"], check=True)
        print("Model downloaded successfully!")
except Exception as e:
    print(f"Warning: Could not setup spaCy model: {e}")

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

try:
    from rake_nltk import Rake
    import nltk
    try:
        nltk.data.find('corpora/stopwords')
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt_tab', quiet=True)
    HAS_RAKE = True
except ImportError:
    HAS_RAKE = False

try:
    import yake
    HAS_YAKE = True
except ImportError:
    HAS_YAKE = False

try:
    from summa import keywords as summa_keywords
    HAS_TEXTRANK = True
except ImportError:
    HAS_TEXTRANK = False


SAMPLE_TEXTS = [
    "Tomorrow I have a work meeting at 5pm in Bangalore.",
    "The company announced a new product launch on March 15th at the convention center in San Francisco.",
    "Machine learning and artificial intelligence are transforming the technology industry rapidly.",
    "The stock market crashed yesterday, causing investors to lose millions of dollars.",
    "Climate change is causing severe weather patterns across the globe, affecting agriculture and water resources.",
]

SAMPLE_KEYWORDS = [
    ["meeting", "time", "place", "date"],
    ["product", "date", "location", "event"],
    ["technology", "machine learning", "artificial intelligence", "industry"],
    ["market", "investors", "money", "stocks"],
    ["climate", "weather", "agriculture", "water"],
]


def benchmark_keywordx(texts, keywords_list):
    ke = KeywordExtractor()
    results = []
    start = time.time()
    for text, keywords in zip(texts, keywords_list):
        result = ke.extract(text, keywords)
        results.append(result)
    elapsed = time.time() - start
    return results, elapsed


def benchmark_tfidf(texts, keywords_list):
    if not HAS_SKLEARN:
        return None, None
    
    vectorizer = TfidfVectorizer(max_features=10, stop_words='english')
    results = []
    start = time.time()
    for text, keywords in zip(texts, keywords_list):
        try:
            tfidf_matrix = vectorizer.fit_transform([text])
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf_matrix.toarray()[0]
            top_indices = scores.argsort()[-len(keywords):][::-1]
            extracted = [{"keyword": feature_names[i], "score": float(scores[i])} 
                        for i in top_indices if scores[i] > 0]
            results.append(extracted)
        except:
            results.append([])
    elapsed = time.time() - start
    return results, elapsed


def benchmark_rake(texts, keywords_list):
    if not HAS_RAKE:
        return None, None
    
    results = []
    start = time.time()
    for text in texts:
        rake = Rake()
        rake.extract_keywords_from_text(text)
        ranked = rake.get_ranked_phrases_with_scores()
        results.append([{"keyword": phrase, "score": float(score)} 
                       for score, phrase in ranked[:5]])
    elapsed = time.time() - start
    return results, elapsed


def benchmark_yake(texts, keywords_list):
    if not HAS_YAKE:
        return None, None
    
    results = []
    start = time.time()
    for text in texts:
        kw_extractor = yake.KeywordExtractor(top=5, stopwords=None)
        keywords_extracted = kw_extractor.extract_keywords(text)
        results.append([{"keyword": kw, "score": float(1-score)} 
                       for kw, score in keywords_extracted])
    elapsed = time.time() - start
    return results, elapsed


def benchmark_textrank(texts, keywords_list):
    if not HAS_TEXTRANK:
        return None, None
    
    results = []
    start = time.time()
    for text in texts:
        try:
            keywords_str = summa_keywords.keywords(text, words=5, scores=True)
            if keywords_str:
                results.append([{"keyword": kw, "score": float(score)} 
                               for kw, score in keywords_str])
            else:
                results.append([])
        except:
            results.append([])
    elapsed = time.time() - start
    return results, elapsed


def calculate_accuracy(results, ground_truth_keywords):
    if not results:
        return 0.0
    
    total_precision = 0.0
    count = 0
    
    for result, truth in zip(results, ground_truth_keywords):
        if not result or not truth:
            continue
        
        if isinstance(result, dict) and "semantic_matches" in result:
            extracted = set([m["match"].lower() for m in result["semantic_matches"]])
        else:
            extracted = set([item["keyword"].lower() for item in result])
        
        truth_set = set([k.lower() for k in truth])
        
        if extracted:
            precision = len(extracted & truth_set) / len(extracted)
            total_precision += precision
            count += 1
    
    return total_precision / count if count > 0 else 0.0


def print_results(name, elapsed, accuracy):
    print(f"{name:15} | Time: {elapsed:.4f}s | Accuracy: {accuracy:.2%}")


def run_benchmarks():
    print("="*60)
    print("KeywordX Performance Benchmark")
    print("="*60)
    print(f"Testing on {len(SAMPLE_TEXTS)} sample texts")
    print("-"*60)
    
    results_kx, time_kx = benchmark_keywordx(SAMPLE_TEXTS, SAMPLE_KEYWORDS)
    acc_kx = calculate_accuracy(results_kx, SAMPLE_KEYWORDS)
    print_results("KeywordX", time_kx, acc_kx)
    
    if HAS_SKLEARN:
        results_tfidf, time_tfidf = benchmark_tfidf(SAMPLE_TEXTS, SAMPLE_KEYWORDS)
        acc_tfidf = calculate_accuracy(results_tfidf, SAMPLE_KEYWORDS)
        print_results("TF-IDF", time_tfidf, acc_tfidf)
    else:
        print("TF-IDF         | Not available (install scikit-learn)")
    
    if HAS_RAKE:
        results_rake, time_rake = benchmark_rake(SAMPLE_TEXTS, SAMPLE_KEYWORDS)
        acc_rake = calculate_accuracy(results_rake, SAMPLE_KEYWORDS)
        print_results("RAKE", time_rake, acc_rake)
    else:
        print("RAKE           | Not available (install rake-nltk)")
    
    if HAS_YAKE:
        results_yake, time_yake = benchmark_yake(SAMPLE_TEXTS, SAMPLE_KEYWORDS)
        acc_yake = calculate_accuracy(results_yake, SAMPLE_KEYWORDS)
        print_results("YAKE", time_yake, acc_yake)
    else:
        print("YAKE           | Not available (install yake)")
    
    if HAS_TEXTRANK:
        results_textrank, time_textrank = benchmark_textrank(SAMPLE_TEXTS, SAMPLE_KEYWORDS)
        acc_textrank = calculate_accuracy(results_textrank, SAMPLE_KEYWORDS)
        print_results("TextRank", time_textrank, acc_textrank)
    else:
        print("TextRank       | Not available (install summa)")
    
    print("-"*60)
    print("Note: Accuracy is calculated as average precision against ground truth")
    print("="*60)


if __name__ == "__main__":
    run_benchmarks()
