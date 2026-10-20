
from sentence_transformers import SentenceTransformer

from chunk_text import split_into_chunks
from extract_text import extract_pdf_text


# Step 1: Load the embedding model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)
print("Model loaded successfully!")


# Step 2: Extract PDF text and create chunks
pages = extract_pdf_text()
chunks = split_into_chunks(pages)

print("Total chunks:", len(chunks))


# Step 3: Extract the text from each chunk
chunk_texts = [chunk["text"] for chunk in chunks]


# Step 4: Generate embeddings
print("Generating embeddings...")

embeddings = model.encode(
    chunk_texts,
    show_progress_bar=True,
    convert_to_numpy=True
)


# Step 5: Verify the embeddings
print("\nEmbedding generation completed!")
print("Number of embeddings:", len(embeddings))
print("Dimensions of each embedding:", embeddings.shape[1])

print("\nFirst chunk:")
print(chunk_texts[0])

print("\nFirst 10 values of its embedding:")
print(embeddings[0][:10])
