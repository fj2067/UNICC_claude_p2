# UNICC_fj2067_project2

AI Safety Council Prototype

This project implements a multi-judge AI safety evaluation system
based on a Mixture-of-Experts architecture. All LLM calls are handled
by a local Ollama instance — no API key is needed.

## Prerequisites

Install and start Ollama before running the project:

1. Install Ollama from https://ollama.com
2. Pull the model: `ollama pull mistral:7b-instruct`
3. Run `ollama serve` (keep it running in the background)

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
a final safety decision.

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
