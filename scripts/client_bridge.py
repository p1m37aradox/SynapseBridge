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
##logging.disable(logging.CRITICAL)

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
            
            # --- Tool Discovery ---
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
                if user_input.lower() in ['exit', 'quit']: 
                    break
                
                log_interaction("User", user_input)
                
                # Fetch fresh context
                if os.path.exists(CONTEXT_PATH):
                    with open(CONTEXT_PATH, 'r') as f:
                        system_context = f.read()
                else:
                    system_context = "You are the Synapse Bridge Agent."

                # Initialize conversation history for this turn
                messages = [
                    {'role': 'system', 'content': system_context},
                    {'role': 'user', 'content': user_input}
                ]

                # Initial chat call
                response = ollama.chat(
                    model=MODEL,
                    messages=messages,
                    tools=ollama_tools,
                    options={
                        "num_ctx": 4096,     
                        "temperature": 0.3,  
                        "num_predict": 1024 
                    }
                )

                message = response.get('message', {})
                tool_calls = message.get('tool_calls', [])

                if tool_calls:
                    messages.append(message) # Save Qwen's intent

                    for tool_call in tool_calls:
                        name = tool_call['function']['name']
                        
                        # Fuzzy matching logic
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
                            tool_output_text = "\n".join([item.text for item in result.content if hasattr(item, 'text')])
                            log_interaction("Palace", tool_output_text)

                            messages.append({
                                'role': 'tool',
                                'content': tool_output_text,
                                'name': name
                            })

                        except Exception as e:
                            error_msg = str(e)
                            log_interaction("Error", error_msg)
                            messages.append({
                                'role': 'tool',
                                'content': f"Error: {error_msg}",
                                'name': name
                            })

                    # Final summary call
                    final_response = ollama.chat(model=MODEL, messages=messages)
                    final_content = final_response.get('message', {}).get('content', '')
                    if final_content:
                        log_interaction("Qwen", final_content)
                else:
                    content = message.get('content', '')
                    if content:
                        log_interaction("Qwen", content)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log_interaction("System", "Bridge Client Terminated.")
