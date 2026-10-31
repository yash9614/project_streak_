# Concepts & Interview Questions

## Core Concepts

### 1. Tool Calling / Function Calling
The LLM decides when and which function to call based on the user query. You define schemas; the model returns structured tool calls; you execute them and feed results back.

**Key idea**: The model is the controller, not hard-coded if/else logic.

### 2. RAG (Retrieval-Augmented Generation)
- Chunk documents
- Embed with a model
- Store in a vector database
- At query time, retrieve relevant chunks and inject them into the prompt

**Why**: Reduces hallucination and grounds answers in your data.

### 3. MCP (Model Context Protocol)
A standard way to expose tools and resources to AI clients.  
In this project the MCP server exposes date, cost estimation, and knowledge search as tools over streamable HTTP.

### 4. Hybrid Agent Pattern
The agent can choose between:
- Structured tools (date, cost)
- Unstructured knowledge search (RAG)

This is closer to real production agents than pure chat or pure RAG.

### 5. Layered Architecture
```
UI (Streamlit)  →  API (FastAPI)  →  MCP Client  →  MCP Server  →  Tools + RAG
```

## Interview Questions

### Tool Calling
1. What is the difference between hard-coded tool routing and LLM tool calling?
2. How does OpenAI's tool calling work under the hood?
3. What happens if the model calls a tool that does not exist?
4. How would you add a new tool (e.g., weather) to this system?

### RAG
5. Why do we use embeddings instead of keyword search?
6. What is the difference between `text-embedding-3-small` and a larger embedding model?
7. How would you improve chunking in this project?
8. What is the role of `distance` / similarity score in retrieval?
9. How would you add source citations to the final answer?

### MCP
10. What problem does MCP solve compared to calling tools directly?
11. What is the difference between stdio and streamable HTTP transport?
12. How would you add authentication to the MCP server?
13. Can multiple clients talk to the same MCP server?

### Architecture & Design
14. Why separate the MCP server from the FastAPI backend?
15. What are the trade-offs of using ChromaDB locally vs a hosted vector DB?
16. How would you add conversation memory that survives restarts?
17. How would you evaluate the quality of the RAG answers?
18. What would you change to make this production-ready?

### Practical
19. Walk through the request flow when a user asks “What is today’s date and any Kyoto tips?”
20. How would you add a new knowledge document without restarting the server?
