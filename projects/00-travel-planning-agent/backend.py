from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="RAG + Tools API (MCP-backed)")

MCP_URL = "http://127.0.0.1:8000/mcp"

class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []

class ChatResponse(BaseModel):
    reply: str
    tool_calls: list[str] = []

async def call_mcp_tool(tool_name: str, arguments: dict) -> str:
    async with streamable_http_client(MCP_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            if result.content and len(result.content) > 0:
                return result.content[0].text
            return str(result)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    messages = [
        {"role": "system", "content": "You are a helpful travel assistant. Use tools when needed. Be concise."}
    ]
    messages.extend(request.history)
    messages.append({"role": "user", "content": request.message})

    async with streamable_http_client(MCP_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools_response = await session.list_tools()
            openai_tools = []
            for tool in tools_response.tools:
                openai_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.input_schema or {"type": "object", "properties": {}}
                    }
                })

    tool_calls_made = []

    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=openai_tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return ChatResponse(
                reply=message.content or "Done.",
                tool_calls=tool_calls_made
            )

        messages.append(message)
        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments or "{}")
            tool_calls_made.append(func_name)

            result = await call_mcp_tool(func_name, func_args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

@app.get("/")
def root():
    return {"status": "RAG + Tools API (MCP-backed) is running", "docs": "/docs"}
