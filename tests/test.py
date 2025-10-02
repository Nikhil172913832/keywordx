from keywordx import KeywordExtractor

ke = KeywordExtractor()
text = "Tomorrow I have a work meeting at 5pm in Bangalore."
keywords = ["meeting", "time", "place", "date"]

result = ke.extract(text, keywords)
print(result)