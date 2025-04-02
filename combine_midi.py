#!/usr/bin/env python3
"""
AI Music Composer - MIDI Combiner
Tool to combine multiple MIDI compositions created by the AI Music Composer
"""

import os
import sys
import logging
import mido
from mido import MidiFile, MidiTrack, merge_tracks, MetaMessage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def list_midi_files():
    """Find all MIDI files in the current directory"""
    midi_files = []
    for file in os.listdir('.'):
        if file.endswith('.mid'):
            midi_files.append(file)
    return sorted(midi_files)

def get_midi_info(midi_file):
    """Get basic info about a MIDI file"""
    try:
        mid = MidiFile(midi_file)
        track_count = len(mid.tracks)
        total_notes = sum(1 for track in mid.tracks for msg in track if msg.type == 'note_on')
        duration = mid.length
        
        # Get instrument names if available
        instruments = []
        for i, track in enumerate(mid.tracks):
            track_name = "Unknown"
            instrument_name = "Unknown"
            
            for msg in track:
                if msg.type == 'track_name':
                    track_name = msg.name
                elif msg.type == 'program_change':
                    instrument_name = f"Program {msg.program}"
            
            if i > 0:  # Skip first track if it's just metadata
                instruments.append(f"{track_name} ({instrument_name})")
        
        return {
            'tracks': track_count,
            'notes': total_notes,
            'duration': duration,
            'instruments': instruments
        }
    except Exception as e:
        logger.error(f"Error reading MIDI file {midi_file}: {e}")
        return None

def combine_midi_files(input_files, output_file, combine_mode='sequential'):
    """Combine multiple MIDI files into one"""
    if not input_files:
        print("No input files specified.")
        return False
    
    # Check that all files exist
    for file in input_files:
        if not os.path.exists(file):
            print(f"File not found: {file}")
            return False
    
    try:
        if combine_mode == 'sequential':
            # In sequential mode, we append one file after another
            combined_midi = None
            current_time = 0
            
            for i, file in enumerate(input_files):
                midi = MidiFile(file)
                
                # For the first file, initialize the combined MIDI
                if i == 0:
                    combined_midi = MidiFile(ticks_per_beat=midi.ticks_per_beat)
                    # Create a metadata track
                    meta_track = MidiTrack()
                    meta_track.append(MetaMessage('track_name', name='Combined Composition', time=0))
                    combined_midi.tracks.append(meta_track)
                
                # Skip the first track if it's just metadata
                for track_idx, track in enumerate(midi.tracks):
                    if track_idx == 0 and all(msg.type != 'note_on' for msg in track):
                        continue
                    
                    # Create a new track for each original track
                    new_track = MidiTrack()
                    
                    # Preserve track name and instrument
                    track_name = f"Track {track_idx} from {os.path.basename(file)}"
                    instrument_program = 0
                    
                    for msg in track:
                        if msg.type == 'track_name':
                            track_name = msg.name
                        elif msg.type == 'program_change':
                            instrument_program = msg.program
                    
                    new_track.append(MetaMessage('track_name', name=track_name, time=0))
                    new_track.append(mido.Message('program_change', program=instrument_program, time=0))
                    
                    # Add all events with adjusted time
                    for msg in track:
                        if msg.type not in ('track_name', 'program_change'):
                            new_msg = msg.copy()
                            if i > 0 and new_msg.time > 0 and track_idx == 1:
                                # Add a small pause between compositions
                                new_msg.time += 960
                            new_track.append(new_msg)
                    
                    combined_midi.tracks.append(new_track)
                
                logger.info(f"Added {file} to combined composition")
            
            combined_midi.save(output_file)
            return True
            
        elif combine_mode == 'layered':
            # In layered mode, we play all files simultaneously
            # This is more complex as we need to properly merge events
            # For simplicity, we'll use mido's merge_tracks
            all_tracks = []
            ticks_per_beat = None
            
            for file in input_files:
                midi = MidiFile(file)
                
                # Ensure all files have the same time format
                if ticks_per_beat is None:
                    ticks_per_beat = midi.ticks_per_beat
                elif ticks_per_beat != midi.ticks_per_beat:
                    logger.warning(f"File {file} has different time format. Results may be unexpected.")
                
                # Add all tracks except first if it's just metadata
                for track_idx, track in enumerate(midi.tracks):
                    if track_idx == 0 and all(msg.type != 'note_on' for msg in track):
                        continue
                    
                    # Create a new track with copied messages to avoid modifying original
                    new_track = MidiTrack()
                    
                    # Add track name
                    original_name = "Unknown"
                    for msg in track:
                        if msg.type == 'track_name':
                            original_name = msg.name
                            break
                    
                    track_name = f"{original_name} from {os.path.basename(file)}"
                    new_track.append(MetaMessage('track_name', name=track_name, time=0))
                    
                    # Copy all messages
                    for msg in track:
                        if msg.type != 'track_name':
                            new_track.append(msg.copy())
                    
                    all_tracks.append(new_track)
            
            # Create new MIDI file with all tracks
            combined_midi = MidiFile(ticks_per_beat=ticks_per_beat)
            
            # Add metadata track
            meta_track = MidiTrack()
            meta_track.append(MetaMessage('track_name', name='Combined Layered Composition', time=0))
            combined_midi.tracks.append(meta_track)
            
            # Add all tracks
            for track in all_tracks:
                combined_midi.tracks.append(track)
            
            combined_midi.save(output_file)
            return True
            
    except Exception as e:
        logger.error(f"Error combining MIDI files: {e}")
        return False

