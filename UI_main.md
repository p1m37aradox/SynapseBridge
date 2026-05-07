#!/bin/bash
# 🌉 SYNAPSE BRIDGE v0.0.4b - HIGH-FIDELITY PORTAL

SESSION="Synapse"

# Fresh start
tmux kill-session -t $SESSION 2>/dev/null

echo "🚀 Launching Synapse v0.0.4b..."

# 1. MCP
tmux new-session -d -s $SESSION -n 'MCP'
tmux send-keys -t $SESSION:0 "synapse" C-m
sleep 3
tmux send-keys -t $SESSION:0 "source ~/SynapseBridge_Root/venv/bin/activate && synapse-mempalace-mcp" C-m

# 2. WEB
tmux new-window -t $SESSION -n 'WEB'
tmux send-keys -t $SESSION:1 "synapse" C-m
sleep 3
tmux send-keys -t $SESSION:1 "ssh -p 443 -R0:localhost:8080 qr@a.pinggy.io" C-m

# 3. VENV
tmux new-window -t $SESSION -n 'VENV'
tmux send-keys -t $SESSION:2 "synapse" C-m
sleep 3
tmux send-keys -t $SESSION:2 "source ~/SynapseBridge_Root/venv/bin/activate" C-m

# 4. DEB
tmux new-window -t $SESSION -n 'DEB'
tmux send-keys -t $SESSION:3 "synapse" C-m
sleep 3
tmux send-keys -t $SESSION:3 "cd /mnt/SynapseBridge" C-m

# 5. HOST
tmux new-window -t $SESSION -n 'HOST'
tmux send-keys -t $SESSION:4 "cd ~" C-m

# 6. EXIT (Clean UI with NO command leak)
tmux new-window -t $SESSION -n 'EXIT'
# Bundling everything into one execution line to hide the 'echo' commands
EXIT_UI="clear; \
printf '\033[1;36m%s\033[0m\n' '=========================================='; \
printf '\033[1;36m%s\033[0m\n' '     🌉 SYNAPSE BRIDGE EXIT PORTAL'; \
printf '\033[1;36m%s\033[0m\n' '=========================================='; \
echo ''; \
echo '  The Bridge is currently operational.'; \
echo ''; \
printf '\033[1;31m%s\033[0m\n' '  [ PRESS ENTER TO SHUT DOWN ALL ]'; \
read; \
tmux kill-session -t $SESSION"

tmux send-keys -t $SESSION:5 "$EXIT_UI" C-m

# Landing
tmux select-window -t $SESSION:1
tmux attach-session -t $SESSION
