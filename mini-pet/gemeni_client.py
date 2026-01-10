from google import genai
from config import config_object

client = genai.Client(api_key=config_object.gemini_api_key)

def get_answer(prompt: str):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )
    return response.text
  
