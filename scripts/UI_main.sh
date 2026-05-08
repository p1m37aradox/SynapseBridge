#!/bin/bash
# 🌉 SYNAPSE BRIDGE v0.1.5-beta - MASTER CONTROL
SESSION="Synapse"

tmux kill-session -t $SESSION 2>/dev/null
echo "🚀 Launching Synapse v0.1.5-beta Gemini Stack..."

# 1. MCP
tmux new-session -d -s $SESSION -n 'MCP'
tmux send-keys -t $SESSION:0 "sb-deb" C-m
sleep 2
tmux send-keys -t $SESSION:0 "sb-init" C-m 
sleep 1
tmux send-keys -t $SESSION:0 "sb-venv-activate" C-m
sleep 1
tmux send-keys -t $SESSION:0 "sb-mcp" C-m

# 2. WEB
tmux new-window -t $SESSION -n 'WEB'
tmux send-keys -t $SESSION:1 "sb-deb" C-m
sleep 2
tmux send-keys -t $SESSION:1 "sb-init" C-m
sleep 1
tmux send-keys -t $SESSION:1 "ssh -p 443 -R0:localhost:8080 qr@a.pinggy.io" C-m

# 3. VENV
tmux new-window -t $SESSION -n 'VENV'
tmux send-keys -t $SESSION:2 "sb-deb" C-m
sleep 2
tmux send-keys -t $SESSION:2 "sb-init" C-m
sleep 1
tmux send-keys -t $SESSION:2 "sb-venv-activate" C-m

# 4. DEB
tmux new-window -t $SESSION -n 'DEB'
tmux send-keys -t $SESSION:3 "sb-deb" C-m
sleep 2
tmux send-keys -t $SESSION:3 "sb-init" C-m
sleep 1
tmux send-keys -t $SESSION:3 "cd-bridge" C-m

# 5. HOST
tmux new-window -t $SESSION -n 'HOST'
tmux send-keys -t $SESSION:4 "sb-init" C-m
sleep 1
tmux send-keys -t $SESSION:4 "cd ~" C-m

# 6. GEM
tmux new-window -t $SESSION -n 'GEM'
tmux send-keys -t $SESSION:5 "sb-init" C-m
sleep 1
tmux send-keys -t $SESSION:5 "gemini" C-m

# 7. EXIT
tmux new-window -t $SESSION -n 'EXIT'
EXIT_UI="clear; echo '🌉 EXIT PORTAL'; echo ' [ PRESS ENTER TO SHUT DOWN ]'; read; tmux kill-session -t $SESSION"
tmux send-keys -t $SESSION:6 "$EXIT_UI" C-m

tmux select-window -t $SESSION:1
tmux attach-session -t $SESSION
