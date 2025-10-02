from .utils import load_spacy_model

def chunk_phrases(text):
    nlp = load_spacy_model("en_core_web_md")
    doc = nlp(text)
    phrases = []

    for chunk in doc.noun_chunks:
        phrases.append(chunk.text)

    for token in doc:
        if token.pos_ in {"VERB", "NOUN"}:
            phrases.append(token.lemma_)

    return list(set(phrases))
