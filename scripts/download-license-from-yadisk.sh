#!/usr/bin/env bash
# Download a Yandex.Disk public file or folder into assets/docs/.
# Runs on GitHub Actions (the dev sandbox can't reach disk.yandex.ru).
set -euo pipefail

PUBLIC_KEY="https://disk.yandex.ru/i/m3P70tEREwGhQQ"
DEST="assets/docs"
mkdir -p "$DEST"

API="https://cloud-api.yandex.net/v1/disk/public/resources"
ENC=$(python3 -c "from urllib.parse import quote; import sys; print(quote(sys.argv[1], safe=''))" "$PUBLIC_KEY")

echo "→ Resource metadata"
curl -sSfL "$API?public_key=$ENC&limit=200" > /tmp/meta.json
TYPE=$(python3 -c "import json; print(json.load(open('/tmp/meta.json'))['type'])")
echo "  type = $TYPE"

if [ "$TYPE" = "file" ]; then
  NAME=$(python3 -c "import json; print(json.load(open('/tmp/meta.json'))['name'])")
  echo "→ Single file: $NAME"
  HREF=$(curl -sSfL "$API/download?public_key=$ENC" | python3 -c "import json, sys; print(json.load(sys.stdin)['href'])")
  curl -sSfL "$HREF" -o "$DEST/license.pdf"
elif [ "$TYPE" = "dir" ]; then
  python3 -c "
import json
items = json.load(open('/tmp/meta.json')).get('_embedded', {}).get('items', [])
for it in items:
    if it.get('type') == 'file':
        print(it['path'])" > /tmp/paths.txt
  i=1
  while read -r path; do
    [ -z "$path" ] && continue
    PATH_ENC=$(python3 -c "from urllib.parse import quote; import sys; print(quote(sys.argv[1], safe=''))" "$path")
    HREF=$(curl -sSfL "$API/download?public_key=$ENC&path=$PATH_ENC" | python3 -c "import json, sys; print(json.load(sys.stdin)['href'])")
    EXT="${path##*.}"
    OUT="$DEST/license-$i.$EXT"
    echo "  ↓ [$i] $path → $OUT"
    curl -sSfL "$HREF" -o "$OUT"
    i=$((i+1))
  done < /tmp/paths.txt
else
  echo "Unknown type: $TYPE"; exit 1
fi

echo ""
echo "→ Result:"
ls -la "$DEST"
