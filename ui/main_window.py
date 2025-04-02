#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main Window module
Defines the primary application window and UI layout
"""

import os
import logging
import webbrowser
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
    QAction, QMenuBar, QFileDialog, QMessageBox, QSplitter,
    QLabel, QStatusBar, QToolBar
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QKeySequence

from ui.composer_panel import ComposerPanel
from ui.editor_panel import EditorPanel
from ui.playback_panel import PlaybackPanel
from ui.styles import StyleManager
from ai_composer import AIComposer
from audio_processor import AudioProcessor

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """Main application window for the AI Music Composer"""
    
    def __init__(self):
        """Initialize the main window"""
        super().__init__()
        
        # Initialize components
        self.ai_composer = AIComposer()
        self.audio_processor = AudioProcessor()
        self.style_manager = StyleManager()
        
        # Set up window
        self.setWindowTitle("AI Music Composer")
        self.setMinimumSize(1000, 700)
        
        # Apply application styles
        self.style_manager.apply_application_style(self)
        
        # Initialize UI
        self._create_menu_bar()
        self._create_tool_bar()
        self._create_status_bar()
        self._create_central_widget()
        
        # Set up file handling
        self.current_file = None
        
        logger.info("Main window initialized")
    
    def _create_menu_bar(self):
        """Create the application menu bar"""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&File")
        
        new_action = QAction("&New Composition", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self._on_new_composition)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self._on_open_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self._on_save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self._on_save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        export_midi_action = QAction("Export as &MIDI...", self)
        export_midi_action.triggered.connect(self._on_export_midi)
        file_menu.addAction(export_midi_action)
        
        export_wav_action = QAction("Export as &WAV...", self)
        export_wav_action.triggered.connect(self._on_export_wav)
        file_menu.addAction(export_wav_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menu_bar.addMenu("&Edit")
        
        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self._on_undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self._on_redo)
        edit_menu.addAction(redo_action)
        
        # Composition menu
        comp_menu = menu_bar.addMenu("&Composition")
        
        generate_action = QAction("&Generate Composition", self)
        generate_action.setShortcut("Ctrl+G")
        generate_action.triggered.connect(self._on_generate_composition)
        comp_menu.addAction(generate_action)
        
        suggest_action = QAction("&Suggest Parameters", self)
        suggest_action.setShortcut("Ctrl+S")
        suggest_action.triggered.connect(self._on_suggest_parameters)
        comp_menu.addAction(suggest_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)
        
        help_action = QAction("&Help", self)
        help_action.setShortcut(QKeySequence.HelpContents)
        help_action.triggered.connect(self._on_help)
        help_menu.addAction(help_action)
    
    def _create_tool_bar(self):
        """Create the main toolbar"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # Add actions with icons
        # Note: In a real application, these would use actual icons
        
        # New composition action
        new_action = QAction("New", self)
        new_action.triggered.connect(self._on_new_composition)
        toolbar.addAction(new_action)
        
        # Open file action
        open_action = QAction("Open", self)
        open_action.triggered.connect(self._on_open_file)
        toolbar.addAction(open_action)
        
        # Save file action
        save_action = QAction("Save", self)
        save_action.triggered.connect(self._on_save_file)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Generate composition action
        generate_action = QAction("Generate", self)
        generate_action.triggered.connect(self._on_generate_composition)
        toolbar.addAction(generate_action)
        
        # Suggest parameters action
        suggest_action = QAction("Suggest", self)
        suggest_action.triggered.connect(self._on_suggest_parameters)
        toolbar.addAction(suggest_action)
        
        toolbar.addSeparator()
        
        # Playback controls
        play_action = QAction("Play", self)
        play_action.triggered.connect(self._on_play)
        toolbar.addAction(play_action)
        
        pause_action = QAction("Pause", self)
        pause_action.triggered.connect(self._on_pause)
        toolbar.addAction(pause_action)
        
        stop_action = QAction("Stop", self)
        stop_action.triggered.connect(self._on_stop)
        toolbar.addAction(stop_action)
    
    def _create_status_bar(self):
        """Create the status bar"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        self.status_label = QLabel("Ready")
        status_bar.addWidget(self.status_label, 1)
    
    def _create_central_widget(self):
        """Create the central widget with panels"""
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Create a splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Create panels
        self.composer_panel = ComposerPanel(self.ai_composer)
        self.editor_panel = EditorPanel()
        self.playback_panel = PlaybackPanel(self.audio_processor)
        
        # Connect signals
        self.composer_panel.composition_generated.connect(self._on_composition_generated)
        self.composer_panel.status_message.connect(self._update_status)
        self.editor_panel.status_message.connect(self._update_status)
        self.playback_panel.status_message.connect(self._update_status)
        
        # Create tabs for editor and playback
        right_tabs = QTabWidget()
        right_tabs.addTab(self.editor_panel, "Editor")
        right_tabs.addTab(self.playback_panel, "Playback")
        
        # Add widgets to splitter
        splitter.addWidget(self.composer_panel)
        splitter.addWidget(right_tabs)
        
        # Set initial sizes (40% composer, 60% editor/playback)
        splitter.setSizes([400, 600])
        
        main_layout.addWidget(splitter)
    
    def _update_status(self, message):
        """Update the status bar message"""
        self.status_label.setText(message)
    
    def _on_new_composition(self):
        """Handle new composition action"""
        # Ask to save if there's unsaved work
        if self._confirm_discard_changes():
            self.current_file = None
            self.composer_panel.reset_parameters()
            self.editor_panel.clear_editor()
            self.playback_panel.clear_playback()
            self._update_status("New composition started")
    
    def _on_open_file(self):
        """Handle open file action"""
        if self._confirm_discard_changes():
            file_dialog = QFileDialog(self)
            file_dialog.setNameFilter("Music files (*.mid *.midi *.wav);;All files (*.*)")
            file_dialog.setViewMode(QFileDialog.Detail)
            
            if file_dialog.exec_():
                selected_files = file_dialog.selectedFiles()
                if selected_files:
                    file_path = selected_files[0]
                    self._load_file(file_path)
    
    def _load_file(self, file_path):
        """Load a music file"""
        try:
            self._update_status(f"Loading {file_path}...")
            
            # Import the file
            if file_path.lower().endswith(('.mid', '.midi')):
                # Handle MIDI file
                score = self.audio_processor.import_audio_file(file_path)
                
                # Analyze the file to extract parameters
                parameters = self.ai_composer.analyze_imported_music(score)
                
                # Update the UI
                self.composer_panel.set_parameters(parameters)
                self.editor_panel.set_score(score)
                self.playback_panel.set_score(score)
                
            elif file_path.lower().endswith(('.wav', '.mp3')):
                # Handle audio file - more limited support
                QMessageBox.information(
                    self, 
                    "Audio Import", 
                    "Audio file import is limited to analysis only. No editing will be available."
                )
                
                audio_data, sample_rate = self.audio_processor.import_audio_file(file_path)
                features = self.audio_processor.analyze_audio(audio_data, sample_rate)
                
                # Create basic parameters from audio analysis
                parameters = self.ai_composer.suggest_parameters()
                if 'tempo' in features:
                    parameters.tempo = int(features['tempo'])
                
                self.composer_panel.set_parameters(parameters)
                self.playback_panel.set_audio(audio_data, sample_rate)
            
            self.current_file = file_path
            self._update_status(f"Loaded {os.path.basename(file_path)}")
            
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {e}")
            QMessageBox.critical(
                self, 
                "Error", 
                f"Failed to load file: {str(e)}"
            )
            self._update_status("Error loading file")
    
    def _on_save_file(self):
        """Handle save file action"""
        if self.current_file:
            self._save_file(self.current_file)
        else:
            self._on_save_file_as()
    
    def _on_save_file_as(self):
        """Handle save file as action"""
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("MIDI files (*.mid);;All files (*.*)")
        file_dialog.setDefaultSuffix("mid")
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                self._save_file(file_path)
    
    def _save_file(self, file_path):
        """Save the current composition to a file"""
        try:
            self._update_status(f"Saving to {file_path}...")
            
            # Get the current score
            score = self.editor_panel.get_score()
            if score:
                # Save as MIDI
                if self.audio_processor.export_midi(score, file_path):
                    self.current_file = file_path
                    self._update_status(f"Saved to {os.path.basename(file_path)}")
                else:
                    raise Exception("Failed to export MIDI file")
            else:
                raise Exception("No composition to save")
                
        except Exception as e:
            logger.error(f"Error saving file {file_path}: {e}")
            QMessageBox.critical(
                self, 
                "Error", 
                f"Failed to save file: {str(e)}"
            )
            self._update_status("Error saving file")
    
    def _on_export_midi(self):
        """Handle export as MIDI action"""
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("MIDI files (*.mid);;All files (*.*)")
        file_dialog.setDefaultSuffix("mid")
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                
                try:
                    self._update_status(f"Exporting MIDI to {file_path}...")
                    
                    # Get the current score
                    score = self.editor_panel.get_score()
                    if score:
                        # Export as MIDI
                        if self.audio_processor.export_midi(score, file_path):
                            self._update_status(f"Exported MIDI to {os.path.basename(file_path)}")
                        else:
                            raise Exception("Failed to export MIDI file")
                    else:
                        raise Exception("No composition to export")
                        
                except Exception as e:
                    logger.error(f"Error exporting MIDI to {file_path}: {e}")
                    QMessageBox.critical(
                        self, 
                        "Error", 
                        f"Failed to export MIDI: {str(e)}"
                    )
                    self._update_status("Error exporting MIDI")
    
    def _on_export_wav(self):
        """Handle export as WAV action"""
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("WAV files (*.wav);;All files (*.*)")
        file_dialog.setDefaultSuffix("wav")
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                
                try:
                    self._update_status(f"Exporting WAV to {file_path}...")
                    
                    # Get the current score
                    score = self.editor_panel.get_score()
                    if score:
                        # Export as WAV
                        if self.audio_processor.export_wav(score, file_path):
                            self._update_status(f"Exported WAV to {os.path.basename(file_path)}")
                        else:
                            raise Exception("Failed to export WAV file")
                    else:
                        raise Exception("No composition to export")
                        
                except Exception as e:
                    logger.error(f"Error exporting WAV to {file_path}: {e}")
                    QMessageBox.critical(
                        self, 
                        "Error", 
                        f"Failed to export WAV: {str(e)}"
                    )
                    self._update_status("Error exporting WAV")
    
    def _on_undo(self):
        """Handle undo action"""
        self.editor_panel.undo()
    
    def _on_redo(self):
        """Handle redo action"""
        self.editor_panel.redo()
    
    def _on_generate_composition(self):
        """Handle generate composition action"""
        self._update_status("Generating composition...")
        self.composer_panel.generate_composition()
    
    def _on_suggest_parameters(self):
        """Handle suggest parameters action"""
        self._update_status("Suggesting parameters...")
        self.composer_panel.suggest_parameters()
    
    def _on_composition_generated(self, score):
        """Handle newly generated composition"""
        self.editor_panel.set_score(score)
        self.playback_panel.set_score(score)
        self._update_status("Composition generated")
    
    def _on_play(self):
        """Handle play action"""
        self.playback_panel.play()
    
    def _on_pause(self):
        """Handle pause action"""
        self.playback_panel.pause()
    
    def _on_stop(self):
        """Handle stop action"""
        self.playback_panel.stop()
    
    def _on_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About AI Music Composer",
            "<h3>AI Music Composer</h3>"
            "<p>Version 1.0</p>"
            "<p>An AI-powered application for music composition</p>"
            "<p>&copy; 2023 AI Music Labs</p>"
        )
    
    def _on_help(self):
        """Show help documentation"""
        # In a real app, this might open a help window or user manual
        try:
            help_file = os.path.join(os.path.dirname(__file__), "..", "resources", "help.html")
            if os.path.exists(help_file):
                webbrowser.open(f"file://{os.path.abspath(help_file)}")
            else:
                QMessageBox.information(
                    self,
                    "Help",
                    "Help documentation not found. Please visit our website for assistance."
                )
        except Exception as e:
            logger.error(f"Error opening help: {e}")
            QMessageBox.warning(
                self,
                "Help",
                "Could not open help documentation."
            )
    
    def _confirm_discard_changes(self):
        """
        Confirm with the user if they want to discard unsaved changes
        
        Returns:
            bool: True if it's okay to proceed, False to cancel
        """
        # In a real app, we would check if there are unsaved changes
        # For now, we'll just return True
        return True
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self._confirm_discard_changes():
            # Clean up resources
            self.audio_processor.stop_playback()
            event.accept()
        else:
            event.ignore()
