# UNICC_fj2067_project2

AI Safety Council Prototype

This project implements a multi-judge AI safety evaluation system
based on a Mixture-of-Experts architecture.

This system runs locally using Ollama (preferred) or via the Anthropic API as a fallback.

## Option 1 — Local (no API key needed)

```bash
ollama pull mistral:7b-instruct
ollama serve
python3 main.py
```

## Option 2 — API fallback (if Ollama is not available)

```bash
export ANTHROPIC_API_KEY=your_key_here
python3 main.py
```

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 main.py
```

You will be prompted to enter text. The three judges (Security, Governance,
Ethics) each query the local Ollama endpoint at `http://localhost:11434/api/generate`
using `mistral:7b-instruct`, then the council arbitration layer produces
a final safety decision. If Ollama is not running, the system automatically
falls back to the Anthropic API using `claude-sonnet-4-20250514`.

## Architecture

        Input AI System
              |
              v
         +-----------------+
         |  Judge 1        |
         |  Security       |
         +-----------------+
              |
         +-----------------+
         |  Judge 2        |
         |  Governance     |
         +-----------------+
              |
         +-----------------+
         |  Judge 3        |
         |  Ethics         |
         +-----------------+
              |
              v
         Council Arbitration Layer
              |
              v
         Safety Decision
