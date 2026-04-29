#!/bin/bash
echo "📡 V4 Baseline Active. Waiting for clean signal..."
LAST=""
while true; do
    CLIP=$(termux-clipboard-get 2>/dev/null)
    if [[ "$CLIP" != "$LAST" && -n "$CLIP" ]]; then
        echo "--- RAW DATA START ---"
        echo "$CLIP"
        echo "--- RAW DATA END ---"
        LAST="$CLIP"
    fi
    sleep 2
done
