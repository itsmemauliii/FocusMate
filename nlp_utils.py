import spacy
from spacy.cli import download

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def parse_task_input(text):
    doc = nlp(text)
    tasks = []
    for sent in doc.sents:
        task = sent.text.strip()
        if task:
            tasks.append(task)
    return tasks
