from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
import os
import uvicorn

# --- THE BRAIN: Official MemPalace Imports ---
try:
    from mempalace.searcher import search_memories
    from mempalace.config import MempalaceConfig
    MEMPAL_AVAILABLE = True
except ImportError:
    MEMPAL_AVAILABLE = False

# --- CONFIGURATION ---
ROOT_DIR = "/mnt/SynapseBridge"
PALACE_PATH = os.path.join(ROOT_DIR, "palace")

# Initialize MCP with the name that shows up in Gemini
mcp = FastMCP("SynapseBridge")

# --- TOOLS ---

@mcp.tool()
async def check_mount():
    """Verify hardware access to the shared project zone."""
    exists = os.path.exists(ROOT_DIR)
    readable = os.access(ROOT_DIR, os.R_OK)
    return {
        "status": "ok" if (exists and readable) else "error",
        "path": ROOT_DIR,
        "files_sample": os.listdir(ROOT_DIR)[:5] if exists else []
    }

@mcp.tool()
async def query_memory(q: str, wing: str = "SynapseBridge-Main"):
    """
    Search the MemPalace semantic database.
    Use this to recall past technical decisions, audit logs, or project history.
    """
    if not MEMPAL_AVAILABLE:
        return {"error": "MemPalace library not found in venv."}
    
    try:
        # Direct call to the official MemPalace search logic
        results = search_memories(
            query=q,
            palace_path=PALACE_PATH,
            wing=wing,
            n_results=5,
            max_distance=1.5 
        )
        return results
    except Exception as e:
        return {"error": str(e), "hint": "Ensure 'mempalace mine' has been run on this path."}

# --- WEB INTERFACE (The Dashboard) ---

async def serve_ui(request):
    html = """
    <html>
    <head>
        <title>Synapse Bridge Node</title>
        <style>
            body { font-family: 'Courier New', monospace; background: #0f0f0f; color: #00ff41; padding: 20px; }
            a { color: #00ff41; text-decoration: none; border-bottom: 1px dashed; }
            .folder { color: #ffff00; font-weight: bold; margin-top: 10px; }
            .status { color: #00ff41; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>🌉 SYNAPSE BRIDGE NODE v0.0.3.1b</h1>
        <p>System Status: <span class="status">ONLINE</span></p>
        <p>Memory Engine: """ + ("OFFICIAL" if MEMPAL_AVAILABLE else "EMULATED") + """</p>
        <hr>
        <div id="file-browser">
    """
    
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.')] # Hide junk
        rel_path = os.path.relpath(root, ROOT_DIR)
        display_path = "ROOT" if rel_path == "." else rel_path
        
        if rel_path != ".":
            html += f"<div class='folder'>📂 {display_path}/</div>"
            
        for file in sorted(files):
            if file.startswith('.') or file == "index.html": continue
            path_prefix = "" if rel_path == "." else rel_path + "/"
            html += f"<div>&nbsp;&nbsp;&nbsp;📄 <a href='/files/{path_prefix}{file}'>{file}</a></div>"

    html += "</div></body></html>"
    return HTMLResponse(content=html)

# --- SYSTEM ENDPOINTS ---

async def health(request):
    return JSONResponse({"status": "active", "mempalace": MEMPAL_AVAILABLE})

# --- APP ASSEMBLY ---

app = Starlette(
    routes=[
        Route("/", serve_ui),
        Route("/health", health),
        Mount("/sse", mcp.sse_app()), # This is the "Tunnel" entrance
        Mount("/files", app=StaticFiles(directory=ROOT_DIR), name="static"),
    ]
)

# --- ENTRY POINT ---

def main():
    """The entry point for the mempalace-mcp system command."""
    print(f"🚀 Synapse Bridge: Welding {ROOT_DIR} to Gemini...")
    uvicorn.run(app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
