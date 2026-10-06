from pdf_loader import load_pdf
from chunker import chunk_text
from embeddings import create_embedding_model, create_embeddings
from vector_store import create_vector_store, store_chunks


pdf_path = "../documents/restaurant_policy.pdf"


# 1. Load PDF
text = load_pdf(pdf_path)

# 2. Create chunks
chunks = chunk_text(text)

print(f"Total chunks: {len(chunks)}")


# 3. Create embeddings
model = create_embedding_model()
embeddings = create_embeddings(model, chunks)


# 4. Create Chroma collection
collection = create_vector_store()

print("\nChroma collection created!")


# 5. Store chunks + embeddings
store_chunks(
    collection,
    chunks,
    embeddings
)

print("Chunks stored successfully!")

print("\nTotal documents in Chroma:", collection.count())