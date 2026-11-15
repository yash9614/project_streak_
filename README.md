# Project Streak

A collection of beginner-to-intermediate Generative AI projects built while learning RAG, agents, and tool-calling.

## Projects

| # | Project | Description | Stack |
|---|---------|-------------|-------|
| 00 | [Travel Planning Agent](./projects/00-travel-planning-agent) | Preference gathering + tools + RAG for grounded itinerary advice. Dual path: direct Streamlit and MCP-backed FastAPI. | Streamlit, FastAPI, MCP, OpenAI, ChromaDB |
| 01 | [Knowledge Intelligence System](./projects/01-knowledge-intelligence-system) | Upload PDFs/TXT and chat with them using RAG. | Streamlit, LangChain, ChromaDB, OpenAI |

## Architecture Overview

```mermaid
flowchart TB
    subgraph Repo["Project Streak"]
        direction TB

        subgraph Travel["00 — Travel Planning Agent"]
            U1[User] --> S1[Streamlit UI]
            U1 --> F1[FastAPI :8001]
            S1 --> L1[OpenAI LLM]
            F1 --> MC[MCP Client]
            MC --> MS[MCP Server :8000]
            L1 --> T1[Tools]
            L1 --> R1[RAG Retriever]
            MS --> T1
            MS --> R1
            R1 --> C1[(ChromaDB)]
        end

        subgraph KIS["01 — Knowledge Intelligence System"]
            U2[User] --> S2[Streamlit UI]
            S2 --> Up[Document Upload]
            Up --> R2[RAG Pipeline]
            R2 --> C2[(ChromaDB)]
            R2 --> L2[OpenAI LLM]
        end
    end
```

## Project Structure

```
.
├── README.md
├── .gitignore
├── .env.example
└── projects/
    ├── 00-travel-planning-agent/      # RAG + MCP + FastAPI travel agent
    │   ├── app.py
    │   ├── backend.py
    │   ├── mcp_server.py
    │   ├── tools.py
    │   ├── llm.py
    │   ├── models.py
    │   ├── rag/
    │   ├── knowledge/
    │   ├── requirements.txt
    │   └── README.md
    └── 01-knowledge-intelligence-system/   # Document Q&A RAG
        ├── app.py
        ├── requirements.txt
        └── README.md
```

## Author

Yash Paprikar  
[GitHub](https://github.com/yash9614)
