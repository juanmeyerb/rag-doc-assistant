# Experiments

All runs use the questions in `eval_set.py`. Runs up to markdown-clean used 20 questions
(18 answerable, 43 key facts); final-21 added a Spanish question (19 answerable, 46 key facts).
Key facts and errors were scored by hand. An error is a statement that is wrong or not
supported by the manual, including wrong citations. Identical runs differ by about one key
fact, almost always on question 3.

| Run | Change | Key facts | Errors | Retrieval (top 5) |
|---|---|---|---|---|
| baseline | llama3.1:8b, plain PyMuPDF extraction, one chunk per page | 30/43 | 1 | 17/18 |
| baseline-run2 | repeat of baseline | 31/43 | 1 | 17/18 |
| prompt-warnings | prompt rule: include all warnings and conditions | 33/43 | 5 | 17/18 |
| prompt-warnings-run2 | repeat | 34/43 | 4 | 17/18 |
| qwen3-8b | qwen3:8b, thinking off | 32/43 | 2 | 17/18 |
| gemma3-4b | gemma3:4b | 23/43 | 4 | 17/18 |
| markdown | pymupdf4llm Markdown extraction | 30/43 | 1 | 16/18 |
| markdown-clean | Markdown extraction, formatting markup removed | 29/43 | 4 | 16/18 |
| translate-instruction | instruction to translate everything and flag mismatches | stopped | - | - |
| final-21 | final configuration, 21 questions | 30/46 | 2 | 18/19 |

## Notes

prompt-warnings: recovered one of four missing restrictions, but in both runs the model
added an unsupported sentence with a citation to question 6. Reverted.

qwen3-8b and gemma3-4b: qwen3:8b found slightly more facts than llama3.1:8b but made more
errors. gemma3:4b was clearly weaker; one answer repeated the system prompt to the user.
Kept llama3.1:8b and dropped the 8 GB target.

markdown and markdown-clean: fixed the step order on the Dyson filter page (q4) and the
torque table (q13), but page 17 of the Ecovacs manual dropped out of retrieval (q15).
Removing the markup did not bring it back. The exact similarity of page 17, computed
without the index, was 0.561 with plain extraction and 0.461 with Markdown, so the search
itself was correct. The page mixes three unrelated sections. Dropped: no measurable gain
and an extra dependency.

translate-instruction: the Bosch battery answer (q6) invented four statements with
citations and repeated them until the context was full. Reverted; added num_predict=800
as a safeguard against loops.

final-21: errors on q13 (torque value attached to the wrong table row) and q21 (says
the filter must be changed monthly; the manual says washed).

## Final configuration

Plain PyMuPDF extraction, one chunk per page, bge-m3 embeddings, language filter per
manual, one manual at a time, llama3.1:8b, tested on a 16 GB Mac.

## Known limitations

Tables lose their row structure. Some pages extract steps out of order. Pages covering
several topics are harder to retrieve. The model sometimes omits warnings and conditions.
Answers to questions in a language other than the manual's can mix both languages. When
the manual doesn't use the question's term, the model may present the closest procedure
as the answer.