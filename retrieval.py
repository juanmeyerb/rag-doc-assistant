import chromadb
import ollama

from language import detect_language

client = chromadb.PersistentClient(path="chroma_db")
COLLECTION_NAME = "manuals"
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    configuration={"hnsw": {"space": "cosine"}},
)


def list_manuals():
    all_metadatas = collection.get(include=["metadatas"])["metadatas"]
    return sorted({entry["source"] for entry in all_metadatas})


def build_filter(question_language, source):
    source_condition = {"source": source}
    if question_language == "unknown":
        return source_condition
    manual_pages = collection.get(where=source_condition, include=["metadatas"])["metadatas"]
    manual_languages = {entry["language"] for entry in manual_pages}
    if question_language not in manual_languages:
        return source_condition
    language_condition = {"$or": [{"language": question_language}, {"language": "unknown"}]}
    return {"$and": [source_condition, language_condition]}


def search(question, source, n_results=5):
    question_language = detect_language(question, min_letters=10)
    where = build_filter(question_language, source)
    question_vector = ollama.embed(model="bge-m3", input=question)["embeddings"][0]
    results = collection.query(query_embeddings=[question_vector], n_results=n_results, where=where)

    hits = []
    for chunk_id, distance, metadata, text in zip(
        results["ids"][0], results["distances"][0], results["metadatas"][0], results["documents"][0]
    ):
        hits.append({
            "id": chunk_id,
            "source": metadata["source"],
            "page": metadata["page"],
            "language": metadata["language"],
            "similarity": 1 - distance,
            "text": text,
        })
    return hits