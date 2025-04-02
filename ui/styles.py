#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Styles module
Defines the application UI styles and themes
"""

import logging
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt

logger = logging.getLogger(__name__)

class StyleManager:
    """Manages application styles and themes"""
    
    def __init__(self):
        """Initialize the style manager"""
        self.available_themes = ["Light", "Dark", "System"]
        self.current_theme = "System"
        logger.info("Style manager initialized")
    
    def apply_application_style(self, window):
        """
        Apply global application style and theme
        
        Args:
            window: The main application window
        """
        try:
            # Use the fusion style for a more modern look
            QApplication.setStyle(QStyleFactory.create("Fusion"))
            
            # Apply theme based on current setting
            if self.current_theme == "Dark":
                self._apply_dark_theme()
            elif self.current_theme == "Light":
                self._apply_light_theme()
            else:
                # Use system default
                pass
            
            # Apply custom fonts
            self._apply_fonts(window)
            
            logger.info(f"Applied application style: {self.current_theme} theme")
        except Exception as e:
            logger.error(f"Error applying application style: {e}")
    
    def _apply_dark_theme(self):
        """Apply a dark color theme to the application"""
        palette = QPalette()
        
        # Base colors
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(35, 35, 35))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        
        # Button colors
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        
        # Link colors
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        
        # Apply the palette
        QApplication.setPalette(palette)
    
    def _apply_light_theme(self):
        """Apply a light color theme to the application"""
        palette = QPalette()
        
        # Base colors
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.WindowText, QColor(20, 20, 20))
        palette.setColor(QPalette.Base, QColor(250, 250, 250))
        palette.setColor(QPalette.AlternateBase, QColor(233, 233, 233))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(20, 20, 20))
        palette.setColor(QPalette.Text, QColor(20, 20, 20))
        
        # Button colors
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, QColor(20, 20, 20))
        palette.setColor(QPalette.BrightText, Qt.red)
        
        # Link colors
        palette.setColor(QPalette.Link, QColor(0, 100, 200))
        palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        
        # Apply the palette
        QApplication.setPalette(palette)
    
    def _apply_fonts(self, window):
        """
        Apply custom fonts to the application
        
        Args:
            window: The main application window
        """
        # Set default font
        default_font = QFont("Arial", 10)
        QApplication.setFont(default_font)
        
        # Apply custom styles for specific widgets (can be extended as needed)
        window.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 3px;
                left: 10px;
            }
            
            QPushButton {
                padding: 5px 10px;
                border-radius: 3px;
            }
            
            QSlider::groove:horizontal {
                height: 8px;
                background: #CCCCCC;
                margin: 2px 0;
                border-radius: 4px;
            }
            
            QSlider::handle:horizontal {
                background: #5A5A5A;
                border: 1px solid #5A5A5A;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            
            QComboBox {
                padding: 3px 10px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
            
            QListWidget {
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
        """)
    
    def get_available_themes(self):
        """
        Get list of available themes
        
        Returns:
            List of theme names
        """
        return self.available_themes
    
    def set_theme(self, theme_name):
        """
        Set the current theme
        
        Args:
            theme_name: Name of the theme to apply
            
        Returns:
            bool: Success status
        """
        if theme_name in self.available_themes:
            self.current_theme = theme_name
            return True
        return False
