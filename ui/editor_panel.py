#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Editor Panel module
Defines the UI panel for editing generated music
"""

import logging
import tempfile
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QSplitter,
    QPushButton, QToolBar, QAction, QScrollArea, QMessageBox,
    QListWidget, QListWidgetItem, QTabWidget
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QPixmap
from music21 import stream, note, chord, instrument, clef, converter

logger = logging.getLogger(__name__)

class EditorPanel(QWidget):
    """Panel for editing generated music"""
    
    # Signals
    status_message = pyqtSignal(str)
    
    def __init__(self):
        """Initialize the editor panel"""
        super().__init__()
        
        # Initialize state
        self.current_score = None
        self.history = []
        self.history_index = -1
        self.max_history = 10
        
        # Initialize UI
        self._init_ui()
        
        logger.info("Editor panel initialized")
    
    def _init_ui(self):
        """Initialize the panel UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title_label = QLabel("Music Editor")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Toolbar
        self._create_toolbar(main_layout)
        
        # Main editor area with splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side: Parts list and properties
        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right side: Note editor
        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set initial sizes (30% left, 70% right)
        splitter.setSizes([300, 700])
        
        main_layout.addWidget(splitter, 1)
        
        # Status info
        self.status_label = QLabel("No composition loaded")
        main_layout.addWidget(self.status_label)
    
    def _create_toolbar(self, layout):
        """Create the editor toolbar"""
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))
        
        # Undo action
        self.undo_action = QAction("Undo", self)
        self.undo_action.triggered.connect(self.undo)
        self.undo_action.setEnabled(False)
        toolbar.addAction(self.undo_action)
        
        # Redo action
        self.redo_action = QAction("Redo", self)
        self.redo_action.triggered.connect(self.redo)
        self.redo_action.setEnabled(False)
        toolbar.addAction(self.redo_action)
        
        toolbar.addSeparator()
        
        # Note editing actions
        self.delete_action = QAction("Delete", self)
        self.delete_action.triggered.connect(self._on_delete_notes)
        toolbar.addAction(self.delete_action)
        
        self.insert_action = QAction("Insert", self)
        self.insert_action.triggered.connect(self._on_insert_note)
        toolbar.addAction(self.insert_action)
        
        toolbar.addSeparator()
        
        # Part actions
        self.add_part_action = QAction("Add Part", self)
        self.add_part_action.triggered.connect(self._on_add_part)
        toolbar.addAction(self.add_part_action)
        
        self.remove_part_action = QAction("Remove Part", self)
        self.remove_part_action.triggered.connect(self._on_remove_part)
        toolbar.addAction(self.remove_part_action)
        
        layout.addWidget(toolbar)
    
    def _create_left_panel(self):
        """Create the left panel with parts list and properties"""
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Parts group
        parts_group = QGroupBox("Parts")
        parts_layout = QVBoxLayout()
        
        # Parts list
        self.parts_list = QListWidget()
        self.parts_list.currentItemChanged.connect(self._on_part_selected)
        parts_layout.addWidget(self.parts_list)
        
        # Part controls
        parts_controls = QHBoxLayout()
        
        self.move_up_button = QPushButton("Up")
        self.move_up_button.clicked.connect(self._on_move_part_up)
        parts_controls.addWidget(self.move_up_button)
        
        self.move_down_button = QPushButton("Down")
        self.move_down_button.clicked.connect(self._on_move_part_down)
        parts_controls.addWidget(self.move_down_button)
        
        parts_layout.addLayout(parts_controls)
        parts_group.setLayout(parts_layout)
        left_layout.addWidget(parts_group)
        
        # Properties group
        properties_group = QGroupBox("Properties")
        properties_layout = QVBoxLayout()
        
        # Simple text for now - would be more detailed in a real app
        self.properties_label = QLabel("No part selected")
        self.properties_label.setWordWrap(True)
        properties_layout.addWidget(self.properties_label)
        
        properties_group.setLayout(properties_layout)
        left_layout.addWidget(properties_group)
        
        return left_widget
    
    def _create_right_panel(self):
        """Create the right panel with the note editor"""
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create tabs for different views
        tabs = QTabWidget()
        
        # Score view
        self.score_view = QScrollArea()
        self.score_view.setWidgetResizable(True)
        self.score_view_content = QLabel("No score to display")
        self.score_view_content.setAlignment(Qt.AlignCenter)
        self.score_view.setWidget(self.score_view_content)
        tabs.addTab(self.score_view, "Score View")
        
        # Piano roll view - placeholder
        piano_roll = QLabel("Piano Roll View\n(Not implemented in this prototype)")
        piano_roll.setAlignment(Qt.AlignCenter)
        tabs.addTab(piano_roll, "Piano Roll")
        
        # Text view - placeholder
        text_view = QLabel("Text View\n(Not implemented in this prototype)")
        text_view.setAlignment(Qt.AlignCenter)
        tabs.addTab(text_view, "Text View")
        
        right_layout.addWidget(tabs)
        
        # Editor controls
        controls_layout = QHBoxLayout()
        
        self.playback_button = QPushButton("Test Playback")
        self.playback_button.clicked.connect(self._on_test_playback)
        controls_layout.addWidget(self.playback_button)
        
        self.apply_button = QPushButton("Apply Changes")
        self.apply_button.clicked.connect(self._on_apply_changes)
        controls_layout.addWidget(self.apply_button)
        
        right_layout.addLayout(controls_layout)
        
        return right_widget
    
    def set_score(self, score):
        """
        Set the current score for editing
        
        Args:
            score: music21 stream object representing the composition
        """
        try:
            if score:
                # Add to history
                self._add_to_history(score)
                
                # Update parts list
                self._update_parts_list()
                
                # Update score view
                self._update_score_view()
                
                # Update status
                part_count = len(score.parts)
                measure_count = len(score.parts[0].getElementsByClass('Measure')) if part_count > 0 else 0
                self.status_label.setText(f"Loaded score with {part_count} parts, {measure_count} measures")
                self.status_message.emit(f"Loaded score with {part_count} parts")
            else:
                self.clear_editor()
                
        except Exception as e:
            logger.error(f"Error setting score: {e}")
            self.status_message.emit("Error loading score")
    
    def get_score(self):
        """
        Get the current score
        
        Returns:
            The current music21 score object
        """
        return self.current_score
    
    def clear_editor(self):
        """Clear the editor state"""
        self.current_score = None
        self.history = []
        self.history_index = -1
        self.parts_list.clear()
        self.score_view_content.setText("No score to display")
        self.properties_label.setText("No part selected")
        self.status_label.setText("No composition loaded")
        self.undo_action.setEnabled(False)
        self.redo_action.setEnabled(False)
    
    def undo(self):
        """Undo the last edit"""
        if self.history_index > 0:
            self.history_index -= 1
            self.current_score = self.history[self.history_index]
            self._update_ui_after_history_change()
            self.status_message.emit("Undo performed")
    
    def redo(self):
        """Redo the last undone edit"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_score = self.history[self.history_index]
            self._update_ui_after_history_change()
            self.status_message.emit("Redo performed")
    
    def _add_to_history(self, score):
        """Add a score to the edit history"""
        # Create a deep copy to store in history
        score_copy = score.deepcopy()
        
        # If we're not at the end of the history, truncate
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        # Add to history
        self.history.append(score_copy)
        self.history_index = len(self.history) - 1
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
            self.history_index = len(self.history) - 1
        
        # Update the current score reference
        self.current_score = score
        
        # Update UI controls
        self.undo_action.setEnabled(self.history_index > 0)
        self.redo_action.setEnabled(False)  # Can't redo after a new edit
    
    def _update_ui_after_history_change(self):
        """Update UI after a history change (undo/redo)"""
        self._update_parts_list()
        self._update_score_view()
        
        # Update undo/redo buttons
        self.undo_action.setEnabled(self.history_index > 0)
        self.redo_action.setEnabled(self.history_index < len(self.history) - 1)
    
    def _update_parts_list(self):
        """Update the parts list based on the current score"""
        self.parts_list.clear()
        
        if not self.current_score:
            return
        
        for i, part in enumerate(self.current_score.parts):
            # Get instrument name
            instr_name = "Unknown"
            for element in part.flat:
                if isinstance(element, instrument.Instrument):
                    instr_name = element.instrumentName
                    break
            
            item = QListWidgetItem(f"Part {i+1}: {instr_name}")
            item.setData(Qt.UserRole, i)  # Store part index
            self.parts_list.addItem(item)
    
    def _update_score_view(self):
        """Update the score visualization"""
        if not self.current_score:
            self.score_view_content.setText("No score to display")
            return
        
        try:
            # This is a simplified approach - in a real application, 
            # we would use a more sophisticated visualization
            
            # Create a temporary file for the score image
            temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            temp_file.close()
            
            # This would require MuseScore or Lilypond for proper rendering
            # For demonstration, we'll use a placeholder approach
            
            # In a real application, you would use:
            # self.current_score.write('musicxml.png', fp=temp_file.name)
            
            # For now, just display text representation
            score_text = "Score Display (Limited Functionality)\n\n"
            
            # Show a basic text representation of the score
            for part_idx, part in enumerate(self.current_score.parts):
                # Find instrument
                instr_name = "Unknown"
                for element in part.flat:
                    if isinstance(element, instrument.Instrument):
                        instr_name = element.instrumentName
                        break
                
                score_text += f"Part {part_idx+1}: {instr_name}\n"
                
                # Count measures and notes
                measures = part.getElementsByClass('Measure')
                note_count = len(part.flat.notes)
                
                score_text += f"  Measures: {len(measures)}, Notes: {note_count}\n"
                
                # Show first few measures as text
                max_measures = min(3, len(measures))
                for i in range(max_measures):
                    measure = measures[i]
                    notes_text = []
                    
                    for note_element in measure.notes:
                        if isinstance(note_element, note.Note):
                            notes_text.append(note_element.nameWithOctave)
                        elif isinstance(note_element, chord.Chord):
                            chord_text = "[" + " ".join(n.nameWithOctave for n in note_element.notes) + "]"
                            notes_text.append(chord_text)
                    
                    score_text += f"  Measure {i+1}: {' '.join(notes_text)}\n"
                
                score_text += "\n"
            
            self.score_view_content.setText(score_text)
            
            # In a real app with proper rendering:
            # pixmap = QPixmap(temp_file.name)
            # self.score_view_content.setPixmap(pixmap)
            
        except Exception as e:
            logger.error(f"Error updating score view: {e}")
            self.score_view_content.setText(f"Error displaying score: {str(e)}")
    
    def _on_part_selected(self, current, previous):
        """Handle selection of a part in the list"""
        if not current:
            self.properties_label.setText("No part selected")
            return
        
        part_idx = current.data(Qt.UserRole)
        
        if self.current_score and part_idx < len(self.current_score.parts):
            part = self.current_score.parts[part_idx]
            
            # Get instrument info
            instr_name = "Unknown"
            for element in part.flat:
                if isinstance(element, instrument.Instrument):
                    instr_name = element.instrumentName
                    break
            
            # Count measures and notes
            measures = part.getElementsByClass('Measure')
            note_count = len(part.flat.notes)
            
            # Get clef
            clef_name = "Treble"  # Default
            for element in part.flat:
                if isinstance(element, clef.Clef):
                    clef_name = element.name
                    break
            
            # Update properties display
            properties = (
                f"Instrument: {instr_name}\n"
                f"Measures: {len(measures)}\n"
                f"Notes: {note_count}\n"
                f"Clef: {clef_name}\n"
            )
            
            self.properties_label.setText(properties)
    
    def _on_move_part_up(self):
        """Move the selected part up in the score"""
        if not self.current_score:
            return
        
        current_item = self.parts_list.currentItem()
        if not current_item:
            return
        
        current_idx = current_item.data(Qt.UserRole)
        if current_idx > 0:
            # Create a copy of the score to modify
            score_copy = self.current_score.deepcopy()
            
            # Swap parts
            score_copy.insert(current_idx - 1, score_copy.pop(current_idx))
            
            # Add to history
            self._add_to_history(score_copy)
            
            # Update UI
            self._update_parts_list()
            self._update_score_view()
            
            # Select the moved part
            for i in range(self.parts_list.count()):
                item = self.parts_list.item(i)
                if item.data(Qt.UserRole) == current_idx - 1:
                    self.parts_list.setCurrentItem(item)
                    break
            
            self.status_message.emit(f"Moved part up")
    
    def _on_move_part_down(self):
        """Move the selected part down in the score"""
        if not self.current_score:
            return
        
        current_item = self.parts_list.currentItem()
        if not current_item:
            return
        
        current_idx = current_item.data(Qt.UserRole)
        if current_idx < len(self.current_score.parts) - 1:
            # Create a copy of the score to modify
            score_copy = self.current_score.deepcopy()
            
            # Swap parts
            score_copy.insert(current_idx + 1, score_copy.pop(current_idx))
            
            # Add to history
            self._add_to_history(score_copy)
            
            # Update UI
            self._update_parts_list()
            self._update_score_view()
            
            # Select the moved part
            for i in range(self.parts_list.count()):
                item = self.parts_list.item(i)
                if item.data(Qt.UserRole) == current_idx + 1:
                    self.parts_list.setCurrentItem(item)
                    break
            
            self.status_message.emit(f"Moved part down")
    
    def _on_add_part(self):
        """Add a new empty part to the score"""
        if not self.current_score:
            QMessageBox.warning(
                self,
                "No Score",
                "No composition is loaded to add parts to."
            )
            return
        
        try:
            # Create a copy of the score to modify
            score_copy = self.current_score.deepcopy()
            
            # Create a new part with a piano
            new_part = stream.Part()
            piano = instrument.Piano()
            new_part.append(piano)
            
            # Get measures from the first part as a template
            if score_copy.parts:
                # Clone measures structure (without notes)
                template_part = score_copy.parts[0]
                for measure in template_part.getElementsByClass('Measure'):
                    # Create a new measure with the same time signature and clef
                    m = stream.Measure(number=measure.number)
                    
                    # Copy time signature if present
                    ts = measure.timeSignature
                    if ts:
                        m.timeSignature = ts
                    
                    # Add a clef
                    m.clef = clef.TrebleClef()
                    
                    # Add to the new part
                    new_part.append(m)
            
            # Add the new part to the score
            score_copy.append(new_part)
            
            # Add to history
            self._add_to_history(score_copy)
            
            # Update UI
            self._update_parts_list()
            self._update_score_view()
            
            # Select the new part
            self.parts_list.setCurrentRow(self.parts_list.count() - 1)
            
            self.status_message.emit("Added new part")
        
        except Exception as e:
            logger.error(f"Error adding part: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to add part: {str(e)}"
            )
    
    def _on_remove_part(self):
        """Remove the selected part from the score"""
        if not self.current_score:
            return
        
        current_item = self.parts_list.currentItem()
        if not current_item:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a part to remove."
            )
            return
        
        # Confirm with user
        response = QMessageBox.question(
            self,
            "Confirm Removal",
            "Are you sure you want to remove this part?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if response == QMessageBox.Yes:
            part_idx = current_item.data(Qt.UserRole)
            
            # Create a copy of the score to modify
            score_copy = self.current_score.deepcopy()
            
            # Check if this is the last part
            if len(score_copy.parts) <= 1:
                QMessageBox.warning(
                    self,
                    "Cannot Remove",
                    "Cannot remove the last part from the composition."
                )
                return
            
            # Remove the part
            score_copy.remove(score_copy.parts[part_idx])
            
            # Add to history
            self._add_to_history(score_copy)
            
            # Update UI
            self._update_parts_list()
            self._update_score_view()
            
            self.status_message.emit(f"Removed part")
    
    def _on_delete_notes(self):
        """Delete selected notes (placeholder implementation)"""
        QMessageBox.information(
            self,
            "Limited Functionality",
            "Detailed note editing is not implemented in this prototype."
        )
    
    def _on_insert_note(self):
        """Insert a new note (placeholder implementation)"""
        QMessageBox.information(
            self,
            "Limited Functionality",
            "Detailed note editing is not implemented in this prototype."
        )
    
    def _on_test_playback(self):
        """Test playback of the current score"""
        if not self.current_score:
            QMessageBox.warning(
                self,
                "No Score",
                "No composition is loaded to play."
            )
            return
        
        # Emit signal to trigger playback in the main window
        self.status_message.emit("Playing score...")
        
        # This would typically communicate with a playback system
        # For the prototype, we'll just show a message
        QMessageBox.information(
            self,
            "Playback",
            "In a complete application, this would play the current state of the score."
        )
    
    def _on_apply_changes(self):
        """Apply any pending changes"""
        # In this prototype, changes are applied immediately
        # In a real app, this might consolidate multiple small edits
        QMessageBox.information(
            self,
            "Changes Applied",
            "All changes have been applied to the score."
        )
        self.status_message.emit("Changes applied")
