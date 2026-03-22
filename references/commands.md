# Mode Rules

Apply the rules in the selected section exactly.

## transcribe

Goal: Convert provided study material into structured markdown while preserving educational text verbatim.

Rules:
- Reproduce educational content word-for-word.
- Do not summarize, paraphrase, simplify, reorder, or shorten.
- Preserve headings, bullets, numbering, and visible structure where they can be recovered reliably.
- Keep the markdown aligned with the source organization.
- Remove only metadata noise: instructor details, headers, footers, page numbers, timestamps, and course codes.
- If a fragment is too broken to recover confidently, omit it rather than guess.

## lecture

Goal: Transform content into an engaging professor-style lecture narrative.

Rules:
- Use authoritative academic tone, but do not roleplay or address students directly.
- Present material directly; avoid source-referential phrasing such as "the lecture", "the slides", "the notes", or "the material".
- State the idea itself rather than saying that the source states it.
- Connect fragmented points into a coherent explanatory flow with smooth transitions.
- Prefer developed paragraphs over bullet-heavy output unless bullets are clearly the best format.
- Preserve technical depth and explain difficult concepts or distinctions clearly.
- Keep the narrative cumulative so each section builds on what came before.
- Include:
  - Topic framing
  - Connected narrative across ideas
  - Deep dive on hardest concepts or contrasts
  - Final synthesis of the big picture

## eli5

Goal: Explain the material in simple, direct language.

Rules:
- Assume the reader is new to the topic.
- Start with the main point in 1-2 short sentences.
- Explain one idea at a time in a clear step-by-step order.
- Define technical terms in plain words on first use.
- Use short examples, not analogies or metaphors.
- Examples may be invented, but only to show an idea already present in the material.
- Do not use "imagine", comparisons, metaphors, or story-like framing.
- Keep the explanation accurate and grounded in the provided material.
- Include:
  - what it is
  - how it works
  - key terms
  - concrete examples
  - why it matters

## flashcard

Goal: Generate concise, exam-ready flashcards.

Rules:
- Include only high-value terms, definitions, formulas, distinctions, and core concepts.
- Make each front a single clear prompt.
- Make each back short, direct, and sufficient for revision.
- Avoid duplicate or heavily overlapping cards.
- Output only a two-column markdown table with these exact headers:
  - `Front (Term/Question)`
  - `Back (Definition/Answer)`

## mindmap

Goal: Produce a hierarchical concept map.

Rules:
- Output only a ` ```mermaid ` code block with no extra text.
- The first line inside the block must be exactly `mindmap`.
- Represent hierarchy through indentation only.
- Do not use bullets, node IDs, connectors, or shape syntax.
- Keep labels short and readable. Use letters, numbers, and spaces only.
- Do not use parentheses, brackets, braces, quotes, punctuation, or colons in labels.

## quiz

Goal: Create practice questions that test understanding and application.

Rules:
- Produce 5-10 questions covering the main concepts.
- Mix multiple-choice questions with exactly 4 options and short-answer questions.
- Prioritize explanation, comparison, and application over recall-only questions.
- Keep questions clear, unambiguous, and answerable from the provided material.
- End with an `Answer Key` section that gives the correct answer for every question.

## essay

Goal: Create exam-style essay practice.

Rules:
- Produce 3-4 essay questions.
- Make each question suitable for a response of about 200 words.
- Include at least one conceptual or theoretical question and at least one applied or integrative question.
- Use strong academic verbs such as `Discuss`, `Evaluate`, `Compare and contrast`, and `Explain`.
- Provide a sample answer of roughly 200 words for each question.
- Keep both questions and sample answers grounded strictly in the provided material.

## study-notes

Goal: Produce exam-focused study notes from provided content.

Rules:
- Organize the notes by major topic using clear markdown headers.
- For each topic include:
  - a clear explanation of the concept
  - the essential facts, definitions, or formulas most relevant for exams
  - links to related concepts, contrasts, or dependencies
- Prioritize understanding, relationships, and exam relevance over rote listing.
- Keep the flow logical and progressive so later sections build on earlier ones.
