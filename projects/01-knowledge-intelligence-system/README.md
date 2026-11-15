# Knowledge Intelligence System

Beginner RAG project: upload PDFs or text files and chat with them.

## Stack

- Streamlit
- LangChain (+ langchain-classic)
- ChromaDB
- OpenAI

## Quick Start

```bash
cd projects/01-knowledge-intelligence-system
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-your-key" > .env

python -m streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
```

Upload documents in the sidebar, click **Process Documents**, then ask questions.
