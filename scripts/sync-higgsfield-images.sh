#!/usr/bin/env bash
#
# Download Higgsfield-generated CDN images into assets/img/generated/
# and patch all HTML files to use local paths instead of CDN URLs.
#
# Why: CDN URLs work fine for visitors, but hosting images on the same
# origin gives faster loads, full control, and survives any change to
# Higgsfield's storage layout. Run this once locally after generation,
# then commit assets/img/generated/ and the patched HTML.
#
# Usage:   bash scripts/sync-higgsfield-images.sh
# Idempotent — safe to re-run.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$ROOT/assets/img/generated"
mkdir -p "$DEST"

# Map of CDN URL → local filename. Edit when you add new generations.
declare -A IMAGES=(
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_141253_d2cb86d1-e4f8-4193-998c-8f65003b9127.png"]="og-banner.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_141240_375cc91a-d896-41da-8027-03acee48282e.png"]="clinic-reception.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_141247_03248a5d-86dc-40f6-b424-f445b2497550.png"]="clinic-treatment-room.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_141608_82a01639-c927-4217-9b03-532c6d78a61e.png"]="implant.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_141613_a55d45f6-fd55-4e6c-887c-96055492bed5.png"]="orthodontics.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_141619_91a31d69-c023-43a3-a00c-ab4fb1d8eaf4.png"]="pediatric.png"
)

echo "→ Downloading ${#IMAGES[@]} images to $DEST"
for url in "${!IMAGES[@]}"; do
  filename="${IMAGES[$url]}"
  out="$DEST/$filename"
  if [[ -f "$out" && -s "$out" ]]; then
    echo "  ✓ $filename (already exists)"
    continue
  fi
  echo "  ↓ $filename"
  curl -sSfL "$url" -o "$out"
done

echo ""
echo "→ Optimizing PNG with pngquant (if installed)"
if command -v pngquant >/dev/null 2>&1; then
  for f in "$DEST"/*.png; do
    pngquant --quality 70-90 --strip --skip-if-larger --force --output "$f" "$f" 2>/dev/null || true
  done
  echo "  ✓ optimized"
else
  echo "  (skipped — install pngquant for ~50% smaller files: brew install pngquant)"
fi

echo ""
echo "→ Patching HTML to use local /assets/img/generated/ paths"
cd "$ROOT"
patched=0
for url in "${!IMAGES[@]}"; do
  filename="${IMAGES[$url]}"
  esc_url=$(printf '%s' "$url" | sed 's/[\/&]/\\&/g')
  # Replace absolute CDN URLs. We use a relative path that works from both
  # root pages (index.html) and nested pages (services/*, doctors/*, blog/*)
  # by inserting an extra prefix per file depth below.
  while IFS= read -r html; do
    rel="assets/img/generated/$filename"
    # Calculate depth (sub-dirs from root)
    depth=$(awk -F'/' '{print NF-1}' <<<"${html#./}")
    if [[ "$depth" -gt 0 ]]; then
      for ((i=0; i<depth; i++)); do rel="../$rel"; done
    fi
    if grep -q "$url" "$html"; then
      sed -i.bak "s|$esc_url|$rel|g" "$html" && rm -f "$html.bak"
      patched=$((patched+1))
    fi
  done < <(find . -name '*.html' -not -path './node_modules/*' -not -path './.git/*')
done

echo "  ✓ $patched replacements made"
echo ""
echo "Done. Review changes with: git diff -- '*.html'"
echo "Then commit: git add assets/img/generated/ '*.html' && git commit -m 'images: host Higgsfield assets locally'"
