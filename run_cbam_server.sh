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

echo "Starting EU CBAM & Green Trade Compliance Engine on http://127.0.0.1:8000 ..."
echo "API Documentation available at: http://127.0.0.1:8000/docs"

export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
exec "$PYTHON_EXEC" -m uvicorn compliance.cbam.api:app --host 127.0.0.1 --port 8000 --reload
