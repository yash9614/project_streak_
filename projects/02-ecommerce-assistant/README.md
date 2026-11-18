# 02 — E-commerce Assistant

Multi-route chatbot that handles:

- **Small-talk** — direct conversational responses
- **FAQ** — RAG over product policies using ChromaDB
- **Product queries** — text-to-SQL against a local SQLite database

Built with OpenAI, semantic-router, ChromaDB, SQLite, and Streamlit.

## Features

- Semantic routing between three intents
- Persistent Chroma collection for FAQs
- Text-to-SQL generation + execution + natural language answer
- Streamlit chat UI with session history

## Run locally

1. Copy `.env.example` to `.env` and add your OpenAI key:
   ```
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL=gpt-4o-mini
   ```

2. Install dependencies (or use an existing venv that already has them):
   ```bash
   pip install -r requirements.txt
   ```

3. Start the app:
   ```bash
   streamlit run app/main.py
   ```

## Project layout

```
app/
├── main.py          # Streamlit UI
├── ask.py           # Central dispatcher
├── router.py        # Semantic router
├── faq.py           # FAQ RAG chain
├── sql.py           # Text-to-SQL chain
└── smalltalk.py     # Small-talk handler
```

Note: Test scripts used during development were intentionally not committed.
