import chromadb
import httpx
import re

OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"
CHUNK_SIZE = 200  # tokens approx, tune this

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("home_kb")

def chunk_markdown(text: str) -> list[str]:
    # Split on section headers and double newlines
    # Keep section header attached to its content
    sections = re.split(r'\n(?=##)', text)
    chunks = []
    for section in sections:
        # If section is long, split further by double newlines
        if len(section) > 800:
            parts = section.split('\n\n')
            chunks.extend([p.strip() for p in parts if p.strip()])
        else:
            if section.strip():
                chunks.append(section.strip())
    return chunks

def embed(text: str) -> list[float]:
    response = httpx.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text}
    )
    return response.json()["embedding"]

def index_knowledge_base(path: str = "knowledge/home.md"):
    with open(path) as f:
        text = f.read()
    chunks = chunk_markdown(text)
    
    # Clear and re-index (good for development, 
    # add a hash check later for production)
    collection.delete(where={"source": "home.md"})
    
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            embeddings=[embed(chunk)],
            ids=[f"chunk_{i}"],
            metadatas=[{"source": "home.md"}]
        )
    print(f"Indexed {len(chunks)} chunks")

def retrieve(query: str, top_k: int = 4) -> list[str]:
    query_embedding = embed(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results["documents"][0]  # list of chunk strings