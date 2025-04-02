#!/bin/bash

# Launch script for AI Music Composer

echo "====================================="
echo "     AI MUSIC COMPOSER LAUNCHER     "
echo "====================================="
echo ""
echo "This script provides quick access to the AI Music Composer functions."
echo ""
echo "What would you like to do?"
echo ""
echo "1) Generate a quick composition with AI-suggested parameters"
echo "2) Start the interactive menu interface"
echo "3) Generate compositions in multiple styles at once"
echo "4) Analyze the last generated composition"
echo "5) Combine multiple MIDI compositions"
echo ""

# Read user choice with a default if in non-interactive mode
read -p "Enter choice (1-5, default: 1): " choice

# Set default if empty
if [ -z "$choice" ]; then
    choice=1
fi

case $choice in
    1)
        echo "Generating a composition with AI-suggested parameters..."
        ./run_composer.sh
        ;;
    2)
        echo "Starting the interactive menu interface..."
        python compose.py
        ;;
    3)
        echo "Generating compositions in multiple styles..."
        ./explore_styles.sh
        ;;
    4)
        echo "Analyzing the last generated composition..."
        python analyze_midi.py ai_composition.mid
        ;;
    5)
        echo "Combining MIDI compositions..."
        python combine_midi.py
        ;;
    *)
        echo "Invalid choice. Using default option (1)."
        ./run_composer.sh
        ;;
esac

echo ""
echo "Thank you for using AI Music Composer!"