def main():
    """Main function to combine MIDI files"""
    print("=== AI Music Composer - MIDI Combiner ===")
    
    midi_files = list_midi_files()
    if not midi_files:
        print("No MIDI files found in the current directory.")
        return
    
    print("\nAvailable MIDI files:")
    for i, file in enumerate(midi_files):
        info = get_midi_info(file)
        if info:
            print(f"{i+1}. {file} ({info['tracks']} tracks, {int(info['duration'])}s)")
            if info['instruments']:
                print(f"   Instruments: {', '.join(info['instruments'][:3])}")
                if len(info['instruments']) > 3:
                    print(f"   ...and {len(info['instruments']) - 3} more")
        else:
            print(f"{i+1}. {file} (Unable to read file info)")
    
    print("\nSelect files to combine (comma-separated numbers, e.g., 1,3,4)")
    try:
        selections = input("Your selection: ")
    except EOFError:
        # In non-interactive mode, use all files
        print("Non-interactive mode detected. Using all files.")
        selections = ",".join(str(i+1) for i in range(len(midi_files)))
    
    if not selections:
        print("No selections made. Exiting.")
        return
    
    try:
        indices = [int(s.strip()) - 1 for s in selections.split(",")]
        selected_files = [midi_files[i] for i in indices if 0 <= i < len(midi_files)]
    except ValueError:
        print("Invalid input. Please enter comma-separated numbers.")
        return
    
    if not selected_files:
        print("No valid files selected. Exiting.")
        return
    
    print(f"\nSelected {len(selected_files)} files:")
    for file in selected_files:
        print(f"- {file}")
    
    print("\nCombine mode:")
    print("1. Sequential (one after another)")
    print("2. Layered (play simultaneously)")
    
    try:
        mode_choice = input("Your choice (1-2, default: 1): ")
    except EOFError:
        # In non-interactive mode, use sequential
        print("Non-interactive mode detected. Using sequential mode.")
        mode_choice = "1"
    
    combine_mode = "sequential" if not mode_choice or mode_choice == "1" else "layered"
    
    try:
        output_name = input("\nEnter output filename (default: combined_composition.mid): ")
    except EOFError:
        # In non-interactive mode, use default name
        print("Non-interactive mode detected. Using default filename.")
        output_name = ""
    
    if not output_name:
        output_name = "combined_composition.mid"
    elif not output_name.endswith('.mid'):
        output_name += '.mid'
    
    print(f"\nCombining {len(selected_files)} files in {combine_mode} mode...")
    if combine_midi_files(selected_files, output_name, combine_mode):
        print(f"Successfully created {output_name}")
        
        # Analyze the combined file
        print("\nAnalyzing combined composition...")
        os.system(f"python analyze_midi.py {output_name}")
    else:
        print("Failed to combine files.")

if __name__ == "__main__":
    main()