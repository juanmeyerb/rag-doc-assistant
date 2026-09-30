from answering import build_prompt, select_relevant
from chunking import clean_text
from language import detect_language


def make_hit(similarity, page=1):
    return {"source": "manual.pdf", "page": page, "similarity": similarity, "text": f"Text of page {page}"}


def test_clean_text_removes_lines_without_letters_or_digits():
    raw = "Connecting\n• • • • • •\n•\n  Plug the adapter in.  \n\n31"
    assert clean_text(raw) == "Connecting\nPlug the adapter in.\n31"


def test_select_relevant_returns_nothing_below_minimum():
    assert select_relevant([make_hit(0.54), make_hit(0.50)]) == []


def test_select_relevant_returns_nothing_without_results():
    assert select_relevant([]) == []


def test_select_relevant_keeps_pages_within_gap():
    hits = [make_hit(0.66, 1), make_hit(0.60, 2), make_hit(0.57, 3), make_hit(0.50, 4)]
    assert [hit["page"] for hit in select_relevant(hits)] == [1, 2, 3]


def test_build_prompt_numbers_sources_and_sets_answer_language():
    prompt = build_prompt("How do I clean the filter?", [make_hit(0.70, 17), make_hit(0.60, 7)])
    assert "[1] manual.pdf, page 17" in prompt
    assert "[2] manual.pdf, page 7" in prompt
    assert prompt.endswith("Answer in English.")


def test_build_prompt_has_no_language_instruction_for_short_question():
    prompt = build_prompt("Akku?", [make_hit(0.70)])
    assert "Answer in" not in prompt


def test_detect_language_recognizes_full_questions():
    assert detect_language("Wie lade ich den Akku auf?", min_letters=10) == "de"
    assert detect_language("How do I connect the router to power?", min_letters=10) == "en"


def test_detect_language_returns_unknown_for_short_text():
    assert detect_language("Akku?", min_letters=10) == "unknown"