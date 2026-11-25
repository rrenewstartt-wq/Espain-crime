#!/usr/bin/env bash
# Render a HyperFrames project with the settings measured on this 4-core cloud machine
# (engine benchmark 2026-11-25: HyperFrames 25% faster than Remotion on long renders).
#   bash scripts/render.sh <hyperframes-project-dir> <out.mp4> [extra hyperframes render args]
# - headless shell → fast BeginFrame capture (default Chromium falls back to slow screenshots, ~2.5x slower)
# - --workers 4 (auto picks 1 on short clips), --video-bitrate 12M (CRF output is ~2 Mbps → fails the 8 Mbps bar)
# - telemetry off by default
set -euo pipefail
PROJ="$1"; OUT="$2"; shift 2
SHELL_BIN=$(ls -d /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell 2>/dev/null | sort | tail -1)
export PRODUCER_HEADLESS_SHELL_PATH="${PRODUCER_HEADLESS_SHELL_PATH:-$SHELL_BIN}"
export HYPERFRAMES_NO_TELEMETRY="${HYPERFRAMES_NO_TELEMETRY:-1}"
mkdir -p "$(dirname "$OUT")"
cd "$PROJ"
start=$(date +%s)
npx --no-install hyperframes render -o "$(realpath -m "$OLDPWD/$OUT" 2>/dev/null || echo "$OUT")" --workers "${HF_WORKERS:-4}" --video-bitrate "${HF_BITRATE:-12M}" "$@"
echo "렌더 시간: $(( $(date +%s) - start ))초"
