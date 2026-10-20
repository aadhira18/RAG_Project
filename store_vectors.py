
import chromadb
from sentence_transformers import SentenceTransformer

from chunk_text import split_into_chunks
from extract_text import extract_pdf_text


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DB_PATH = "./chroma_db"
COLLECTION_NAME = "docquery"


# 1. Extract the PDF and create chunks
pages = extract_pdf_text()
chunks = split_into_chunks(pages)

if not chunks:
    raise ValueError("No chunks found in the PDF.")

chunk_texts = [chunk["text"] for chunk in chunks]


# 2. Generate embeddings
print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

print("Generating embeddings...")
embeddings = model.encode(
    chunk_texts,
    show_progress_bar=True,
    convert_to_numpy=True
)


# 3. Create the database directly inside RAG_Project
client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)


# 4. Prepare unique IDs and metadata
ids = [f"revision_notes_chunk_{i}" for i in range(len(chunks))]

metadatas = [
    {
        "source": "Complete_Revision_Notes_OS_CN_DBMS.pdf",
        "page_number": chunk["page_number"]
    }
    for chunk in chunks
]


# 5. Store vectors and text in ChromaDB
collection.upsert(
    ids=ids,
    documents=chunk_texts,
    embeddings=embeddings.tolist(),
    metadatas=metadatas
)


# 6. Verify storage
print("\nStorage successful!")
print("Database location:", DB_PATH)
print("Collection:", COLLECTION_NAME)
print("Stored chunks:", collection.count())
