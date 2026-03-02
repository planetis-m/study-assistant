# pdfocr Install Fallback

Use this only when `command -v pdfocr` fails.

As of February 28, 2026 (`pdfocr` v0.2.6), release assets exist for:
- Linux `x86_64`
- macOS `arm64`
- Windows `x86_64`

Release page:
- `https://github.com/planetis-m/pdfocr/releases/latest`

## Linux x86_64

```bash
set -euo pipefail
mkdir -p "$HOME/.local/opt/pdfocr" "$HOME/.local/bin"
tmp_dir="$(mktemp -d)"
curl -fsSL -o "$tmp_dir/pdfocr.tar.gz" \
  "https://github.com/planetis-m/pdfocr/releases/latest/download/pdfocr-linux-x86_64.tar.gz"
tar -xzf "$tmp_dir/pdfocr.tar.gz" -C "$HOME/.local/opt/pdfocr"
pdfocr_bin="$(find "$HOME/.local/opt/pdfocr" -type f -name pdfocr | head -n1)"
install -m 0755 "$pdfocr_bin" "$HOME/.local/bin/pdfocr"
export PATH="$HOME/.local/bin:$PATH"
pdfocr --help >/dev/null
```

## macOS arm64

```bash
set -euo pipefail
mkdir -p "$HOME/.local/opt/pdfocr" "$HOME/.local/bin"
tmp_dir="$(mktemp -d)"
curl -fsSL -o "$tmp_dir/pdfocr.tar.gz" \
  "https://github.com/planetis-m/pdfocr/releases/latest/download/pdfocr-macos-arm64.tar.gz"
tar -xzf "$tmp_dir/pdfocr.tar.gz" -C "$HOME/.local/opt/pdfocr"
pdfocr_bin="$(find "$HOME/.local/opt/pdfocr" -type f -name pdfocr | head -n1)"
install -m 0755 "$pdfocr_bin" "$HOME/.local/bin/pdfocr"
export PATH="$HOME/.local/bin:$PATH"
pdfocr --help >/dev/null
```

## Windows x86_64 (PowerShell)

```powershell
$ErrorActionPreference = "Stop"
$dst = "$HOME\.local\opt\pdfocr"
$bin = "$HOME\.local\bin"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
New-Item -ItemType Directory -Force -Path $bin | Out-Null
$zip = Join-Path $env:TEMP "pdfocr.zip"
Invoke-WebRequest -Uri "https://github.com/planetis-m/pdfocr/releases/latest/download/pdfocr-windows-x86_64.zip" -OutFile $zip
Expand-Archive -Path $zip -DestinationPath $dst -Force
$exe = Get-ChildItem -Path $dst -Recurse -Filter "pdfocr.exe" | Select-Object -First 1
Copy-Item $exe.FullName (Join-Path $bin "pdfocr.exe") -Force
$env:Path = "$bin;$env:Path"
pdfocr --help | Out-Null
```

## Notes

- Keep the extracted runtime files (including `libpdfium`) alongside the installed binary tree.
- If install fails due to permissions, retry in a user-writable location as shown above.
- If platform/architecture is unsupported, stop and ask the user for manual installation steps.
