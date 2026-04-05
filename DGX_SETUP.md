# DGX Cluster Setup Guide

## Prerequisites

- Access to a DGX node with GPU
- Python 3.8+
- Ollama installed on the node

## Step 1: Install Ollama on DGX

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## Step 2: Start Ollama Server

```bash
# Start ollama in the background
ollama serve &

# Wait a few seconds for it to start
sleep 5

# Verify it is running
curl http://localhost:11434/api/tags
```

## Step 3: Pull the Model

```bash
ollama pull mistral:7b-instruct
```

This downloads ~4GB. On DGX with good network this should be fast.

## Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This only installs `requests` and `pytest` — no API keys or external services needed.

## Step 5: Run the Project

```bash
python3 main.py
```

Enter a prompt when asked. The three judges will query the local Ollama
endpoint and return a safety report.

## Step 6: Run Tests

```bash
python3 -m pytest tests/test_basic.py -v
```

## Troubleshooting

### "Connection refused" on port 11434
Ollama is not running. Start it with:
```bash
ollama serve &
```

### "Model not found"
Pull the model first:
```bash
ollama pull mistral:7b-instruct
```

### Ollama running on a different host/port
If Ollama runs on a different node or port, edit `judges/base_judge.py` line 4:
```python
OLLAMA_URL = "http://<your-host>:<your-port>/api/generate"
```

### Timeout errors
The default timeout is 120 seconds. For slower hardware, increase it in
`judges/base_judge.py` line 14:
```python
resp = requests.post(OLLAMA_URL, json=payload, timeout=300)
```

### GPU not detected by Ollama
Check that NVIDIA drivers and CUDA are visible:
```bash
nvidia-smi
ollama run mistral:7b-instruct "hello"
```

## File Structure

```
UNICC_claude_p2/
├── main.py                 # Entry point
├── requirements.txt        # requests + pytest only
├── README.md               # Project overview
├── DGX_SETUP.md            # This file
├── judges/
│   ├── __init__.py
│   ├── base_judge.py       # Ollama connection (localhost:11434)
│   ├── technical_judge.py  # Security Judge
│   ├── ethics_judge.py     # Ethics Judge
│   └── governance_judge.py # Governance Judge
├── council/
│   ├── __init__.py
│   ├── arbitration.py      # Voting logic
│   └── moe_council.py      # Council runner
├── output/
│   ├── __init__.py
│   └── report.py           # Report generator
└── tests/
    └── test_basic.py       # Unit tests
```
