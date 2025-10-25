# Benchmarks

Benchmark KeywordX against popular keyword extraction methods.

## Installation

Install benchmark dependencies:

```bash
pip install -r benchmarks/requirements.txt
```

## Running Benchmarks

```bash
python benchmarks/benchmark.py
```

## Methods Compared

- **KeywordX**: Semantic similarity with entity boosting
- **TF-IDF**: Term frequency-inverse document frequency (statistical)
- **RAKE**: Rapid Automatic Keyword Extraction (graph-based)
- **YAKE**: Yet Another Keyword Extractor (statistical with linguistic features)
- **TextRank**: PageRank-based keyword extraction (graph-based)

## Metrics

- **Speed**: Execution time in seconds
- **Accuracy**: Precision against ground truth keywords
