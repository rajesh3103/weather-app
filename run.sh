#!/bin/bash
source .venv/bin/activate
PYTHONWARNINGS="ignore:::urllib3" python app.py

