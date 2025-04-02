#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Handlers module
Handles file operations for importing and exporting music files
"""

import os
import logging
import tempfile
from typing import Tuple, Optional, Any
import mido
from PyQt5.QtWidgets import QFileDialog

logger = logging.getLogger(__name__)

def get_save_file_path(parent: Any, title: str, directory: str, filter_str: str) -> Optional[str]:
    """
    Show a file save dialog and return the selected path
    
    Args:
        parent: Parent widget for the dialog
        title: Dialog title
        directory: Initial directory
        filter_str: File type filter string
        
    Returns:
        Selected file path or None if cancelled
    """
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getSaveFileName(
        parent, title, directory, filter_str, options=options
    )
    
    if file_path:
        # Ensure the file has the correct extension
        if "MIDI" in filter_str and not file_path.lower().endswith(('.mid', '.midi')):
            file_path += '.mid'
        elif "WAV" in filter_str and not file_path.lower().endswith('.wav'):
            file_path += '.wav'
        
        return file_path
    
    return None

def get_open_file_path(parent: Any, title: str, directory: str, filter_str: str) -> Optional[str]:
    """
    Show a file open dialog and return the selected path
    
    Args:
        parent: Parent widget for the dialog
        title: Dialog title
        directory: Initial directory
        filter_str: File type filter string
        
    Returns:
        Selected file path or None if cancelled
    """
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getOpenFileName(
        parent, title, directory, filter_str, options=options
    )
    
    if file_path:
        return file_path
    
    return None

def is_midi_file(file_path: str) -> bool:
    """
    Check if a file is a MIDI file
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is a MIDI file, False otherwise
    """
    if not os.path.isfile(file_path):
        return False
    
    # Check file extension
    if not file_path.lower().endswith(('.mid', '.midi')):
        return False
    
    # Try to open as MIDI
    try:
        mido.MidiFile(file_path)
        return True
    except:
        return False

def is_audio_file(file_path: str) -> bool:
    """
    Check if a file is an audio file
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is an audio file, False otherwise
    """
    if not os.path.isfile(file_path):
        return False
    
    # Check file extension
    audio_extensions = ('.wav', '.mp3', '.ogg', '.flac', '.aac')
    if not file_path.lower().endswith(audio_extensions):
        return False
    
    # For more thorough validation, we would analyze the file header
    # but that would require additional libraries
    
    return True

def get_file_type(file_path: str) -> str:
    """
    Determine the type of a music file
    
    Args:
        file_path: Path to the file
        
    Returns:
        String describing the file type ("midi", "audio", or "unknown")
    """
    if is_midi_file(file_path):
        return "midi"
    elif is_audio_file(file_path):
        return "audio"
    else:
        return "unknown"

def create_temp_file(suffix: str = '.mid') -> Tuple[str, Any]:
    """
    Create a temporary file with the specified suffix
    
    Args:
        suffix: File extension
        
    Returns:
        Tuple of (file path, file object)
    """
    temp_file = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    return temp_file.name, temp_file

def clean_up_temp_file(file_path: str) -> bool:
    """
    Remove a temporary file
    
    Args:
        file_path: Path to the temporary file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.debug(f"Removed temporary file: {file_path}")
            return True
    except Exception as e:
        logger.warning(f"Failed to remove temporary file {file_path}: {e}")
    
    return False
