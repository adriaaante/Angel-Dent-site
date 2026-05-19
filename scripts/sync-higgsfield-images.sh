#!/usr/bin/env bash
#
# Download Higgsfield-generated CDN images into assets/img/generated/
# (or assets/img/portfolio/ for before/after pairs) and patch all HTML
# files to use local paths instead of CDN URLs.
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
PORTFOLIO_DEST="$ROOT/assets/img/portfolio"
mkdir -p "$DEST" "$PORTFOLIO_DEST"

# Map of CDN URL → local filename. Edit when you add new generations.
declare -A IMAGES=(
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_194252_9fe5f763-f182-4172-886e-4ea08abdb435.png"]="hero-clinic.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_141253_d2cb86d1-e4f8-4193-998c-8f65003b9127.png"]="og-banner.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_141240_375cc91a-d896-41da-8027-03acee48282e.png"]="clinic-reception.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_141247_03248a5d-86dc-40f6-b424-f445b2497550.png"]="clinic-treatment-room.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_141608_82a01639-c927-4217-9b03-532c6d78a61e.png"]="implant.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_141613_a55d45f6-fd55-4e6c-887c-96055492bed5.png"]="orthodontics.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_141619_91a31d69-c023-43a3-a00c-ab4fb1d8eaf4.png"]="pediatric.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_143240_c61b0fa7-a73e-4a49-8152-a5de7432f764.png"]="caries-treatment.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_143245_60201c42-7daa-49bb-b0dd-9c9420c12045.png"]="surgery.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_143250_e87b0be6-c221-4378-9036-6672d737a04a.png"]="prosthetics.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_143258_a832387a-a99c-4e5b-ab53-be476d556a52.png"]="veneers.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_143304_59c46749-b25e-43ff-913d-27f572ebfe99.png"]="hygiene.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_143310_31c544fb-50ef-4356-9eb4-f0592f0d7950.png"]="periodontology.png"
)

# Portfolio before/after images — downloaded to assets/img/portfolio/
# These are referenced from portfolio.js (not from HTML), so the patching
# step below safely ignores them.
declare -A PORTFOLIO=(
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260519_114447_2aebdc3a-a198-4cbd-8cec-62bba2e19340.png"]="ortho-crowded.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260519_114508_1657467a-4806-49ce-858a-b17907e2006f.png"]="ortho-straight.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260519_114518_9ecd1d0d-eab9-42c9-8484-2df9137f2b0c.png"]="ortho-bite-class2.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260519_114526_7e2b0274-e827-4cb5-9c16-d2082b9580e4.png"]="ortho-bite-corrected.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260519_114535_92e18d0d-53df-43d5-b22d-8896fbe6fde2.png"]="implant-gap.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260519_114546_be371e62-e53b-48f3-9d02-8a6959233f21.png"]="implant-restored.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260519_114555_259b852d-b128-4803-b97c-0cbb9ec78cbd.png"]="implant-noteeth.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260519_114603_29557d9b-8c8e-4554-ae0e-863ef7e0b1da.png"]="implant-arch.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260519_114614_01cde10a-1437-46ed-bcce-7050ed3db320.png"]="veneers-before.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260519_114624_ed547ec5-0da2-459a-9d3e-6df717781d32.png"]="veneers-after.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260519_114634_21465b70-85c2-42b8-8f29-3d5bece84220.png"]="crowns-before.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260519_114643_4c38de80-d7cb-495b-a5bb-75446d5ac04e.png"]="crowns-after.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260519_114651_f3d68a99-adf5-4e90-89a0-a5daa1345602.png"]="restoration-before.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260519_114659_4b58f99e-6f84-450c-a2de-4930e8ca61b3.png"]="restoration-after.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260519_114707_c06cb251-6993-4c03-957e-c49aa76a2946.png"]="caries-cavity.png"
  ["https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260519_114718_2e55b190-9cc8-4bcd-85e5-da3bc22f481e.png"]="caries-restored.png"
)

echo "→ Downloading ${#IMAGES[@]} site images to $DEST"
for url in "${!IMAGES[@]}"; do
  filename="${IMAGES[$url]}"
  out="$DEST/$filename"
  if [[ -f "$out" && -s "$out" ]] || [[ -f "${out%.png}.webp" ]]; then
    echo "  ✓ $filename (already exists)"
    continue
  fi
  echo "  ↓ $filename"
  curl -sSfL "$url" -o "$out"
done

