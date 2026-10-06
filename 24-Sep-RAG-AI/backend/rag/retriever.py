from rag.embeddings import create_embedding_model
from rag.vector_store import create_vector_store


def retrieve_relevant_chunks(
    question: str,
    top_k: int = 3
):
    """
    Find the most relevant PDF chunks for a question.
    """

    model = create_embedding_model()

    collection = create_vector_store()

    question_embedding = model.encode(
        [question]
    ).tolist()

    results = collection.query(
        query_embeddings=question_embedding,
        n_results=top_k
    )

    return results