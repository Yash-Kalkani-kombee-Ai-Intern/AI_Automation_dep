from pdf_loader import load_pdf
from chunker import chunk_text
from embeddings import create_embedding_model, create_embeddings


pdf_path = "../documents/restaurant_policy.pdf"


# 1. Load PDF
text = load_pdf(pdf_path)

# 2. Create chunks
chunks = chunk_text(text)

print(f"Total chunks: {len(chunks)}")


# 3. Load embedding model
print("\nLoading embedding model...")

model = create_embedding_model()

print("Embedding model loaded!")


# 4. Create embeddings
print("\nCreating embeddings...")

embeddings = create_embeddings(model, chunks)


# 5. Show result
print("\n========== EMBEDDING RESULT ==========")

print("Number of chunks:", len(chunks))
print("Number of embeddings:", len(embeddings))
print("Embedding dimensions:", embeddings.shape[1])

print("\nFirst chunk:")
print(chunks[0][:300])

print("\nFirst embedding:")
print(embeddings[0])