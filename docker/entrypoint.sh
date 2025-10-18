#!/bin/bash

# Initiate Ollama
ollama serve &

# Download Ollama Model
OLLAMA_MODEL=${OLLAMA_MODEL}
ollama pull $OLLAMA_MODEL

# Executing API
python -m uvicorn adapted_work.app:app --host 0.0.0.0 --port 8000 &
sleep 5

# Executing scheduler
export PYTHONPATH=$(pwd)
python adapted_work/scheduler/scheduler.py
