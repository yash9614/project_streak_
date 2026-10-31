from mcp.server.mcpserver import MCPServer
from tools import get_current_date, estimate_trip_cost, search_knowledge_base
from rag.ingestion import load_and_index

mcp = MCPServer("Travel RAG Agent")

load_and_index()

@mcp.tool()
def get_current_date_tool() -> str:
    """Get today's date."""
    return get_current_date()

@mcp.tool()
def estimate_trip_cost_tool(days: int, budget_level: str = "medium") -> str:
    """Estimate trip cost. days: number of days, budget_level: low/medium/high"""
    return estimate_trip_cost(days, budget_level)

@mcp.tool()
def search_knowledge_base_tool(query: str) -> str:
    """Search the travel knowledge base for tips and destination info."""
    return search_knowledge_base(query)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
