import os
import sys
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route, Mount, Router
from starlette.staticfiles import StaticFiles

# --- 1. CORE LOGIC IMPORT ---
try:
    import mempalace.mcp_server as mempal_core
except ImportError:
    print("❌ Critical: mempalace package not found. Run in venv.")
    sys.exit(1)

# --- 2. CONFIGURATION ---
ROOT_DIR = "/mnt/SynapseBridge"
mcp = FastMCP("SynapseBridge")

# --- 3. THE TOOL BRIDGE ---
@mcp.tool()
async def mempal_status():
    """Total drawers and wing/room breakdown."""
    return mempal_core.handle_request({"method": "mempalace_status", "params": {}})

@mcp.tool()
async def mempal_search(q: str, wing: str = None):
    """Semantic search across the palace."""
    return mempal_core.handle_request({"method": "mempalace_search", "params": {"q": q, "wing": wing}})

@mcp.tool()
async def check_mount():
    """Verify hardware access to the shared project zone."""
    return {"status": "ok" if os.path.exists(ROOT_DIR) else "error", "path": ROOT_DIR}

# --- 4. THE PATH-SLICER MIDDLEWARE (v0.0.5.9.1) 
mcp_app = mcp.sse_app()

class MCPPathFixMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            new_scope = dict(scope)
            # Kill the root_path to prevent the /sse/sse recursion
            new_scope["root_path"] = ""
            
            # If the SDK sends /sse/sse, we slice it back to /sse
            if scope["path"] == "/sse/sse":
                new_scope["path"] = "/sse"
            
            await self.app(new_scope, receive, send)
        else:
            await self.app(scope, receive, send)

mcp_fixed_app = MCPPathFixMiddleware(mcp_app)

# --- 5. THE CLEAN ROUTER (v0.0.5.9.2 - Session Matcher) ---
router = Router(
    routes=[
        # Route handles the initial GET/HEAD handshake
        Route("/sse", endpoint=mcp_fixed_app, methods=["GET", "POST", "HEAD"]),
        
        # Mount /messages to catch EVERYTHING after it (like /messages/ or ?session_id=...)
        # This is the secret sauce for the POST communication channel
        Mount("/messages", app=mcp_fixed_app),
        
        Route("/", lambda r: HTMLResponse("<h1>Synapse Bridge v0.0.5.9.2</h1>"), methods=["GET", "HEAD"]),
        Mount("/files", StaticFiles(directory=ROOT_DIR), name="static"),
    ],
    redirect_slashes=False 
)

app = Starlette()
app.mount("/", router)

# --- 6. EXECUTION ---
def main():
    os.system("fuser -k 8080/tcp > /dev/null 2>&1")
    
    print("🚀 UNIFIED BRIDGE ONLINE (v0.0.5.8.1 - Iron Weld)")
    print("  -> Handshake: http://127.0.0.1:8080/sse")
    print("  -> Mailbox:   http://127.0.0.1:8080/messages")
    print("  -> Files:     http://127.0.0.1:8080/files")
    
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")

if __name__ == "__main__":
    main()
