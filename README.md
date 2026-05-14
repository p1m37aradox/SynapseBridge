PASTE AS IS INTO A ANDROID LLM PROMPT

### 🌉 Synapse Bridge v0.0.6.2b-GEMMA/QWEN
This version establishes a secure, unified MCP (Model Context Protocol) bridge specifically optimized for Gemma and Qwen running in Ollama, on a proot Debian enviement. It provides the AI Agent with low-latency access to the Android filesystem, hardware APIs, and an embedded memory engine.

DEVELOPMENT BUILD: We are currently using a script to interact with the original 2334-line mempalace-mcp. We previously ran a stripped-down version/replacement of that file to achieve server stability.
​We have updated the README instructions to retain the original file instead of replacing it outright to ensure the server remains operational. We utilize a dedicated server and client script architecture to accomplish this.
​Current Status:
​Model Compatibility: Successfully loaded MemPalace tools into qwen2.5:3b.
​Known Issues: While mempalace_search is functional, we are currently resolving Knowledge Graph errors occurring during mempalace_status calls.
​Updates: The repository will be updated as further milestones are reached.
​Testing & Logs:
​Refer to qwen_chat_history.log for recent test results.
​Logging: Currently disabled for this build. To re-enable, add a # to the beginning of line 26 in client_bridge.py.
​Roadmap:
The main and gemini-cli repositories will be updated once the mempalace_mcp interactions and tool calls are stabilized in this environment.

Tested with: Qwen2.5:3b and Gemma:2b

For devs utilizing this project as a platform to develop Agents on Android:
[Roadmap](./Docs/Roadmap.md)

