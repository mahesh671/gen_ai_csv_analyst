"""
Application settings and configuration.
"""
import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Directory for CSV files
CSV_DIR = os.path.join(BASE_DIR, 'data', 'csv_files')

# LLM configuration
LLM_MODEL = 'llama-3.3-70b-versatile'
LLM_TEMPERATURE = 0.7
LLM_TOP_P = 0.8

# Agent configuration
AGENT_MAX_STEPS = 10