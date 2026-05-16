import sys
import os
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route, Mount, Router
from starlette.staticfiles import StaticFiles

# 1. Environment: Point to the venv inside Root
VENV_SITES = "/root/SynapseBridge_Root/venv/lib/python3.13/site-packages"
if VENV_SITES not in sys.path:
    sys.path.insert(0, VENV_SITES)

# 2. Initialization
ROOT_DIR = "/mnt/SynapseBridge"
mcp = FastMCP("SynapseBridge")

# 3. Custom Tools (Decoupled Logic)
@mcp.tool()
async def mempalace_status():
    """Total drawers and wing/room breakdown."""
    from mempalace.mcp_server import _get_collection, _config
    from mempalace.palace_graph import graph_stats
    
    col = _get_collection()
    
    try:
        # Pass collection directly to avoid the KnowledgeGraph vs Collection type error
        nodes, _ = graph_stats(col=col)
        drawer_count = sum(d.get('count', 0) for d in nodes.values())
        stats = {"nodes": nodes}
    except Exception as e:
        drawer_count = col.count() if hasattr(col, 'count') else "Connected"
        stats = {"error": str(e)}

    return {
        "status": "Online",
        "drawers": drawer_count, 
        "path": _config.palace_path if _config else "unknown",
        "graph_stats": stats
    }

@mcp.tool()
async def mempalace_search(q: str = "", wing: str = None, limit: int = 5):
    """Semantic search. Defaults to limit=5 if not provided."""
    from mempalace.mcp_server import search_memories, _config
    
    clean_q = q if isinstance(q, str) else ""
    clean_limit = limit if isinstance(limit, int) else 5

    try:
        res = search_memories(query=clean_q, palace_path=_config.palace_path, wing=wing, n_results=clean_limit)
        return res
    except Exception as e:
        return f"Search Error: {str(e)}"

@mcp.tool()
async def mempalace_get_taxonomy():
    """Full wing -> room hierarchy."""
    from mempalace.mcp_server import _get_collection, _call_kg
    try:
        try:
            from mempalace.palace_graph import get_taxonomy
        except ImportError:
            from mempalace.palace_logic import get_taxonomy

        col = _get_collection()
        return _call_kg(lambda kg: get_taxonomy(kg)) if col else "Palace not found"
    except Exception as e:
        return f"Taxonomy Tool unavailable: {str(e)}"
    
@mcp.tool()
async def mempalace_diary_write(entry_text: str, wing: str = "daily_logs", room: str = "general"):
    """Writes a diary entry to record session summaries or notes."""
    from mempalace.mcp_server import _get_collection, _call_kg
    from mempalace.palace_logic import diary_write
    
    col = _get_collection()
    if not col: return "Error: Palace connection offline."

    try:
        result = _call_kg(lambda kg: diary_write(
            kg=kg, 
            collection=col, 
            text=entry_text, 
            wing=wing, 
            room=room,
            agent_name="SynapseBridge"
        ))
        return f"✅ Entry secured in {wing}/{room}: {result}"
    except Exception as e:
        return f"❌ Diary Write Failed: {str(e)}"

@mcp.tool()
async def mempalace_list_wings():
    """List all wings via graph stats."""
    from mempalace.mcp_server import _get_collection, _call_kg
    from mempalace.palace_graph import graph_stats

    col = _get_collection()
    if not col: return "No collection"

    stats = _call_kg(lambda kg: graph_stats(kg))
    return stats.get("wings", "No wing data available")

# 4. SSE Infrastructure & Path Fixing
mcp_app = mcp.sse_app()

class MCPPathFixMiddleware:
    def __init__(self, app): 
        self.app = app
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            new_scope = dict(scope)
            new_scope["root_path"] = ""
            if scope["path"] == "/sse/sse": 
                new_scope["path"] = "/sse"
            await self.app(new_scope, receive, send)
        else: 
            await self.app(scope, receive, send)

mcp_fixed_app = MCPPathFixMiddleware(mcp_app)

router = Router(routes=[
    Route("/", lambda r: HTMLResponse("<h1>Synapse Bridge: Decoupled</h1>")),
    Route("/sse", endpoint=mcp_fixed_app, methods=["GET", "POST", "HEAD"]),
    Mount("/messages", app=mcp_fixed_app),
    Mount("/files", StaticFiles(directory=ROOT_DIR), name="static"),
])

app = Starlette()
app.mount("/", router)

if __name__ == "__main__":
    os.system("fuser -k 8080/tcp > /dev/null 2>&1")
    print("🚀 DECOUPLED BRIDGE STARTING...")
    uvicorn.run(app, host="0.0.0.0", port=8080)
