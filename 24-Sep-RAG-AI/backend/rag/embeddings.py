from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def create_embedding_model():
    """
    Load the local embedding model.
    """
    return SentenceTransformer(MODEL_NAME)


def create_embeddings(model, chunks):
    """
    Convert text chunks into numerical vectors.
    """
    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return embeddings