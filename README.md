# KeywordX

[![PyPI version](https://badge.fury.io/py/keywordx.svg)](https://pypi.org/project/keywordx/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

KeywordX is a lightweight Python library for extracting and matching keywords from text using **semantic similarity** and **entity-based boosting**.  
Perfect for NLP pipelines, chatbots, search systems, and event extraction.

---

##  Features

-  Extract keywords with semantic similarity scoring  
-  Boost keyword matches using entities (dates, times, places, etc.)  
-  Supports custom IDF weighting for better relevance  
-  Easy-to-use API for integration into NLP pipelines  

---

##  Installation

Install from PyPI:

```bash
pip install keywordx
```

Or install from source:

```
git clone https://github.com/keikurono7/keywordx.git
cd keywordx
pip install -e .
```

## Quick Start

Here is a quick example to get you started:

```python
from keywordx import KeywordExtractor

ke = KeywordExtractor()
text = "Tomorrow I have a work meeting at 5pm in Bangalore."
keywords = ["meeting", "time", "place", "date"]

result = ke.extract(text, keywords)
print(result)
```

## Example Output

The result will include extracted entities and semantic matches with scores:

```json
{
  "entities": [
    {"span": [0, 8], "text": "Tomorrow", "type": "DATE"},
    {"span": [34, 37], "text": "5pm", "type": "TIME"},
    {"span": [41, 50], "text": "Bangalore", "type": "GPE"}
  ],
  "semantic_matches": [
    {"keyword": "meeting", "match": "meeting", "score": 0.99},
    {"keyword": "time", "match": "5pm", "score": 1.0},
    {"keyword": "place", "match": "Bangalore", "score": 1.0},
    {"keyword": "date", "match": "Tomorrow", "score": 1.0}
  ]
}
```
# API Reference

- KeywordExtractor() <br>
  Initializes the keyword extractor.

- .extract(text, keywords) → dict <br>
  Extracts keywords and entities from text.
  - text: input string
  - keywords: list of keywords to match

- Returns:
  - entities: named entities (DATE, TIME, GPE, etc.)
  - semantic_matches: list of matched keywords with similarity scores

# Use Cases

- Event and meeting extraction for calendar assistants
- Chatbot intent detection
- Automatic tagging of documents and notes
- Context-aware search and indexing

# Contributing

Contributions are welcome. For significant changes, please open an issue first to discuss the proposal.

## Contributors

- Madhusudan
    - Email: dmpathani@gmail.com
    - GitHub: [keikurono7](https://github.com/keikurono7)
    - Role: Code implementation

- Saniya Naaz
    - Email: saniyanaaz2k4@gmail.com
    - GitHub: [Saniyanaaz11](https://github.com/Saniyanaaz11)
    - Role: Research work

- Dr. Nandeeswar S B
    - Email: hodcse.aiml@amceducation.in
    - Role: Concept and idea generation

# License

This project is licensed under the MIT License. See the LICENSE file for details.
---
