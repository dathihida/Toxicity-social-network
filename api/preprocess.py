import re
from underthesea import word_tokenize

SHORT_MAP = {
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
    'idc': 'đi được',
    'kkk': 'cười'
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
