import ollama

from language import detect_language
from retrieval import collection


def index_chunks(chunks, progress_callback=None):
    for number, chunk in enumerate(chunks, start=1):
        chunk_id = f"{chunk['source']}:{chunk['page']}"
        vector = ollama.embed(model="bge-m3", input=chunk["text"])["embeddings"][0]
        language = detect_language(chunk["text"], min_letters=100)
        collection.upsert(
            ids=[chunk_id],
            embeddings=[vector],
            documents=[chunk["text"]],
            metadatas=[{"source": chunk["source"], "page": chunk["page"], "language": language}],
        )
        if progress_callback:
            progress_callback(number, len(chunks))