#!/bin/zsh
set -u
PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export PATH
KEYCHAIN_SERVICE="WebCoRE MCP Tunnel Runtime"
PROFILE="webcore"
RUNTIME_KEY="$(/usr/bin/security find-generic-password -a "$USER" -s "$KEYCHAIN_SERVICE" -w 2>/dev/null || true)"
if [[ -z "$RUNTIME_KEY" ]]; then
  echo "ERROR: Missing macOS Keychain item: $KEYCHAIN_SERVICE" >&2
  exit 78
fi
export CONTROL_PLANE_API_KEY="$RUNTIME_KEY"
unset RUNTIME_KEY
exec /opt/homebrew/bin/tunnel-client run --profile "$PROFILE"
