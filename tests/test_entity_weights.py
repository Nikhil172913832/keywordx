import pytest
from keywordx import KeywordExtractor

def test_custom_entity_weights():
    # Test with custom weights
    ke = KeywordExtractor(entity_weights={
        'DATE': 1.5,
        'GPE': 1.2,
        'TIME': 0.8
    })
    
    text = "Tomorrow I have a work meeting at 5pm in Bangalore."
    keywords = ["meeting", "time", "place", "date"]
    
    result = ke.extract(text, keywords)
    
    # Check if entities are present
    assert len(result["entities"]) == 3
    
    # Convert semantic matches to dict for easier testing
    matches = {m["keyword"]: m for m in result["semantic_matches"]}
    
    # Check if DATE has higher score due to boost
    assert matches["date"]["score"] == 1.5  # DATE boosted to 1.5
    assert matches["place"]["score"] == 1.2  # GPE boosted to 1.2
    assert matches["time"]["score"] == 0.8   # TIME reduced to 0.8

def test_invalid_entity_weights():
    # Test with invalid entity type
    with pytest.raises(ValueError) as exc_info:
        KeywordExtractor(entity_weights={'INVALID': 1.5})
    assert "Invalid entity types" in str(exc_info.value)
    
    # Test with invalid type
    with pytest.raises(TypeError) as exc_info:
        KeywordExtractor(entity_weights=[1, 2, 3])
    assert "must be a dict" in str(exc_info.value)

def test_default_weights():
    # Test without custom weights
    ke = KeywordExtractor()
    text = "Tomorrow I have a meeting at 5pm in Bangalore."
    keywords = ["meeting", "time", "place", "date"]
    
    result = ke.extract(text, keywords)
    matches = {m["keyword"]: m for m in result["semantic_matches"]}
    
    # Check if default score of 1.0 is used
    assert matches["date"]["score"] == 1.0
    assert matches["place"]["score"] == 1.0
    assert matches["time"]["score"] == 1.0