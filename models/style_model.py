#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Style Model module
Defines musical style models for different genres
"""

import logging
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

@dataclass
class StyleModel:
    """
    Class representing a musical style model with characteristic parameters
    
    Attributes:
        name (str): Name of the style
        chord_complexity (float): Typical chord complexity (0.0 to 1.0)
        rhythm_variation (float): Typical rhythm variation (0.0 to 1.0)
        typical_progressions (List[List[str]]): List of typical chord progressions
        typical_instruments (List[str]): List of typical instruments
        tempo_range (tuple): Typical tempo range (min, max)
        description (str): Description of the style
    """
    
    name: str
    chord_complexity: float = 0.5
    rhythm_variation: float = 0.5
    typical_progressions: List[List[str]] = field(default_factory=list)
    typical_instruments: List[str] = field(default_factory=list)
    tempo_range: tuple = (80, 120)
    description: str = ""
    
    def __post_init__(self):
        """Initialize style-specific defaults if not provided"""
        # Set default progressions based on style if not provided
        if not self.typical_progressions:
            self.typical_progressions = self._get_default_progressions()
        
        # Set default instruments based on style if not provided
        if not self.typical_instruments:
            self.typical_instruments = self._get_default_instruments()
        
        # Set default description if not provided
        if not self.description:
            self.description = self._get_default_description()
    
    def _get_default_progressions(self) -> List[List[str]]:
        """Get default chord progressions for this style"""
        # Define common progressions by style
        progression_map = {
            "classical": [
                ["I", "IV", "V", "I"],
                ["I", "V", "vi", "IV"],
                ["I", "vi", "IV", "V"],
                ["I", "IV", "I", "V"]
            ],
            "jazz": [
                ["ii7", "V7", "Imaj7", "VI7"],
                ["Imaj7", "VI7", "ii7", "V7"],
                ["iii7", "VI7", "ii7", "V7"],
                ["I7", "IV7", "I7", "V7"]
            ],
            "pop": [
                ["I", "V", "vi", "IV"],
                ["I", "IV", "V", "IV"],
                ["vi", "IV", "I", "V"],
                ["I", "V", "IV", "V"]
            ],
            "rock": [
                ["I", "IV", "V", "IV"],
                ["I", "V", "IV", "IV"],
                ["I", "III", "IV", "IV"],
                ["I", "bVII", "IV", "I"]
            ],
            "electronic": [
                ["I", "vi", "IV", "V"],
                ["I", "V", "vi", "IV"],
                ["vi", "IV", "I", "V"],
                ["I", "I", "IV", "V"]
            ]
        }
        
        # Return default progressions or generic ones if style not found
        return progression_map.get(self.name.lower(), [["I", "IV", "V", "I"]])
    
    def _get_default_instruments(self) -> List[str]:
        """Get default instruments for this style"""
        # Define common instruments by style
        instrument_map = {
            "classical": ["Piano", "Violin", "Cello", "Flute"],
            "jazz": ["Piano", "Saxophone", "Double Bass", "Drums"],
            "pop": ["Piano", "Guitar", "Bass", "Drums", "Synth"],
            "rock": ["Electric Guitar", "Bass Guitar", "Drums", "Piano"],
            "electronic": ["Synth Lead", "Synth Bass", "Drums", "Pad"]
        }
        
        # Return default instruments or generic ones if style not found
        return instrument_map.get(self.name.lower(), ["Piano", "Guitar", "Bass", "Drums"])
    
    def _get_default_description(self) -> str:
        """Get default description for this style"""
        # Define descriptions by style
        description_map = {
            "classical": "Traditional Western art music with formal structures and orchestral instrumentation.",
            "jazz": "Improvisation-heavy style characterized by swing rhythms and extended harmonic vocabulary.",
            "pop": "Contemporary popular music with catchy melodies, verse-chorus structure, and modern production.",
            "rock": "Guitar-driven style with strong beats and often rebellious themes.",
            "electronic": "Computer-generated music with electronic sounds and repetitive beats."
        }
        
        # Return description or generic one if style not found
        return description_map.get(
            self.name.lower(), 
            f"{self.name.title()} music style."
        )
    
    def get_typical_progression(self) -> List[str]:
        """
        Get a randomly selected typical chord progression for this style
        
        Returns:
            List of chord symbols (Roman numerals)
        """
        if self.typical_progressions:
            return random.choice(self.typical_progressions)
        else:
            return ["I", "IV", "V", "I"]  # Default progression
    
    def get_random_instrument_set(self, min_count=2, max_count=4) -> List[str]:
        """
        Get a random selection of instruments typical for this style
        
        Args:
            min_count: Minimum number of instruments
            max_count: Maximum number of instruments
            
        Returns:
            List of instrument names
        """
        if not self.typical_instruments:
            return ["Piano", "Bass"]
        
        # Determine how many instruments to include
        count = min(max(min_count, 2), min(max_count, len(self.typical_instruments)))
        
        # Return a random selection
        return random.sample(self.typical_instruments, count)
    
    def get_random_tempo(self) -> int:
        """
        Get a random tempo within the typical range for this style
        
        Returns:
            Tempo in BPM
        """
        return random.randint(self.tempo_range[0], self.tempo_range[1])
