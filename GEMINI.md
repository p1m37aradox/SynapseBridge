# 🌉 Synapse Bridge v0.0.3-beta System Context
You are the active agent for Synapse Bridge. 

## 🏗️ Architecture Map (Dual-Path Awareness)
- **Shared Zone (Debian):** /mnt/SynapseBridge
- **Shared Zone (Termux):** ~/storage/shared/SynapseBridge
- **Guest Root:** ~/SynapseBridge_Root (Internal Debian/venv)
- **Memory Palace:** /mnt/SynapseBridge/palace
- **Chroma Database:** /mnt/SynapseBridge/palace/db/chroma.sqlite3

## 📡 Port & API Protocol
- **Port 8000:** ChromaDB + MCP Bridge (The Core)
- **API Version:** **Always use /api/v2/ endpoints** for ChromaDB heartbeats and queries.
- **Port 443:** Pinggy External Tunnel (Mapping to Local 8000)

## 🛠️ Operational Rules
1. **Never** create files in the Guest Root; always use the Shared Zone.
2. **Primary Output:** Use `/mnt/SynapseBridge/GeminiGenerated` for all logs, reports, and generated code.
3. **Fallback Output:** If mount points fail, use `~/storage/shared/SynapseBridge/junk_drawer`.
4. **Database Maintenance:** Use sqlite3 directly for PRAGMA checks if bridge traffic fails.
5. **Hardware Access:** Use 'termux-battery-status' for host telemetry.

## ✅ Verification Protocol
The "Weld" is confirmed. Proceed with agentic tasks without re-confirming paths. If a path is "Not Found," immediately pivot to the Termux absolute path.
