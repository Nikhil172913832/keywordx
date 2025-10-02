from .chunker import chunk_phrases
from .embeddings import embed_texts, whiten
from .matcher import score_matches
from .ner import extract_structured
from .utils import load_spacy_model

class KeywordExtractor:
    def __init__(self, baseline_text="is the a"):
        self.baseline_text = baseline_text
        self._load_model()

    def _load_model(self):
        self.model = load_spacy_model("en_core_web_md")

    def extract(self, text, keywords, idf_vectorizer=None, idf_map=None, min_score=0.3):
        phrases = chunk_phrases(text)
        cand_embs = embed_texts(phrases, self.model)
        cand_embs = whiten(cand_embs)
        kw_embs = embed_texts(keywords, self.model)
        baseline_emb = embed_texts([self.baseline_text], self.model)[0]
        results = []

        for i, kw in enumerate(keywords):
            scores = score_matches(kw_embs[i], cand_embs, phrases, idf_vectorizer, idf_map, baseline_emb)
            top_idx = scores.argmax()
            if scores[top_idx] >= min_score:
                results.append({
                    "keyword": kw,
                    "match": phrases[top_idx],
                    "score": float(scores[top_idx])
                })

        final_results = {}
        for r in results:
            kw = r["keyword"]
            if kw not in final_results or r["score"] > final_results[kw]["score"]:
                final_results[kw] = r

        results = list(final_results.values())
        ents = extract_structured(text)

        entity_map = {
            "DATE": "date",
            "TIME": "time",
            "GPE": "place",
            "LOC": "place"
        }
        for ent in ents:
            mapped_keyword = entity_map.get(ent["type"])
            if mapped_keyword and mapped_keyword in keywords:
                if mapped_keyword not in final_results or 1.0 > final_results[mapped_keyword]["score"]:
                    final_results[mapped_keyword] = {
                        "keyword": mapped_keyword,
                        "match": ent["text"],
                        "score": 1.0
                    }

        results = list(final_results.values())
        return {"semantic_matches": results, "entities": ents}
