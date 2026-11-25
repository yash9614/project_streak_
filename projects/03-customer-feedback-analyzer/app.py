"""
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
    reviews = [line.strip() for line in reviews_text.split("\n") if line.strip()]

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