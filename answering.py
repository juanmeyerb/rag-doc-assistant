import ollama

from retrieval import search
from language import detect_language_name

MIN_SIMILARITY = 0.55
MAX_GAP = 0.10
CHAT_MODEL = "llama3.1:8b"

SYSTEM_PROMPT = """You answer questions about product manuals using only the numbered sources provided.

Rules:
- Use only information from the sources. Do not add knowledge of your own.
- After each statement, cite the source number in square brackets, for example [1] or [2][3].
- The sources may be in different languages. Always answer in the language of the question.
- If the sources do not contain the answer, say that the manuals do not cover this question."""


def select_relevant(hits):
    if not hits or hits[0]["similarity"] < MIN_SIMILARITY:
        return []
    best = hits[0]["similarity"]
    return [hit for hit in hits if hit["similarity"] >= best - MAX_GAP]


def build_prompt(question, hits):
    blocks = []
    for number, hit in enumerate(hits, start=1):
        blocks.append(f"[{number}] {hit['source']}, page {hit['page']}\n{hit['text']}")
    sources = "\n\n".join(blocks)
    language_name = detect_language_name(question, min_letters=10)
    instruction = f"\n\nAnswer in {language_name}." if language_name else ""
    return f"Sources:\n\n{sources}\n\nQuestion: {question}{instruction}"


def answer(question, source, model=CHAT_MODEL):
    hits = select_relevant(search(question, source))
    if not hits:
        return "The manuals don't seem to cover this question.", []
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_prompt(question, hits)},
        ],
        options={"temperature": 0, "num_ctx": 8192, "num_predict": 800},
    )
    return response["message"]["content"], hits