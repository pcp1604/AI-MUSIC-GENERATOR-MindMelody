#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Playback Panel module
Defines the UI panel for playback controls
"""

import logging
import threading
import time
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, 
    QPushButton, QSlider, QStyle, QSizePolicy, QProgressBar,
    QComboBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

logger = logging.getLogger(__name__)

class PlaybackPanel(QWidget):
    """Panel for audio playback controls"""
    
    # Signals
    status_message = pyqtSignal(str)
    
    def __init__(self, audio_processor):
        """Initialize the playback panel"""
        super().__init__()
        self.audio_processor = audio_processor
        self.current_score = None
        self.current_audio = None
        self.current_sample_rate = None
        self.playback_timer = QTimer(self)
        self.playback_timer.timeout.connect(self._update_playback_position)
        
        # Initialize UI
        self._init_ui()
        
        logger.info("Playback panel initialized")
    
    def _init_ui(self):
        """Initialize the panel UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title_label = QLabel("Playback Controls")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Playback control group
        control_group = QGroupBox("Controls")
        control_layout = QVBoxLayout()
        
        # Transport controls
        transport_layout = QHBoxLayout()
        
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play)
        transport_layout.addWidget(self.play_button)
        
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause)
        self.pause_button.setEnabled(False)
        transport_layout.addWidget(self.pause_button)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setEnabled(False)
        transport_layout.addWidget(self.stop_button)
        
        control_layout.addLayout(transport_layout)
        
        # Progress bar
        progress_layout = QHBoxLayout()
        self.position_label = QLabel("0:00")
        progress_layout.addWidget(self.position_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar, 1)
        
        self.duration_label = QLabel("0:00")
        progress_layout.addWidget(self.duration_label)
        
        control_layout.addLayout(progress_layout)
        
        # Volume control
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("Volume:"))
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        volume_layout.addWidget(self.volume_slider, 1)
        
        control_layout.addLayout(volume_layout)
        
        # Playback speed
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Speed:"))
        
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.5x", "0.75x", "1.0x", "1.25x", "1.5x", "2.0x"])
        self.speed_combo.setCurrentText("1.0x")
        self.speed_combo.currentTextChanged.connect(self._on_speed_changed)
        speed_layout.addWidget(self.speed_combo)
        
        control_layout.addLayout(speed_layout)
        
        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)
        
        # Info group
        info_group = QGroupBox("Playback Information")
        info_layout = QVBoxLayout()
        
        self.info_label = QLabel("No audio loaded")
        self.info_label.setWordWrap(True)
        info_layout.addWidget(self.info_label)
        
        info_group.setLayout(info_layout)
        main_layout.addWidget(info_group)
        
        # Export group
        export_group = QGroupBox("Export")
        export_layout = QHBoxLayout()
        
        self.export_midi_button = QPushButton("Export as MIDI")
        self.export_midi_button.clicked.connect(self._on_export_midi)
        export_layout.addWidget(self.export_midi_button)
        
        self.export_wav_button = QPushButton("Export as WAV")
        self.export_wav_button.clicked.connect(self._on_export_wav)
        export_layout.addWidget(self.export_wav_button)
        
        export_group.setLayout(export_layout)
        main_layout.addWidget(export_group)
    
    def set_score(self, score):
        """
        Set the current score for playback
        
        Args:
            score: music21 stream object representing the composition
        """
        try:
            self.current_score = score
            self.current_audio = None
            self.current_sample_rate = None
            
            if score:
                # Calculate duration from tempo and measures
                try:
                    # Get tempo
                    tempo = 120  # Default
                    for element in score.flat:
                        if element.classes[0] == 'MetronomeMark':
                            tempo = element.number
                            break
                    
                    # Get measure count from first part
                    if score.parts:
                        measures = score.parts[0].getElementsByClass('Measure')
                        measure_count = len(measures)
                    else:
                        measure_count = 0
                    
                    # Calculate approximate duration in seconds
                    # This is simplified - a real app would calculate more precisely
                    duration_secs = measure_count * 4 * 60 / tempo
                    
                    # Update UI
                    self._set_duration(duration_secs)
                    
                    # Update info
                    info = (
                        f"Composition loaded\n"
                        f"Parts: {len(score.parts)}\n"
                        f"Measures: {measure_count}\n"
                        f"Tempo: {tempo} BPM\n"
                        f"Approx. Duration: {self._format_time(duration_secs)}"
                    )
                    self.info_label.setText(info)
                    
                except Exception as e:
                    logger.error(f"Error calculating score duration: {e}")
                    self._set_duration(0)
                    self.info_label.setText("Error calculating score information")
            else:
                self.clear_playback()
            
        except Exception as e:
            logger.error(f"Error setting score for playback: {e}")
            self.status_message.emit("Error loading score for playback")
    
    def set_audio(self, audio_data, sample_rate):
        """
        Set raw audio data for playback
        
        Args:
            audio_data: NumPy array of audio samples
            sample_rate: Sample rate of the audio
        """
        try:
            self.current_score = None
            self.current_audio = audio_data
            self.current_sample_rate = sample_rate
            
            if audio_data is not None:
                # Calculate duration
                duration_secs = len(audio_data) / sample_rate
                
                # Update UI
                self._set_duration(duration_secs)
                
                # Update info
                info = (
                    f"Audio loaded\n"
                    f"Sample Rate: {sample_rate} Hz\n"
                    f"Channels: {'Stereo' if audio_data.ndim > 1 else 'Mono'}\n"
                    f"Duration: {self._format_time(duration_secs)}"
                )
                self.info_label.setText(info)
            else:
                self.clear_playback()
                
        except Exception as e:
            logger.error(f"Error setting audio for playback: {e}")
            self.status_message.emit("Error loading audio for playback")
    
    def clear_playback(self):
        """Clear the current playback state"""
        self.stop()
        self.current_score = None
        self.current_audio = None
        self.current_sample_rate = None
        self._set_duration(0)
        self.info_label.setText("No audio loaded")
    
    def play(self):
        """Start or resume playback"""
        try:
            if self.current_score:
                # Play the score
                if self.audio_processor.is_playback_active():
                    # Resume paused playback
                    success = self.audio_processor.resume_playback()
                else:
                    # Start new playback
                    success = self.audio_processor.play_score(self.current_score)
                
                if success:
                    # Update UI
                    self.play_button.setEnabled(False)
                    self.pause_button.setEnabled(True)
                    self.stop_button.setEnabled(True)
                    
                    # Start progress timer
                    self.playback_timer.start(100)  # Update every 100ms
                    
                    self.status_message.emit("Playback started")
                else:
                    self.status_message.emit("Failed to start playback")
            
            elif self.current_audio is not None:
                # This would normally play the audio data
                # For the prototype, just show an info message
                self.status_message.emit("Audio playback not implemented in prototype")
            
            else:
                self.status_message.emit("No audio to play")
                
        except Exception as e:
            logger.error(f"Error during playback: {e}")
            self.status_message.emit("Error during playback")
    
    def pause(self):
        """Pause playback"""
        try:
            success = self.audio_processor.pause_playback()
            
            if success:
                # Update UI
                self.play_button.setEnabled(True)
                self.pause_button.setEnabled(False)
                
                # Stop progress timer
                self.playback_timer.stop()
                
                self.status_message.emit("Playback paused")
            else:
                self.status_message.emit("Failed to pause playback")
                
        except Exception as e:
            logger.error(f"Error pausing playback: {e}")
            self.status_message.emit("Error pausing playback")
    
    def stop(self):
        """Stop playback"""
        try:
            success = self.audio_processor.stop_playback()
            
            if success:
                # Update UI
                self.play_button.setEnabled(True)
                self.pause_button.setEnabled(False)
                self.stop_button.setEnabled(False)
                
                # Reset progress
                self.progress_bar.setValue(0)
                self.position_label.setText("0:00")
                
                # Stop progress timer
                self.playback_timer.stop()
                
                self.status_message.emit("Playback stopped")
            else:
                self.status_message.emit("Failed to stop playback")
                
        except Exception as e:
            logger.error(f"Error stopping playback: {e}")
            self.status_message.emit("Error stopping playback")
    
    def _on_volume_changed(self, value):
        """Handle volume slider change"""
        try:
            volume = value / 100.0
            success = self.audio_processor.set_volume(volume)
            
            if success:
                self.status_message.emit(f"Volume set to {value}%")
            else:
                self.status_message.emit("Failed to set volume")
                
        except Exception as e:
            logger.error(f"Error setting volume: {e}")
            self.status_message.emit("Error setting volume")
    
    def _on_speed_changed(self, speed_text):
        """Handle playback speed change"""
        try:
            speed = float(speed_text.replace('x', ''))
            
            # Real implementation would change the playback speed
            # This is a placeholder for the prototype
            self.status_message.emit(f"Playback speed set to {speed_text}")
            
        except Exception as e:
            logger.error(f"Error setting playback speed: {e}")
            self.status_message.emit("Error setting playback speed")
    
    def _update_playback_position(self):
        """Update the playback position indicator"""
        if self.audio_processor.is_playback_active():
            # Calculate current position
            # This is a rough estimate for the prototype
            # A real app would track the actual playback position
            
            progress = self.progress_bar.value() + 1
            if progress > 100:
                progress = 100
            
            self.progress_bar.setValue(progress)
            
            # Calculate time based on progress and duration
            duration = self._get_duration_seconds()
            current_time = duration * (progress / 100.0)
            self.position_label.setText(self._format_time(current_time))
        else:
            # Playback finished or stopped
            self.playback_timer.stop()
            self.play_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            
            # Reset or complete the progress bar
            if self.progress_bar.value() >= 99:
                # Playback completed
                self.progress_bar.setValue(100)
                self.position_label.setText(self.duration_label.text())
                self.status_message.emit("Playback complete")
    
    def _set_duration(self, duration_secs):
        """Set the duration display"""
        self.duration_label.setText(self._format_time(duration_secs))
        self._duration_seconds = duration_secs
    
    def _get_duration_seconds(self):
        """Get the duration in seconds"""
        return getattr(self, '_duration_seconds', 0)
    
    def _format_time(self, seconds):
        """Format seconds as mm:ss"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"
    
    def _on_export_midi(self):
        """Handle export as MIDI action"""
        # This would communicate with the main window to trigger export
        self.status_message.emit("MIDI export requested")
    
    def _on_export_wav(self):
        """Handle export as WAV action"""
        # This would communicate with the main window to trigger export
        self.status_message.emit("WAV export requested")
