# Study Skill

`study-skill` is an installable Agent Skill for exam prep from lecture slides.

It provides one workflow with multiple modes:
- `transcribe`
- `analyze`
- `lecture`
- `eli5`
- `flashcard`
- `mindmap`
- `quiz`
- `essay`
- `study-notes`

The skill is optimized for PDF slides via the `pdfocr` CLI.

## Requirements

- `pdfocr` must be installed and available on `PATH`
- PDF OCR API credentials must be configured for your `pdfocr` setup

## Install In Codex

Codex docs recommend installing non-built-in skills with `$skill-installer`.

In Codex, prompt:

```text
$skill-installer install the skill from https://github.com/planetis-m/study-skill
```

Then restart Codex if the skill does not appear immediately.

## Manual Install (Agent Skills Layout)

Clone this repo and place it in a scanned skills path, for example:

```bash
git clone https://github.com/planetis-m/study-skill.git ~/.agents/skills/study-skill
```

Codex scans skill locations such as:
- `REPO`: `.agents/skills` (from current directory up to repo root)
- `USER`: `~/.agents/skills`

## Usage Examples

Use explicit invocation with `$study-skill` in your prompt.

```text
Use $study-skill in transcribe mode for lecture1.pdf and keep text verbatim.
```

```text
Use $study-skill in study-notes mode for lecture1.pdf.
```

```text
Use $study-skill in quiz mode on this transcribed content: ...
```

## Skill Files

- `SKILL.md`: main instructions and trigger metadata
- `references/commands.md`: mode-specific generation rules
- `agents/openai.yaml`: UI metadata and default prompt
