---
name: study-skill
description: Study assistant workflow for lecture-slide exam prep using the `pdfocr` CLI. Use when a task involves reading PDF slides, transcribing slide text, cleaning OCR output, and generating exam-focused deliverables such as study notes, lecture-style explanations, ELI5 explanations, flashcards, Mermaid mind maps, quizzes, essay questions, or one-step PDF-to-notes output.
---

# Study Assistant

Follow this workflow exactly to convert lecture material into exam-ready outputs.

## Select Mode

Map the user request to one mode:

- `transcribe`: Convert PDF slides into markdown while keeping educational text verbatim.
- `analyze`: Generate structured study notes from provided text.
- `lecture`: Turn provided content into cohesive professor-style teaching narrative.
- `eli5`: Explain provided material in plain English while keeping technical depth.
- `flashcard`: Generate two-column markdown flashcards.
- `mindmap`: Generate Mermaid mindmap only.
- `quiz`: Generate mixed quiz and answer key.
- `essay`: Generate 3-4 essay prompts and sample answers.
- `study-notes`: End-to-end pipeline (OCR from PDF, then generate notes in one pass).

## Process PDF Input

If the source is a PDF, always run `pdfocr` through shell execution.

- Never read PDFs with direct file readers or ad-hoc parsers.
- Use full document extraction:
  - `pdfocr INPUT.pdf --all-pages`
- If page ranges are provided, pass them to `pdfocr`:
  - `pdfocr INPUT.pdf --pages:"8-20,22-27"`
- Parse stdout as JSONL:
  - Treat each line as one JSON object.
  - Keep `"text"` only for records with `"status":"ok"`.
  - Report pages with `"status":"error"` but continue with successful pages.

## Clean OCR Text

Before generation, remove only clear metadata:

- Instructor details
- Headers and footers
- Page numbers
- Timestamps
- Course codes

Preserve educational content (concepts, definitions, examples). If text is severely fragmented, skip that fragment instead of guessing.

## Generate Output

Read and apply mode-specific rules from [references/commands.md](references/commands.md). Use the section matching the selected mode.

Global rules across all modes:

- Base all factual content only on user-provided material and extracted OCR text.
- Do not add outside facts, theories, examples, or claims.
- Use markdown output.
- Use LaTeX with `$...$` (inline) and `$$...$$` (display) for math.
- Do not include conversational intros or conclusions.

For `study-notes`, do OCR and notes generation in one workflow and do not recursively call other mode names.
