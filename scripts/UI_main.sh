#!/bin/bash
# 🌉 SYNAPSE BRIDGE v0.0.6.2b-beta - MASTER CONTROL
SESSION="Synapse"

tmux kill-session -t $SESSION 0>/dev/null
echo "🚀 Launching Synapse v0.1.6-beta Qwen+MemPalace Stack..."

# 1. MCP
tmux new-session -d -s $SESSION -n 'MCP'
tmux send-keys -t $SESSION:0 "sb-deb" C-m
sleep 2
tmux send-keys -t $SESSION:0 "sb-venv-activate" C-m
sleep 1
tmux send-keys -t $SESSION:0 "sb-chat" C-m

# 2. QWEN
#tmux new-window -t $SESSION -n 'WEBUI'
#tmux send-keys -t $SESSION:1 "sb-deb" C-m
#sleep 2
#tmux send-keys -t $SESSION:1 "sb-venv-activate" C-m
#sleep 1
#tmux send-keys -t $SESSION:1 "WEBUI_AUTH=False open-webui serve --port 3000" C-m
#sleep 1

# 3. VENV
tmux new-window -t $SESSION -n 'VENV'
tmux send-keys -t $SESSION:1 "sb-deb" C-m
sleep 2
tmux send-keys -t $SESSION:1 "sb-venv-activate" C-m
sleep 1
tmux send-keys -t $SESSION:1 "cd-bridge" C-m

# 4. DEB
#tmux new-window -t $SESSION -n 'DEB'
#tmux send-keys -t $SESSION:3 "sb-deb" C-m
#sleep 2
#tmux send-keys -t $SESSION:3 "cd-bridge" C-m

# 5. TRMX
#tmux new-window -t $SESSION -n 'TRMX'
#tmux send-keys -t $SESSION:4 "sb-init" C-m
#sleep 1

# 6. OLLAMA
tmux new-window -t $SESSION -n 'OLLAMA'
tmux send-keys -t $SESSION:2 "sb-deb" C-m
tmux send-keys -t $SESSION:2 "sb-init" C-m
tmux send-keys -t $SESSION:2 "ollama serve &" C-m

# 7. EXIT
tmux new-window -t $SESSION -n 'EXIT'
EXIT_UI="clear; echo '🌉 EXIT PORTAL'; echo ' [ PRESS ENTER TO SHUT DOWN ]'; read; tmux kill-session -t $SESSION"
tmux send-keys -t $SESSION:3 "$EXIT_UI" C-m

tmux select-window -t $SESSION:0
tmux attach-session -t $SESSION