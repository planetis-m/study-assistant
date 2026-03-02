# OCR Cache Procedure

Use this procedure for any mode that starts from a PDF.

## 1. Build Cache Key

POSIX shell:

```bash
pdf_abs="$(realpath "$PDF_INPUT")"
pdf_size="$(stat -c %s "$pdf_abs" 2>/dev/null || stat -f %z "$pdf_abs")"
pdf_mtime="$(stat -c %Y "$pdf_abs" 2>/dev/null || stat -f %m "$pdf_abs")"
page_sel="${PAGE_SELECTION:-all-pages}"
cache_key="$(printf '%s|%s|%s|%s\n' "$pdf_abs" "$page_sel" "$pdf_size" "$pdf_mtime" | sha256sum | awk '{print $1}')"
cache_dir=".study-assistant-cache"
mkdir -p "$cache_dir"
cache_raw="$cache_dir/$cache_key.raw.jsonl"
cache_meta="$cache_dir/$cache_key.meta"
```

## 2. Check Cache

```bash
if [ -s "$cache_raw" ]; then
  echo "OCR cache hit: $cache_raw"
fi
```

If `cache_raw` exists and is non-empty, skip `pdfocr`.

## 3. Populate Cache on Miss

Before running `pdfocr`, request user approval for unrestricted network execution.

Run OCR:

```bash
# all pages
pdfocr "$pdf_abs" --all-pages > "$cache_raw"
# or selected pages
pdfocr "$pdf_abs" --pages:"$page_sel" > "$cache_raw"
```

Write `cache_meta` with key inputs and command used.

## 4. Reuse Across Modes

When user asks another mode for the same PDF/pages in the same session:
- recompute key
- load `cache_raw`
- read JSONL lines directly:
  - use `status:"ok"` lines as content source (`text` field)
  - report `status:"error"` lines with page/error info
- do not rerun OCR unless cache miss

## 5. Invalidation

Treat as miss when any of these change:
- file path
- page selection
- file size
- file mtime
