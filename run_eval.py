import sys

from answering import CHAT_MODEL, answer
from eval_set import EVAL_SET
from retrieval import COLLECTION_NAME, search

answerable = 0
found_count = 0
passed_count = 0
no_answer_total = 0
no_answer_correct = 0

model = sys.argv[1] if len(sys.argv) > 1 else CHAT_MODEL
print("Model:", model, "| Collection:", COLLECTION_NAME)

for number, item in enumerate(EVAL_SET, start=1):
    manual = item["manual"]
    question = item["question"]
    expected = set(item["expected_pages"])

    found_ids = [hit["id"] for hit in search(question, manual)]
    text, used_hits = answer(question, manual, model)
    used_ids = [hit["id"] for hit in used_hits]

    print(f"\n=== {number}. {manual} | {question}")
    if expected:
        answerable += 1
        found = bool(expected & set(found_ids))
        passed = bool(expected & set(used_ids))
        found_count += found
        passed_count += passed
        print("Expected:", sorted(expected))
        print("In top 5:", "yes" if found else "NO", found_ids)
        print("Passed to model:", "yes" if passed else "NO", used_ids)
    else:
        no_answer_total += 1
        stopped = not used_ids
        no_answer_correct += stopped
        print("Expected: no answer")
        print("Stopped before the model:", "yes" if stopped else "NO", used_ids)

    print("Answer:", text)
    print("Check these key facts:", item["key_facts"])

print("\n=== Summary")
print(f"Expected page in top 5: {found_count}/{answerable}")
print(f"Expected page passed to model: {passed_count}/{answerable}")
print(f"No-answer questions stopped before the model: {no_answer_correct}/{no_answer_total}")