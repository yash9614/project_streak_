# Project Streak — RAG + MCP + FastAPI Agent

A progressive GenAI project that combines conversational chat, tool calling, vector RAG, MCP server, and a FastAPI backend.

Built as a practical learning path from simple tools → embeddings → tool-calling loop → MCP → FastAPI.

## Stack

| Layer | Choice |
|-------|--------|
| UI | Streamlit |
| LLM | OpenAI (`gpt-4o-mini`) |
| Embeddings | `text-embedding-3-small` |
| Vector DB | ChromaDB (persistent) |
| MCP | MCP 2.x (streamable HTTP) |
| Backend | FastAPI + Uvicorn |
| Config | `python-dotenv` |

## Architecture

```mermaid
flowchart TB
    User[\"User\"] --> Streamlit[\"Streamlit UI<br/>(app.py)\"]
    User --> FastAPI[\"FastAPI<br/>(backend.py :8001)\"]
    
    Streamlit --> AgentLoop[\"Tool-calling Loop\"]
    FastAPI --> MCPClient[\"MCP Client\"]
    
    AgentLoop --> Tools[\"Tools\"]
    AgentLoop --> RAG[\"RAG Retriever\"]
    
    MCPClient --> MCPServer[\"MCP Server<br/>(mcp_server.py :8000)\"]
    MCPServer --> Tools
    MCPServer --> RAG
    
    RAG --> Chroma[(\"ChromaDB<br/>chroma_db/\")]
    Tools --> AgentLoop
    RAG --> AgentLoop
    MCPServer --> MCPClient
```

```mermaid
flowchart LR
    subgraph knowledge [Knowledge Base]
        Docs[\"knowledge/*.md\"]
    end
    Docs --> Ingest[\"ingestion.py\"]
    Ingest --> Embed[\"OpenAI Embeddings\"]
    Embed --> Chroma[(\"ChromaDB\")]
    Query[\"User Query\"] --> Retriever[\"retriever.py\"]
    Retriever --> Chroma
    Chroma --> Snippets[\"Relevant Snippets\"]
```

## Project Structure

```
.
├── app.py                  # Streamlit UI + tool-calling loop
├── backend.py              # FastAPI that talks to MCP server
├── mcp_server.py           # MCP server (streamable HTTP)
├── tools.py                # Tool functions + OpenAI schemas
├── rag/
│   ├── embeddings.py
│   ├── vectorstore.py      # ChromaDB client
│   ├── ingestion.py
│   └── retriever.py
├── knowledge/
│   └── sample-faq.md
├── requirements.txt
├── .env.example
├── concepts.md             # Concepts + interview questions
└── README.md
```

## Quick Start

```powershell
# Create venv (uv recommended)
uv venv
.\.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt

copy .env.example .env
# Add OPENAI_API_KEY and CHROMA_OPENAI_API_KEY

# Terminal 1 — MCP server
python mcp_server.py

# Terminal 2 — FastAPI
uvicorn backend:app --reload --port 8001

# Terminal 3 — Streamlit (optional)
streamlit run app.py
```

## Test the API

```powershell
irm -Method Post -Uri "http://127.0.0.1:8001/chat" -ContentType "application/json" -Body '{"message": "What is today date and any Kyoto tips?"}'
```

## Skills practiced

- Conversational memory
- Structured tool calling (OpenAI tools)
- Vector RAG with ChromaDB
- MCP server (streamable HTTP)
- MCP client inside FastAPI
- Separation of UI / API / MCP layers

## Author

Yash Paprikar  
[GitHub](https://github.com/yash9614)
