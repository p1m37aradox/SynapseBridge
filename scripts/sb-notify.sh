#!/bin/bash
START_KEY="SB_NOTIFY_START"
END_KEY="SB_NOTIFY_END"

echo "🛡️ Synapse Bridge: NOTIFY LISTENER (DUAL OUTPUT)"
while true; do
  MATCH=$(termux-notification-list | jq -rc ".[] | select(.content != null and (.content | contains(\"$START_KEY\")))" | head -n 1)
  
  if [ -n "$MATCH" ] && [ "$MATCH" != "null" ]; then
    ID=$(echo "$MATCH" | jq -r ".id")
    TAG=$(echo "$MATCH" | jq -r ".tag")
    CONTENT=$(echo "$MATCH" | jq -r ".content")
    CMD=$(echo "$CONTENT" | sed "s/.*$START_KEY//;s/$END_KEY.*//")
    
    if [ -n "$CMD" ]; then
      echo "📥 [$(date +%T)] Executing: $CMD"
      
      # 1. Execute and show output in terminal immediately
      # 2. Capture that output into a variable
      OUTPUT=$(eval "$CMD" 2>&1 | tee /dev/tty)
      
      # 3. Silently try to push to clipboard if tool is available
      if [ -n "$OUTPUT" ]; then
         echo "$OUTPUT" | termux-clipboard-set 2>/dev/null
         echo "📤 [$(date +%T)] Sync attempted."
      fi
      
      termux-notification-remove "$TAG" 2>/dev/null
      termux-notification-remove "$ID" 2>/dev/null
    fi
  fi
  sleep 5
done
