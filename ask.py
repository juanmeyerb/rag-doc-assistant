import sys

from answering import answer

source = sys.argv[1]
question = sys.argv[2]
text, hits = answer(question, source)

print(text)
print()
print("Sources:")
for number, hit in enumerate(hits, start=1):
    print(f"[{number}] {hit['source']}, p. {hit['page']} (similarity {hit['similarity']:.3f})")