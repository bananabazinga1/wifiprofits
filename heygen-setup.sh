#!/usr/bin/env bash
# HeyGen Skills + CLI setup for this project.
# Run from your local machine — HeyGen API requires an allowlisted IP.

set -e

SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
CLI_INSTALL="https://static.heygen.ai/cli/install.sh"

echo "==> Cloning HeyGen Skills into $SKILLS_DIR/heygen-skills"
git clone --depth 1 https://github.com/heygen-com/skills.git "$SKILLS_DIR/heygen-skills" 2>/dev/null \
  || (cd "$SKILLS_DIR/heygen-skills" && git pull)

echo "==> Installing HeyGen CLI"
if curl -fsSL "$CLI_INSTALL" -o /tmp/heygen-install.sh 2>/dev/null; then
  bash /tmp/heygen-install.sh
else
  # Fallback: build from source (requires Go 1.21+)
  echo "    Install script unavailable, building from source..."
  TMP=$(mktemp -d)
  git clone --depth 1 https://github.com/heygen-com/heygen-cli.git "$TMP/heygen-cli"
  cd "$TMP/heygen-cli"
  go build -ldflags "-s -w" -o /usr/local/bin/heygen ./cmd/heygen/
  cd -
  rm -rf "$TMP"
fi

echo "==> Verifying CLI"
heygen --version

echo ""
echo "Next steps:"
echo "  export HEYGEN_API_KEY=<your-key-from-app.heygen.com/api>"
echo "  heygen auth status"
echo "  heygen avatar list"
echo ""
echo "Then ask Claude: 'use heygen-avatar and heygen-video to create my intro video'"
