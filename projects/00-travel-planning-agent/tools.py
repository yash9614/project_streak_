from datetime import datetime
from rag.retriever import search_knowledge

def get_current_date() -> str:
    """Return today's date in a readable format."""
    return datetime.now().strftime("%A, %d %B %Y")

def estimate_trip_cost(days: int, budget_level: str = "medium") -> str:
    """Rough daily cost estimate. budget_level: low / medium / high"""
    rates = {"low": 50, "medium": 120, "high": 250}
    daily = rates.get(budget_level.lower(), 120)
    total = days * daily
    return f"Estimated total for {days} days at {budget_level} level: ~${total}"

def search_knowledge_base(query: str) -> str:
    """Search the travel knowledge base and return relevant snippets."""
    results = search_knowledge(query, top_k=3)
    if not results:
        return "No relevant information found in the knowledge base."
    snippets = []
    for r in results:
        snippets.append(f"Source: {r['source']}\n{r['content'][:400]}")
    return "\n\n---\n\n".join(snippets)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_date",
            "description": "Get today's date",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "estimate_trip_cost",
            "description": "Estimate trip cost based on number of days and budget level",
            "parameters": {
                "type": "object",
                "properties": {
                    "days": {"type": "integer", "description": "Number of days"},
                    "budget_level": {"type": "string", "enum": ["low", "medium", "high"], "description": "Budget level"}
                },
                "required": ["days"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Search the knowledge base for travel tips, destination info, or general advice",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"]
            }
        }
    }
]

TOOL_MAP = {
    "get_current_date": get_current_date,
    "estimate_trip_cost": estimate_trip_cost,
    "search_knowledge_base": search_knowledge_base,
}
