#!/bin/bash

# Script to generate compositions in multiple styles

echo "Starting Style Explorer..."
python generate_styles.py

echo "Analyzing the first generated composition..."
find generated_compositions_* -name "*.mid" | head -n 1 | xargs python analyze_midi.py