#!/bin/bash
# 🌉 SYNAPSE BRIDGE v0.0.6.2b-beta - MASTER CONTROL
SESSION="Synapse"

tmux kill-session -t $SESSION 2>/dev/null
echo "🚀 Launching Synapse v0.1.5-beta Qwen+MemPalace Stack..."

# 1. MCP
tmux new-session -d -s $SESSION -n 'MCP'
tmux send-keys -t $SESSION:0 "sb-deb" C-m
sleep 2
tmux send-keys -t $SESSION:0 "sb-init" C-m 
sleep 1
tmux send-keys -t $SESSION:0 "sb-venv-activate" C-m
sleep 1
tmux send-keys -t $SESSION:0 "sb-mcp" C-m

# 2. QWEN
tmux new-window -t $SESSION -n 'QWEN'
tmux send-keys -t $SESSION:1 "sb-deb" C-m
sleep 2
tmux send-keys -t $SESSION:1 "sb-init" C-m
sleep 1
tmux send-keys -t $SESSION:1 "sb-venv-activate" C-m
sleep 1
tmux send-keys -t $SESSION:1 "sb-chat" C-m
sleep 1

# 3. VENV
tmux new-window -t $SESSION -n 'VENV'
tmux send-keys -t $SESSION:2 "sb-deb" C-m
sleep 2
tmux send-keys -t $SESSION:2 "sb-init" C-m
sleep 1
tmux send-keys -t $SESSION:2 "sb-venv-activate" C-m
sleep 1
tmux send-keys -t $SESSION:2 "cd-bridge" C-m

# 4. DEB
tmux new-window -t $SESSION -n 'DEB'
tmux send-keys -t $SESSION:3 "sb-deb" C-m
sleep 2
tmux send-keys -t $SESSION:3 "sb-init" C-m
sleep 1
tmux send-keys -t $SESSION:3 "cd-bridge" C-m

# 5. TRMX
tmux new-window -t $SESSION -n 'TRMX'
tmux send-keys -t $SESSION:4 "sb-init" C-m
sleep 1

# 6. OLLAMA
tmux new-window -t $SESSION -n 'OLLAMA'
tmux send-keys -t $SESSION:5 "sb-deb" C-m
tmux send-keys -t $SESSION:5 "ollama" C-m

# 7. EXIT
tmux new-window -t $SESSION -n 'EXIT'
EXIT_UI="clear; echo '🌉 EXIT PORTAL'; echo ' [ PRESS ENTER TO SHUT DOWN ]'; read; tmux kill-session -t $SESSION"
tmux send-keys -t $SESSION:6 "$EXIT_UI" C-m

tmux select-window -t $SESSION:1
tmux attach-session -t $SESSION
