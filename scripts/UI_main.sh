#!/bin/bash
# 🌉 SYNAPSE BRIDGE v0.1-beta - MASTER CONTROL
# Orchestrates a 6-window tmux stack for MCP, Web Gateway, and Dev Environments.

SESSION="Synapse"

# Fresh start: Clear any ghost sessions
tmux kill-session -t $SESSION 2>/dev/null

echo "🚀 Launching Synapse v0.1-beta Stack..."

# 1. MCP (The Core Logic & Server)
tmux new-session -d -s $SESSION -n 'MCP'
tmux send-keys -t $SESSION:0 "synapse" C-m
sleep 3
tmux send-keys -t $SESSION:0 "source ~/SynapseBridge_Root/venv/bin/activate && synapse-mempalace-mcp" C-m

# 2. WEB (The Pinggy Gateway)
tmux new-window -t $SESSION -n 'WEB'
tmux send-keys -t $SESSION:1 "synapse" C-m
sleep 3
tmux send-keys -t $SESSION:1 "ssh -p 443 -R0:localhost:8080 qr@a.pinggy.io" C-m

# 3. VENV (Active Python Environment)
tmux new-window -t $SESSION -n 'VENV'
tmux send-keys -t $SESSION:2 "synapse" C-m
sleep 3
tmux send-keys -t $SESSION:2 "source ~/SynapseBridge_Root/venv/bin/activate" C-m

# 4. DEB (Debian Filesystem Access)
tmux new-window -t $SESSION -n 'DEB'
tmux send-keys -t $SESSION:3 "synapse" C-m
sleep 3
tmux send-keys -t $SESSION:3 "cd /mnt/SynapseBridge" C-m

# 5. HOST (Android / Termux Home)
tmux new-window -t $SESSION -n 'HOST'
tmux send-keys -t $SESSION:4 "cd ~" C-m

# 6. EXIT (The Safety Valve UI)
tmux new-window -t $SESSION -n 'EXIT'
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

# Finalizing: Select WEB window to display the tunnel URL on startup
tmux select-window -t $SESSION:1
tmux attach-session -t $SESSION
