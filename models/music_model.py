#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Music Model module
Defines data models for music parameters and compositions
"""

import logging
from dataclasses import dataclass, field
from typing import List, Optional

logger = logging.getLogger(__name__)

@dataclass
class MusicParameters:
    """
    Class for storing and managing music composition parameters
    
    Attributes:
        tempo (int): Tempo in beats per minute
        key (str): Musical key (e.g., "C", "F#")
        mode (str): Musical mode (e.g., "major", "minor")
        style (str): Musical style (e.g., "classical", "jazz")
        instruments (List[str]): List of instruments
        duration (int): Duration in seconds
        chord_progression (List[str]): Roman numeral chord progression
        chord_complexity (float): Complexity of chord voicings (0.0 to 1.0)
        rhythm_variation (float): Amount of rhythmic variation (0.0 to 1.0)
    """
    
    tempo: int = 120
    key: str = "C"
    mode: str = "major"
    style: str = "pop"
    instruments: List[str] = field(default_factory=lambda: ["Piano", "Bass", "Drums"])
    duration: int = 60
    chord_progression: List[str] = field(default_factory=list)
    chord_complexity: Optional[float] = None
    rhythm_variation: Optional[float] = None
    
    def __post_init__(self):
        """Validate parameters after initialization"""
        # Ensure tempo is within reasonable range
        if self.tempo < 40:
            logger.warning(f"Tempo {self.tempo} too low, setting to minimum 40 BPM")
            self.tempo = 40
        elif self.tempo > 240:
            logger.warning(f"Tempo {self.tempo} too high, setting to maximum 240 BPM")
            self.tempo = 240
        
        # Normalize mode to lowercase
        self.mode = self.mode.lower()
        
        # Normalize style to lowercase
        self.style = self.style.lower()
        
        # Ensure duration is within reasonable range
        if self.duration < 10:
            logger.warning(f"Duration {self.duration}s too short, setting to minimum 10s")
            self.duration = 10
        elif self.duration > 300:
            logger.warning(f"Duration {self.duration}s too long, setting to maximum 300s")
            self.duration = 300
        
        # Ensure chord_complexity is within range if set
        if self.chord_complexity is not None:
            self.chord_complexity = max(0.0, min(1.0, self.chord_complexity))
        
        # Ensure rhythm_variation is within range if set
        if self.rhythm_variation is not None:
            self.rhythm_variation = max(0.0, min(1.0, self.rhythm_variation))
    
    def __str__(self):
        """String representation for logging and debugging"""
        return (
            f"MusicParameters(tempo={self.tempo}, key={self.key}, mode={self.mode}, "
            f"style={self.style}, instruments={self.instruments}, duration={self.duration}s)"
        )

@dataclass
class Note:
    """
    Class representing a musical note
    
    Attributes:
        pitch (str): Note pitch (e.g., "C4", "D#5")
        duration (float): Duration in quarter notes
        velocity (int): MIDI velocity (0-127)
        tied (bool): Whether this note is tied to the next note
    """
    
    pitch: str
    duration: float = 1.0
    velocity: int = 90
    tied: bool = False

@dataclass
class Chord:
    """
    Class representing a musical chord
    
    Attributes:
        notes (List[str]): List of note pitches in the chord
        duration (float): Duration in quarter notes
        velocity (int): MIDI velocity (0-127)
    """
    
    notes: List[str]
    duration: float = 1.0
    velocity: int = 90

@dataclass
class Measure:
    """
    Class representing a musical measure
    
    Attributes:
        elements (List): List of notes and chords
        time_signature (str): Time signature (e.g., "4/4")
        number (int): Measure number
    """
    
    elements: List = field(default_factory=list)
    time_signature: str = "4/4"
    number: int = 1

@dataclass
class Part:
    """
    Class representing an instrumental part
    
    Attributes:
        instrument (str): Instrument name
        measures (List[Measure]): List of measures
    """
    
    instrument: str
    measures: List[Measure] = field(default_factory=list)

@dataclass
class Composition:
    """
    Class representing a complete musical composition
    
    Attributes:
        title (str): Title of the composition
        composer (str): Composer name
        parameters (MusicParameters): Parameters used for generation
        parts (List[Part]): List of instrumental parts
    """
    
    title: str = "Untitled Composition"
    composer: str = "AI Music Composer"
    parameters: MusicParameters = field(default_factory=MusicParameters)
    parts: List[Part] = field(default_factory=list)
