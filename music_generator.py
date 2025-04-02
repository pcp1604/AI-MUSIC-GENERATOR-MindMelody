#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Music Generator module
Handles the generation of music based on parameters
"""

import logging
import random
import numpy as np
from music21 import stream, note, chord, instrument, tempo, meter, key
from models.music_model import MusicParameters
from utils.music_theory import (
    get_scale_notes, get_chord_progression, 
    generate_melody, generate_bass_line,
    generate_rhythm_pattern
)

logger = logging.getLogger(__name__)

class MusicGenerator:
    """Generates music compositions based on provided parameters"""
    
    def __init__(self):
        """Initialize the music generator"""
        logger.info("Music Generator initialized")
    
    def generate(self, params: MusicParameters):
        """
        Generate a musical composition based on the parameters
        
        Args:
            params: MusicParameters object containing composition settings
            
        Returns:
            music21 stream object representing the composition
        """
        logger.info(f"Generating music with: tempo={params.tempo}, key={params.key}, mode={params.mode}")
        
        # Create the main score
        score = stream.Score()
        
        # Add metadata
        score.insert(0, tempo.MetronomeMark(number=params.tempo))
        score.insert(0, key.Key(params.key, params.mode))
        score.insert(0, meter.TimeSignature('4/4'))  # Default to 4/4 time
        
        # Get scale notes for the selected key and mode
        scale_notes = get_scale_notes(params.key, params.mode)
        
        # Get chord progression if not specified
        if not params.chord_progression:
            params.chord_progression = get_chord_progression(params.key, params.mode)
        
        # Calculate total measures based on duration and tempo
        measures_per_minute = params.tempo / 4  # In 4/4 time
        total_measures = int((params.duration / 60) * measures_per_minute)
        
        # Generate parts for each instrument
        for instrument_name in params.instruments:
            part = self._generate_part(
                instrument_name, 
                scale_notes, 
                params.chord_progression,
                total_measures,
                params
            )
            score.insert(0, part)
        
        logger.info(f"Generated composition with {len(params.instruments)} instruments, {total_measures} measures")
        return score
    
    def _generate_part(self, instrument_name, scale_notes, chord_progression, total_measures, params):
        """Generate a music part for a specific instrument"""
        part = stream.Part()
        
        # Set the instrument
        instr = self._get_instrument_by_name(instrument_name)
        part.insert(0, instr)
        
        # Generate music based on instrument type
        if self._is_bass_instrument(instrument_name):
            self._generate_bass_part(part, scale_notes, chord_progression, total_measures, params)
        elif self._is_rhythm_instrument(instrument_name):
            self._generate_rhythm_part(part, scale_notes, chord_progression, total_measures, params)
        elif self._is_chord_instrument(instrument_name):
            self._generate_chord_part(part, scale_notes, chord_progression, total_measures, params)
        else:
            self._generate_melody_part(part, scale_notes, chord_progression, total_measures, params)
        
        return part
    
    def _generate_melody_part(self, part, scale_notes, chord_progression, total_measures, params):
        """Generate a melodic line for instruments like violin, flute, etc."""
        # Generate a melody using the scale notes and chord progression
        melody_pattern = generate_melody(
            scale_notes, 
            chord_progression, 
            total_measures,
            rhythm_variation=params.rhythm_variation or 0.5
        )
        
        # Add notes to the part
        measure = stream.Measure(number=1)
        current_measure = 1
        offset = 0.0
        
        for note_info in melody_pattern:
            pitch, duration = note_info
            
            # Create a music21 note object
            if pitch == "rest":
                n = note.Rest()
            else:
                n = note.Note(pitch)
                # Vary velocity for more natural sound
                n.volume.velocity = random.randint(70, 100)
            
            n.quarterLength = duration
            
            # Check if we need a new measure
            if offset + duration > 4.0:  # 4.0 for 4/4 time
                # Add current measure to part
                part.append(measure)
                
                # Start a new measure
                current_measure += 1
                measure = stream.Measure(number=current_measure)
                offset = 0.0
            
            # Add note to current measure
            measure.insert(offset, n)
            offset += duration
        
        # Add the last measure if it's not empty
        if measure.elements:
            part.append(measure)
    
    def _generate_bass_part(self, part, scale_notes, chord_progression, total_measures, params):
        """Generate a bass line for instruments like bass guitar, double bass, etc."""
        # Generate a bass line using the chord progression
        bass_pattern = generate_bass_line(
            scale_notes,
            chord_progression,
            total_measures
        )
        
        # Add notes to the part
        measure = stream.Measure(number=1)
        current_measure = 1
        offset = 0.0
        
        for note_info in bass_pattern:
            pitch, duration = note_info
            
            # Create a music21 note object
            if pitch == "rest":
                n = note.Rest()
            else:
                n = note.Note(pitch)
                # Bass notes typically have consistent velocity
                n.volume.velocity = 90
            
            n.quarterLength = duration
            
            # Check if we need a new measure
            if offset + duration > 4.0:
                part.append(measure)
                current_measure += 1
                measure = stream.Measure(number=current_measure)
                offset = 0.0
            
            # Add note to current measure
            measure.insert(offset, n)
            offset += duration
        
        # Add the last measure if it's not empty
        if measure.elements:
            part.append(measure)
    
    def _generate_chord_part(self, part, scale_notes, chord_progression, total_measures, params):
        """Generate chord patterns for instruments like piano, guitar, etc."""
        measure = stream.Measure(number=1)
        current_measure = 1
        
        # Repeat chord progression as needed
        full_progression = []
        while len(full_progression) < total_measures:
            full_progression.extend(chord_progression)
        full_progression = full_progression[:total_measures]
        
        # Use chord complexity to determine voicing
        complexity = params.chord_complexity or 0.5
        
        for measure_num, chord_name in enumerate(full_progression, 1):
            measure = stream.Measure(number=measure_num)
            
            # Get chord notes
            chord_notes = self._get_chord_notes(chord_name, scale_notes)
            
            # Create chord pattern based on style and complexity
            if params.style == "classical":
                self._add_classical_chord_pattern(measure, chord_notes, complexity)
            elif params.style == "jazz":
                self._add_jazz_chord_pattern(measure, chord_notes, complexity)
            elif params.style == "pop" or params.style == "rock":
                self._add_pop_chord_pattern(measure, chord_notes, complexity)
            else:
                # Default pattern
                c = chord.Chord(chord_notes)
                c.quarterLength = 4.0  # Whole measure
                measure.append(c)
            
            part.append(measure)
    
    def _add_classical_chord_pattern(self, measure, chord_notes, complexity):
        """Add classical-style chord patterns to a measure"""
        if complexity > 0.7:
            # Arpeggiated pattern
            for i in range(8):
                note_idx = i % len(chord_notes)
                n = note.Note(chord_notes[note_idx])
                n.quarterLength = 0.5
                n.volume.velocity = 75 + (i % 4) * 5  # Subtle dynamics
                measure.insert(i * 0.5, n)
        else:
            # Block chords with some movement
            c1 = chord.Chord(chord_notes)
            c1.quarterLength = 2.0
            measure.append(c1)
            
            # Second half with slight variation
            if len(chord_notes) > 3 and random.random() < 0.5:
                c2 = chord.Chord(chord_notes[1:] + [chord_notes[0]])  # Inversion
            else:
                c2 = chord.Chord(chord_notes)
            c2.quarterLength = 2.0
            measure.insert(2.0, c2)
    
    def _add_jazz_chord_pattern(self, measure, chord_notes, complexity):
        """Add jazz-style chord patterns to a measure"""
        # Add extensions for jazz chords
        if complexity > 0.6 and len(chord_notes) >= 3:
            root = chord_notes[0]
            # Add 9th
            ninth = note.Note(root).transpose(14).nameWithOctave
            # Add 11th or 13th
            if complexity > 0.8:
                extension = note.Note(root).transpose(18 if random.random() > 0.5 else 21).nameWithOctave
                chord_notes = chord_notes + [ninth, extension]
            else:
                chord_notes = chord_notes + [ninth]
        
        # Jazz comping pattern
        offsets = [0.0, 1.5, 2.5, 3.5] if random.random() > 0.5 else [0.5, 1.5, 2.0, 3.0]
        for i, offset in enumerate(offsets):
            c = chord.Chord(chord_notes)
            c.quarterLength = 0.5
            c.volume.velocity = 70 + (i % 3) * 10  # Jazz dynamics
            measure.insert(offset, c)
    
    def _add_pop_chord_pattern(self, measure, chord_notes, complexity):
        """Add pop/rock-style chord patterns to a measure"""
        # Pattern depends on complexity
        if complexity < 0.4:
            # Simple strumming pattern
            for i in range(4):
                c = chord.Chord(chord_notes)
                c.quarterLength = 1.0
                measure.insert(i, c)
        else:
            # Arpeggiated or syncopated pattern
            pattern = generate_rhythm_pattern(complexity)
            current_offset = 0.0
            
            for duration in pattern:
                if current_offset >= 4.0:
                    break
                    
                if random.random() < 0.2:  # Occasional rest
                    r = note.Rest()
                    r.quarterLength = duration
                    measure.insert(current_offset, r)
                else:
                    c = chord.Chord(chord_notes)
                    c.quarterLength = duration
                    measure.insert(current_offset, c)
                
                current_offset += duration
    
    def _generate_rhythm_part(self, part, scale_notes, chord_progression, total_measures, params):
        """Generate a rhythm part for percussion instruments"""
        # For simplicity, we'll use a repeating pattern based on style
        measure = stream.Measure(number=1)
        current_measure = 1
        
        # Create different patterns based on style
        patterns = {
            "rock": [
                (0.0, "C2", 0.5),  # Kick
                (1.0, "C2", 0.5),  # Kick
                (2.0, "C2", 0.5),  # Kick
                (3.0, "C2", 0.5),  # Kick
                (1.0, "E2", 0.5),  # Snare
                (3.0, "E2", 0.5),  # Snare
                (0.5, "A2", 0.5),  # Hi-hat
                (1.5, "A2", 0.5),  # Hi-hat
                (2.5, "A2", 0.5),  # Hi-hat
                (3.5, "A2", 0.5),  # Hi-hat
            ],
            "pop": [
                (0.0, "C2", 0.5),  # Kick
                (1.0, "E2", 0.5),  # Snare
                (2.0, "C2", 0.5),  # Kick
                (3.0, "E2", 0.5),  # Snare
                (0.0, "A2", 0.25), # Hi-hat
                (0.5, "A2", 0.25), # Hi-hat
                (1.0, "A2", 0.25), # Hi-hat
                (1.5, "A2", 0.25), # Hi-hat
                (2.0, "A2", 0.25), # Hi-hat
                (2.5, "A2", 0.25), # Hi-hat
                (3.0, "A2", 0.25), # Hi-hat
                (3.5, "A2", 0.25), # Hi-hat
            ],
            "jazz": [
                (0.0, "C2", 0.5),  # Kick
                (1.0, "E2", 0.5),  # Snare
                (2.0, "C2", 0.5),  # Kick
                (3.0, "E2", 0.5),  # Snare
                (0.0, "A2", 0.25), # Ride
                (0.5, "A2", 0.25), # Ride
                (1.0, "A2", 0.25), # Ride
                (1.75, "A2", 0.25), # Ride
                (2.0, "A2", 0.25), # Ride
                (2.5, "A2", 0.25), # Ride
                (3.0, "A2", 0.25), # Ride
                (3.5, "A2", 0.25), # Ride
            ],
            "electronic": [
                (0.0, "C2", 0.5),  # Kick
                (1.0, "C2", 0.5),  # Kick
                (1.5, "E2", 0.5),  # Snare
                (2.0, "C2", 0.5),  # Kick
                (3.5, "E2", 0.5),  # Snare
                (0.0, "A2", 0.25), # Hi-hat
                (0.5, "A2", 0.25), # Hi-hat
                (1.0, "A2", 0.25), # Hi-hat
                (1.5, "A2", 0.25), # Hi-hat
                (2.0, "A2", 0.25), # Hi-hat
                (2.5, "A2", 0.25), # Hi-hat
                (3.0, "A2", 0.25), # Hi-hat
                (3.5, "A2", 0.25), # Hi-hat
            ]
        }
        
        # Get pattern based on style, default to pop
        rhythm_pattern = patterns.get(params.style, patterns["pop"])
        
        # Add variations based on complexity
        variation_frequency = params.rhythm_variation or 0.3
        
        # Generate measures with occasional variations
        for i in range(1, total_measures + 1):
            measure = stream.Measure(number=i)
            
            # Add variation every few measures
            add_variation = random.random() < variation_frequency
            
            for offset, pitch, duration in rhythm_pattern:
                # Add slight variation to velocity and timing
                if add_variation:
                    offset_var = random.uniform(-0.05, 0.05)
                    velocity_var = random.randint(-10, 10)
                else:
                    offset_var = 0
                    velocity_var = 0
                
                n = note.Note(pitch)
                n.quarterLength = duration
                n.volume.velocity = 90 + velocity_var
                
                # Ensure offset stays within measure bounds
                adjusted_offset = max(0, min(3.99, offset + offset_var))
                measure.insert(adjusted_offset, n)
            
            part.append(measure)
    
    def _get_chord_notes(self, chord_name, scale_notes):
        """Get the notes for a specific chord"""
        # Simple implementation - in a real application this would be more sophisticated
        roman_to_scale_degree = {
            'I': 0, 'II': 1, 'III': 2, 'IV': 3, 'V': 4, 'VI': 5, 'VII': 6,
            'i': 0, 'ii': 1, 'iii': 2, 'iv': 3, 'v': 4, 'vi': 5, 'vii': 6
        }
        
        # Remove any additional markings like 7, dim, etc. for simplicity
        base_chord = chord_name.split('7')[0].split('dim')[0].split('aug')[0]
        
        if base_chord in roman_to_scale_degree:
            root_idx = roman_to_scale_degree[base_chord]
            
            # For triads: 1-3-5
            root = scale_notes[root_idx]
            third = scale_notes[(root_idx + 2) % 7]
            fifth = scale_notes[(root_idx + 4) % 7]
            
            # Check if we need seventh
            if '7' in chord_name:
                seventh = scale_notes[(root_idx + 6) % 7]
                return [root, third, fifth, seventh]
            
            return [root, third, fifth]
        
        # Fallback
        return [scale_notes[0], scale_notes[2], scale_notes[4]]
    
    def _get_instrument_by_name(self, instrument_name):
        """Convert instrument name to music21 instrument object"""
        # Map common names to music21 instrument classes
        instrument_map = {
            "Piano": instrument.Piano(),
            "Guitar": instrument.Guitar(),
            "Electric Guitar": instrument.ElectricGuitar(),
            "Bass": instrument.ElectricBass(),
            "Bass Guitar": instrument.ElectricBass(),
            "Double Bass": instrument.Contrabass(),
            "Violin": instrument.Violin(),
            "Cello": instrument.Violoncello(),
            "Flute": instrument.Flute(),
            "Saxophone": instrument.SopranoSaxophone(),
            "Drums": instrument.Percussion(),
            "Synth": instrument.Piano(),  # Using Piano as a proxy for synth
            "Synth Lead": instrument.Piano(),
            "Synth Bass": instrument.ElectricBass(),
            "Pad": instrument.Piano()
        }
        
        return instrument_map.get(instrument_name, instrument.Piano())
    
    def _is_bass_instrument(self, instrument_name):
        """Check if the instrument is a bass instrument"""
        bass_instruments = [
            "Bass", "Bass Guitar", "Double Bass", "Synth Bass", "Electric Bass", "Contrabass"
        ]
        return instrument_name in bass_instruments
    
    def _is_rhythm_instrument(self, instrument_name):
        """Check if the instrument is primarily a rhythm instrument"""
        rhythm_instruments = ["Drums", "Percussion", "Drum Kit"]
        return instrument_name in rhythm_instruments
    
    def _is_chord_instrument(self, instrument_name):
        """Check if the instrument primarily plays chords"""
        chord_instruments = ["Piano", "Guitar", "Electric Guitar", "Synth", "Pad"]
        return instrument_name in chord_instruments
