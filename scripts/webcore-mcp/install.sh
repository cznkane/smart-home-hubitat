#!/bin/zsh
set -euo pipefail
ROOT="$HOME/Library/Application Support/WebCoRE-MCP"
OPS="$ROOT/ops"
LOG="$HOME/Library/Logs/WebCoRE-MCP"
LAUNCHERS="$HOME/Applications/WebCoRE MCP"
AGENTS="$HOME/Library/LaunchAgents"
LABEL="com.kaneconsulting.webcore-mcp"
SERVICE="WebCoRE MCP Tunnel Runtime"
HERE="$(cd "$(dirname "$0")" && pwd)"
echo "WebCoRE MCP recovery installer"
echo "=============================="
for exe in /opt/homebrew/bin/tunnel-client /opt/homebrew/bin/node /usr/bin/security /usr/bin/launchctl /usr/bin/curl; do
  [[ -x "$exe" ]] || { echo "STOP: missing prerequisite $exe"; exit 1; }
done
[[ -f "$HOME/.config/tunnel-client/webcore.yaml" ]] || { echo "STOP: missing tunnel profile ~/.config/tunnel-client/webcore.yaml"; exit 2; }
[[ -f "$ROOT/webcore-cli/0.4.7/server/index.js" ]] || { echo "STOP: missing pinned webcore-CLI 0.4.7 production payload"; exit 3; }
mkdir -p "$OPS" "$LOG" "$LAUNCHERS" "$AGENTS"
install -m 700 "$HERE/runner.sh" "$OPS/runner.sh"
sed -e "s|__RUNNER_PATH__|$OPS/runner.sh|g" -e "s|__LOG_DIR__|$LOG|g" "$HERE/$LABEL.plist.template" > "$AGENTS/$LABEL.plist"
chmod 600 "$AGENTS/$LABEL.plist"
for f in "Start WebCoRE MCP.command" "WebCoRE MCP Status.command" "Stop WebCoRE MCP.command"; do
  install -m 700 "$HERE/$f" "$LAUNCHERS/$f"
done
if ! /usr/bin/security find-generic-password -a "$USER" -s "$SERVICE" >/dev/null 2>&1; then
  echo
  echo "Runtime API key is not yet in macOS Keychain."
  echo "Paste it at the hidden prompt. It will not be echoed."
  read -s "KEY?Runtime API key: "
  echo
  [[ -n "$KEY" ]] || { echo "STOP: no key supplied"; exit 4; }
  /usr/bin/security add-generic-password -U -a "$USER" -s "$SERVICE" -w "$KEY" >/dev/null
  unset KEY
  echo "Keychain item created."
else
  echo "Existing Keychain runtime credential preserved."
fi
echo
echo "Installed launchers:"
echo "  $LAUNCHERS/Start WebCoRE MCP.command"
echo "  $LAUNCHERS/WebCoRE MCP Status.command"
echo "  $LAUNCHERS/Stop WebCoRE MCP.command"
echo
echo "Installer complete. No tunnel was started automatically."
