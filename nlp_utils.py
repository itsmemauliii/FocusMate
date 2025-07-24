import spacy
from dateparser import parse

nlp = spacy.load("en_core_web_sm")

def parse_task_input(text):
    doc = nlp(text)
    task = text
    date = None

    for ent in doc.ents:
        if ent.label_ in ["DATE", "TIME"]:
            date = parse(ent.text)
            task = text.replace(ent.text, "").strip()
            break

    return task, date.strftime("%Y-%m-%d") if date else None
