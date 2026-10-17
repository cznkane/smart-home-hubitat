#!/bin/zsh
set -u
HEALTH="http://127.0.0.1:8080/healthz"
READY="http://127.0.0.1:8080/readyz"
echo "WebCoRE MCP status"
echo "=================="
if /usr/bin/curl -fsS --max-time 2 "$HEALTH" >/dev/null 2>&1; then echo "Health: live"; else echo "Health: OFFLINE"; fi
if /usr/bin/curl -fsS --max-time 2 "$READY" >/dev/null 2>&1; then echo "Readiness: ready"; echo "🟢 WebCoRE MCP ONLINE"; else echo "Readiness: NOT READY"; fi
read -k 1 "?Press any key to close..."
