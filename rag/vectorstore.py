import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["CHROMA_OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

client = chromadb.PersistentClient(path="./chroma_db")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

collection = client.get_or_create_collection(
    name="knowledge",
    embedding_function=openai_ef
)
