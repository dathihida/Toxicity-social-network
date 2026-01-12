import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.0-flash")

def llm_predict(comment: str, title: str = "", topic: str = "") -> bool:
    """
    Sử dụng Gemini để phân tích bình luận khi model chính phân vân.
    Trả về:
        True  -> Toxic
        False -> Non-toxic
    """

    prompt = f"""
Bạn là một chuyên gia kiểm duyệt nội dung tiếng Việt.

Nhiệm vụ của bạn là xác định xem bình luận dưới đây có tính chất TOXIC
(chửi thề, xúc phạm, quấy rối, công kích cá nhân, ngôn từ thù ghét) hay không.

Ngữ cảnh:
- Tiêu đề bài viết: {title}
- Chủ đề: {topic}

Bình luận:
\"\"\"{comment}\"\"\"

Yêu cầu:
- Chỉ trả lời DUY NHẤT một từ:
    True  (nếu Toxic)
    False (nếu Không Toxic)
- Không giải thích thêm.
"""

    try:
        response = model.generate_content(prompt)
        result = response.text.strip()

        if result.lower().startswith("true"):
            return True
        return False

    except Exception as e:
        print("Gemini API error, fallback used:", e)
        toxic_keywords = [
            "địt", "đụ", "cặc", "lồn", "đéo", "đm", "vãi l", "ngu", "óc chó"
        ]

        text = comment.lower()
        return any(word in text for word in toxic_keywords)
