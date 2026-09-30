from collections import Counter

from chunking import load_chunks
from indexing import index_chunks
from retrieval import collection


def print_progress(number, total):
    if number % 100 == 0:
        print(f"{number}/{total} done")


chunks = load_chunks()
print("Chunks to embed:", len(chunks))
index_chunks(chunks, print_progress)
print("Stored in database:", collection.count())

all_entries = collection.get(include=["metadatas"])
counts = Counter((entry["source"], entry["language"]) for entry in all_entries["metadatas"])
for (source, language), count in sorted(counts.items()):
    print(source, language, count)