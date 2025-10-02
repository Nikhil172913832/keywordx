def chunk_phrases(text):
    import spacy
    nlp = spacy.load("en_core_web_md")
    doc = nlp(text)
    phrases = []

    for chunk in doc.noun_chunks:
        phrases.append(chunk.text)

    for token in doc:
        if token.pos_ in {"VERB", "NOUN"}:
            phrases.append(token.lemma_)

    return list(set(phrases))
