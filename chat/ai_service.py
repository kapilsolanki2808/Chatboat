import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(override=True)
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set in the environment. Add it to .env or export it before running.")

client = Groq(api_key=API_KEY)

def get_ai_response(user_message):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": user_message}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI service error: {str(e)}"
