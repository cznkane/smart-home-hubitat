#!/bin/zsh
set -u
LABEL="com.kaneconsulting.webcore-mcp"
DOMAIN="gui/$UID"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
HEALTH="http://127.0.0.1:8080/healthz"
READY="http://127.0.0.1:8080/readyz"
echo "WebCoRE MCP startup"
echo "==================="
if [[ ! -f "$PLIST" ]]; then
  echo "STOP: recovery package is not installed. Run scripts/webcore-mcp/install.sh first."
  read -k 1 "?Press any key to close..."
  exit 1
fi
if /usr/bin/curl -fsS --max-time 2 "$HEALTH" >/dev/null 2>&1 && /usr/bin/curl -fsS --max-time 2 "$READY" >/dev/null 2>&1; then
  echo "🟢 WebCoRE MCP ONLINE"
  echo "Tunnel health: live"
  echo "Tunnel readiness: ready"
  read -k 1 "?Press any key to close..."
  exit 0
fi
if ! /usr/bin/security find-generic-password -a "$USER" -s "WebCoRE MCP Tunnel Runtime" >/dev/null 2>&1; then
  echo "STOP: runtime API key is not stored in macOS Keychain."
  echo "Run the installer again to securely provision it."
  read -k 1 "?Press any key to close..."
  exit 2
fi
/usr/bin/launchctl bootstrap "$DOMAIN" "$PLIST" 2>/dev/null || true
/usr/bin/launchctl kickstart -k "$DOMAIN/$LABEL" || {
  echo "STOP: launchd could not start WebCoRE MCP."
  echo "Check: $HOME/Library/Logs/WebCoRE-MCP/tunnel.err.log"
  read -k 1 "?Press any key to close..."
  exit 3
}
for i in {1..20}; do
  if /usr/bin/curl -fsS --max-time 2 "$HEALTH" >/dev/null 2>&1 && /usr/bin/curl -fsS --max-time 2 "$READY" >/dev/null 2>&1; then
    echo "🟢 WebCoRE MCP ONLINE"
    echo "Tunnel health: live"
    echo "Tunnel readiness: ready"
    read -k 1 "?Press any key to close..."
    exit 0
  fi
  /bin/sleep 1
done
echo "STOP: started but did not become ready within 20 seconds."
echo "Check: $HOME/Library/Logs/WebCoRE-MCP/tunnel.err.log"
read -k 1 "?Press any key to close..."
exit 4