echo ""
echo "→ Downloading ${#PORTFOLIO[@]} portfolio before/after to $PORTFOLIO_DEST"
for url in "${!PORTFOLIO[@]}"; do
  filename="${PORTFOLIO[$url]}"
  out="$PORTFOLIO_DEST/$filename"
  if [[ -f "$out" && -s "$out" ]] || [[ -f "${out%.png}.webp" ]]; then
    echo "  ✓ $filename (already exists)"
    continue
  fi
  echo "  ↓ $filename"
  curl -sSfL "$url" -o "$out"
done

echo ""
echo "→ Optimizing PNG with pngquant (if installed)"
if command -v pngquant >/dev/null 2>&1; then
  for f in "$DEST"/*.png "$PORTFOLIO_DEST"/*.png; do
    [[ -f "$f" ]] || continue
    pngquant --quality 70-90 --strip --skip-if-larger --force --output "$f" "$f" 2>/dev/null || true
  done
  echo "  ✓ optimized"
else
  echo "  (skipped — install pngquant for ~50% smaller files: brew install pngquant)"
fi

echo ""
echo "→ Converting PNG → WebP (lossy q=82) for ~70% size reduction"
if command -v cwebp >/dev/null 2>&1; then
  for f in "$DEST"/*.png "$PORTFOLIO_DEST"/*.png; do
    [[ -f "$f" ]] || continue
    webp="${f%.png}.webp"
    cwebp -q 82 -quiet "$f" -o "$webp" || continue
    rm -f "$f"  # keep only WebP — modern browsers + Yandex/Google support it
  done
  echo "  ✓ converted to WebP and removed source PNGs"
else
  echo "  (skipped — install webp for smaller files: apt-get install webp / brew install webp)"
fi

echo ""
echo "→ Patching HTML to use local /assets/img/generated/ paths"
echo "  (og:image / twitter:image → absolute URL,"
echo "   regular <img> tags → relative path that respects page depth)"
cd "$ROOT"

SITE_URL="https://angel-denta.ru"
# WebP is supported by Yandex.Browser, Chrome, Safari 14+, Firefox 65+,
# Edge — i.e. essentially everyone. We default to .webp; if cwebp wasn't
# available the files keep .png and we fall back automatically.
target_ext=".png"
if [[ -f "$DEST/og-banner.webp" ]]; then target_ext=".webp"; fi

patched=0
for url in "${!IMAGES[@]}"; do
  filename="${IMAGES[$url]%.png}${target_ext}"
  cdn_url_any="${url}"
  cdn_url_webp="${url%.png}${target_ext}"
  abs_url="$SITE_URL/assets/img/generated/$filename"
  esc_url=$(printf '%s' "$cdn_url_any" | sed 's/[\/&|]/\\&/g')

  while IFS= read -r html; do
    # Relative path with ../ for each nested directory level
    rel="assets/img/generated/$filename"
    depth=$(awk -F'/' '{print NF-1}' <<<"${html#./}")
    if [[ "$depth" -gt 0 ]]; then
      for ((i=0; i<depth; i++)); do rel="../$rel"; done
    fi

    if grep -q "$cdn_url_any" "$html"; then
      # Pass 1 — only on og:image / twitter:image lines → absolute URL
      sed -i.bak "/og:image\|twitter:image/s|$esc_url|$abs_url|g" "$html"
      # Pass 2 — remaining occurrences (regular <img> tags) → relative path
      sed -i "s|$esc_url|$rel|g" "$html"
      rm -f "$html.bak"
      patched=$((patched+1))
    fi
  done < <(find . -name '*.html' -not -path './node_modules/*' -not -path './.git/*')
done

echo "  ✓ $patched replacements made"

# If we converted to WebP, rewrite any earlier .png references in HTML
# that the previous sync put there. Idempotent.
if [[ "$target_ext" == ".webp" ]]; then
  echo ""
  echo "→ Replacing residual .png paths inside /assets/img/generated/ with .webp"
  find . -name '*.html' -not -path './node_modules/*' -not -path './.git/*' \
    -exec sed -i 's|\(assets/img/generated/[A-Za-z0-9-]*\)\.png|\1.webp|g' {} \;
  echo "  ✓ done"
fi

# Once images are local, the CloudFront preconnect line is dead weight.
echo ""
echo "→ Removing now-unused CloudFront preconnect lines"
find . -name '*.html' -not -path './node_modules/*' -not -path './.git/*' \
  -exec sed -i '/<link rel="preconnect" href="https:\/\/d8j0ntlcm91z4\.cloudfront\.net"[^>]*>/d' {} \;
echo "  ✓ done"
echo ""
echo "Done. Review changes with: git diff -- '*.html'"
echo "Then commit: git add assets/img/generated/ '*.html' && git commit -m 'images: host Higgsfield assets locally'"
