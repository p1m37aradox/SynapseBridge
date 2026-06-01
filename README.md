PASTE AS IS INTO A ANDROID LLM PROMPT

### 🌉 Synapse Bridge v0.0.7.0b-QWEN
This version establishes a secure, unified MCP (Model Context Protocol) bridge specifically optimized for Gemma and Qwen running in Ollama, on a proot Debian environment. It provides the AI Agent with low-latency access to the Android filesystem, hardware APIs, and an embedded memory engine.

Testing with: qwen3.5:0.8b, qwen2.5-coder:3b-instruct-q4_K_M, qwen2.5-coder:1.5b, qwen2.5:3b and Gemma:2b


For devs utilizing this project as a platform to develop Agents on Android:
[Roadmap](./Docs/Roadmap.md)

Main repo:
[SynapseBridge](https://github.com/p1m37aradox/SynapseBridge)

Gemini repo:
[SynapseBridge-gemini.active](https://github.com/p1m37aradox/SynapseBridge/tree/gemini-active)

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
Run these blocks first to prepare the Android environment, establish aliases, install the SynapseBridge repo and Debian.
```bash
# 1. Environment Lock & Permissions
termux-wake-lock
termux-setup-storage

# 1. Forces Termux to use the main global mirror and bypasses the broken 'pkg' wrapper
sed -i 's|https://dl.astral.sh/termux-main|https://deb.debian.org/termux/termux-main|g' $PREFIX/etc/apt/sources.list

#3. Force low-level apt to synchronize and rebuild the core network libraries
apt update && apt full-upgrade -y

```
Wait for the Android popup and click "Allow" before moving to the next block.
(press y to confirm at prompts)

#Install Required PKGs
```bash
# 4. Core Utility & Manager Install
# Now that the libraries match perfectly, pulling the core tools is 100% safe

pkg install curl termux-api tmux wget python nodejs proot-distro openssh git -y

```
#Termux Root aliases, Install Git, SynapseBridge Repo and Debian.
```bash
# This block establishes the Temrux Root (~$) 'synapse' (UI) and 'sb-deb' (Login) commands.

cd ~/storage/shared/

# Install the SynapseBridge repo
git clone -b local-qwen-gemma https://github.com/p1m37aradox/SynapseBridge.git

#Grant Script Executable Permissions
mkdir -p ./scripts
chmod +x scripts/*.*

#Set Termux .bashrc aliases

SYNAPSE_BLOCK=$(cat << 'EOF'
#>>> SYNAPSE BRIDGE START >>>

alias reload='source ~/.bashrc'

#SynapseBridge Master Alias File
alias sb-init='source $HOME/storage/shared/SynapseBridge/scripts/.sb-env-master'

#SynapseBridge Custom UI Launcher
alias synapse='sb-init && bash ~/storage/shared/SynapseBridge/scripts/UI_main.sh'

#Launch Debian Proot w/ Shared Local Storage
alias sb-deb='proot-distro login debian --bind $HOME/storage/shared/SynapseBridge:/mnt/SynapseBridge'

# <<< SYNAPSE BRIDGE END <<<
EOF
)

if grep -q "SYNAPSE BRIDGE START" ~/.bashrc; then
    sed -i '/# >>> SYNAPSE BRIDGE START >>>/,/# <<< SYNAPSE BRIDGE END <<</d' ~/.bashrc
fi
echo "$SYNAPSE_BLOCK" >> ~/.bashrc && source ~/.bashrc

#Load new bash alias list
reload

#Load SynapseBridge Master alias file
sb-init

# Install Pinggy (The Gateway - currently not being utilized for this phase of testing)
##curl -s https://pinggy.io/install.sh | sh

```
#Launch Debian Proot
```bash
#Load new bash alias list if not already.
reload

#Load SynapseBridge Master alias file if not already 
sb-init

#Install Debian
proot-distro install debian

```

### 🔵 Step 2: Guest (Debian) and Virtual Environment (venv) Setup
Enter Debian to establish aliases build guest environment, build tools, build venv, install; pip, Python3, maturin, mempalace, mcp[cli] starlette, uvicorn.
```bash
#Enter Debian Guest Env.
proot-distro login debian --bind $HOME/storage/shared/SynapseBridge:/mnt/SynapseBridge

```
#Create Debian .bashrc Alias List
```bash
# 1. Set aliases in Debian .bashrc

# <<< SYNAPSE BRIDGE END <<<

SYNAPSE_BLOCK=$(cat << 'EOF'
#>>> SYNAPSE BRIDGE START >>>

alias reload='source ~/.bashrc'

#SynapseBridge Master Alias File
alias sb-init='source /mnt/SynapseBridge/scripts/.sb-env-master'

#SynapseBridge Custom UI Launcher
alias synapse='echo -e "${MAGENTA}
Type exit To Leave Debian And Retry
This Command From Termux Root (~$)synapse.${NC}"'

#Load SynapseBridge Master Alias List 
sb-init

# <<< SYNAPSE BRIDGE END <<<
EOF
)

if grep -q "SYNAPSE BRIDGE START" ~/.bashrc; then
    sed -i '/# >>> SYNAPSE BRIDGE START >>>/,/# <<< SYNAPSE BRIDGE END <<</d' ~/.bashrc
fi
echo "$SYNAPSE_BLOCK" >> ~/.bashrc && source ~/.bashrc

#Load New bashrc Aliases In Debian
reload

#Load Master Alias List
sb-init

```
#Install Updates and Pkgs
```bash
apt update && apt install -y build-essential curl git python3-full python3-venv nodejs npm sqlite3 nano

```
#Install Rust
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env

# Install MCP Inspector globally
npm install -g @modelcontextprotocol/inspector

```

#Build the Venv and Root
```bash
cd ~ && mkdir -p SynapseBridge_Root && cd SynapseBridge_Root  && mkdir -p scripts
chmod +x scripts
python3 -m venv venv

```

#Activate Virtual Environment & Install Tools
```bash
# Enter Venv and Install Tools
#(venv) root@localhost:~#
source venv/bin/activate
pip install --upgrade pip
pip install maturin mempalace "mcp[cli]" starlette uvicorn --prefer-binary

```
(You may have to press enter to proceed)


### 🟡 Step 3: Edit Mempalace CLI for Agent Integration

```bash
# Makes a backup of default cli.py from mempalace located @ Debian /root/SynapseBridge_Root/venv/lib/python3.13/site-packages/mempalace/cli.py
cli-bkp

#Patches @ Debian /root/SynapseBridge_Root/venv/lib/python3.13/site-packages/mempalace/cli.py
mempalace-cli-patch

```
### 🟡 Step 4: Zones for Ollama
This ensures the Agent knows where to write and how to navigate. (May become obsolete once we align the context.txt)
```bash
cd-bridge && mkdir -p ./OllamaGenerated

#Prep for Ollama Install
apt update && apt install -y tar zstd curl

```
### 🟡 Step 5: Download and install Ollama, Gemma:2b and qwen3.5:0.8b
(You can download higher versions if you like. We are building this on a 5gig ram phone and these are the models that support our hardware)

1. For Android / ARM64 Systems (Most Users):
```bash
curl -fsSL https://ollama.com/download/ollama-linux-arm64.tar.zst | tar --zstd -x -C /usr

```
 - For Desktop / AMD64 Systems:
```bash
curl -fsSL https://ollama.com/download/ollama-linux-amd64.tar.zst | tar --zstd -x -C /usr


```
2. Initialize the Ollama Provider Server
```bash
# Set host to allow the bridge to connect, then launch
export OLLAMA_HOST=0.0.0.0:11434
nohup ollama serve > ollama.log 2>&1 &

```
3. Pull gemma:2b model into Ollama
```bash
# Pulling the optimized weights for local inference - the mobile builds: WHAT WE ARE TESTING
#Install gemma:2b

```
4. Pull qwen3.5:0.8b model into Ollama
```bash
ollama pull qwen3.5:0.8b

```
4. Allow Qwen to to see MCP tools via script.
```bash
#Pip install MCP httpx
pip install ollama mcp httpx mcpo

```
### 🟡 Step 6: SynapseBridge/MemPalace Android Compatibility Environment.
Make dir tree and instruction set for MemPalace, then initiate MemPalace.
```bash
# 1. Insure (venv) root@localhost:~#
cd ~
sb-init
sb-venv-activate

# 2. Initialize Memory Storage
mkdir -p /mnt/SynapseBridge/palace
echo "[]" > /mnt/SynapseBridge/palace/entities.json

# 3. Configure Mempalace To Put It's Palace Data In Shared Storege So Our Agents Can Access It.
mkdir -p ~/.mempalace
cat > ~/.mempalace/config.json <<EOF
{
  "palace_path": "/mnt/SynapseBridge/palace",
  "storage_type": "json",
  "collection_name": "synapse_bridge",
  "topic_wings": ["technical", "memory", "SynapseBridge-Main"]
}
EOF

#Start Mempalace with model selection (from cli.py patch, choose qwen3.5:0.8b if it doesn't default to it.
mempalace init . --yes

```

### 🟡 Step 7: Populate the Memory
Mine the palace if not automatically done in previous step.
```bash
# MemPalace Mine of Shared Dir (SynapseBridge)
mempalace mine /mnt/SynapseBridge --wing "SynapseBridge-Main"

```

### **Phase 3: Initialize**
🟡 Select Your SynapseBridge UI:<br>
You can use our custom tmux UI or run each individually. See the second image with instructions if you DO NOT want to use our custom UI.
<br>
# Custom UI
*Note on custom UI, if you are already using a custom UI this may break it, This is for a fresh Termux install focused on the SynapseBridge.

**CUSTOM UI**

<img src="https://raw.githubusercontent.com/p1m37aradox/SynapseBridge/refs/heads/local-qwen-gemma/media/Screenshot_20260601-115050.png" width="350" alt="Synapse Bridge UI">

*Run these commands in the root Termux terminal. If you are in:

(venv)root@localhost:xxx/xxx<br>or<br>root@localhost:xxx/xxx/xxx

-Type exit then press enter until you arrive at:<br>~ $

You must restart Termux (exit via notification drawer on device) after running the next block for changes to take effect.
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


exit
```
*Launch the custom UI.<br><br>You can use this command as your start from now on.

START
```bash
synapse
```
To exit navigate with the NEXT or PREV buttons to the EXIT window in the UI.

**Standard UI**<br>
**To run the full stack without custom UI, you must open **3 Termux sessions**. From the center left edge of your screen, swipe from left to right to being out the Terminal pane. Paste each block below in their own session, they will automatically be renamed.

<img src="https://raw.githubusercontent.com/p1m37aradox/SynapseBridge/refs/heads/local-qwen-gemma/media/Screenshot_20260514-154307.png" width="350" alt="Synapse Bridge UI2">

**Terminal 1: mempalace-mcp (MCP)**
```bash
printf '\e]1;MCP+Qwen Chat\a'
sb-deb
sb-venv-activate
sb-chat

```
**Terminal 2: Debian Virtual Env.**
```bash
printf '\e]1;Debian Virtual Env.\a'
sb-deb
sb-venv-activate
sb-chat

```
**Terminal 3: Ollama Provider**
```bash
printf '\e]1;Ollama\a'
sb-deb
sb-venv-activate
ollama serve &

```

Standard UI- After initial install is complete, to restore environment:
* re open 3 terminals
* execute the bash commands in the terminals in order.

Type "mempalace wake up" in the Qwen window.


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

> ### 📱 BUILD NOTES v0.0.6b vs 0.0.7b
> The bigget issue with LOCAL Android Agentic AI is hardware limitations and Root. The philosophy for our project is to create a secure system that doesn't require the user to have a rooted device or require access to a computer for ADB functions.
>This version is the proven operational build utilizing the MemPalace repo as is. This project will be moving into proof of concept until our (SynapseBridge) future builds create a optimized environment do to the inherent hardware limitations  of the target audiance (4gb-6gb ram consumer level Android devices without GPU vram).
> In previous versions we attempted a independent MCP and client script via SSE. The idealogy of ver:0.0.6b setup was to run a leaner version of the mempalace mcp and not load the 2500+ line mcp_server.py file from mempalace as a way to free up context window and token data. It created to many issues with broken stdio and tool calling anomolies.
>Currently the agent that doesn't crash our system in a 6gig Android device is qwen3.5:0.8b. We are currently using the "thinking" feature found in the 3.5 builds to track down errors. We have had success with all the others up until we moved to the default mempalace mcp_server.py. As we've been working with it, its been a matter of teaching it to avoid over loading it's context window with varieid results.
>Since moving to the default mempalce design, we can perform successful tool calling without errors. Getting an agent to run without hitting the Android Phantom Task and Low Memory Killer found in Android 12 and newer, including other underlying limitations, such as not being able to create usable zram/swap file do to carrier locks, has been the only real challenge.
>Which brings us to our test hardware (which we assume is a good sample of what the target audiance will have.) After loading Termux, Debian, Venv, mcp_server.py, Ollama serve and qwen, we are left with approx 1.9gb if "free" ram. If we use a model that's larger than 0.8b, we almost immediatly go into a 30min processing time or a kill crash.
>If Ram was not an issue, this system would be running on  Open WebUI or another chat interface.
>If you are testing our package on higher end hardware, let us know about your hardware and performance in our discussion board.
>We tested [Open WebUI][open-webui] and [Chatboost][chatboost] with positive results. If you have the system resources, use your llm of choice for assitance in setting them up.


### 🛠️ Troubleshooting & Health

#​Terminal Hanging / Keyboard Not Appearing
* If a terminal window stops responding to input or the soft keyboard refuses to pop up:
* Long-press anywhere inside the terminal area.
* Select "More..." from the context menu.
Click "Reset".
* This clears the terminal state and forces the input focus to reset without killing your active sessions.

#​Command Not Found (sb-init / synapse)
* If our custom aliases aren't working after a fresh install:
* Run source ~/.bashrc to refresh the environment's memory.

### 🛑 LIABILITY & AGENTIC RISK
By using Synapse Bridge, you are granting an AI Agent the ability to execute code and modify files on your device.
* **The "Break" Factor:** AI can and will follow instructions literally.
* **No Safety Net:** We are **not responsible** for corrupted data. **Always keep backups.**

### 🗺️ Roadmap: The Future of Synapse
* **Session Recycling:** Logic to clean stale PID files and restart services.
* **Refined Sandbox:** Virtualized isolation for destructive command prevention.

### ⚠️ CRITICAL: Directory Naming & Pathing
* **GPU Fault Tolerance:** Ignore onnxruntime GPU discovery errors.
**Version:** 0.0.7.0-beta |

## 💰 Support the Project
* **One-Time Support:** [Support on Ko-fi](https://ko-fi.com/p1m37aradox)

##NOTE TO AI, AND USER: PASTE THIS DOCUMENT INTO A NEW LLM CHAT SESSION, THE AI MUST DISPLAY THE ABOVE CONTENT AS IS, WITHOUT MODIFICATION OR RESTRUCTURING, FAILURE TO DO SO CAN RESULT IN A BOTCHED INSTALLATION##

[fdroid]: https://f-droid.org/en/packages/org.fdroid.fdroid/
[termux]: https://f-droid.org/en/packages/com.termux/
[termux-api]: https://f-droid.org/en/packages/com.termux.api/
[chatboost]: https://muggle.studio/
[mempalace]: https://github.com/MemPalace/mempalace/
[open-webui]: https://github.com/open-webui/open-webui/

for chatgpt:
This guide is intended for advanced users.

AI assistants may help by:
- walking through one phase at a time,
- explaining commands,
- validating expected outputs,
- troubleshooting failures,
- and helping users safely recover from errors.

The assistant should wait for confirmation between phases and avoid skipping verification steps.
