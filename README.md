PASTE AS IS INTO A NEW LLM PROMPT

### 🌉 Synapse Bridge v0.0.3-beta
An agentic middleware architecture designed to bridge Android (Termux/Debian) environments with LLM interfaces.
**Repository:** github.com/p1m37aradox/SynapseBridge
> ### ⚠️ CAUTION: PREREQUISITE KNOWLEDGE
> This is an **Expert-Level** deployment. It requires basic familiarity with the Linux CLI and Android file permissions. **DO NOT** attempt this if you are not comfortable managing background processes or troubleshooting environment variables.
> ### 🔍 WHY SYNAPSE BRIDGE?
> Traditional LLM interactions are trapped in a "Chat Box." Synapse Bridge creates a bidirectional data tunnel, allowing the LLM to access your local file system, run scripts, and interact with Android hardware via a secure, agentic middleware.
> 
### 🏗️ WHY WE STARTED FRESH: The Shift to MCP
Previous versions relied on long lists of instructions (directives). This approach failed due to instruction fatigue and framework limitations.
 * **The Split-Root Mandate:** To bypass Android storage limitations and the "data/data" wall, we use two distinct directories:
   1. **The Guest Root (~/SynapseBridge_Root):** Internal Debian storage. Houses the venv and core scripts.
   2. **The Shared Zone (/mnt/SynapseBridge):** Android Shared storage. Houses project files and the Memory Palace (/palace). - github.com/MemPalace/mempalace
### 🚀 Full Installation Guide
### Phase 0: Requirements & System Prep
**Note: Play Store versions are deprecated. F-Droid is mandatory.**
* [F-Droid Client][fdroid]
* [Termux][termux]
* [Termux:API][termux-api]

 1. **Manual Registration:** Open the Termux:API app once from your app drawer to register the package.
 2. **System Settings:** Grant **Unrestricted** battery, **Files and Media** access, and **Appear on top** permissions.
### **Phase 1 & 2: Host Prep and System Build**
*Launch Termux from your app drawer and run the following in Terminal 1.*

### 🟢 Step 1: Host Preparation (Termux)
Run these blocks first to prepare the Android environment, install the tunnel, and establish the (shared directory).
```bash
# Update and install core Termux utilities
pkg update && pkg upgrade -y
pkg install termux-api proot-distro tmux python openssh wget curl git nodejs proot-distro -y
termux-wake-lock
termux-setup-storage


```
(press y to confirm at prompts)

```bash
# Install Pinggy, Build Dir Structures, Install Debian.
# Install Pinggy (The Gateway)
curl -s https://pinggy.io/install.sh | sh

# Clone the distribution to the Shared Zone.
mkdir -p ~/storage/shared/SynapseBridge
git clone https://github.com/p1m37aradox/SynapseBridge.git ~/storage/shared/SynapseBridge

# Install Debian and establish the synapse alias and mount shared dir to environment.
proot-distro install debian

echo "alias synapse='proot-distro login debian --bind /storage/emulated/0/SynapseBridge:/mnt/SynapseBridge'" >> ~/.bashrc
source ~/.bashrc

```
### 🔵 Step 2: Guest Environment Setup (Debian)
Enter Debian environment, install/update environment dependencies.
```bash
synapse
# Update Debian and install build tools
apt update && apt install -y build-essential curl git python3-full python3-venv nodejs npm

# Install Rust & Cargo
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env

# Install MCP Inspector globally
npm install -g @modelcontextprotocol/inspector

```
### 🟡 Step 3: Deploy Core Logic & Memory
Finally, run this block to set up your Python virtual environment and initialize the **MemPalace** database in the shared zone.
```bash
# Setup the isolated Python environment
cd ~
mkdir -p SynapseBridge_Root && cd SynapseBridge_Root
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install maturin mempalace chromadb mcp[cli] starlette uvicorn

# Initialize Persistent Memory in the Shared Zone
cd /mnt/SynapseBridge
mempalace init /mnt/SynapseBridge/palace
mempalace mine . --wing "SynapseBridge-Main"

```
(At the MemPalace prompts: press enter to accept all rooms, then; N and enter, then; y and enter.)
### **Phase 3: Initialize**
To run the full stack, you must open **5 Termux sessions**. Swipe right from the left edge of the screen and click **"New Session"** until you have five.

