import asyncio
import httpx
import json
import time
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
import logging
logging.basicConfig(level=logging.DEBUG)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3.5:0.8b"

MEMORY_KEYWORDS = {
    "remember", "save", "store", "recall", "forget", "search",
    "memory", "memories", "memorize", "retrieve", "find", "lookup"
}

def needs_tools(text):
    return any(word in text.lower() for word in MEMORY_KEYWORDS)

async def stream_response(client, payload):
    full_thinking = ""
    full_content = ""
    final_message = {}
    in_thinking = False

    async with client.stream("POST", OLLAMA_URL, json=payload, timeout=300.0) as response:
        if response.status_code != 200:
            print(f"\n❌ Server Error ({response.status_code})")
            return None, None, None

        async for line in response.aiter_lines():
            if not line.strip():
                continue

            chunk = json.loads(line)
            msg = chunk.get("message", {})

            thinking_chunk = msg.get("thinking", "")
            if thinking_chunk:
                if not in_thinking:
                    print("\n💭 Thinking: ", end="", flush=True)
                    in_thinking = True
                print(thinking_chunk, end="", flush=True)
                full_thinking += thinking_chunk

            content_chunk = msg.get("content", "")
            if content_chunk:
                if in_thinking:
                    print("\n")
                    in_thinking = False
                    print("Qwen: ", end="", flush=True)
                elif not full_content:
                    print("\nQwen: ", end="", flush=True)
                print(content_chunk, end="", flush=True)
                full_content += content_chunk

            if chunk.get("done"):
                final_message = msg
                final_message["thinking"] = full_thinking
                final_message["content"] = full_content
                print()

    return full_thinking, full_content, final_message

async def route_tool(client, user_input, tools_response):
    tool_index = "\n".join(
        f"- {tool.name}: {(tool.description or '').splitlines()[0]}"
        for tool in tools_response.tools
    )

    router_messages = [
        {
            "role": "system",
            "content": (
                "You are a tool router. Given a user request and a list of available tools, "
                "respond ONLY with a JSON object like:\n"
                '{"tool": "tool_name", "args": {"key": "value"}}\n'
                "If no tool is needed, respond with: {\"tool\": null}\n"
                "Do not explain. Do not add any other text."
            )
        },
        {
            "role": "user",
            "content": f"Available tools:\n{tool_index}\n\nUser request: {user_input}"
        }
    ]

    resp = await client.post(
        OLLAMA_URL,
        json={"model": MODEL_NAME, "messages": router_messages, "stream": False, "think": False},
        timeout=300.0
    )
    result = resp.json()
    content = result.get("message", {}).get("content", "").strip()

    try:
        clean = content.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(clean)
        tool_name = parsed.get("tool")
        tool_args = parsed.get("args", {})
        if tool_name:
            return tool_name, tool_args
    except Exception:
        pass

    return None, None

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mempalace.mcp_server"]
    )

    print("Launching MemPalace MCP via stdio...")

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("Connected to MemPalace!")

            tools_response = await session.list_tools()
            print(f"Loaded {len(tools_response.tools)} MemPalace tools.")
            print("\n--- Chat Session Started (Type 'exit' to quit) ---")

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant with access to a memory system. "
                        "Only call tools when the user explicitly asks to save, retrieve, "
                        "search, or manage memories. For general conversation, respond directly."
                    )
                }
            ]

            while True:
                try:
                    user_input = input("\nYou: ")
                    if user_input.strip().lower() == "exit":
                        print("Ending session.")
                        break
                    if not user_input.strip():
                        continue
                except (KeyboardInterrupt, EOFError):
                    print("\nEnding session.")
                    break

                messages.append({"role": "user", "content": user_input})

                async with httpx.AsyncClient() as client:
                    try:
                        if needs_tools(user_input):
                            print("\n🔍 Routing to tool...")
                            tool_name, tool_args = await route_tool(client, user_input, tools_response)

                            if tool_name:
                                print(f"\n⚙️  [MemPalace]: {tool_name}...")
                                print(f"   Args: {json.dumps(tool_args, indent=2)}")

                                t_start = time.time()
                                tool_result = await session.call_tool(name=tool_name, arguments=tool_args)
                                elapsed = time.time() - t_start

                                print(f"   ✅ Completed in {elapsed:.2f}s")

                                tool_text = "Tool executed successfully."
                                if hasattr(tool_result, 'content') and tool_result.content:
                                    if isinstance(tool_result.content, list):
                                        tool_text = getattr(tool_result.content[0], 'text', str(tool_result.content[0]))
                                    else:
                                        tool_text = getattr(tool_result.content, 'text', str(tool_result.content))

                                print(f"   📦 Raw result ({len(tool_text)} chars):\n{tool_text[:500]}")

                                messages.append({"role": "tool", "content": tool_text})

                        payload = {
                            "model": MODEL_NAME,
                            "messages": messages,
                            "stream": True,
                            "think": True
                        }

                        _, _, final_message = await stream_response(client, payload)

                        if final_message:
                            messages.append(final_message)
                        else:
                            messages.pop()

                    except Exception as e:
                        print(f"\n❌ Error: {type(e).__name__}: {e}")
                        messages.pop()
                        continue

if __name__ == "__main__":
    asyncio.run(main())