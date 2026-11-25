"""
The backend: a small FastAPI service that analyzes ONE customer review
using OpenAI structured outputs.

Run it with:
    uv run fastapi dev api.py
"""

import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()


class Review(BaseModel):
    text: str


class Analysis(BaseModel):
    label: str   # "positive", "negative", or "neutral"
    score: int   # 1 (very bad) to 5 (very good)
    theme: str   # one word, e.g. "delivery"


@app.post("/analyze")
def analyze(review: Review):
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You analyze customer reviews. "
                    "label must be 'positive', 'negative', or 'neutral'. "
                    "score must be an integer from 1 (very bad) to 5 (very good). "
                    "theme must be ONE lowercase word for the main topic "
                    "(examples: delivery, taste, price, service, quality)."
                ),
            },
            {
                "role": "user",
                "content": f"Review: {review.text}",
            },
        ],
        response_format=Analysis,
    )
    return response.choices[0].message.parsed