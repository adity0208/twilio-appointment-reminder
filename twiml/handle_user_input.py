import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def parse_response(response):
    doc = nlp(response.lower())
    if "yes" in response or "confirm" in response:
        return "confirm"
    elif "no" in response or "cancel" in response:
        return "cancel"
    elif "reschedule" in response:
        return "reschedule"
    else:
        return "unknown"
