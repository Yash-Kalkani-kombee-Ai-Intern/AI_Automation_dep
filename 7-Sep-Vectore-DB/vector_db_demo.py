import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


# ============================================================
# STEP 1: LOAD TXT DATASET
# ============================================================

file_path = "data/airline_docs.txt"

with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

# Split documents using blank lines
documents = [
    doc.strip()
    for doc in content.split("\n\n")
    if doc.strip()
]

print("\n--- Dataset Loaded ---")
print("Total documents:", len(documents))


# ============================================================
# STEP 2: LOAD EMBEDDING MODEL
# ============================================================

print("\nLoading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


# ============================================================
# STEP 3: GENERATE EMBEDDINGS
# ============================================================

print("\nGenerating embeddings...")

embeddings = model.encode(
    documents,
    show_progress_bar=True
)

embeddings = np.array(embeddings).astype("float32")

print("\n--- Embedding Information ---")
print("Embedding shape:", embeddings.shape)


# ============================================================
# STEP 4: CREATE VECTOR DATABASE / FAISS INDEX
# ============================================================

dimension = embeddings.shape[1]

# FAISS L2 index
index = faiss.IndexFlatL2(dimension)

# Add document vectors into index
index.add(embeddings)

print("\n--- FAISS Vector Index ---")
print("Vector dimension:", dimension)
print("Total vectors stored:", index.ntotal)


# ============================================================
# STEP 5: SEMANTIC SEARCH FUNCTION
# ============================================================

def search_documents(query, top_k=3):

    # Convert user query into embedding
    query_embedding = model.encode([query])

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    # Search similar vectors
    distances, indices = index.search(
        query_embedding,
        top_k
    )

    print("\n========================================")
    print("QUERY:", query)
    print("========================================")

    for rank, (idx, distance) in enumerate(
        zip(indices[0], distances[0]),
        start=1
    ):

        print(f"\nResult {rank}")
        print(f"Distance: {distance:.4f}")
        print(f"Document:\n{documents[idx]}")


# ============================================================
# STEP 6: TEST SEARCH
# ============================================================

search_documents(
    "If I cancel my flight, when will I receive my money?",
    top_k=3
)


# ============================================================
# STEP 7: INTERACTIVE SEARCH
# ============================================================

while True:

    query = input(
        "\nAsk your question (type 'exit' to stop): "
    )

    if query.lower() == "exit":
        print("Program stopped.")
        break

    search_documents(
        query,
        top_k=3
    )