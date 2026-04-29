# 🧠 SYNAPSE BRIDGE (v3.0.0)
### *The Agency Protocol: Transforming LLMs into Active Operators*

**SynapseBridge** is a technical framework designed to wrap around standard Large Language Models (LLMs) such as **ChatGPT (OpenAI)**, **Claude (Anthropic)**, **Gemini (Google)**, and **Llama (Meta)**. Its goal is to provide these non-agentic AI models with the memory, system access, and toolset required to perform autonomous tasks on a local device.

---

## ⚠️ USE AT YOUR OWN RISK (BETA)
**SynapseBridge is currently in early-stage Beta development.** By using this software, you acknowledge that you are granting an AI the ability to execute code and manipulate files on your local system. 
- **No Warranty**: Provided "as-is." Developers are not responsible for data loss or system corruption.
- **Experimental Agency**: AI models can hallucinate. Always monitor the Dispatcher’s logs.

---

## 🎯 THE MISSION
To transform a passive AI into an **Active Operator**. 
- **The Gap**: Standard AI models are restricted to text generation with no system presence.
- **The Bridge**: Provides a "Body" (System access) and a "Memory" (Contextual Persistence via MemPalace).
- **The Goal**: Move the AI from *responding* to a prompt to *executing* a task based on user intent.

---

## 🚀 INSTALLATION & QUICK START
To transition from a standard Debian environment to a **Subsidized SynapseBridge Environment**, follow the distribution deployment steps:

1.  **Deploy the Archive**:
    Unpack the distribution tarball into your home directory:
    ```bash
    tar -xzvf SynapseBridge.tar.gz && cd SynapseBridge
    ```
2.  **Run the Subsidizer**:
    Execute the setup script to install all core dependencies, including Rust 1.95+, Python-pip, ChromaDB, and MemPalace.
    ```bash
    bash bin/setup_env.sh
    ```
3.  **Activate the Environment**:
    ```bash
    source ~/.bashrc
    ```
    *Use the `sb` alias to return to the bridge at any time.*

---

## 🛠️ FUNCTIONAL COMPONENTS

### 1. Persistent Context (MemPalace)
* **Location**: `palace/`
* **Function**: Utilizes **MemPalace** and **ChromaDB** to provide a vector-searchable history of local files, manuals, and past session data.

### 2. Execution Core (The Dispatcher)
* **Location**: `core/`
* **Function**: Python-based logic (`cortex.py`) that parses AI JSON payloads into system commands.

### 3. Actuators & Scripts (The Binary)
* **Location**: `bin/`
* **Function**: A library of predefined bash/python scripts the AI triggers to interact with hardware and the filesystem.

### 4. System State (The Vault)
* **Location**: `data/`
* **Function**: Maintains `entities.json` to track system variables and project status.

---

## 🔒 SECURITY ARCHITECTURE (Gatekeeper v1.2.7)
* **Environment Isolation**: Execution is confined to the Debian `proot` layer.
* **Actuator Whitelisting**: The AI can only trigger approved scripts within the `bin/` directory.
* **Recycle Protocol**: Direct deletion is intercepted; files are moved to `~/SynapseBridge/RECYCLE_BIN/` for audit.

---

## 🌐 SOURCES & DEPENDENCIES
* **Termux & proot-distro**: [GitHub/termux](https://github.com/termux)
* **Debian GNU/Linux**: [Debian.org](https://www.debian.org/)
* **MemPalace**: [GitHub/tycoonbro/mempalace](https://github.com/tycoonbro/mempalace)
* **ChromaDB**: [GitHub/chroma-core/chroma](https://github.com/chroma-core/chroma)
* **Rust & Python**: Official toolchains for Aarch64.

---
*“Logic is the beginning of wisdom, not the end.”*
