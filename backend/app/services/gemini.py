import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.gemini_api_key)
_model = genai.GenerativeModel(settings.gemini_model)


async def generate(prompt: str) -> str:
    response = _model.generate_content(prompt)
    return response.text
