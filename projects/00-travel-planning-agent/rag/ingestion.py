from pathlib import Path
from .vectorstore import collection

def load_and_index():
    knowledge_dir = Path("knowledge")
    docs = []
    ids = []
    metadatas = []

    for i, file in enumerate(knowledge_dir.glob("*.md")):
        text = file.read_text(encoding="utf-8")
        docs.append(text)
        ids.append(f"doc_{i}")
        metadatas.append({"source": file.name})

    if docs:
        collection.add(documents=docs, ids=ids, metadatas=metadatas)
        print(f"Indexed {len(docs)} documents.")
    else:
        print("No documents found in knowledge/")
