PASTE AS IS INTO A ANDROID LLM PROMPT

### 🌉 Synapse Bridge v0.0.6.2b-GEMMA/QWEN
This version establishes a secure, unified MCP (Model Context Protocol) bridge specifically optimized for Gemma and Qwen running in Ollama, on a proot Debian environment. It provides the AI Agent with low-latency access to the Android filesystem, hardware APIs, and an embedded memory engine.

Testing with: Qwen2.5:3b and Gemma:2b

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


### 🟡 Step 3: Move MCP File and Edit Mempalace CLI
(YOU CAN MODIFY .synapse_mcp.py FILE IN SynapseBridge/scripts TO ADD CUSTOM TOOLS,
use the alias sb-sync to update it throughout the system after this step).
```bash
# Copy the shared MCP script (.synapse_mcp.py) to SynapseBridge_Root - We do it to reduce token counts.
sb-init
sb-sync

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
### 🟡 Step 5: Download and install Ollama, Gemma:2b and Qwen2.5:3b
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
4. Pull qwen2.5:3b model into Ollama
```bash
ollama pull qwen2.5:3b

```
4. Allow Qwen to to see MCP tools via script.
```bash
#Pip install MCP httpx
pip install ollama mcp httpx

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

#Start Mempalace with model selection (from cli.py patch, choose qwen2.5:3b if it doesn't default to it.
mempalace init . --yes

```

<img src="https://raw.githubusercontent.com/p1m37aradox/SynapseBridge/refs/heads/local-qwen-gemma/media/Screenshot_20260516-223328.png" width="350" alt="Synapse Bridge UI">


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

<img src="https://raw.githubusercontent.com/p1m37aradox/SynapseBridge/refs/heads/local-qwen-gemma/media/Screenshot_20260514-151232.png" width="350" alt="Synapse Bridge UI">

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
**To run the full stack without custom UI, you must open **6 Termux sessions**. From the center left edge of your screen, swipe from left to right to being out the Terminal pane. Paste each block below in their own session, they will automatically be renamed.

<img src="https://raw.githubusercontent.com/p1m37aradox/SynapseBridge/refs/heads/local-qwen-gemma/media/Screenshot_20260514-154307.png" width="350" alt="Synapse Bridge UI2">

**Terminal 1: synapse-mempalace-mcp (MCP)**
```bash
printf '\e]1;synapse-mempalace-mcp\a'
sb-deb
sb-venv-activate
sb-mcp

```
**Terminal 2: Qwen + MemPalace**
```bash
printf '\e]1;QWEN2.5:3b+mempalace\a'
sb-deb
sb-venv-activate
sb-chat

```
**Terminal 3: SB_Venv (Debian Logic)**
```bash
printf '\e]1;SB_Venv\a'
sb-deb
source ~/SynapseBridge_Root/venv/bin/activate

```
**Terminal 4: Debian_CLI**
```bash
printf '\e]1;Debian_CLI\a'
sb-deb
cd /mnt/SynapseBridge

```
**Terminal 5: Termux_CLI**
```bash
printf '\e]1;Termux_CLI\a'
cd ~
sb-init

```
**Terminal 6: Ollama**
```bash
printf '\e]1;Ollama\a'
sb-deb
ollama

```

Standard UI- After initial install is complete, to restore environment:
* re open 6 terminals
* execute the bash commands in the terminals in order.

Type "mempalace wake up" in the Qwen window.

### 🟡 Step 8: (Optional) ChatBoost App
We found this might be a useful tool. We will be testing it more later. It successfully loaded 3 tools from the mcp during our testing but our MCP requires more customization for it to fully function. (have not tried to load our client script into the app)

[Chatboost][chatboost]

1. Start the MCP server in a fresh terminal:
```bash
sb-deb
sb-init
sb-mcp

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
