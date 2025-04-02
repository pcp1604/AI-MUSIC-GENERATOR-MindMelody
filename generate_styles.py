#!/usr/bin/env python3
"""
AI Music Composer - Style Explorer
Generate compositions in multiple styles to showcase the AI capabilities
"""

import os
import sys
import logging
from datetime import datetime
from models.music_model import MusicParameters
from ai_composer import AIComposer
from audio_processor import AudioProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_composition_for_style(style, output_dir):
    """Generate a composition for a specific style"""
    # Create composer and audio processor
    composer = AIComposer()
    audio_processor = AudioProcessor()
    
    # Generate parameters with the specified style
    params = composer.suggest_parameters()
    params.style = style
    
    # Log the parameters
    logger.info(f"Generating {style} composition with parameters: {params}")
    
    # Generate the composition
    composition = composer.compose(params)
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Export to MIDI
    output_path = os.path.join(output_dir, f"{style}_composition.mid")
    audio_processor.export_midi(composition, output_path)
    logger.info(f"Exported {style} composition to {output_path}")
    
    return output_path

def main():
    """Generate compositions in different styles"""
    print("=== AI Music Composer - Style Explorer ===")
    print("Generating compositions in multiple styles...")
    
    # List of available styles
    styles = ["classical", "jazz", "rock", "pop", "electronic"]
    
    # Create a timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"generated_compositions_{timestamp}"
    
    # Track successful generations
    generated_files = []
    
    # Generate a composition for each style
    for style in styles:
        print(f"\nGenerating {style.capitalize()} composition...")
        try:
            output_path = generate_composition_for_style(style, output_dir)
            generated_files.append((style, output_path))
            print(f"Successfully generated {style.capitalize()} composition.")
        except Exception as e:
            logger.error(f"Error generating {style} composition: {e}")
            print(f"Failed to generate {style.capitalize()} composition: {e}")
    
    # Print summary
    print("\n=== Generated Compositions ===")
    for style, path in generated_files:
        print(f"{style.capitalize()}: {path}")
    
    print(f"\nAll compositions saved to directory: {output_dir}")
    print("Use 'python analyze_midi.py [filename]' to analyze any of these compositions.")

if __name__ == "__main__":
    main()