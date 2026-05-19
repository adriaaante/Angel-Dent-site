#!/usr/bin/env bash
#
# Download files from a Yandex.Disk public link into assets/docs/.
# Works with single-file links (/i/) and folder links (/d/).
#
# Why a script: this dev sandbox can't reach disk.yandex.ru
# (host allowlist), but GitHub Actions runners can. The companion
# workflow .github/workflows/download-yadisk.yml runs this script
# on a runner and commits the result back.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$ROOT/assets/docs"
mkdir -p "$DEST"

# Public Yandex.Disk link with the clinic license + its appendices.
PUBLIC_KEY="https://disk.yandex.ru/i/m3P70tEREwGhQQ"

API="https://cloud-api.yandex.net/v1/disk/public/resources"
PKEY_ENC=$(python3 -c "from urllib.parse import quote; print(quote('$PUBLIC_KEY', safe=''))")

# Get top-level resource metadata
META=$(curl -sSfL "$API?public_key=$PKEY_ENC&limit=200")
TYPE=$(echo "$META" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('type',''))")
echo "→ Yandex.Disk public resource type: $TYPE"

download_file() {
  local public_path="$1"  # e.g. "" for top-level file, "/subdir/file.pdf" for inside-folder file
  local out_name="$2"
  echo "  ↓ $out_name"
  local dl_url
  if [[ -z "$public_path" ]]; then
    dl_url=$(curl -sSfL "$API/download?public_key=$PKEY_ENC" | python3 -c "import json,sys; print(json.load(sys.stdin)['href'])")
  else
    local pp_enc
    pp_enc=$(python3 -c "from urllib.parse import quote; print(quote('$public_path', safe=''))")
    dl_url=$(curl -sSfL "$API/download?public_key=$PKEY_ENC&path=$pp_enc" | python3 -c "import json,sys; print(json.load(sys.stdin)['href'])")
  fi
  curl -sSfL "$dl_url" -o "$DEST/$out_name"
  echo "    saved → $DEST/$out_name ($(du -h "$DEST/$out_name" | cut -f1))"
}

slugify() {
  python3 -c "
import sys, re, unicodedata
s = sys.argv[1]
# transliterate Russian to ASCII via NFKD
trans = str.maketrans('абвгдеёжзийклмнопрстуфхцчшщъыьэюя АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
                      'abvgdeezhzijklmnoprstufhcchshschyyeyu_ABVGDEEZHZIJKLMNOPRSTUFHCCHSHSCHYYEYU')
s = s.translate(trans)
s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
s = re.sub(r'[^a-zA-Z0-9._-]+', '-', s).strip('-').lower()
print(s or 'file')
" "$1"
}

if [[ "$TYPE" == "file" ]]; then
  # Single file — preserve original name slugified
  ORIG_NAME=$(echo "$META" | python3 -c "import json,sys; print(json.load(sys.stdin)['name'])")
  EXT="${ORIG_NAME##*.}"
  BASE="${ORIG_NAME%.*}"
  SLUG=$(slugify "$BASE")
  download_file "" "license-$SLUG.$EXT"
elif [[ "$TYPE" == "dir" ]]; then
  # Folder — iterate items
  echo "$META" | python3 <<'PY' > /tmp/yadisk-items.txt
import json, sys
data = json.load(open('/dev/stdin'))
items = data.get('_embedded', {}).get('items', [])
for it in items:
    if it.get('type') == 'file':
        print(f"{it['path']}\t{it['name']}")
PY
  while IFS=$'\t' read -r path name; do
    [[ -z "$path" ]] && continue
    # path is like "/folder/file.pdf"; for download API we need the path inside the public link
    # Yandex returns absolute disk path, but the download API expects path relative to the public_key root
    # Strip leading "/" and prefix "/" to make it /folder/file.pdf
    rel_path="${path}"
    EXT="${name##*.}"
    BASE="${name%.*}"
    SLUG=$(slugify "$BASE")
    download_file "$rel_path" "license-$SLUG.$EXT"
  done < /tmp/yadisk-items.txt
else
  echo "Unknown resource type: $TYPE" >&2
  exit 1
fi

echo ""
echo "✓ Done. Files in $DEST:"
ls -la "$DEST"
