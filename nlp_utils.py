from textblob import TextBlob

def extract_task_details(text):
    # Naive NLP approach – look for "on <day>" or "by <date>"
    blob = TextBlob(text)
    due = None
    if " on " in text:
        due = text.split(" on ")[-1]
    elif " by " in text:
        due = text.split(" by ")[-1]
    return blob.sentences[0], due
