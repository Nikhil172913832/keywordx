import numpy as np

def embed_texts(texts, nlp_model):

    return np.array([nlp_model(text).vector for text in texts])

def whiten(embs):
    
    from sklearn.preprocessing import normalize
    return normalize(embs)
