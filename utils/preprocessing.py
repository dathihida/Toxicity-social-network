import re
from underthesea import word_tokenize


SHORTCUT_MAP = {
    'vd': 'ví dụ',
    'cmt': 'bình luận',
    'dc': 'được',
    'vl': 'vãi lồn',
    'cmm': 'cha mẹ mày',
    'đcmm': 'địt con mẹ mày',
    'dmm': 'địt mẹ mày',
    'ad': 'admin',
    'kkk': 'cười',
    'blv': 'bình luận viên',
    'vn': 'Việt Nam',
    'đna': 'Đông Nam Á',
    'fb': 'facebook',
    'kh': 'không',
    'V.L': 'vãi lồn',
    'iu': 'yêu',
    'hqua': 'hôm qua',
    'tr': 'trời',
    'cíuuuuuuu': 'cứu',
    'kh': 'không',
    'e': 'em',
    'a': 'anh',
    'rựu': 'rượu',
    'ng': 'người',
    'Zạ': 'dạ',
    'nma': 'nhưng mà',
    'sốp': 'cửa hàng',
    'shop': 'cửa hàng',
    'bđs': 'bất động sản',
    'tht': 'thiệt',
    'mas': 'mà sao',
    't': 'tao',
    'z': 'vậy',
    'đm': 'địt mẹ',
    'ak': 'à',
    'ezai': 'em giai',
    'lol': 'lồn',
    'post': 'bài viết',
    'đell': 'đéo',
    'dell': 'đéo',
    'idc': 'đi được'
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

