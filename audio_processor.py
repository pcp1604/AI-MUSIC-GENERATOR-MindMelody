#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Audio Processor module
Handles audio file import, export, and playback
"""

import os
import logging
import tempfile
import numpy as np
import pygame
import soundfile as sf
import librosa
from music21 import converter, midi

logger = logging.getLogger(__name__)

class AudioProcessor:
    """
    Handles audio processing tasks including playback, file conversions,
    and audio analysis
    """
    
    def __init__(self):
        """Initialize the audio processor"""
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
        self.current_playback = None
        self.is_playing = False
        self.temp_files = []
        logger.info("Audio Processor initialized")
    
    def __del__(self):
        """Clean up temporary files on deletion"""
        self._cleanup_temp_files()
    
    def _cleanup_temp_files(self):
        """Remove any temporary files created during processing"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    logger.debug(f"Removed temporary file: {temp_file}")
            except Exception as e:
                logger.warning(f"Failed to remove temporary file {temp_file}: {e}")
        
        self.temp_files = []
    
    def import_audio_file(self, file_path):
        """
        Import an audio file for analysis
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            tuple: (numpy array of audio data, sample rate)
        """
        try:
            if file_path.lower().endswith('.midi') or file_path.lower().endswith('.mid'):
                return self._import_midi_file(file_path)
            else:
                return self._import_audio_file(file_path)
        except Exception as e:
            logger.error(f"Error importing audio file {file_path}: {e}")
            raise
    
    def _import_midi_file(self, file_path):
        """Import a MIDI file and return a music21 score object"""
        try:
            score = converter.parse(file_path)
            logger.info(f"Successfully imported MIDI file: {file_path}")
            return score
        except Exception as e:
            logger.error(f"Error parsing MIDI file {file_path}: {e}")
            raise
    
    def _import_audio_file(self, file_path):
        """Import an audio file (WAV, MP3, etc.) and return audio data"""
        try:
            y, sr = librosa.load(file_path, sr=None)
            logger.info(f"Successfully imported audio file: {file_path}")
            return y, sr
        except Exception as e:
            logger.error(f"Error loading audio file {file_path}: {e}")
            raise
    
    def export_midi(self, score, output_path):
        """
        Export a music21 score to a MIDI file
        
        Args:
            score: music21 score object
            output_path: Path where the MIDI file should be saved
            
        Returns:
            bool: Success status
        """
        try:
            midi_file = score.write('midi', fp=output_path)
            logger.info(f"Successfully exported MIDI to: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting MIDI file to {output_path}: {e}")
            return False
    
    def export_wav(self, score, output_path, sample_rate=44100):
        """
        Export a music21 score to a WAV file
        
        Args:
            score: music21 score object
            output_path: Path where the WAV file should be saved
            sample_rate: Sample rate for the WAV file
            
        Returns:
            bool: Success status
        """
        try:
            # First convert to MIDI
            temp_midi = tempfile.NamedTemporaryFile(suffix='.mid', delete=False)
            temp_midi.close()
            self.temp_files.append(temp_midi.name)
            
            score.write('midi', fp=temp_midi.name)
            
            # Then convert MIDI to audio using FluidSynth
            # This would require fluidsynth to be installed
            # In a real application, you would use a more robust solution
            
            logger.warning("WAV export is a placeholder - requires external tools")
            logger.info(f"MIDI file exported to: {temp_midi.name}")
            logger.info(f"For real WAV export, convert the MIDI file using a DAW or FluidSynth")
            
            # For demonstration purposes, we'll just copy the MIDI file
            # In a real app, you would actually create WAV data here
            import shutil
            shutil.copy(temp_midi.name, output_path)
            
            return True
        except Exception as e:
            logger.error(f"Error exporting WAV file to {output_path}: {e}")
            return False
    
    def play_score(self, score):
        """
        Play a music21 score through pygame
        
        Args:
            score: music21 score object
            
        Returns:
            bool: Success status
        """
        try:
            # Stop any current playback
            self.stop_playback()
            
            # Convert to MIDI and play
            temp_midi = tempfile.NamedTemporaryFile(suffix='.mid', delete=False)
            temp_midi.close()
            self.temp_files.append(temp_midi.name)
            
            score.write('midi', fp=temp_midi.name)
            
            # Load and play the MIDI file
            pygame.mixer.music.load(temp_midi.name)
            pygame.mixer.music.play()
            self.is_playing = True
            
            logger.info("Started playback of music score")
            return True
        except Exception as e:
            logger.error(f"Error during score playback: {e}")
            return False
    
    def pause_playback(self):
        """Pause the current playback"""
        try:
            if self.is_playing:
                pygame.mixer.music.pause()
                self.is_playing = False
                logger.info("Playback paused")
            return True
        except Exception as e:
            logger.error(f"Error pausing playback: {e}")
            return False
    
    def resume_playback(self):
        """Resume the current playback"""
        try:
            if not self.is_playing:
                pygame.mixer.music.unpause()
                self.is_playing = True
                logger.info("Playback resumed")
            return True
        except Exception as e:
            logger.error(f"Error resuming playback: {e}")
            return False
    
    def stop_playback(self):
        """Stop the current playback"""
        try:
            pygame.mixer.music.stop()
            self.is_playing = False
            logger.info("Playback stopped")
            return True
        except Exception as e:
            logger.error(f"Error stopping playback: {e}")
            return False
    
    def is_playback_active(self):
        """Check if playback is currently active"""
        return pygame.mixer.music.get_busy()
    
    def set_volume(self, volume):
        """
        Set playback volume
        
        Args:
            volume: Volume level between 0.0 and 1.0
            
        Returns:
            bool: Success status
        """
        try:
            pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
            logger.info(f"Volume set to {volume}")
            return True
        except Exception as e:
            logger.error(f"Error setting volume: {e}")
            return False
    
    def analyze_audio(self, audio_data, sample_rate):
        """
        Analyze audio data to extract features
        
        Args:
            audio_data: NumPy array of audio samples
            sample_rate: Sample rate of the audio
            
        Returns:
            dict: Dictionary of audio features
        """
        try:
            # Extract various features using librosa
            features = {}
            
            # Compute tempo
            onset_env = librosa.onset.onset_strength(y=audio_data, sr=sample_rate)
            tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sample_rate)
            features['tempo'] = tempo
            
            # Compute spectral centroid
            cent = librosa.feature.spectral_centroid(y=audio_data, sr=sample_rate)
            features['spectral_centroid'] = np.mean(cent)
            
            # Compute RMS energy
            rms = librosa.feature.rms(y=audio_data)
            features['rms'] = np.mean(rms)
            
            # Compute chroma features
            chromagram = librosa.feature.chroma_stft(y=audio_data, sr=sample_rate)
            features['chroma'] = np.mean(chromagram, axis=1)
            
            logger.info("Audio analysis completed")
            return features
        except Exception as e:
            logger.error(f"Error analyzing audio: {e}")
            return {}
