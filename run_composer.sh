#!/bin/bash

# Script to run the AI Music Composer with predefined jazz parameters

# Just run with simple parameters - we'll specify the output file manually
echo "2" | python main.py

# Rename the output file to our desired name
if [ -f "output.mid" ]; then
    mv output.mid ai_composition.mid
    echo "Renamed output.mid to ai_composition.mid"
fi

echo "Analyzing generated composition..."
python analyze_midi.py ai_composition.mid

echo "Attempting to play composition (note: may not work in Replit environment)..."
python play_music.py ai_composition.mid