import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def talk(query: str) -> str:
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": f"You are a friendly e-commerce assistant. Keep answers short.\n\nUser: {query}"}]
    )
    return response.choices[0].message.content