from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import FileResponse
from starlette.routing import Route, Mount
import os
import uvicorn

# Set the path explicitly
ROOT_DIR = "/mnt/SynapseBridge"
mcp = FastMCP("SynapseBridge")

@mcp.tool()
async def check_mount():
    return f"Accessing: {ROOT_DIR}"

# Define the UI handler
async def serve_ui(request):
    return FileResponse(os.path.join(ROOT_DIR, "index.html"))

# Build the app using standard Starlette components
# This avoids the 'AttributeError' entirely
app = Starlette(
    routes=[
        Route("/", serve_ui),
        Mount("/sse", mcp.sse_app()),
    ]
)

if __name__ == "__main__":
    print(f"🚀 Synapse Bridge starting at {ROOT_DIR}")
    uvicorn.run(app, host="0.0.0.0", port=8080)
