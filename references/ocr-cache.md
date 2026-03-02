# OCR Cache Procedure

Use this procedure for any mode that starts from a PDF.

All cache functions must go through `python3 scripts/ocr_cache.py`.

## 1. Validate Input and Normalize Page Selection

```bash
PDF_INPUT="path/to/file.pdf"
PAGE_SELECTION=""
```

## 2. Check Cache

```bash
python3 scripts/ocr_cache.py check \
  --pdf-input "$PDF_INPUT" \
  --page-sel "$PAGE_SELECTION"
```

Interpretation:
- `0`: cache hit, skip OCR and use `read`
- `3`: cache miss, continue to step 3
- `1` or `2`: runtime/argument error, stop and report

## 3. Populate Cache on Miss (Pipe to `store`)

`store` reads OCR JSONL from stdin, validates all-or-nothing, writes cache via internal temp file + atomic replace.

Use one OCR command argument:
- `--all-pages` when `PAGE_SELECTION` is empty
- `--pages:"$PAGE_SELECTION"` when a range is provided

```bash
pdfocr "$PDF_INPUT" <OCR_PAGE_ARG> | python3 scripts/ocr_cache.py store \
  --pdf-input "$PDF_INPUT" \
  --page-sel "$PAGE_SELECTION"
```

Interpretation:
- `0`: OCR output was all-ok and cached
- `3`: OCR output is non-cacheable (page/parse errors or empty)
- `1` or `2`: runtime/argument error, stop and report

## 4. Reuse Across Modes

```bash
python3 scripts/ocr_cache.py read \
  --pdf-input "$PDF_INPUT" \
  --page-sel "$PAGE_SELECTION"
```

Use the JSON response field:
- `ok_text_concat`: merged text from all cached `status:"ok"` records

Do not rerun OCR unless `check` returns miss (`3`).
Partial OCR runs are not cached.

## 5. Cache Layout

- Raw JSONL entries: `.study-assistant-cache/<key>.jsonl`

The key is derived from normalized `pdf_input + page_sel`.
