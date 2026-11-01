# Design Notes & Interview Questions

## Design decisions

### Tool calling
The LLM decides when to call a tool. Schemas live in `tools.py`; the model returns structured calls; results are fed back into the conversation.

### RAG
Simple retrieval: one chunk per markdown file, OpenAI embeddings, ChromaDB, top-k=3. Sources are returned with the snippets so the model can cite them.

### MCP
The MCP server exposes the same tools over streamable HTTP. FastAPI acts as an MCP client. Streamlit calls the tools directly for faster local iteration.

### Stateless chat
The `/chat` endpoint does not store conversation history. The client must send prior messages if multi-turn context is needed.

## Interview questions

### Tool calling
1. What is the difference between hard-coded routing and LLM tool calling?
2. How does OpenAI tool calling work under the hood?
3. What happens if the model calls a non-existent tool?
4. How would you add a weather tool?

### RAG
5. Why embeddings instead of keyword search?
6. What would you change about the current chunking strategy?
7. How would you add source citations in the final answer?
8. How would you evaluate retrieval quality?

### MCP & architecture
9. Why put an MCP server between FastAPI and the tools?
10. What is the difference between stdio and streamable HTTP?
11. Why does Streamlit bypass MCP?
12. How would you add authentication to the MCP server?
13. How would you make `/chat` keep session memory?

### Production
14. What are the trade-offs of local ChromaDB vs a hosted vector DB?
15. How would you add logging and error handling?
16. How would you containerize the two services?
17. What would you measure before calling this production-ready?
