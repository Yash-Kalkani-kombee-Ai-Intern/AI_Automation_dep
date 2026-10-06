import chromadb


CHROMA_PATH = "../../data/chroma"


def create_vector_store():
    """
    Create or open the local Chroma database.
    """

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name="restaurant_policy"
    )

    return collection


def store_chunks(collection, chunks, embeddings):
    """
    Store chunks and their embeddings in Chroma.
    """

    ids = [
        f"chunk-{index}"
        for index in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
    )

    return collection