#!/usr/bin/env bash
# Launcher for EU CBAM & Green Trade Compliance FastAPI Server
# Vistara Trade Acceleration & Compliance Desk (2026)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_EXEC="$HOME/.venvs/trade-engine/bin/python"

if [ ! -f "$PYTHON_EXEC" ]; then
    echo "Creating virtual environment at $HOME/.venvs/trade-engine..."
    uv venv "$HOME/.venvs/trade-engine"
    uv pip install --python "$PYTHON_EXEC" fastapi uvicorn pydantic httpx
fi

if [ ! -f "$SCRIPT_DIR/portal-svelte/dist/index.html" ]; then
    echo "Client portal build not found. Building Svelte 5 frontend..."
    if command -v bun &> /dev/null; then
        (cd "$SCRIPT_DIR/portal-svelte" && bun install && bun run build)
    elif command -v npm &> /dev/null; then
        (cd "$SCRIPT_DIR/portal-svelte" && npm install && npm run build)
    fi
fi

echo "=================================================================="
echo " Vistara Trade Acceleration & Compliance Desk (2026 Micro-SaaS)"
echo "=================================================================="
echo " Svelte 5 Client Portal : http://127.0.0.1:8000/portal (or http://127.0.0.1:8000/)"
echo " Interactive API Docs   : http://127.0.0.1:8000/docs"
echo " Alternative ReDoc      : http://127.0.0.1:8000/redoc"
echo "=================================================================="

export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
exec "$PYTHON_EXEC" -m uvicorn compliance.cbam.api:app --host 127.0.0.1 --port 8000 --reload
