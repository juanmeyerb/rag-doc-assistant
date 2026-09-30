import sys

from retrieval import search

source = sys.argv[1]
question = sys.argv[2]
for hit in search(question, source):
    print()
    print(f"=== {hit['id']} | {hit['language']} | similarity {hit['similarity']:.3f}")
    print(hit["text"][:300])