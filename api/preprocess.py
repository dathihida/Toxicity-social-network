import re
from underthesea import word_tokenize

SHORT_MAP = {
    "ko": "không",
    "k": "không",
    "khum": "không",
    "hok": "không",
    "đc": "được",
    "dc": "được",
    "vl": "vãi l*n",
    "cl": "cái l*n",
}

def normalize_shortmap(text: str) -> str:
    words = text.split()
    return " ".join([SHORT_MAP.get(w, w) for w in words])

def clean_text(text: str) -> str:
    text = text.lower()
    text = normalize_shortmap(text)
    text = re.sub(r"[^a-zA-ZÀ-ỹ0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return word_tokenize(text, format="text")

def build_input(comment, title, topic):
    return f"[TITLE] {clean_text(title)} [TOPIC] {clean_text(topic)} [COMMENT] {clean_text(comment)}"
