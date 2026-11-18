import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
chroma_client = chromadb.PersistentClient(path="data/chroma_db")
collection = chroma_client.get_or_create_collection(
    name="faqs", embedding_function=ef
)

def ingest_faq_data(path: str):
    df = pd.read_csv(path)
    collection.add(
        documents=df["question"].tolist(),
        metadatas=[{"answer": a} for a in df["answer"]],
        ids=[f"id_{i}" for i in range(len(df))]
    )

def get_relevant_qa(query: str, n_results: int = 2):
    result = collection.query(query_texts=[query], n_results=n_results)
    answers = [meta["answer"] for meta in result["metadatas"][0]]
    return " ".join(answers)

from openai import OpenAI

client = OpenAI()

def generate_answer(query: str, context: str) -> str:
    prompt = f"""Answer the question using only the context below. 
If the answer is not in the context, say "I don't know".

CONTEXT: {context}
QUESTION: {query}"""
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content