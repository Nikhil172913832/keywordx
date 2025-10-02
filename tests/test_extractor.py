from keywordx.extractor import KeywordExtractor

def test_basic_extract():
    ke = KeywordExtractor()
    text = "Tomorrow I have a work meeting at 5pm in Bangalore."
    keywords = ["meeting", "time", "place"]
    res = ke.extract(text, keywords)
    assert "semantic_matches" in res
    assert "entities" in res