Main repo:
[SynapseBridge](https://github.com/p1m37aradox/SynapseBridge)

Gemini repo:
[SynapseBridge-gemini.active](https://github.com/p1m37aradox/SynapseBridge/tree/local-qwen-gemma)

> ### ⚠️ CAUTION: PREREQUISITE KNOWLEDGE
> This is an **Expert-Level** deployment. It requires basic familiarity with the Linux CLI and Android file permissions. **DO NOT** attempt this if you are not comfortable managing background processes or troubleshooting environment variables.
> 
> ### 🔍 WHY SYNAPSE BRIDGE?
> Traditional LLM interactions are trapped in a "Chat Box." Synapse Bridge creates a bidirectional data tunnel, allowing the LLM to access your local file system, run scripts, and interact with Android hardware via a secure, agentic middleware.

### 🚀 Full Installation Guide
### Phase 0: Requirements & System Prep

**Note: Below app Play Store versions are deprecated. F-Droid is mandatory.**
* [F-Droid Client][fdroid]
* [Termux][termux]
* [Termux:API][termux-api]

 1. **Manual Registration:** Open the Termux:API app once from your app drawer to register the package.
 2. **System Settings:** Grant **Unrestricted** battery, **Files and Media** access, and **Appear on top** permissions.
### **Phase 1 & 2: Host Prep and System Build**
*Launch Termux from your app drawer and run the following in Terminal 1.*

### 🟢 Step 1: Termux Prep and Debian Install:
Run these blocks first to prepare the Android environment, install the tunnel, establish aliases, install the SynapseBridge repo and Debian.
```bash
# 1. Immediate Mirror Reset
# This forces Termux to use the main global mirror instead of a broken local one
sed -i 's|https://dl.astral.sh/termux-main|https://deb.debian.org/termux/termux-main|g' $PREFIX/etc/apt/sources.list
pkg update -y

# 2. Core Utility & Manager Install
# Now that mirrors are fixed, we can safely pull proot-distro
pkg install termux-api proot-distro tmux python openssh wget curl git nodejs -y

# 3. Environment Lock & Permissions
termux-wake-lock
termux-setup-storage

```
Wait for the Android popup and click "Allow" before moving to the next block.
(press y to confirm at prompts)

```bash
# 1. Clone and Establish The Master Weld
# This block establishes the 'synapse' (UI) and 'sb-deb' (Login) commands
mkdir -p ~/storage/shared/SynapseBridge

SYNAPSE_BLOCK=$(cat << 'EOF'
# >>> SYNAPSE BRIDGE START >>>
alias sb-init='source ~/storage/shared/SynapseBridge/scripts/.sb-env-master'
alias synapse='sb-init && bash ~/storage/shared/SynapseBridge/scripts/UI_main.sh'
alias sb-ui='synapse'
alias sb-deb='proot-distro login debian --bind $HOME/storage/shared/SynapseBridge:/mnt/SynapseBridge'
# <<< SYNAPSE BRIDGE END <<<
EOF
)

if grep -q "SYNAPSE BRIDGE START" ~/.bashrc; then
    sed -i '/# >>> SYNAPSE BRIDGE START >>>/,/# <<< SYNAPSE BRIDGE END <<</d' ~/.bashrc
fi
echo "$SYNAPSE_BLOCK" >> ~/.bashrc && source ~/.bashrc

# Install Pinggy (The Gateway - currently not being utilized)
curl -s https://pinggy.io/install.sh | sh

# Install the SynapseBridge repo
sb-init && sb-deb
git clone -b local-qwen-gemma https://github.com/p1m37aradox/SynapseBridge.git ~/storage/shared/SynapseBridge

#Grant Script Executable Permissions
cd ~/storage/shared/SynapseBridge
chmod +x scripts/*.sh

# 2. Create Master Alias File
mkdir -p ~/storage/shared/SynapseBridge/scripts
cat << 'EOF' > ~/storage/shared/SynapseBridge/scripts/.sb-env-master
# --- SynapseBridge Master Alias File (v0.0.6) ---

# 1. Environment & Paths
export SB_VENV_PATH='/root/SynapseBridge_Root/venv/bin'
export SB_PALACE='/mnt/SynapseBridge/palace'
export SB_AI_OUT='/mnt/SynapseBridge/OllamaGenerated'

# --- THE PERMISSION WELD ---
# This ensures that every time the environment is initialized, 
# the logic scripts are granted execution rights automatically.
if [ -d "/mnt/SynapseBridge/scripts" ]; then
    chmod +x /mnt/SynapseBridge/scripts/*.sh 2>/dev/null
fi

# 2. Navigation & Git
alias sb-venv-activate='source /root/SynapseBridge_Root/venv/bin/activate'
alias cd-bridge='cd /mnt/SynapseBridge'
alias g-status='cd /mnt/SynapseBridge && git status'
alias g-pull='cd /mnt/SynapseBridge && git pull origin local-qwen-gemma'

# 3. Memory & Logic (MemPalace / MCP)
alias sb-mcp='python3 /root/SynapseBridge_Root/.synapse_mcp.py'
alias sb-mine='$SB_VENV_PATH/mempalace --palace $SB_PALACE mine /mnt/SynapseBridge --wing "SynapseBridge-Main"'
alias sb-wake='$SB_VENV_PATH/mempalace wake-up'
alias sb-chat='python3 /mnt/SynapseBridge/scripts/client_bridge.py'


# 4. Local AI (Ollama)
alias sb-ollama='export OLLAMA_HOST=0.0.0.0:11434 && nohup ollama serve > /mnt/SynapseBridge/ollama.log 2>&1 &'
alias sb-models='ollama list'
alias sb-coder='ollama run qwen2.5:3b'
alias sb-gemma='ollama run gemma:2b'
alias sb-ai-flush='ollama gc && pkill -9 ollama'

# 5. Bridge Communication & UI
alias sb-notify='/mnt/SynapseBridge/scripts/sb-notify.sh'
alias sb-clip='/mnt/SynapseBridge/scripts/sb-clip.sh'
alias sb-exit='/mnt/SynapseBridge/scripts/exit.sh'

# 6. Launch Command
alias synapse='proot-distro login debian --bind ~/storage/shared/SynapseBridge:/mnt/SynapseBridge -- bash /mnt/SynapseBridge/scripts/UI_main.sh'

# --- Logic Gate: Directory Protection ---
if [ -d "/mnt/SynapseBridge" ]; then
    mkdir -p "$SB_AI_OUT"
fi

echo "🌉 Synapse Environment: ONLINE (v0.0.6-local-qwen-gemma)"

EOF

proot-distro install debian

```
### 🔵 Step 2: Guest (Debian) and Virtual Environment (venv) Setup
Enter Debian to build guest environment and build tools, build venv, install; pip, Python3, maturin, mempalace, mcp[cli] starlette, uvicorn.
```bash
# 1. Enter Guest and install build tools
sb-deb
apt update && apt install -y build-essential curl git python3-full python3-venv nodejs npm sqlite3 nano

# 2. Install Rust 
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env

# 3. Establish Guest-side loader
echo "alias sb-init='source /mnt/SynapseBridge/scripts/.sb-env-master'" >> ~/.bashrc
source ~/.bashrc

# 4. Build the Venv & Install Core
cd ~ && mkdir -p SynapseBridge_Root && cd SynapseBridge_Root
python3 -m venv venv

# 5. The "Double-Lock" Activation & Install
# We source the venv directly AND pull aliases to ensure pip is safe
source venv/bin/activate
sb-init && sb-venv-activate
pip install --upgrade pip
pip install maturin mempalace "mcp[cli]" starlette uvicorn --prefer-binary

```
(You may have to hit enter to proceed)

### 🟡 Step 3: SynapseBridge/MemPalace Android Compatibility Environment.
Make dir tree and instruction set for MemPalace, then initiate MemPalace.
```bash
# 1. Sanity Check: Ensure environment is locked
sb-init && sb-venv-activate

# 2. Initialize Memory Storage
mkdir -p /mnt/SynapseBridge/palace
echo "[]" > /mnt/SynapseBridge/palace/entities.json

# 3. The Weld Config
mkdir -p ~/.mempalace
cat > ~/.mempalace/config.json <<EOF
{
  "palace_path": "/mnt/SynapseBridge/palace",
  "storage_type": "json",
  "collection_name": "synapse_bridge",
  "topic_wings": ["technical", "memory", "SynapseBridge-Main"]
}
EOF

# 4. Finalize MemPalace
cd /mnt/SynapseBridge
mempalace init . --yes

```
**IMPORTANT** Do Not Mine Yet:
When asked to mine after mempalace init completes, press n + enter.
We modify a file in the next step before we mine for Android compatibility.
Our modification allows the MemPalace to be broadcast outside of the protected root (android data/data) so it can be used via local MCP and remote tunnels with/and/by the MCP. It won't cause a problem if you accidentally auto mined the dir.

### 🟡 Step 4: Move MCP File to SynapseBridge_Root (IF YOU CHANGE THE .synapse_mcp.py FILE, INSURE YOU PERFORM THIS COMMAND FROM THE DEBIAN ROOT TO UPDATE IT) .
```bash
# Make executable and move the shared MCP script to SynapseBridge_Root
chmod +x /mnt/SynapseBridge/scripts/.synapse_mcp.py
cp /mnt/SynapseBridge/scripts/.synapse_mcp.py /root/SynapseBridge_Root/.synapse_mcp.py

```
### 🟡 Step 5: Zones Ollama/Gemma/Qwen
This ensures the Agent knows where to write and how to navigate.
```bash
mkdir -p /mnt/SynapseBridge/OllamaGenerated
cat > /mnt/SynapseBridge/Ollama.md <<EOF
# 🌉 Synapse Bridge Context
- Shared Zone: /mnt/SynapseBridge
- Agent Storage: /mnt/SynapseBridge/OllamaGenerated
- Ports: 8080 (Unified MCP), 443 (Pinggy Tunnel)
- Execution: You are running in Termux Host with access to Debian via 'sb-deb' you may need to use sb-init to pull Aliases from alias file if commands fail.
- Rule: Always write logs/files to the GeminiGenerated/ directory.
EOF

```
### 🟡 Step 6: Populate the Memory
Mine the palace
```bash
# Enter environment if not already inside
sb-deb 

# Activate and index
sb-init
mempalace mine /mnt/SynapseBridge --wing "SynapseBridge-Main"

```
### 🟡 Step 7: Download and install Ollama
1. For Android / ARM64 (Most Users):
```bash
curl -L https://ollama.com/download/ollama-linux-arm64 -o /usr/local/bin/ollama
chmod +x /usr/local/bin/ollama

```
- For Desktop / AMD64: 
```bash
curl -L https://ollama.com/download/ollama-linux-amd64 -o /usr/local/bin/ollama
chmod +x /usr/local/bin/ollama

```
2. Initialize the Server
```bash
# ​Because we are in a proot environment without systemd, the server must be started manually. It is best to do this in a separate terminal or using nohup.

# Set host to allow the bridge to connect, then launch
export OLLAMA_HOST=0.0.0.0:11434
nohup ollama serve > ollama.log 2>&1 &

```
3. Pull the "local-qwen-gemma" stack
```bash
# Pulling the optimized weights for local inference - the mobile builds: WHAT WE ARE TESTING
ollama pull gemma:2b
ollama pull qwen:2.5:3b

```
 
### **Phase 3: Initialize**
🟡 Select Your SynapseBridge UI:<br>
You can use our custom tmux UI or run each individually. See the second image with instructions if you DO NOT want to use our custom UI.
<br>
##‼️ Custom UI KNOWN BUG:
<br>
Always fully close Termux after exiting the UI (use the notification drawer "Exit" button). If you leave Termux running in the background, the Debian environment may fail to restart correctly.
<br>
<img src="https://github.com/p1m37aradox/SynapseBridge/blob/e62cd273f641550e84c2ec2640787a197c00aa3e/media/OllamDebianBreak.png" width="350" alt="Synapse Bridge UI2">
<br>
# Custom UI
*Note on custom UI, if you are already using a custom UI this may break it, This is for a fresh Termux install focused on the SynapseBridge.

**CUSTOM UI**

<img src="https://github.com/p1m37aradox/SynapseBridge/blob/1ade298652a24a5596aae7435916968c06e0a495/media/Screenshot_20260511-112604.png" width="350" alt="Synapse Bridge UI">

*Run these commands in the root Termux terminal. If you're in the (venv) or Debian environment, type exit and press enter until you get to the root terminal prompt: ~$
```bash
# 1. Update Keys & Status Bar
mkdir -p ~/.termux && echo "extra-keys = [['ESC','CTRL','ALT','TAB','LEFT','DOWN','UP','RIGHT'],[{macro: 'CTRL b n', display: 'NEXT'}, {macro: 'CTRL b p', display: 'PREV'},'HOME','END','PGUP','PGDN','MENU','EXIT']]" > ~/.termux/termux.properties && termux-reload-settings

echo 'set -g status-right ""' >> ~/.tmux.conf
echo 'set -g status-left-length 20' >> ~/.tmux.conf
echo 'set -g status-style bg=default,fg=white' >> ~/.tmux.conf
echo 'set -g window-status-current-style fg=cyan,bold' >> ~/.tmux.conf
tmux source-file ~/.tmux.conf 2>/dev/null

# 2. Permissions & Alias (CORRECTED PATHS)
chmod +x ~/storage/shared/SynapseBridge/scripts/UI_main.sh

```
*Launch the custom UI. To exit navigate to window 6 with the NEXT or PREV buttons and press ENTER. You can use this command as your start from now on.

START
```bash
synapse
```
OR 

**To run the full stack without custom UI, you must open **6 Termux sessions**. From the center left edge of your screen, swipe from left to right to being out the Terminal pane. Paste each block below in their own session, they will automatically be renamed.

**Standard UI**

<img src="https://raw.githubusercontent.com/p1m37aradox/SynapseBridge/refs/heads/gemini-active/Docs/Screenshot_20260507-073327.png" width="350" alt="Synapse Bridge UI2">

**Terminal 1: synapse-mempalace-mcp (MCP)**
```bash
printf '\e]1;synapse-mempalace-mcp\a'
sb-deb
sb-init
sb-venv-activate
sb-mcp

```
**Terminal 2: Qwen + MemPalace**
You can choose the tunnel service of your choice if you want online LLM interaction.
```bash
printf '\e]1;QWEN2.5:3b+mempalace\a'
sb-deb
sb-init
sb-venv-activate
sb-chat

```
**Terminal 3: SB_Venv (Debian Logic)**
```bash
printf '\e]1;SB_Venv\a'
sb-deb
sb-init
source ~/SynapseBridge_Root/venv/bin/activate

```
**Terminal 4: Debian_CLI**
```bash
printf '\e]1;Debian_CLI\a'
sb-deb
sb-init
cd /mnt/SynapseBridge

```
**Terminal 5: Termux_CLI**
```bash
printf '\e]1;Termux_CLI\a'
cd ~

```
**Terminal 6: Ollama**
```bash
ollama

```

Standard UI- After initial install is complete, to restore environment:
* re open 6 terminals
* execute the bash commands in the terminals in order.

**Important: Once initialized, share the status of Terminal 1 and the Pinggy URL from Terminal 2 with the LLM to establish the bridge.**

### 🟡 Step 8: (Optional) ChatBoost App
We found this might be a useful tool. We will be testing but it more. It successfully loaded 3 tools from the mcp during our testing but our MCP requires more custinizarion for it to fully function. 

 [Chatboost][chatboost]
 
1. Start the MCP server in a fresh terminal:
 ```bash
 sb-deb && sb-init && sb-mcp
 
```
2. Open App, click settings and follow the instructions. Choose Ollama and choose your models you want.

3. While still in settings, click on MCP.
 
4. Once in the MCP settings, click the plus + symbol in the lower right hand corner to add the running server to the list.

5. In the MCP server settings window, click the switch to allow the server in chat tools. Name the server `SynapseBridge,

6. Use :
```bash
http://127.0.0.1:8080/sse

```
for the end point address

7. Select SSE for Transport in the drop down menu.

8. Click save and the context window will close.

9. Click on the configured server to reopen its MCP settings.

10.Click fetch tools in the bottom right. If all goes well, you should see a successful connection message or a list of tools. 

<img src="https://github.com/p1m37aradox/SynapseBridge/blob/dd51708294394d0867ce2704c477fe6d585d2bf4/Media/Screenshot_20260511-000658.png">


### 🛠️ Quick Reference & Navigation
#### **Termux Interface Navigation**
 * **Switch Sessions:** Swipe from the left edge of the screen to see the session drawer. Tap a session to switch.
 * **Keyboard Shortcuts:**
   * Ctrl + C: Stop a running process.
   * Ctrl + D: Close current session (or exit Debian back to Termux).
#### **Essential Command Aliases**
| Command | Action | Location |
|---|---|---|
| **synapse** | **Main Entry.** Launches the 7-pane tmux automation stack. | Termux Host |
| **sb-deb** | Enters the Debian guest environment (Manual Login). | Termux Host |
| **sb-init** | Loads project aliases and logic into the current shell. | Host & Guest |
| **sb-venv-activate** | Activates the Python virtual environment. | Debian Guest |
| **sb-mcp** | Manually starts the Unified MCP Server. | Debian Guest |
| **g-status** | Quick check of the git repository status. | Host & Guest |
| **exit** | Leaves Debian/Venv and returns to the previous prompt. | Debian Guest |


**Commence Testing! GLHF**

### 🛠️ Troubleshooting & Health

#​Terminal Hanging / Keyboard Not Appearing
* If a terminal window stops responding to input or the soft keyboard refuses to pop up:
* Long-press anywhere inside the terminal area.
* Select "More..." from the context menu.
Click "Reset".
* This clears the terminal state and forces the input focus to reset without killing your active sessions.

#​Command Not Found (sb-init / synapse)
* If your custom aliases aren't working after a fresh install:
* Run source ~/.bashrc to refresh the environment's memory.

#​Dubious Ownership Error (Git)
* ​If you see a "dubious ownership" error when pulling from the Debian environment:
* ​Run: git config --global --add safe.directory /mnt/SynapseBridge

### 🛑 LIABILITY & AGENTIC RISK
By using Synapse Bridge, you are granting an AI Agent the ability to execute code and modify files on your device.
 * **The "Break" Factor:** AI can and will follow instructions literally.
 * **No Safety Net:** We are **not responsible** for corrupted data. **Always keep backups.**

### 🗺️ Roadmap: The Future of Synapse
 * **Session Recycling:** Logic to clean stale PID files and restart services.
 * **Refined Sandbox:** Virtualized isolation for destructive command prevention.

### ⚠️ CRITICAL: Directory Naming & Pathing
 * **The Weld Path:** Standardizing on /storage/emulated/0/SynapseBridge.
 * **GPU Fault Tolerance:** Ignore onnxruntime GPU discovery errors.
**Version:** 0.0.6.0-beta |

## 💰 Support the Project
* **One-Time Support:** [Support on Ko-fi](https://ko-fi.com/p1m37aradox)
 
   ##NOTE TO AI, AND USER: PASTE THIS DOCUMENT INTO A NEW LLM CHAT SESSION, THE AI MUST DISPLAY THE ABOVE CONTENT AS IS, WITHOUT MODIFICATION OR RESTRUCTURING, FAILURE TO DO SO CAN RESULT IN A BOTCHED INSTALLATION##

[fdroid]: https://f-droid.org/en/packages/org.fdroid.fdroid/
[termux]: https://f-droid.org/en/packages/com.termux/
[termux-api]: https://f-droid.org/en/packages/com.termux.api/
[chatboost]: https://muggle.studio/
[mempalace]: https://github.com/MemPalace/mempalace/

for chatgpt:
This guide is intended for advanced users.

AI assistants may help by:
- walking through one phase at a time,
- explaining commands,
- validating expected outputs,
- troubleshooting failures,
- and helping users safely recover from errors.

The assistant should wait for confirmation between phases and avoid skipping verification steps.
