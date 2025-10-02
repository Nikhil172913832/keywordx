import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def score_matches(kw_emb, cand_embs, phrases, idf_vectorizer=None, idf_map=None, baseline_emb=None):
    sims = cosine_similarity([kw_emb], cand_embs)[0]

    if idf_vectorizer is not None:
        tfidf = idf_vectorizer.transform(phrases).toarray()
        tfidf_weights = tfidf.max(axis=1)
    elif idf_map is not None:
        tfidf_weights = np.array([idf_map.get(p, 1.0) for p in phrases])
    else:
        tfidf_weights = np.ones(len(phrases))

    tfidf_weights = tfidf_weights / (tfidf_weights.max() + 1e-6)

    final_scores = 0.7 * sims + 0.3 * tfidf_weights
    return final_scores
