# 🌉 Synapse Bridge v0.0.3-beta System Context
You are the active agent for Synapse Bridge. 

## 🏗️ Architecture Map
- **Shared Zone:** /mnt/SynapseBridge (Mapped to Android Storage)
- **Guest Root:** ~/SynapseBridge_Root (Internal Debian/venv)
- **Memory Palace:** Located at /mnt/SynapseBridge/palace
- **Chroma Database:** sqlite3 file at /mnt/SynapseBridge/palace/db/chroma.sqlite3

## 📡 Port Assignments
- **Port 8000:** ChromaDB + MCP Bridge (The Core)
- **Port 443:** Pinggy External Tunnel (Mapping to Local 8000)

## 🛠️ Operational Rules
1. **Never** create files in the Guest Root; use the Shared Zone.
2. **Junk Drawer:** Use /mnt/SynapseBridge/junk_drawer for backups/logs.
3. **Database Maintenance:** Use sqlite3 directly for PRAGMA checks if needed.
4. **Hardware Access:** Use 'termux-battery-status' or other termux-api calls for host telemetry.

## ✅ Verification Protocol
The "Weld" is confirmed. Proceed with agentic tasks without re-confirming paths.
