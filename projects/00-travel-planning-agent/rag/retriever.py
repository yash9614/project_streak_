from .vectorstore import collection

def search_knowledge(query: str, top_k: int = 3) -> list[dict]:
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    formatted = []
    if results["documents"] and results["documents"][0]:
        for i in range(len(results["documents"][0])):
            formatted.append({
                "content": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "distance": results["distances"][0][i] if results.get("distances") else None
            })
    return formatted
