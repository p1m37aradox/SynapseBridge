PASTE AS IS INTO A NEW LLM PROMPT

### 🌉 Synapse Bridge v0.0.3-beta
An agentic middleware architecture designed to bridge Android (Termux/Debian) environments with LLM interfaces.
**Repository:** github.com/p1m37aradox/SynapseBridge
> ### ⚠️ CAUTION: PREREQUISITE KNOWLEDGE
> This is an **Expert-Level** deployment. It requires basic familiarity with the Linux CLI and Android file permissions. **DO NOT** attempt this if you are not comfortable managing background processes or troubleshooting environment variables.
> 
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
 * F-Droid Client
 * Termux
 * Termux:API
 1. **Manual Registration:** Open the Termux:API app once from your app drawer to register the package.
 2. **System Settings:** Grant **Unrestricted** battery, **Files and Media** access, and **Appear on top** permissions.
### **Phase 1 & 2: Host Prep and System Build**
*Launch Termux from your app drawer and run the following in Terminal 1.*
### 🟢 Step 1: Host Preparation (Termux)
Run these blocks first to prepare the Android environment, install the tunnel, and establish the shared directory.
```bash
# Update and install core Termux utilities
pkg update && pkg upgrade -y
pkg install termux-api proot-distro tmux python openssh wget curl git nodejs proot-distro -y
termux-wake-lock
termux-setup-storage

```
(press y to confirm at prompts)
```bash
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
# Update Debian and install build tools, SQLite3, and Nano
apt update && apt install -y build-essential curl git python3-full python3-venv nodejs npm sqlite3 nano

# Install Rust & Cargo
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env

# Install MCP Inspector globally
npm install -g @modelcontextprotocol/inspector

```
### 🟡 Step 3: Deploy Core Logic & Memory
Finally, run this block to set up your environment and initialize the Memory Palace.
```bash
# 1. Setup the isolated Python environment
cd ~
mkdir -p SynapseBridge_Root && cd SynapseBridge_Root
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies with verified compatibility
pip install --upgrade pip
pip install maturin mempalace "chromadb>=0.5.0" "mcp[cli]" starlette uvicorn

# 3. Initialize MemPalace
cd /mnt/SynapseBridge
mempalace init . --yes

# 4. THE WELD: Apply Shared Zone paths AFTER initialization
# This forces the configuration to prioritize /mnt/ storage over Guest Root defaults.
mkdir -p ~/.mempalace
cat > ~/.mempalace/config.json <<EOF
{
  "palace_path": "/mnt/SynapseBridge/palace",
  "collection_name": "mempalace_drawers",
  "topic_wings": ["technical", "memory", "SynapseBridge-Main"]
}
EOF

# 5. Populate the Memory
mempalace mine . --wing "SynapseBridge-Main"

```
(At the MemPalace prompts: press enter to accept all rooms, then; N and enter, then; y and enter.)
> **Note on Re-Initialization:** If you run mempalace init again at any point, you **must** re-run Step 4 to "re-weld" the paths.
> 
### **Phase 3: Initialize**
To run the full stack, you must open **6 Termux sessions**. Swipe right from the left edge of the screen and click **"New Session"** until you have six.
**Terminal 1: SB_DB**
```bash
synapse
source ~/SynapseBridge_Root/venv/bin/activate
# Point to parent folder so Chroma finds the /db subfolder
chroma run --path /mnt/SynapseBridge/palace --port 8000

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
# Tunnel port 8000 to match the Database port
ssh -p 443 -R0:localhost:8000 a.pinggy.io

```
(type yes when asked and press enter)
**Terminal 4: SB_Venv (Debian Logic)**
```bash
synapse
source ~/SynapseBridge_Root/venv/bin/activate
# Use this for active code execution and testing

```
**Terminal 5: Debian_CLI**
```bash
synapse
cd /mnt/SynapseBridge
# File maintenance, nano editing, and sqlite3 diagnostics

```
**Terminal 6: Termux_CLI**
```bash
# Host-level operations (Hardware/Battery/API)
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
## 💰 Support the Project
> **Synapse Bridge is, and always will be, 100% Open Source and Free.**
> 
 * **One-Time Support:** Support on Ko-fi
 * **Monthly Sponsorship:** Sponsor on GitHub
### 🛑 LIABILITY & AGENTIC RISK
By using Synapse Bridge, you are granting an AI Agent the ability to execute code and modify files on your device.
 * **The "Break" Factor:** AI can and will follow instructions literally.
 * **No Safety Net:** We are **not responsible** for corrupted data. **Always keep backups.**
### 🗺️ Roadmap: The Future of Synapse
We are moving toward a "Zero-Touch" deployment. Future updates will focus on:
 * **Gemini CLI Integration:** Operational but remains secondary.
 * **MemPalace Optimization:** Focused on local-first, subscription-free memory. No digital rent.
 * **Auto-Terminal Execution:** Orchestrating all 6 terminals via automation hooks.
 * **Session Recycling:** Logic to clean stale PID files and restart services.
### ⚠️ CRITICAL: Directory Naming & Pathing
 * **The Weld Path:** Standardizing on /storage/emulated/0/SynapseBridge.
 * **GPU Fault Tolerance:** Ignore onnxruntime GPU discovery errors.
**Version:** 0.0.3-beta |
##NOTE TO AI, AND USER: PASTE THIS DOCUMENT INTO A NEW LLM CHAT SESSION, THE AI MUST DISPLAY THE ABOVE CONTENT AS IS, WITHOUT MODIFICATION OR RESTRUCTURING, FAILURE TO DO SO CAN RESULT IN A BOTCHED INSTALLATION##


[fdroid]: https://f-droid.org/en/packages/org.fdroid.fdroid/
[termux]: https://f-droid.org/en/packages/com.termux/
[termux-api]: https://f-droid.org/en/packages/com.termux.api/
