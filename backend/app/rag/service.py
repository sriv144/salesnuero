import os
import chromadb
from chromadb.utils import embedding_functions

_persist_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "chroma_db")

_client = chromadb.PersistentClient(path=os.path.abspath(_persist_dir))
_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

_personality_collection = _client.get_or_create_collection(
    name="personality-corpus", embedding_function=_ef
)
_product_collection = _client.get_or_create_collection(
    name="product-corpus", embedding_function=_ef
)


def query_personality(query: str, n_results: int = 3) -> str:
    results = _personality_collection.query(query_texts=[query], n_results=n_results)
    docs = results.get("documents", [[]])
    return " ".join(docs[0]) if docs and docs[0] else "No relevant personality data found."


def query_product(query: str, n_results: int = 3) -> str:
    results = _product_collection.query(query_texts=[query], n_results=n_results)
    docs = results.get("documents", [[]])
    return " ".join(docs[0]) if docs and docs[0] else "No relevant product data found."
