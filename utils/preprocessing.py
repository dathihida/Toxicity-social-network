import re
from underthesea import word_tokenize


SHORT_MAP = {
    "đm": "địt mẹ",
    "dm": "địt mẹ",
    "vl": "vãi lồn",
    "vcl": "vãi cả lồn",
    "cc": "con cặc",
    "đéo": "đéo",
    "ko": "không",
    "k": "không"
}

def load_stopwords(path="data/raw/vietnamese-stopwords-dash.txt"):
    with open(path, encoding="utf-8") as f:
        return set(
            line.strip().replace("-", " ")
            for line in f
            if line.strip()
        )

STOPWORDS = load_stopwords()

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def expand_short_words(text: str) -> str:
    for k, v in SHORT_MAP.items():
        text = re.sub(rf"\b{k}\b", v, text)
    return text

def remove_stopwords(tokens):
    return [t for t in tokens if t not in STOPWORDS]

def preprocess_text(comment, title, topic):
    text = f"{title} {topic} {comment}".lower()
    text = text.replace("_", " ")
    return text

