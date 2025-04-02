#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Composer Panel module
Defines the UI panel for music composition controls
"""

import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QComboBox,
    QSpinBox, QSlider, QPushButton, QListWidget, QListWidgetItem, 
    QDoubleSpinBox, QFormLayout, QCheckBox, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QFont

from models.music_model import MusicParameters

logger = logging.getLogger(__name__)

class CompositionThread(QThread):
    """Thread for running composition in the background"""
    composition_complete = pyqtSignal(object)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, ai_composer, params):
        """Initialize the composition thread"""
        super().__init__()
        self.ai_composer = ai_composer
        self.params = params
    
    def run(self):
        """Run the composition"""
        try:
            composition = self.ai_composer.compose(self.params)
            self.composition_complete.emit(composition)
        except Exception as e:
            logger.error(f"Error in composition thread: {e}")
            self.error_occurred.emit(str(e))


class ComposerPanel(QWidget):
    """Panel for controlling the music composition parameters"""
    
    # Signals
    composition_generated = pyqtSignal(object)
    status_message = pyqtSignal(str)
    
    def __init__(self, ai_composer):
        """Initialize the composer panel"""
        super().__init__()
        self.ai_composer = ai_composer
        self.composition_thread = None
        
        # Initialize UI
        self._init_ui()
        
        # Set default parameters
        self.reset_parameters()
        
        logger.info("Composer panel initialized")
    
    def _init_ui(self):
        """Initialize the panel UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title_label = QLabel("AI Music Composer")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Basic parameters group
        basic_group = QGroupBox("Basic Parameters")
        basic_layout = QFormLayout()
        
        # Tempo control
        self.tempo_spin = QSpinBox()
        self.tempo_spin.setRange(40, 240)
        self.tempo_spin.setSuffix(" BPM")
        basic_layout.addRow("Tempo:", self.tempo_spin)
        
        # Key selection
        self.key_combo = QComboBox()
        self.key_combo.addItems([
            "C", "C#/Db", "D", "D#/Eb", "E", "F", 
            "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"
        ])
        basic_layout.addRow("Key:", self.key_combo)
        
        # Mode selection
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Major", "Minor"])
        basic_layout.addRow("Mode:", self.mode_combo)
        
        # Style selection
        self.style_combo = QComboBox()
        self.style_combo.addItems([
            "Classical", "Jazz", "Pop", "Rock", "Electronic"
        ])
        basic_layout.addRow("Style:", self.style_combo)
        
        # Duration control
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(10, 300)
        self.duration_spin.setSuffix(" seconds")
        basic_layout.addRow("Duration:", self.duration_spin)
        
        basic_group.setLayout(basic_layout)
        main_layout.addWidget(basic_group)
        
        # Advanced parameters group
        advanced_group = QGroupBox("Advanced Parameters")
        advanced_layout = QFormLayout()
        
        # Chord complexity
        self.complexity_slider = QSlider(Qt.Horizontal)
        self.complexity_slider.setRange(0, 100)
        self.complexity_slider.setTickPosition(QSlider.TicksBelow)
        self.complexity_slider.setTickInterval(10)
        advanced_layout.addRow("Chord Complexity:", self.complexity_slider)
        
        # Rhythm variation
        self.rhythm_slider = QSlider(Qt.Horizontal)
        self.rhythm_slider.setRange(0, 100)
        self.rhythm_slider.setTickPosition(QSlider.TicksBelow)
        self.rhythm_slider.setTickInterval(10)
        advanced_layout.addRow("Rhythm Variation:", self.rhythm_slider)
        
        advanced_group.setLayout(advanced_layout)
        main_layout.addWidget(advanced_group)
        
        # Instruments group
        instruments_group = QGroupBox("Instruments")
        instruments_layout = QVBoxLayout()
        
        # Available instruments list
        instruments_layout.addWidget(QLabel("Available Instruments:"))
        self.instruments_list = QListWidget()
        self.instruments_list.addItems([
            "Piano", "Guitar", "Electric Guitar", "Bass", "Bass Guitar", 
            "Double Bass", "Violin", "Cello", "Flute", "Saxophone", 
            "Drums", "Synth", "Synth Lead", "Synth Bass", "Pad"
        ])
        self.instruments_list.setSelectionMode(QListWidget.MultiSelection)
        instruments_layout.addWidget(self.instruments_list)
        
        instruments_group.setLayout(instruments_layout)
        main_layout.addWidget(instruments_group)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.suggest_button = QPushButton("Suggest Parameters")
        self.suggest_button.clicked.connect(self.suggest_parameters)
        buttons_layout.addWidget(self.suggest_button)
        
        self.generate_button = QPushButton("Generate Composition")
        self.generate_button.clicked.connect(self.generate_composition)
        self.generate_button.setDefault(True)
        buttons_layout.addWidget(self.generate_button)
        
        main_layout.addLayout(buttons_layout)
    
    def reset_parameters(self):
        """Reset parameters to default values"""
        # Set default values
        self.tempo_spin.setValue(120)
        self.key_combo.setCurrentText("C")
        self.mode_combo.setCurrentText("Major")
        self.style_combo.setCurrentText("Pop")
        self.duration_spin.setValue(60)
        self.complexity_slider.setValue(50)
        self.rhythm_slider.setValue(50)
        
        # Clear instrument selection
        for i in range(self.instruments_list.count()):
            item = self.instruments_list.item(i)
            item.setSelected(False)
        
        # Select default instruments (Piano, Bass, Drums)
        for i in range(self.instruments_list.count()):
            item = self.instruments_list.item(i)
            if item.text() in ["Piano", "Bass", "Drums"]:
                item.setSelected(True)
    
    def get_parameters(self):
        """
        Get the current music parameters from the UI
        
        Returns:
            MusicParameters object with current settings
        """
        # Get basic parameters
        tempo = self.tempo_spin.value()
        key = self.key_combo.currentText()
        mode = self.mode_combo.currentText().lower()
        style = self.style_combo.currentText().lower()
        duration = self.duration_spin.value()
        
        # Get advanced parameters
        chord_complexity = self.complexity_slider.value() / 100.0
        rhythm_variation = self.rhythm_slider.value() / 100.0
        
        # Get selected instruments
        instruments = []
        for item in self.instruments_list.selectedItems():
            instruments.append(item.text())
        
        # Ensure at least one instrument is selected
        if not instruments:
            instruments = ["Piano"]
        
        # Create parameters object
        params = MusicParameters(
            tempo=tempo,
            key=key,
            mode=mode,
            style=style,
            duration=duration,
            chord_complexity=chord_complexity,
            rhythm_variation=rhythm_variation,
            instruments=instruments
        )
        
        return params
    
    def set_parameters(self, params):
        """
        Set UI controls to match provided parameters
        
        Args:
            params: MusicParameters object with settings to apply
        """
        # Set basic parameters
        self.tempo_spin.setValue(params.tempo)
        self.key_combo.setCurrentText(params.key)
        self.mode_combo.setCurrentText(params.mode.title())
        
        # Set style if valid
        style_idx = self.style_combo.findText(params.style.title())
        if style_idx >= 0:
            self.style_combo.setCurrentIndex(style_idx)
        
        # Set duration
        self.duration_spin.setValue(params.duration)
        
        # Set advanced parameters
        if params.chord_complexity is not None:
            self.complexity_slider.setValue(int(params.chord_complexity * 100))
        
        if params.rhythm_variation is not None:
            self.rhythm_slider.setValue(int(params.rhythm_variation * 100))
        
        # Set instruments
        for i in range(self.instruments_list.count()):
            item = self.instruments_list.item(i)
            item.setSelected(item.text() in params.instruments)
    
    def suggest_parameters(self):
        """Suggest music parameters using AI"""
        try:
            # Get AI suggestions
            suggested_params = self.ai_composer.suggest_parameters()
            
            # Update UI with suggested parameters
            self.set_parameters(suggested_params)
            
            self.status_message.emit("Parameters suggested by AI")
            
        except Exception as e:
            logger.error(f"Error suggesting parameters: {e}")
            QMessageBox.warning(
                self,
                "Suggestion Error",
                f"Error suggesting parameters: {str(e)}"
            )
            self.status_message.emit("Error suggesting parameters")
    
    def generate_composition(self):
        """Generate a composition with the current parameters"""
        try:
            # Get parameters from UI
            params = self.get_parameters()
            
            # Check if thread is already running
            if self.composition_thread and self.composition_thread.isRunning():
                QMessageBox.information(
                    self,
                    "In Progress",
                    "A composition is already being generated. Please wait."
                )
                return
            
            # Disable the generate button while composing
            self.generate_button.setEnabled(False)
            self.status_message.emit("Generating composition...")
            
            # Create and start the composition thread
            self.composition_thread = CompositionThread(self.ai_composer, params)
            self.composition_thread.composition_complete.connect(self._on_composition_complete)
            self.composition_thread.error_occurred.connect(self._on_composition_error)
            self.composition_thread.finished.connect(lambda: self.generate_button.setEnabled(True))
            self.composition_thread.start()
            
        except Exception as e:
            logger.error(f"Error generating composition: {e}")
            QMessageBox.critical(
                self,
                "Generation Error",
                f"Error generating composition: {str(e)}"
            )
            self.status_message.emit("Error generating composition")
            self.generate_button.setEnabled(True)
    
    def _on_composition_complete(self, composition):
        """Handle the completed composition"""
        self.status_message.emit("Composition generated successfully")
        self.composition_generated.emit(composition)
    
    def _on_composition_error(self, error_message):
        """Handle composition error"""
        logger.error(f"Composition error: {error_message}")
        QMessageBox.critical(
            self,
            "Composition Error",
            f"Error during composition: {error_message}"
        )
        self.status_message.emit("Composition failed")
