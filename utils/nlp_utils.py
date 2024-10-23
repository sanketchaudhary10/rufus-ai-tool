import spacy

def load_nlp_model():
    return spacy.load("en_core_web_sm")
