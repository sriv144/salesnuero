import os
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Initialize ChromaDB Persistent Client
persist_directory = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
client = chromadb.PersistentClient(path=persist_directory)

# 2. Setup Embedding Function (all-MiniLM-L6-v2)
# Note: requires 'sentence-transformers' package
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# 3. Create Collections
personality_collection = client.get_or_create_collection(
    name="personality-corpus", 
    embedding_function=sentence_transformer_ef
)

product_collection = client.get_or_create_collection(
    name="product-corpus", 
    embedding_function=sentence_transformer_ef
)

# 4. Setup Text Splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
    is_separator_regex=False,
)

def ingest_markdown_file(file_path: str, collection):
    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} not found.")
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Chunk the document
    chunks = text_splitter.split_text(text)
    
    # Generate metadata and IDs
    file_name = os.path.basename(file_path)
    ids = [f"{file_name}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": file_path, "chunk": i} for i in range(len(chunks))]
    
    # Add to ChromaDB
    collection.add(
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )
    print(f"[OK] Ingested {len(chunks)} chunks from {file_name} into {collection.name}")

if __name__ == "__main__":
    # Define sample data paths (creates dummy files if not found)
    data_dir = os.path.join(os.path.dirname(__file__), "raw_data")
    os.makedirs(data_dir, exist_ok=True)
    
    personality_file = os.path.join(data_dir, "psychology.md")
    product_file = os.path.join(data_dir, "product.md")
    
    if not os.path.exists(personality_file):
        with open(personality_file, 'w', encoding='utf-8') as f:
            f.write("# BIG FIVE PERSONALITY TRAITS\nOpenness, Conscientiousness, Extraversion, Agreeableness, Neuroticism are the five broad domains of personality that are used to describe human personality.")
            
    if not os.path.exists(product_file):
        with open(product_file, 'w', encoding='utf-8') as f:
            f.write("# PLATFORM FEATURES\nOur new predictive analytics tool helps you score leads based on their psychographics, increasing conversion rates by 30%.")

    print("Starting ingestion process...\n")
    ingest_markdown_file(personality_file, personality_collection)
    ingest_markdown_file(product_file, product_collection)
    
    print("\n--- Testing Retrieval ---")
    
    # 5. Test Queries to Verify Retrieval
    results_p = personality_collection.query(
        query_texts=["What are the big five traits?"],
        n_results=1
    )
    print(f"\nPersonality Query Results:\n{results_p['documents']}")

    results_prod = product_collection.query(
        query_texts=["How much does the predictive tool increase conversions?"],
        n_results=1
    )
    print(f"\nProduct Query Results:\n{results_prod['documents']}")
