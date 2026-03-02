#!/usr/bin/env python3
"""Deterministic OCR cache CLI for study-assistant."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_RUNTIME_ERROR = 1
EXIT_INVALID_ARGS = 2
EXIT_CACHE_MISS = 3

CACHE_DIR = Path(".study-assistant-cache")
DEFAULT_PAGE_SEL = "all-pages"


class CacheCliError(Exception):
    def __init__(self, message: str, exit_code: int = EXIT_RUNTIME_ERROR) -> None:
        super().__init__(message)
        self.exit_code = exit_code


def to_json(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=True, separators=(",", ":"))


def normalize_pdf_input(pdf_input: str) -> str:
    value = pdf_input.strip() if pdf_input else ""
    if not value:
        raise CacheCliError("Error: --pdf-input is required.", EXIT_INVALID_ARGS)
    return str(Path(os.path.expanduser(value)).resolve())


def normalize_page_sel(page_sel: str | None) -> str:
    value = (page_sel or "").strip()
    return value if value else DEFAULT_PAGE_SEL


def build_key_and_raw_path(pdf_input: str, page_sel: str | None) -> tuple[str, Path]:
    pdf_norm = normalize_pdf_input(pdf_input)
    page_norm = normalize_page_sel(page_sel)
    seed = f"{pdf_norm}\n{page_norm}".encode("utf-8")
    key = hashlib.sha256(seed).hexdigest()[:32]
    raw_path = CACHE_DIR / f"{key}.jsonl"
    return key, raw_path


def cmd_check(args: argparse.Namespace) -> int:
    key, raw_path = build_key_and_raw_path(args.pdf_input, args.page_sel)
    cache_hit = raw_path.exists() and raw_path.stat().st_size > 0
    print(to_json({"cache_hit": cache_hit, "key": key, "raw_path": str(raw_path)}))
    return EXIT_OK if cache_hit else EXIT_CACHE_MISS


def cmd_store(args: argparse.Namespace) -> int:
    key, raw_path = build_key_and_raw_path(args.pdf_input, args.page_sel)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    bytes_written = 0
    with raw_path.open("wb") as handle:
        while True:
            chunk = sys.stdin.buffer.read(65536)
            if not chunk:
                break
            handle.write(chunk)
            bytes_written += len(chunk)

    print(to_json({"key": key, "raw_path": str(raw_path), "bytes_written": bytes_written}))
    return EXIT_OK


def cmd_read(args: argparse.Namespace) -> int:
    key, raw_path = build_key_and_raw_path(args.pdf_input, args.page_sel)
    if not raw_path.exists():
        raise CacheCliError(f"Error: raw cache file not found: {raw_path}", EXIT_CACHE_MISS)

    ok_pages: list[dict[str, object]] = []
    error_pages: list[dict[str, object]] = []
    ok_text_parts: list[str] = []

    with raw_path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                error_pages.append({"line": line_no, "page": None, "error": f"invalid_json: {exc.msg}"})
                continue

            status = obj.get("status")
            page = obj.get("page")
            if status == "ok":
                text = obj.get("text")
                if isinstance(text, str) and text:
                    ok_pages.append({"page": page, "text": text})
                    ok_text_parts.append(text)
                else:
                    error_pages.append({"line": line_no, "page": page, "error": "ok_status_without_text"})
            elif status == "error":
                error_pages.append({"line": line_no, "page": page, "error": obj.get("error", "unknown_error")})

    print(
        to_json(
            {
                "key": key,
                "raw_path": str(raw_path),
                "ok_pages": ok_pages,
                "error_pages": error_pages,
                "ok_text_concat": "\n\n".join(ok_text_parts),
            }
        )
    )
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scripts/ocr_cache.py",
        description="Minimal deterministic cache CLI for study-assistant OCR reuse.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Commands:\n"
            "  check        Return hit/miss for one PDF + page selection\n"
            "  store        Read OCR JSONL from stdin and write cache file\n"
            "  read         Parse cached JSONL into ok/error payloads\n\n"
            "Exit codes:\n"
            f"  {EXIT_OK}=success, {EXIT_RUNTIME_ERROR}=runtime error, "
            f"{EXIT_INVALID_ARGS}=invalid arguments, {EXIT_CACHE_MISS}=cache miss"
        ),
    )

    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    for name, fn, help_text in (
        ("check", cmd_check, "Check cache for one PDF/page selection."),
        ("store", cmd_store, "Store OCR JSONL from stdin into cache."),
        ("read", cmd_read, "Read one cached JSONL entry."),
    ):
        sub = subparsers.add_parser(name, help=help_text)
        sub.add_argument("--pdf-input", required=True, help="Path to PDF.")
        sub.add_argument("--page-sel", default=DEFAULT_PAGE_SEL, help=f'Page selection (default: "{DEFAULT_PAGE_SEL}").')
        sub.set_defaults(func=fn)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except CacheCliError as exc:
        print(str(exc), file=sys.stderr)
        return exc.exit_code
    except BrokenPipeError:
        return EXIT_OK
    except Exception as exc:  # pragma: no cover
        print(f"Error: unexpected failure: {exc}", file=sys.stderr)
        return EXIT_RUNTIME_ERROR


if __name__ == "__main__":
    sys.exit(main())
