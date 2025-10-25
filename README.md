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

##  Working Mechanism

KeywordX processes text in multiple logical stages to extract and score contextually relevant keywords:

1. **Input**  
   The user provides raw text and a list of target keywords to search for.

2. **Text Chunking**  
   Candidate phrases are extracted using **noun chunks** and important **lemmas** via the `chunk_phrases` method.  
   These chunks represent potential keyword matches.

3. **Embeddings Generation**  
   Candidate phrases, target keywords, and a baseline phrase are converted into **vector embeddings** using the **spaCy model** (`en_core_web_md`).  
   The helper functions `embed_texts` and `whiten` handle embedding and normalization.

4. **Semantic Scoring**  
   Cosine similarity is computed between each keyword embedding and all candidate phrase embeddings.  
   Optional **IDF weighting** refines the relevance score for each match (`score_matches`).

5. **Semantic Selection**  
   For each keyword, the **highest-scoring phrase** is selected if it surpasses the configurable `min_score` threshold (default = 0.3).  
   This logic is implemented in `KeywordExtractor.extract`.

6. **Named Entity Recognition (NER)**  
   Named entities (like DATE, TIME, GPE, etc.) are extracted using **spaCy’s NER** and structured date parsing (`extract_structured`).

7. **Entity Boosting & Merging**  
   Extracted entities are mapped to logical keyword types (e.g., `DATE → "date"`, `GPE → "location"`).  
   Each entity match receives a **base score (0.6)**, optionally boosted by user-defined `entity_weights` (capped at **2.0**).  
   If an entity score exceeds the semantic match score for the same keyword, the entity match is prioritized.

8. **Output Generation**  
   The final output is a dictionary containing:
   - `"entities"` → list of extracted entities (text, type, span)  
   - `"semantic_matches"` → top-scoring matches for each keyword with their similarity scores

---

### Key Implementation Files

| File | Responsibility |
|------|----------------|
| **extractor.py** | Orchestrates the full extraction pipeline, handles entity merging and  validation |
| **chunker.py** | Extracts candidate phrases (noun chunks, lemmas) |
| **embeddings.py** | Handles embedding creation and normalization |
| **matcher.py** | Performs cosine similarity + IDF scoring |
| **ner.py** | Performs NER and structured date parsing |
| **utils.py** | Loads spaCy model and cleans text |

---

### Tunable Parameters

| Parameter | Default | Purpose |
|------------|----------|----------|
| `min_score` | 0.3 | Minimum semantic score required to accept a match |
| `base_entity_score` | 0.6 | Default confidence score for entity matches |
| `entity_weights` | — | User-defined boosts for specific entity types (max 2.0) |
| `baseline_text` | — | Used for embedding normalization |

---

##  Installation

Install from PyPI:

```bash
pip install keywordx
```

The en_core_web_md spaCy model is required for the library to function. Install it using the following command:

```
python -m spacy download en_core_web_md
```
If the en_core_web_md model is not available, the library will attempt to fall back to the smaller en_core_web_sm model. However, this may result in reduced accuracy. You can install the fallback model using:

```
python -m spacy download en_core_web_sm
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

or you can try it out at : [hugging face/keywordx](https://huggingface.co/spaces/KeiKurono/keywordx)

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
    - GitHub: [Madhusudan](https://github.com/keikurono7)
    - Role: Code implementation

- Saniya Naaz
    - Email: saniyanaaz2k4@gmail.com
    - GitHub: [Saniya Naaz](https://github.com/Saniyanaaz11)
    - Role: Research work

- Dr. Nandeeswar S B
    - Email: hodcse.aiml@amceducation.in
    - Role: Concept and idea generation

- Pratham Tomar
    - Github: [Pratham Tomar](https://github.com/prathamtomar99)
    - Role: Upgrading model implementation

# License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/keikurono7/keywordx/blob/main/LICENSE.txt) file for details.
---
