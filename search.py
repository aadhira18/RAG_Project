
import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DB_PATH = "./chroma_db"
COLLECTION_NAME = "docquery"
TOP_K = 3

# 1. Load the same embedding model used during storage
print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

# 2. Connect to the existing vector database
client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_collection(
    name=COLLECTION_NAME
)

# 3. Accept a question from the user
query = input("\nEnter your question: ").strip()

if not query:
    raise ValueError("Please enter a question.")

# 4. Convert the question into a 384-dimensional vector
query_embedding = model.encode(
    query,
    convert_to_numpy=True
)

# 5. Search for the three most similar chunks
results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=min(TOP_K, collection.count()),
    include=["documents", "metadatas", "distances"]
)

# 6. Display the retrieved results
print("\nMost relevant chunks:\n")

for rank, (document, metadata, distance) in enumerate(
    zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ),
    start=1
):
    print("=" * 60)
    print(f"Result {rank}")
    print("Page:", metadata["page_number"])
    print("Distance:", round(distance, 4))
    print("Text:")
    print(document)
    print()
