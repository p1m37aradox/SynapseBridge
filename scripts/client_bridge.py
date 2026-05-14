import asyncio
import ollama
import os
import re
import json
import logging
import sys
from datetime import datetime
from mcp import ClientSession
from mcp.client.sse import sse_client

# --- 1. LOGGING SETUP ---
SHARED_LOG_DIR = "/mnt/SynapseBridge"
CLIENT_LOG_FILE = os.path.join(SHARED_LOG_DIR, "qwen_chat_history.log")
os.makedirs(SHARED_LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    handlers=[
        logging.FileHandler(CLIENT_LOG_FILE),
        logging.StreamHandler(sys.stdout) 
    ]
)
# To Reenable logging add a # infront of logging on the next line.
logging.disable(logging.CRITICAL)


logger = logging.getLogger("SynapseClient")

def log_interaction(role, content):
    logger.info(f"[{role.upper()}]: {content}")
    
    
# --- 2. CONFIGURATION ---
SERVER_URL = "http://127.0.0.1:8080/sse"
MODEL = "qwen2.5:3b" 
CONTEXT_PATH = "/mnt/SynapseBridge/scripts/context.txt"

async def main():
    print(f"🔗 Connecting to Synapse Bridge at {SERVER_URL}...")
    log_interaction("System", f"Connecting to Bridge. Log: {CLIENT_LOG_FILE}")
    
    async with sse_client(SERVER_URL) as streams:
        async with ClientSession(streams[0], streams[1]) as session:
            await session.initialize()
            
            tools_data = await session.list_tools()
            ollama_tools = []
            server_tool_names = [tool.name for tool in tools_data.tools]
            
            for tool in tools_data.tools:
                ollama_tools.append({
                    'type': 'function',
                    'function': {
                        'name': tool.name,
                        'description': tool.description,
                        'parameters': tool.inputSchema,
                    }
                })
            
            print(f"✅ {MODEL} armed with {len(ollama_tools)} tools.")

            while True:
                user_input = input("\n[Synapse User] > ")
                if user_input.lower() in ['exit', 'quit']: break
                log_interaction("User", user_input)

                if os.path.exists(CONTEXT_PATH):
                    with open(CONTEXT_PATH, 'r') as f:
                        system_context = f.read()
                else:
                    # FIXED: Added triple quotes for multi-line string
                    system_context = """# MISSION
You are the Synapse Bridge Agent. Your memory engine is MemPalace.

# TOOL DISCOVERY PROTOCOL
You have a limited set of registered tools.
- SOURCE CODE: The full logic is at: /mnt/SynapseBridge/.mcp_server.py
- ACTION: If you see a 'KnowledgeGraph' error, refer to the logic in .mcp_server.py to realize that drawer counts come from the collection, not the KG object.

# MEMPALACE WAKE-UP
1. Call mempalace_status.
2. If it fails, use mempalace_search to find recent activity.
3. Summarize findings.

# OPERATIONAL CONSTRAINTS
- Current Palace Path: /mnt/SynapseBridge/palace
- System: Termux/Debian Proot"""

                response = ollama.chat(
                    model=MODEL,
                    messages=[
                        {'role': 'system', 'content': system_context},
                        {'role': 'user', 'content': user_input}
                    ],
                    tools=ollama_tools,
                )

                message = response.get('message', {})
                content = message.get('content', '')
                tool_calls = message.get('tool_calls', [])

                if tool_calls:
                    for tool_call in tool_calls:
                        name = tool_call['function']['name']
                        
                        if name not in server_tool_names:
                            if name.startswith('mempal_'):
                                alt_name = name.replace('mempal_', 'mempalace_')
                                if alt_name in server_tool_names:
                                    log_interaction("System", f"Fuzzy Match: {name} -> {alt_name}")
                                    name = alt_name

                        raw_args = tool_call['function']['arguments']
                        clean_args = {k: (v['value'] if isinstance(v, dict) and 'value' in v else v) 
                                     for k, v in raw_args.items()}

                        log_interaction("System", f"Executing Tool: {name}({clean_args})")
                        
                        try:
                            result = await session.call_tool(name, clean_args)
                            for item in result.content:
                                log_interaction("Palace", item.text)
                        except Exception as e:
                            log_interaction("Error", str(e))
                else:
                    if content:
                        log_interaction("Qwen", content)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log_interaction("System", "Bridge Client Terminated.")