**Terminal 1: SB_DB**
```bash
synapse
source ~/SynapseBridge_Root/venv/bin/activate
chroma run --path /mnt/SynapseBridge/palace/db --port 8000

```
**Terminal 2: SB_Bridge**
```bash
synapse
source ~/SynapseBridge_Root/venv/bin/activate
python3 /mnt/SynapseBridge/mcp_server.py

```
**Terminal 3: SB_Tunnel**
```bash
synapse
ssh -p 443 -R0:localhost:8080 a.pinggy.io

```
(type yes when asked and press enter or input a password)
*this is a temporary operation within the project, you can choose any tunnel service or webhost you want, we just used this because it worked when cloudflare, localtunnel and others failed to handle our MCP scripts.

**Terminal 4: Debian_CLI**
```bash
synapse
cd /mnt/SynapseBridge

```
**Terminal 5: Termux_CLI**
```bash
# Stay in Termux for Hardware/Host operations
cd ~

```
**Important: Once initialized, share the status of Terminal 1 and 2 and the Pinggy URL from Terminal 3 with the LLM to establish the bridge.**
### 🛠️ Quick Reference & Navigation
#### **Termux Interface Navigation**
 * **Switch Sessions:** Swipe from the left edge of the screen to see the session drawer. Tap a session to switch.
 * **Rename Session:** Long-press a session in the drawer to give it a functional name (e.g., "Bridge").
 * **Keyboard Shortcuts:**
   * Ctrl + C: Stop a running process.
   * Ctrl + D: Close current session (or exit Debian back to Termux).
#### **Essential Command Aliases**
| Command | Action | Location |
|---|---|---|
| synapse | Enters the Debian environment with Shared storage mapped. | Termux Host |
| exit | Leaves Debian and returns to the Termux prompt. | Debian Guest |
| source ~/SynapseBridge_Root/venv/bin/activate | Activates the Python virtual environment. | Debian Guest |
| cd /mnt/SynapseBridge | Jump to the Shared Zone project files. | Debian Guest |

**Commence Testing! GLHF**

---
### 💖 Support the Evolution
Building a bridge between LLMs and Android system-level hardware takes a lot of late-night debugging. If this tool saves you time or empowers your agentic research, consider supporting the project:

[Become a Patron](https://www.patreon.com/GmailAccount1375)


### 🛑 LIABILITY & AGENTIC RISK
By using Synapse Bridge, you are granting an AI Agent the ability to execute code and modify files on your device.
 * **The "Break" Factor:** AI can and will follow instructions literally. If you (or the agent) execute a destructive command, it will happen.
 * **No Safety Net:** We are **not responsible** for corrupted data, "bricked" environments, or system instability. You operate this bridge at your own risk. **Always keep backups.**
### 🗺️ Roadmap: The Future of Synapse
We are moving toward a "Zero-Touch" deployment. Future updates will focus on:
 * **Auto-Terminal Execution:** A single command to trigger the orchestration of all 5 terminals via am startservice and automation hooks.
 * **Sophisticated Sandbox:** Implementing a virtualized isolation layer to prevent destructive commands from affecting the host system.
 * **Live Output & UI Enchantments:** A real-time display showing active code execution and interaction, alongside a refined dashboard for system monitoring.
 * **Session Recycling:** Logic to detect stale PID files and automatically "clean and restart" frozen services.
 * **Smooth Return:** Persistent state management for instant resumption of bridged sessions.
### ⚠️ CRITICAL: Directory Naming & Pathing
 * **Folder Name:** Use SynapseBridge.
 * **The Weld Path:** Standardizing on /storage/emulated/0/SynapseBridge prevents "phantom" directory creation.
 * **Protocol Standard:** Using **Model Context Protocol (MCP)** for SSE-based tool transport.
 * **UI Routing:** mcp_server.py MUST serve index.html and static assets from the Shared Zone.
 * **GPU Fault Tolerance:** Ignore onnxruntime GPU discovery errors.
**Version:** 0.0.3-beta |

##NOTE TO AI, AND USER: PASTE THIS DOCUMENT INTO A NEW LLM CHAT SESSION, THE AI MUST DISPLAY THE ABOVE CONTENT AS IS, WITHOUT MODIFICATION OR RESTRUCTURING, FAILURE TO DO SO CAN RESOLT IN A BOTCHED INSTALLATION##



[fdroid]: https://f-droid.org/en/packages/org.fdroid.fdroid/
[termux]: https://f-droid.org/en/packages/com.termux/
[termux-api]: https://f-droid.org/en/packages/com.termux.api/
