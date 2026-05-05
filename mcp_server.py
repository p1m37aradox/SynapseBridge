from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
import os
import uvicorn
import requests


# Set the path explicitly
ROOT_DIR = "/mnt/SynapseBridge"
mcp = FastMCP("SynapseBridge")

@mcp.tool()
async def check_mount():
    return f"Accessing: {ROOT_DIR}"

# Updated UI handler to show dynamic content
async def serve_ui(request):
    html = """
    <html>
    <head>
        <title>Synapse Bridge Index</title>
        <style>
            body { font-family: sans-serif; padding: 20px; line-height: 1.6; }
            ul { list-style-type: none; }
            li { margin: 5px 0; }
            a { text-decoration: none; color: #007bff; }
            a:hover { text-decoration: underline; }
            .folder { font-weight: bold; color: #333; margin-top: 15px; }
        </style>
    </head>
    <body>
        <h1>🌉 Synapse Bridge Node</h1>
        <p>Status: 🟢 Online</p>
        <hr>
        <ul>
    """
    
    # Walk through the shared zone and build links
    for root, dirs, files in os.walk(ROOT_DIR):
        # 1. Filter out hidden directories (like .git, .palace, .trash)
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        rel_path = os.path.relpath(root, ROOT_DIR)
        if rel_path == ".":
            display_path = "Root"
            prefix = ""
        else:
            display_path = rel_path
            prefix = rel_path + "/"
            html += f"<li class='folder'>📂 {display_path}/</li>"

        for file in sorted(files):
            if file.startswith('.') or file.endswith('.pyc') or file == "index.html":
                continue

            file_url = f"/files/{prefix}{file}"
            html += f"<li>&nbsp;&nbsp;&nbsp;📄 <a href='{file_url}'>{file}</a></li>"

    html += "</ul></body></html>"
    return HTMLResponse(content=html)

# --- MACHINE & MEMORY ENDPOINTS ---

async def health(request):
    return JSONResponse({"status": "ok"})

async def tools(request):
    return JSONResponse({
        "tools": [
            {"name": "check_mount", "description": "Verify access to shared root"},
            {"name": "query_memory", "description": "Semantic search through MemPalace"}
        ]
    })

async def query_memory(request):
    user_query = request.query_params.get("q", "")
    if not user_query:
        return JSONResponse({"error": "No query provided"}, status_code=400)

    # Payload for the ChromaDB instance running in Terminal 1
    payload = {
        "where": {},
        "n_results": 3,
        "query_texts": [user_query]
    }
    
    try:
        # Note: 'SynapseBridge-Main' is the wing we initialized in Phase 2
        response = requests.post(
    "http://localhost:8000/api/v2/collections/mempalace_closets/query",
    json=payload
)

        return JSONResponse(response.json())
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# Build the app with the /files mount added
app = Starlette(
    routes=[
        Route("/", serve_ui),
        Route("/health", health),
        Route("/tools", tools),
        Route("/query", query_memory),
        Mount("/sse", mcp.sse_app()),
        Mount("/files", app=StaticFiles(directory=ROOT_DIR), name="static"),
    ]
)

if __name__ == "__main__":
    print(f"🚀 Synapse Bridge starting at {ROOT_DIR}")
    uvicorn.run(app, host="0.0.0.0", port=8080)

