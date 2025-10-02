import dateparser
from datetime import datetime
from .utils import load_spacy_model

def extract_structured(text, ref_date=None):
    nlp = load_spacy_model("en_core_web_md")
    doc = nlp(text)
    res = []

    for ent in doc.ents:
        if ent.label_ in {"DATE", "TIME", "MONEY", "CARDINAL", "LOC", "GPE"}:
            res.append({"type": ent.label_, "text": ent.text, "span": (ent.start_char, ent.end_char)})

    if ref_date is None:
        ref_date = datetime.now()

    d = dateparser.parse(text, settings={"RELATIVE_BASE": ref_date})
    if d:
        res.append({"type": "PARSED_DATE", "text": text, "value": d.isoformat()})

    return res
