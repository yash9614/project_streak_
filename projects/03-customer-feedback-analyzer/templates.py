"""
templates.py
Automatically creates the project folder structure and starter files
for the Customer Feedback Analyzer (OpenAI version).

Usage:
    python templates.py
"""

import os
from pathlib import Path

# Project root (where this script lives)
ROOT = Path(__file__).parent

FILES = {
    "database.py": '''"""
All the database work lives here.
"""

import sqlite3

DB_FILE = "feedback.db"


def init_db():
    """Create the feedback table the first time we run."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY,
            review TEXT,
            label TEXT,
            score INTEGER,
            theme TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_results(results):
    """Write all analyzed reviews into the database."""
    conn = sqlite3.connect(DB_FILE)
    for r in results:
        conn.execute(
            "INSERT INTO feedback (review, label, score, theme) VALUES (?, ?, ?, ?)",
            (r["review"], r["label"], r["score"], r["theme"]),
        )
    conn.commit()
    conn.close()


def load_history():
    """Read every review we have saved so far."""
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute(
        "SELECT review, label, score, theme FROM feedback"
    ).fetchall()
    conn.close()
    return rows
''',

    "api.py": '''"""
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
''',

    "app.py": '''"""
The frontend: a Streamlit dashboard.

Run it (in a SECOND terminal, while api.py is also running):
    uv run streamlit run app.py
"""

from collections import Counter

import requests
import streamlit as st

from database import init_db, save_results, load_history, DB_FILE

API_URL = "http://127.0.0.1:8000/analyze"

init_db()

st.title("📝 Customer Feedback Analyzer")
st.write("Paste your customer reviews below, one review per line.")

reviews_text = st.text_area("Reviews", height=200)

if st.button("Analyze"):
    reviews = [line.strip() for line in reviews_text.split("\\n") if line.strip()]

    if not reviews:
        st.warning("Please paste at least one review.")
    else:
        results = []
        for review in reviews:
            try:
                response = requests.post(API_URL, json={"text": review})
                response.raise_for_status()
                data = response.json()
                results.append({
                    "review": review,
                    "label": data["label"],
                    "score": data["score"],
                    "theme": data["theme"],
                })
            except Exception:
                results.append({
                    "review": review,
                    "label": "error",
                    "score": 0,
                    "theme": "error",
                })

        st.session_state.results = results

if "results" in st.session_state:
    results = st.session_state.results

    st.subheader("Results")
    st.dataframe(results)

    scores = [r["score"] for r in results if r["label"] != "error"]
    positive = [r for r in results if r["label"] == "positive"]
    themes = [r["theme"] for r in results if r["theme"] != "error"]

    st.subheader("Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Reviews", len(results))
    if scores:
        col2.metric("Average score", round(sum(scores) / len(scores), 1))
        col3.metric("% Positive", f"{round(len(positive) / len(results) * 100)}%")

    if themes:
        top_theme = Counter(themes).most_common(1)[0][0]
        st.info(f"Customers talk most about: **{top_theme}**")

    if st.button("💾 Save to database"):
        save_results(results)
        st.success(f"Saved {len(results)} reviews to {DB_FILE}")

with st.expander("📚 Saved history (all reviews in the database)"):
    history = load_history()
    if history:
        st.write(f"Total saved so far: {len(history)}")
        st.dataframe(
            [{"review": r[0], "label": r[1], "score": r[2], "theme": r[3]} for r in history]
        )
    else:
        st.write("Nothing saved yet. Analyze some reviews and click Save.")
''',

    "sample_reviews.txt": '''The food was delicious but the delivery took over an hour. Not happy.
Amazing taste and the order arrived hot and early. Will order again!
Prices have gone up too much for the same small portion.
Service was rude when I called to ask about my order.
The biryani was perfect, exactly like last time. Very consistent.
Okay food, nothing special. Average experience overall.
Delivery boy was very polite and on time. Good job.
Cold food again. This is the third time the delivery was slow.
Great value for money, big portion and tasty.
The app kept crashing while I was trying to place my order.
''',

    ".env.example": '''OPENAI_API_KEY=sk-your-openai-key-here
''',
}


def create_structure():
    print(f"Creating project files in: {ROOT}")
    for filename, content in FILES.items():
        path = ROOT / filename
        if path.exists():
            print(f"  Skipped (already exists): {filename}")
            continue
        path.write_text(content.strip() + "\\n", encoding="utf-8")
        print(f"  Created: {filename}")

    # Create .env from example if it doesn't exist
    env_path = ROOT / ".env"
    example_path = ROOT / ".env.example"
    if not env_path.exists() and example_path.exists():
        env_path.write_text(example_path.read_text(encoding="utf-8"), encoding="utf-8")
        print("  Created: .env (from .env.example) — remember to put your real OpenAI key in it")

    print("\\nDone. Next steps:")
    print("1. Edit .env and add your real OPENAI_API_KEY")
    print("2. Activate your existing venv from set_e_memory")
    print("3. uv add openai fastapi[standard] pydantic python-dotenv requests streamlit")
    print("4. Terminal 1: uv run fastapi dev api.py")
    print("5. Terminal 2: uv run streamlit run app.py")


if __name__ == "__main__":
    create_structure()