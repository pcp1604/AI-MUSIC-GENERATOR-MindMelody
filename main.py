#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI Music Composer Application
Main entry point for the application
"""

import sys
import os
import logging
import random
from music21 import stream, note, chord, instrument
from ai_composer import AIComposer
from audio_processor import AudioProcessor
from models.music_model import MusicParameters

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def generate_composition(params):
    """Generate a composition using AI Composer"""
    ai_composer = AIComposer()
    composition = ai_composer.compose(params)
    return composition

def export_composition(composition, output_path):
    """Export the composition to a MIDI file"""
    audio_processor = AudioProcessor()
    success = audio_processor.export_midi(composition, output_path)
    return success

def suggest_parameters():
    """Suggest parameters for composition"""
    ai_composer = AIComposer()
    params = ai_composer.suggest_parameters()
    return params

def display_parameters(params):
    """Display composition parameters"""
    print("\nComposition Parameters:")
    print(f"Tempo: {params.tempo} BPM")
    print(f"Key: {params.key}")
    print(f"Mode: {params.mode}")
    print(f"Style: {params.style}")
    print(f"Duration: {params.duration} seconds")
    print(f"Instruments: {', '.join(params.instruments)}")
    if params.chord_complexity is not None:
        print(f"Chord Complexity: {params.chord_complexity:.2f}")
    if params.rhythm_variation is not None:
        print(f"Rhythm Variation: {params.rhythm_variation:.2f}")
    print()

def get_user_input():
    """Get user input for composition parameters"""
    params = MusicParameters()
    
    print("\nEnter composition parameters (press Enter to use default values):")
    
    try:
        # Get tempo
        tempo_input = input(f"Tempo (BPM) [{params.tempo}]: ")
        if tempo_input:
            try:
                params.tempo = int(tempo_input)
            except ValueError:
                print("Invalid tempo, using default")
        
        # Get key
        key_input = input(f"Key [{params.key}]: ")
        if key_input:
            params.key = key_input
        
        # Get mode
        mode_input = input(f"Mode (major/minor) [{params.mode}]: ")
        if mode_input and mode_input.lower() in ["major", "minor"]:
            params.mode = mode_input.lower()
        
        # Get style
        print("Available styles: classical, jazz, pop, rock, electronic")
        style_input = input(f"Style [{params.style}]: ")
        if style_input and style_input.lower() in ["classical", "jazz", "pop", "rock", "electronic"]:
            params.style = style_input.lower()
        
        # Get duration
        duration_input = input(f"Duration (seconds) [{params.duration}]: ")
        if duration_input:
            try:
                params.duration = int(duration_input)
            except ValueError:
                print("Invalid duration, using default")
        
        # Get instruments
        print("Available instruments: Piano, Guitar, Electric Guitar, Bass, Bass Guitar, Double Bass, Violin, Cello, Flute, Saxophone, Drums, Synth, Synth Lead, Synth Bass, Pad")
        instruments_input = input(f"Instruments (comma-separated) [{', '.join(params.instruments)}]: ")
        if instruments_input:
            params.instruments = [instr.strip() for instr in instruments_input.split(",")]
        
        # Get complexity
        complexity_input = input(f"Chord Complexity (0.0-1.0) [{params.chord_complexity or 0.5}]: ")
        if complexity_input:
            try:
                params.chord_complexity = float(complexity_input)
            except ValueError:
                print("Invalid complexity, using default")
        
        # Get rhythm variation
        rhythm_input = input(f"Rhythm Variation (0.0-1.0) [{params.rhythm_variation or 0.5}]: ")
        if rhythm_input:
            try:
                params.rhythm_variation = float(rhythm_input)
            except ValueError:
                print("Invalid rhythm variation, using default")
    
    except EOFError:
        # Handle EOF gracefully (when input is redirected from a file)
        print("\nReading input from file. Using defaults where needed.")
    
    return params

def display_composition_info(composition):
    """Display information about the generated composition"""
    print("\nComposition Information:")
    print(f"Parts: {len(composition.parts)}")
    
    for i, part in enumerate(composition.parts):
        # Get instrument name
        instr_name = "Unknown"
        for element in part.flat:
            if isinstance(element, instrument.Instrument):
                instr_name = element.instrumentName
                break
        
        # Count measures and notes
        measures = part.getElementsByClass('Measure')
        note_count = len(part.flat.notes)
        
        print(f"Part {i+1}: {instr_name}")
        print(f"  Measures: {len(measures)}, Notes: {note_count}")
        
        # Show first few notes as text (limited preview)
        if note_count > 0:
            notes_preview = []
            for idx, note_element in enumerate(part.flat.notes):
                if idx >= 10:  # Only show first 10 notes
                    break
                    
                if isinstance(note_element, note.Note):
                    notes_preview.append(note_element.nameWithOctave)
                elif isinstance(note_element, chord.Chord):
                    chord_text = "[" + " ".join(n.nameWithOctave for n in note_element.notes) + "]"
                    notes_preview.append(chord_text)
            
            print(f"  Preview: {' '.join(notes_preview)}")
        print()

def main():
    """Main function for the command-line version of AI Music Composer"""
    try:
        print("=== AI Music Composer - Command Line Edition ===")
        print("Generate AI-composed music in various styles")
        
        while True:
            print("\nOptions:")
            print("1. Generate with custom parameters")
            print("2. Generate with AI-suggested parameters")
            print("3. Exit")
            
            try:
                choice = input("\nEnter your choice (1-3): ")
                
                if choice == "1":
                    # Get custom parameters
                    params = get_user_input()
                    
                    # Display parameters
                    display_parameters(params)
                    
                    # Generate composition
                    print("Generating composition...")
                    composition = generate_composition(params)
                    
                    # Display composition info
                    display_composition_info(composition)
                    
                    try:
                        # Export to MIDI
                        output_path = input("Enter output MIDI file path [output.mid]: ") or "output.mid"
                        if export_composition(composition, output_path):
                            print(f"Composition exported to {output_path}")
                        else:
                            print("Failed to export composition")
                    except EOFError:
                        # Use default output path if EOF detected
                        output_path = "output.mid"
                        if export_composition(composition, output_path):
                            print(f"Composition exported to {output_path}")
                        else:
                            print("Failed to export composition")
                    
                elif choice == "2":
                    # Get AI-suggested parameters
                    print("Generating AI-suggested parameters...")
                    params = suggest_parameters()
                    
                    # Display parameters
                    display_parameters(params)
                    
                    try:
                        # Ask if user wants to proceed
                        proceed = input("Generate with these parameters? (y/n): ").lower()
                    except EOFError:
                        # Default to yes if EOF detected
                        proceed = "y"
                        print("Auto-proceeding with these parameters (y)")
                        
                    if proceed == "y":
                        # Generate composition
                        print("Generating composition...")
                        composition = generate_composition(params)
                        
                        # Display composition info
                        display_composition_info(composition)
                        
                        try:
                            # Export to MIDI
                            output_path = input("Enter output MIDI file path [output.mid]: ") or "output.mid"
                        except EOFError:
                            # Use default output path if EOF detected
                            output_path = "output.mid"
                            print(f"Using default output path: {output_path}")
                            
                        if export_composition(composition, output_path):
                            print(f"Composition exported to {output_path}")
                        else:
                            print("Failed to export composition")
                    
                elif choice == "3":
                    print("Exiting AI Music Composer. Goodbye!")
                    break
                    
                else:
                    print("Invalid choice. Please try again.")
                    
            except EOFError:
                print("\nEnd of input detected. Exiting.")
                break
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
