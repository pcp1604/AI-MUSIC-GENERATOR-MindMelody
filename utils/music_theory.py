#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Music Theory module
Contains utility functions for music theory and composition
"""

import logging
import random
import numpy as np
from typing import List, Tuple, Optional, Dict, Any

logger = logging.getLogger(__name__)

# Define major and minor scales
MAJOR_SCALE_STEPS = [0, 2, 4, 5, 7, 9, 11]
MINOR_SCALE_STEPS = [0, 2, 3, 5, 7, 8, 10]

# Define note names and octaves
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
DEFAULT_OCTAVE = 4

# Map of Roman numeral to scale degree (0-indexed)
ROMAN_TO_SCALE_DEGREE = {
    'I': 0, 'II': 1, 'III': 2, 'IV': 3, 'V': 4, 'VI': 5, 'VII': 6,
    'i': 0, 'ii': 1, 'iii': 2, 'iv': 3, 'v': 4, 'vi': 5, 'vii': 6
}

def get_note_index(note_name: str) -> int:
    """
    Get the index of a note in the chromatic scale
    
    Args:
        note_name: The name of the note (e.g., "C", "F#")
        
    Returns:
        The index in the chromatic scale (0-11)
    """
    # Handle flats by converting to equivalent sharps
    if 'b' in note_name:
        flat_map = {'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#'}
        if note_name in flat_map:
            note_name = flat_map[note_name]
    
    # Get the base note without any accidentals
    base_note = note_name[0]
    
    # Find the index in NOTE_NAMES
    index = NOTE_NAMES.index(base_note)
    
    # Adjust for sharp or flat
    if len(note_name) > 1:
        if note_name[1] == '#':
            index = (index + 1) % 12
        elif note_name[1] == 'b':
            index = (index - 1) % 12
    
    return index

def get_scale_notes(key: str, mode: str) -> List[str]:
    """
    Get the notes in a specific scale
    
    Args:
        key: The root note of the scale (e.g., "C", "F#")
        mode: The mode ("major" or "minor")
        
    Returns:
        List of note names in the scale
    """
    # Get the root note index
    root_index = get_note_index(key)
    
    # Select the appropriate scale steps
    scale_steps = MAJOR_SCALE_STEPS if mode.lower() == "major" else MINOR_SCALE_STEPS
    
    # Generate the scale notes
    scale_notes = []
    for step in scale_steps:
        note_index = (root_index + step) % 12
        scale_notes.append(NOTE_NAMES[note_index])
    
    return scale_notes

def get_chord_notes(key: str, mode: str, roman_numeral: str) -> List[str]:
    """
    Get the notes for a specific chord based on scale degree
    
    Args:
        key: The root note of the scale (e.g., "C", "F#")
        mode: The mode ("major" or "minor")
        roman_numeral: The Roman numeral indicating the chord (e.g., "I", "V7")
        
    Returns:
        List of notes in the chord
    """
    scale_notes = get_scale_notes(key, mode)
    
    # Parse the roman numeral to get base degree and quality
    base_numeral = ''.join(c for c in roman_numeral if c.isalpha())
    
    if base_numeral not in ROMAN_TO_SCALE_DEGREE:
        logger.warning(f"Unknown roman numeral: {roman_numeral}, defaulting to I")
        base_numeral = 'I' if mode.lower() == 'major' else 'i'
    
    degree = ROMAN_TO_SCALE_DEGREE[base_numeral]
    
    # Determine chord quality
    is_major = base_numeral.isupper()
    is_diminished = 'dim' in roman_numeral or '°' in roman_numeral
    is_augmented = 'aug' in roman_numeral or '+' in roman_numeral
    is_seventh = '7' in roman_numeral
    
    # Get the root note
    root = scale_notes[degree]
    
    # Build the chord based on quality
    chord_notes = [root]
    
    # Add third
    if is_major and not is_diminished:
        # Major third
        third_idx = (degree + 2) % 7
        chord_notes.append(scale_notes[third_idx])
    else:
        # Minor third
        third_idx = (degree + 2) % 7
        minor_third = scale_notes[third_idx]
        # Check if we need to flatten the third (for minor chords)
        # This is a simplified approach that would need more sophistication in a real app
        chord_notes.append(minor_third)
    
    # Add fifth
    if is_diminished:
        # Diminished fifth
        fifth_idx = (degree + 4) % 7
        fifth = scale_notes[fifth_idx]
        # Flatten the fifth (simplified)
        chord_notes.append(fifth + 'b')
    elif is_augmented:
        # Augmented fifth
        fifth_idx = (degree + 4) % 7
        fifth = scale_notes[fifth_idx]
        # Sharpen the fifth (simplified)
        chord_notes.append(fifth + '#')
    else:
        # Perfect fifth
        fifth_idx = (degree + 4) % 7
        chord_notes.append(scale_notes[fifth_idx])
    
    # Add seventh if needed
    if is_seventh:
        seventh_idx = (degree + 6) % 7
        chord_notes.append(scale_notes[seventh_idx])
    
    return chord_notes

def get_chord_progression(key: str, mode: str, length: int = 4) -> List[str]:
    """
    Generate a common chord progression
    
    Args:
        key: The root note of the scale (e.g., "C", "F#")
        mode: The mode ("major" or "minor")
        length: The number of chords in the progression
        
    Returns:
        List of Roman numerals representing the chord progression
    """
    # Common progressions by mode
    major_progressions = [
        ["I", "IV", "V", "I"],
        ["I", "vi", "IV", "V"],
        ["I", "V", "vi", "IV"],
        ["ii", "V", "I", "IV"]
    ]
    
    minor_progressions = [
        ["i", "iv", "v", "i"],
        ["i", "VI", "III", "VII"],
        ["i", "iv", "VII", "III"],
        ["i", "v", "VI", "v"]
    ]
    
    # Select a random progression based on mode
    progressions = major_progressions if mode.lower() == "major" else minor_progressions
    progression = random.choice(progressions)
    
    # If requested length is different than the provided progression length,
    # adjust by repeating or trimming
    if length > len(progression):
        # Repeat the progression until reaching desired length
        repeated = []
        while len(repeated) < length:
            repeated.extend(progression)
        progression = repeated[:length]
    elif length < len(progression):
        # Trim the progression
        progression = progression[:length]
    
    return progression

def generate_melody(
    scale_notes: List[str],
    chord_progression: List[str],
    num_measures: int,
    rhythm_variation: float = 0.5
) -> List[Tuple[str, float]]:
    """
    Generate a melodic line based on scale and chord progression
    
    Args:
        scale_notes: List of notes in the scale
        chord_progression: List of chord symbols
        num_measures: Number of measures to generate
        rhythm_variation: Amount of rhythmic variation (0.0 to 1.0)
        
    Returns:
        List of (note, duration) tuples representing the melody
    """
    melody = []
    
    # Extend chord progression to cover all measures if needed
    extended_progression = []
    while len(extended_progression) < num_measures:
        extended_progression.extend(chord_progression)
    chord_progression = extended_progression[:num_measures]
    
    # For each measure
    for measure_idx in range(num_measures):
        chord = chord_progression[measure_idx % len(chord_progression)]
        
        # Get chord tones (simplified)
        chord_tones = []
        if chord.startswith('I') or chord.startswith('i'):
            chord_tones = [scale_notes[0], scale_notes[2], scale_notes[4]]
        elif chord.startswith('II') or chord.startswith('ii'):
            chord_tones = [scale_notes[1], scale_notes[3], scale_notes[5]]
        elif chord.startswith('III') or chord.startswith('iii'):
            chord_tones = [scale_notes[2], scale_notes[4], scale_notes[6]]
        elif chord.startswith('IV') or chord.startswith('iv'):
            chord_tones = [scale_notes[3], scale_notes[5], scale_notes[0]]
        elif chord.startswith('V') or chord.startswith('v'):
            chord_tones = [scale_notes[4], scale_notes[6], scale_notes[1]]
        elif chord.startswith('VI') or chord.startswith('vi'):
            chord_tones = [scale_notes[5], scale_notes[0], scale_notes[2]]
        elif chord.startswith('VII') or chord.startswith('vii'):
            chord_tones = [scale_notes[6], scale_notes[1], scale_notes[3]]
        
        # Generate rhythm pattern
        rhythm_pattern = generate_rhythm_pattern(rhythm_variation)
        total_duration = sum(rhythm_pattern)
        
        # Scale the rhythm pattern to fit the measure (4 beats in 4/4 time)
        scale_factor = 4.0 / total_duration
        rhythm_pattern = [duration * scale_factor for duration in rhythm_pattern]
        
        # Generate notes for this measure
        for rhythm_value in rhythm_pattern:
            # Decide whether to use chord tone or scale tone
            if random.random() < 0.7:  # 70% chance of chord tone
                note = random.choice(chord_tones)
            else:
                note = random.choice(scale_notes)
            
            # Occasionally add a rest
            if random.random() < 0.1:
                note = "rest"
            
            # Add the note with its duration
            melody.append((note, rhythm_value))
    
    return melody

def generate_bass_line(
    scale_notes: List[str],
    chord_progression: List[str],
    num_measures: int
) -> List[Tuple[str, float]]:
    """
    Generate a bass line based on scale and chord progression
    
    Args:
        scale_notes: List of notes in the scale
        chord_progression: List of chord symbols
        num_measures: Number of measures to generate
        
    Returns:
        List of (note, duration) tuples representing the bass line
    """
    bass_line = []
    
    # Extend chord progression to cover all measures if needed
    extended_progression = []
    while len(extended_progression) < num_measures:
        extended_progression.extend(chord_progression)
    chord_progression = extended_progression[:num_measures]
    
    # For each measure
    for measure_idx in range(num_measures):
        chord = chord_progression[measure_idx % len(chord_progression)]
        
        # Get the root note for this chord
        root_degree = ROMAN_TO_SCALE_DEGREE.get(chord[0], 0)
        root_note = scale_notes[root_degree]
        
        # Various bass patterns
        patterns = [
            # Root note whole note
            [(root_note, 4.0)],
            
            # Root note half notes
            [(root_note, 2.0), (root_note, 2.0)],
            
            # Root-fifth pattern
            [(root_note, 2.0), (scale_notes[(root_degree + 4) % 7], 2.0)],
            
            # Walking bass (root, third, fifth, approach)
            [
                (root_note, 1.0),
                (scale_notes[(root_degree + 2) % 7], 1.0),
                (scale_notes[(root_degree + 4) % 7], 1.0),
                (scale_notes[(root_degree + 6) % 7], 1.0)
            ],
            
            # Rhythmic pattern
            [(root_note, 1.0), ("rest", 0.5), (root_note, 1.0), (root_note, 1.0), ("rest", 0.5)]
        ]
        
        # Choose a pattern
        pattern = random.choice(patterns)
        
        # Add the pattern to the bass line
        bass_line.extend(pattern)
    
    return bass_line

def generate_rhythm_pattern(complexity: float) -> List[float]:
    """
    Generate a rhythm pattern with varying complexity
    
    Args:
        complexity: Complexity level (0.0 to 1.0)
        
    Returns:
        List of note durations
    """
    # Basic note durations (whole, half, quarter, eighth, sixteenth)
    durations = [4.0, 2.0, 1.0, 0.5, 0.25]
    
    # Adjust available durations based on complexity
    if complexity < 0.3:
        # Simple rhythms (mostly quarter and half notes)
        available_durations = [2.0, 1.0, 1.0, 1.0]
    elif complexity < 0.6:
        # Moderate rhythms (quarter and eighth notes, some half notes)
        available_durations = [2.0, 1.0, 1.0, 0.5, 0.5]
    else:
        # Complex rhythms (eighth and sixteenth notes, some quarter notes)
        available_durations = [1.0, 0.5, 0.5, 0.25, 0.25]
    
    # Generate a pattern
    pattern = []
    total_duration = 0.0
    
    # We'll aim for approximately 4 beats (a full measure in 4/4)
    # but we'll let generate_melody() scale it to fit exactly
    target_duration = 4.0
    
    while total_duration < target_duration:
        # Choose a duration
        duration = random.choice(available_durations)
        
        # Add it to the pattern
        pattern.append(duration)
        total_duration += duration
    
    return pattern

def transpose_note(note: str, semitones: int) -> str:
    """
    Transpose a note by a number of semitones
    
    Args:
        note: The note name (e.g., "C", "F#")
        semitones: Number of semitones to transpose (positive or negative)
        
    Returns:
        The transposed note name
    """
    if note == "rest":
        return "rest"
    
    # Get the index in the chromatic scale
    index = get_note_index(note)
    
    # Calculate the new index
    new_index = (index + semitones) % 12
    
    # Return the new note name
    return NOTE_NAMES[new_index]

def is_consonant(note1: str, note2: str) -> bool:
    """
    Check if two notes form a consonant interval
    
    Args:
        note1: First note name
        note2: Second note name
        
    Returns:
        True if the interval is consonant, False otherwise
    """
    if note1 == "rest" or note2 == "rest":
        return True
    
    # Get the indices in the chromatic scale
    index1 = get_note_index(note1)
    index2 = get_note_index(note2)
    
    # Calculate the interval in semitones
    interval = abs(index1 - index2) % 12
    
    # Consonant intervals: unison, minor third, major third, perfect fourth,
    # perfect fifth, minor sixth, major sixth, octave
    consonant_intervals = [0, 3, 4, 5, 7, 8, 9]
    
    return interval in consonant_intervals
