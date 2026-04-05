#!/bin/bash
# DGX Cluster Setup Script for UNICC AI Safety Council
# Run this script once on the DGX node to set everything up.

set -e

echo "=== UNICC AI Safety Council - DGX Setup ==="

# Step 1: Install Ollama if not present
if ! command -v ollama &> /dev/null; then
    echo "[1/5] Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "[1/5] Ollama already installed."
fi

# Step 2: Start Ollama server
echo "[2/5] Starting Ollama server..."
ollama serve &
sleep 5

# Step 3: Pull the model
echo "[3/5] Pulling mistral:7b-instruct model..."
ollama pull mistral:7b-instruct

# Step 4: Install Python dependencies
echo "[4/5] Installing Python dependencies..."
pip install -r requirements.txt

# Step 5: Run tests to verify
echo "[5/5] Running tests..."
python3 -m pytest tests/test_basic.py -v

echo ""
echo "=== Setup complete! ==="
echo "Run the project with: python3 main.py"
