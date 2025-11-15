from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("MISSING_KEY")
    raise SystemExit(2)

client = OpenAI(api_key=api_key)

try:
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user", "content": "短く日本語で挨拶してください。"}],
        max_tokens=60,
        temperature=0.2,
    )
    print("SUCCESS")
    print(resp.choices[0].message.content.strip())
except Exception as e:
    print("ERROR", str(e))
    raise
