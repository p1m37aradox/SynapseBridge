#!/usr/bin/env python3
import os
import shutil

# Configuration
TARGET = "/root/SynapseBridge_Root/venv/lib/python3.13/site-packages/mempalace/cli.py"
BACKUP = TARGET + ".bak"

# 1. Discovery Function (Uses urllib to avoid venv dependency issues)
MENU_FUNC = """
def select_model_interactive():
    import json
    from urllib.request import Request, urlopen
    try:
        req = Request("http://localhost:11434/api/tags")
        with urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode())
            models = [m['name'] for m in data.get('models', [])]
        
        if not models:
            return "qwen2.5:3b"

        print("\\n--- [ SYNAPSE BRIDGE: MODEL DISCOVERY ] ---")
        for i, m in enumerate(models):
            print(f"  [{i}] {m}")
        
        choice = input(f"\\nSelect model index [0-{len(models)-1}] (default 0): ").strip()
        index = int(choice) if choice.isdigit() else 0
        selected = models[index] if 0 <= index < len(models) else models[0]
        print(f"✅ Active Model: {selected}\\n")
        return selected
    except Exception:
        return "qwen2.5:3b"
"""

# 2. Logic Block Replacement (Handles indentation safely)
REPLACEMENT_LOGIC = """        # Synapse Bridge: Interactive selection for Ollama users
        passed_model = getattr(args, "llm_model", None)
        if passed_model is None and provider_name == "ollama":
            provider_model = select_model_interactive()
        else:
            provider_model = passed_model or "qwen2.5:3b"
        try:"""

def apply_patch():
    if not os.path.exists(BACKUP):
        print("❌ Backup not found. Please restore manually first.")
        return

    # Read from backup to ensure we have a clean source
    with open(BACKUP, 'r') as f:
        content = f.read()

    # Inject the menu function
    if "def select_model_interactive():" not in content:
        content = content.replace("import argparse", "import argparse" + MENU_FUNC)

    # Replace the hardcoded model assignment block
    target_block = '        provider_model = getattr(args, "llm_model", "gemma4:e4b") or "gemma4:e4b"\n        try:'
    content = content.replace(target_block, REPLACEMENT_LOGIC)

    # Clean up argparse defaults and comments
    content = content.replace('default="gemma4:e4b"', 'default=None')
    content = content.replace('gemma4:e4b', 'qwen2.5:3b')

    with open(TARGET, 'w') as f:
        f.write(content)
    
    print("🚀 Synapse Patch Applied.")

if __name__ == "__main__":
    apply_patch()
