import re
from underthesea import word_tokenize
from shortmap import SHORT_MAP


def normalize_shortmap(text: str) -> str:
    words = text.split()
    words = [SHORT_MAP.get(w, w) for w in words]
    return " ".join(words)


def clean_special_char(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-ZÀ-ỹ0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> str:
    return word_tokenize(text, format="text")


def load_stopwords(path: str) -> set:
    with open(path, encoding="utf-8") as f:
        return set(line.strip() for line in f)


def remove_stopwords(text: str, stopwords: set) -> str:
    return " ".join([w for w in text.split() if w not in stopwords])


def preprocess_text(text: str, stopwords: set) -> str:
    text = normalize_shortmap(text)
    text = clean_special_char(text)
    text = tokenize(text)
    text = remove_stopwords(text, stopwords)
    return text
