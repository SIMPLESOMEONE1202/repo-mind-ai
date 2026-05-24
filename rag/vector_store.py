import chromadb

from sentence_transformers import (
    SentenceTransformer
)

# Embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# Chroma client
chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)


def get_collection(repo_name):

    collection_name = (
        repo_name
        .replace("-", "_")
        .replace(" ", "_")
        .lower()
    )

    return chroma_client.get_or_create_collection(
        name=collection_name
    )


def store_chunks(repo_name, chunks):

    collection = get_collection(repo_name)

    documents = []
    embeddings = []
    metadatas = []
    ids = []

    for index, chunk in enumerate(chunks):

        content = chunk["content"]

        embedding = embedding_model.encode(
            content
        ).tolist()

        documents.append(content)

        embeddings.append(embedding)

        metadatas.append(chunk["metadata"])

        unique_id = (
            f"{repo_name}_{index}"
        )

        ids.append(unique_id)

    # Clear old repo embeddings
    existing = collection.get()

    if existing["ids"]:
        collection.delete(
            ids=existing["ids"]
        )

    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )


def search_similar_chunks(
    repo_name,
    query,
    n_results=5
):

    collection = get_collection(repo_name)

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results