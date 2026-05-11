#!/bin/bash
CLIP_START="##SB_START##"
CLIP_END="##SB_END##"
NOTIFY_START="SB_NOTIFY_START"
NOTIFY_END="SB_NOTIFY_END"

echo "📋 Synapse Bridge: CLIPBOARD MONITOR ACTIVE"
LAST_CLIP=$(termux-clipboard-get)
while true; do
  CURRENT_CLIP=$(termux-clipboard-get)
  if [[ "$CURRENT_CLIP" != "$LAST_CLIP" ]] && [[ "$CURRENT_CLIP" == *"$CLIP_START"* ]]; then
    RAW_CMD=$(echo "$CURRENT_CLIP" | sed "s/.*$CLIP_START//;s/$CLIP_END.*//")
    if [ -n "$RAW_CMD" ]; then
      termux-notification --id 999 -t "Bridge" -c "$NOTIFY_START$RAW_CMD$NOTIFY_END" --priority high
      termux-clipboard-set ""
      echo "🚀 [$(date +%T)] Dispatched & Scrubbed: $RAW_CMD"
      LAST_CLIP=""
    fi
  else
    LAST_CLIP="$CURRENT_CLIP"
  fi
  sleep 5
done
