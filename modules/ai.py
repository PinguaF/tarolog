import google.generativeai as genai
import io, json

from config.config import TOKEN_AI

with io.open('config/lang-ru-0.json', encoding='utf-8') as file:
    config_lang = json.load(file)
genai.configure(api_key= TOKEN_AI)

def generate_goroskope(astrolog_type, zodiak):
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 64,
      "max_output_tokens": 200,
      "response_mime_type": "application/json",
    }
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(config_lang["promt-astrolog"+str(astrolog_type)]+" "+config_lang[str(zodiak)])
    return response.text