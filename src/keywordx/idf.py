from sklearn.feature_extraction.text import TfidfVectorizer

def build_idf(corpus):
    vect = TfidfVectorizer(ngram_range=(1,2), smooth_idf=True)
    vect.fit(corpus)
    return vect
