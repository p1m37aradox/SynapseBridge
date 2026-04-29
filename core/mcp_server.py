from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("SynapseBridge")
ROOT = os.path.expanduser("~/SynapseBridge_Root")

@mcp.tool()
def read_project_file(filename: str):
    path = os.path.join(ROOT, filename)
    return open(path).read() if os.path.exists(path) else "Error"

if __name__ == "__main__":
    from mcp.server.sse import SseServerTransport
    from starlette.applications import Starlette
    from starlette.routing import Route
    import uvicorn

    sse = SseServerTransport("/messages")

    async def handle_sse(request):
        async with sse.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
            await mcp.server.run(read_stream, write_stream, mcp.server.create_initialization_options())

    app = Starlette(routes=[Route("/sse", endpoint=handle_sse), Route("/messages", endpoint=sse.handle_post_message, methods=["POST"])])
    uvicorn.run(app, host="0.0.0.0", port=8080)