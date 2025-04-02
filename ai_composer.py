#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI Composer module
Handles the high-level logic for music composition
"""

import logging
import numpy as np
from sklearn.cluster import KMeans
from music_generator import MusicGenerator
from models.music_model import MusicParameters
from models.style_model import StyleModel
from utils.music_theory import get_chord_progression, get_scale_notes

logger = logging.getLogger(__name__)

class AIComposer:
    """Main AI composer class that orchestrates the music generation process"""
    
    def __init__(self):
        """Initialize the AI composer with necessary components"""
        self.music_generator = MusicGenerator()
        self.style_models = self._load_style_models()
        logger.info("AI Composer initialized")
    
    def _load_style_models(self):
        """Load and prepare style models for different music genres"""
        styles = {
            "classical": StyleModel("classical", chord_complexity=0.8, rhythm_variation=0.6),
            "jazz": StyleModel("jazz", chord_complexity=0.9, rhythm_variation=0.9),
            "pop": StyleModel("pop", chord_complexity=0.5, rhythm_variation=0.4),
            "rock": StyleModel("rock", chord_complexity=0.6, rhythm_variation=0.7),
            "electronic": StyleModel("electronic", chord_complexity=0.4, rhythm_variation=0.8)
        }
        return styles
    
    def compose(self, parameters: MusicParameters):
        """
        Generate a musical composition based on the provided parameters
        
        Args:
            parameters: MusicParameters object containing composition settings
            
        Returns:
            A music21 stream object representing the composition
        """
        logger.info(f"Starting composition with parameters: {parameters}")
        
        # Apply style model if specified
        if parameters.style in self.style_models:
            self._apply_style_model(parameters, self.style_models[parameters.style])
        
        # Generate the music
        composition = self.music_generator.generate(parameters)
        
        logger.info("Composition completed")
        return composition
    
    def _apply_style_model(self, parameters, style_model):
        """Apply a style model's characteristics to the parameters"""
        # Adjust parameters based on style
        parameters.chord_complexity = style_model.chord_complexity
        parameters.rhythm_variation = style_model.rhythm_variation
        
        # Set typical chord progressions for the style
        if not parameters.chord_progression:
            parameters.chord_progression = style_model.get_typical_progression()
    
    def suggest_parameters(self, seed=None):
        """
        Suggest a set of music parameters that could work well together
        
        Args:
            seed: Optional seed value for reproducible suggestions
            
        Returns:
            MusicParameters object with suggested values
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Choose a random style
        style = np.random.choice(list(self.style_models.keys()))
        style_model = self.style_models[style]
        
        # Generate tempo within appropriate range for the style
        tempo_ranges = {
            "classical": (60, 120),
            "jazz": (80, 140),
            "pop": (90, 130),
            "rock": (100, 160),
            "electronic": (110, 180)
        }
        tempo_range = tempo_ranges.get(style, (80, 140))
        tempo = np.random.randint(tempo_range[0], tempo_range[1])
        
        # Select a key
        keys = ["C", "G", "D", "A", "E", "B", "F#", "C#", "F", "Bb", "Eb", "Ab", "Db", "Gb", "Cb"]
        key = np.random.choice(keys)
        
        # Decide major or minor
        is_major = np.random.choice([True, False], p=[0.7, 0.3])  # Biased toward major
        mode = "major" if is_major else "minor"
        
        # Select instruments based on style
        instruments = self._suggest_instruments_for_style(style)
        
        # Create suggested parameters
        suggested = MusicParameters(
            tempo=tempo,
            key=key,
            mode=mode,
            style=style,
            instruments=instruments,
            chord_progression=style_model.get_typical_progression(),
            duration=np.random.randint(30, 180)  # 30s to 3m
        )
        
        logger.info(f"Suggested parameters: {suggested}")
        return suggested
    
    def _suggest_instruments_for_style(self, style):
        """Suggest appropriate instruments for a given style"""
        instrument_sets = {
            "classical": ["Piano", "Violin", "Cello", "Flute"],
            "jazz": ["Piano", "Saxophone", "Double Bass", "Drums"],
            "pop": ["Piano", "Guitar", "Bass", "Drums", "Synth"],
            "rock": ["Electric Guitar", "Bass Guitar", "Drums", "Piano"],
            "electronic": ["Synth Lead", "Synth Bass", "Drums", "Pad"]
        }
        
        # Select 2-4 instruments from the appropriate set
        available_instruments = instrument_sets.get(style, ["Piano", "Guitar", "Bass", "Drums"])
        count = np.random.randint(2, min(4, len(available_instruments)) + 1)
        return list(np.random.choice(available_instruments, size=count, replace=False))
    
    def analyze_imported_music(self, music_stream):
        """
        Analyze imported music to extract key parameters
        
        Args:
            music_stream: A music21 stream object to analyze
            
        Returns:
            MusicParameters object with extracted parameters
        """
        from music21 import analysis, meter
        
        try:
            # Analyze key
            key_analysis = analysis.discrete.analyzeStream(music_stream, 'key')
            key = key_analysis.tonic.name
            mode = "major" if key_analysis.mode == "major" else "minor"
            
            # Extract tempo
            tempo = 120  # Default
            for m in music_stream.flat.getElementsByClass(meter.MetronomeMark):
                tempo = m.number
                break
            
            # Count unique instruments
            instruments = []
            for instrument in music_stream.flat.getInstruments():
                if instrument.instrumentName and instrument.instrumentName not in instruments:
                    instruments.append(instrument.instrumentName)
            
            # Create parameters from analysis
            parameters = MusicParameters(
                tempo=tempo,
                key=key,
                mode=mode,
                instruments=instruments if instruments else ["Piano"],
                duration=int(music_stream.duration.quarterLength * 60 / tempo)
            )
            
            # Try to determine style
            # (This would be more sophisticated in a real application)
            parameters.style = self._guess_style(music_stream)
            
            return parameters
        
        except Exception as e:
            logger.error(f"Error analyzing imported music: {e}")
            # Return default parameters if analysis fails
            return MusicParameters()
    
    def _guess_style(self, music_stream):
        """Make a basic guess at the style of the music"""
        # This would use more sophisticated analysis in a real application
        # Here we're using a very simplified approach
        
        # Count syncopation, chord complexity, and note density
        syncopation_count = 0
        chord_sizes = []
        note_count = 0
        
        for measure in music_stream.measures(0, None):
            # Count notes to estimate density
            notes = measure.flat.notes
            note_count += len(notes)
            
            # Look at chord sizes
            for chord in measure.flat.getElementsByClass('Chord'):
                chord_sizes.append(len(chord.pitches))
            
            # Check for off-beat notes as a rough syncopation estimate
            for note in notes:
                if note.offset % 1.0 != 0:
                    syncopation_count += 1
        
        # Very simple classification
        if len(chord_sizes) > 0 and np.mean(chord_sizes) > 3.5:
            return "jazz"  # Complex chords suggest jazz
        elif syncopation_count > note_count * 0.4:
            return "electronic"  # Lots of syncopation suggests electronic
        elif note_count > len(music_stream.measures(0, None)) * 8:
            return "classical"  # High note density suggests classical
        elif note_count < len(music_stream.measures(0, None)) * 3:
            return "rock"  # Sparser texture suggests rock
        else:
            return "pop"  # Default to pop
