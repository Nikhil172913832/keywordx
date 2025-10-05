from .chunker import chunk_phrases
from .embeddings import embed_texts, whiten
from .matcher import score_matches
from .ner import extract_structured
from .utils import load_spacy_model
from collections.abc import Mapping


class KeywordExtractor:
    # same entities u have checked in .ner/extract_structures.py
    VALID_ENTITY_TYPES = {"DATE", "TIME", "MONEY", "CARDINAL", "LOC", "GPE"}

    def __init__(self, baseline_text="is the a", entity_weights: Mapping | None = None):
        """
        Initialize KeywordExtractor with optional entity boost weights.
        Args:
            baseline_text (str): Text used for embedding normalization.
            entity_weights (dict): Custom boost weights for entity types.
                                   Example: {'DATE': 1.5, 'GPE': 1.2, 'MONEY': 0.8}
        """
        # type enforcement
        if entity_weights is not None and not isinstance(entity_weights, Mapping):
            raise TypeError(f"entity_weights must be a dict, not {type(entity_weights).__name__}")

        # validate entity labels , vaidate typos
        if entity_weights:
            invalid_keys = [k for k in entity_weights if k not in self.VALID_ENTITY_TYPES]
            if invalid_keys:
                raise ValueError(
                    f"Invalid entity types in entity_weights: {invalid_keys}. "
                    f"Valid options are: {sorted(self.VALID_ENTITY_TYPES)}"
                )

        self.entity_weights = dict(entity_weights) if entity_weights else {}
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

        ents = extract_structured(text)

        # Map entity types to domain keywords
        entity_map = {
            "DATE": "date",
            "TIME": "time",
            "MONEY": "money",
            "CARDINAL": "number",
            "GPE": "place",
            "LOC": "place"
        }

        for ent in ents:
            ent_type = ent["type"]
            mapped_keyword = entity_map.get(ent_type)

            if mapped_keyword and mapped_keyword in keywords:
                boost = self.entity_weights.get(ent_type, 1.0)

                boosted_score = min(boost, 2.0)  # keep it reasonable

                final_results[mapped_keyword] = {
                    "keyword": mapped_keyword,
                    "match": ent["text"],
                    "score": boosted_score
                }

        results = list(final_results.values())
        return {"semantic_matches": results, "entities": ents}