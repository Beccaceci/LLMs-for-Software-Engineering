#!/usr/bin/env bash
# ==============================================================================
# Render Manim Assets for Politecnico di Torino Study Guide
# Usage:
#   ./scripts/render_manim.sh stills    # Renders high-res 4K PNG stills for LaTeX
#   ./scripts/render_manim.sh video     # Renders MP4 video companions
#   ./scripts/render_manim.sh all       # Renders both stills and videos
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STUDY_GUIDE_DIR="$(dirname "$SCRIPT_DIR")"
MANIM_DIR="$STUDY_GUIDE_DIR/manim"
FIG_DIR="$STUDY_GUIDE_DIR/figures/manim"
ANIM_DIR="$STUDY_GUIDE_DIR/animations"

mkdir -p "$FIG_DIR" "$ANIM_DIR"

MODE="${1:-stills}"

if ! command -v manim &> /dev/null; then
    echo "[!] Manim Community is not installed or not in PATH."
    echo "    Install with: pip install manim"
    exit 1
fi

echo "[*] Rendering Manim assets in mode: $MODE"

for scene_file in "$MANIM_DIR"/scene_*.py; do
    [ -e "$scene_file" ] || continue
    base_name="$(basename "$scene_file" .py)"
    echo "[+] Processing $base_name..."

    if [ "$MODE" = "stills" ] || [ "$MODE" = "all" ]; then
        echo "    -> Rendering high-DPI still frame (-s -qh)..."
        manim -s -qh --media_dir "$STUDY_GUIDE_DIR/.manim_cache" "$scene_file"
        # Find latest rendered image and copy to figures/manim/
        latest_img="$(find "$STUDY_GUIDE_DIR/.manim_cache/images" -type f -name "*.png" -newermt "1 minute ago" | head -n 1 || true)"
        if [ -n "$latest_img" ]; then
            cp "$latest_img" "$FIG_DIR/${base_name}.png"
            echo "    -> Saved to $FIG_DIR/${base_name}.png"
        fi
    fi

    if [ "$MODE" = "video" ] || [ "$MODE" = "all" ]; then
        echo "    -> Rendering MP4 video companion (-qh)..."
        manim -qh --media_dir "$STUDY_GUIDE_DIR/.manim_cache" "$scene_file"
        latest_vid="$(find "$STUDY_GUIDE_DIR/.manim_cache/videos" -type f -name "*.mp4" -newermt "1 minute ago" | head -n 1 || true)"
        if [ -n "$latest_vid" ]; then
            cp "$latest_vid" "$ANIM_DIR/${base_name}.mp4"
            echo "    -> Saved to $ANIM_DIR/${base_name}.mp4"
        fi
    fi
done

echo "[*] Manim asset generation complete."
