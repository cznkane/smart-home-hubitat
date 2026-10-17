#!/bin/zsh
set -u
LABEL="com.kaneconsulting.webcore-mcp"
DOMAIN="gui/$UID"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
echo "Stopping WebCoRE MCP..."
/usr/bin/launchctl bootout "$DOMAIN" "$PLIST" 2>/dev/null || true
/bin/sleep 1
if /usr/bin/curl -fsS --max-time 2 http://127.0.0.1:8080/healthz >/dev/null 2>&1; then
  echo "STOP: health endpoint is still live. Another tunnel-client process may be running."
  echo "No processes were killed blindly."
  read -k 1 "?Press any key to close..."
  exit 1
fi
echo "WebCoRE MCP stopped."
read -k 1 "?Press any key to close..."
