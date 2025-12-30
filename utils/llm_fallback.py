# TOXIC_KEYWORDS = [
#     "địt", "đụ", "cặc", "lồn", "đéo", "đm", "vãi l"
# ]

# def llm_predict(comment: str, title: str, topic: str) -> bool:
#     text = comment.lower()

#     for word in TOXIC_KEYWORDS:
#         if word in text:
#             return True

#     return False

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('models/gemini-2.0-flash')

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

def llm_predict(comment: str, title: str, topic: str) -> bool:
    """
    Sử dụng Gemini để phân tích bình luận khi model chính phân vân.
    """
    prompt = f"""
    Bạn là một chuyên gia kiểm duyệt nội dung tiếng Việt. 
    Nhiệm vụ của bạn là xác định xem bình luận dưới đây có tính chất "Toxic" (độc hại, chửi thề, xúc phạm, quấy rối) hay không.
    
    Ngữ cảnh:
    - Tiêu đề bài viết: {title}
    - Chủ đề: {topic}
    - Nội dung bình luận: "{comment}"
    
    Yêu cầu: Chỉ trả lời duy nhất "True" nếu là Toxic và "False" nếu không Toxic. Không giải thích gì thêm.
    """

    try:
        response = model.generate_content(prompt)
        result = response.text.strip()
        
        if "True" in result:
            return True
        return False
    except Exception as e:
        print(f"Lỗi khi gọi Gemini API: {e}")
        return False