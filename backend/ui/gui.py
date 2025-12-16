"""
GUI for C.L.A.I.R.E using PyQt6
Graphical interface for the assistant
"""

import sys
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ClaireGUI:
    """Graphical User Interface for Claire"""
    
    def __init__(self, assistant):
        """Initialize GUI"""
        self.assistant = assistant
        
        # Try to import PyQt6
        try:
            from PyQt6.QtWidgets import QApplication
            self.app = QApplication(sys.argv)
        except ImportError:
            raise ImportError(
                "PyQt6 not installed. Install with: pip install PyQt6\n"
                "Or use terminal mode instead."
            )
    
    def run(self):
        """Run the GUI"""
        try:
            from PyQt6.QtWidgets import (
                QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                QTextEdit, QLineEdit, QPushButton, QLabel
            )
            from PyQt6.QtCore import Qt
            from PyQt6.QtGui import QFont
            
            class MainWindow(QMainWindow):
                def __init__(self, assistant):
                    super().__init__()
                    self.assistant = assistant
                    self.init_ui()
                
                def init_ui(self):
                    """Initialize the UI"""
                    self.setWindowTitle(f"{self.assistant.name} - AI Assistant")
                    self.setGeometry(100, 100, 800, 600)
                    
                    # Central widget
                    central_widget = QWidget()
                    self.setCentralWidget(central_widget)
                    
                    # Layout
                    layout = QVBoxLayout()
                    
                    # Title
                    title = QLabel(f"✨ {self.assistant.name}")
                    title.setFont(QFont('Arial', 20, QFont.Weight.Bold))
                    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    layout.addWidget(title)
                    
                    # Chat display
                    self.chat_display = QTextEdit()
                    self.chat_display.setReadOnly(True)
                    self.chat_display.setFont(QFont('Consolas', 10))
                    layout.addWidget(self.chat_display)
                    
                    # Input area
                    input_layout = QHBoxLayout()
                    
                    self.input_field = QLineEdit()
                    self.input_field.setPlaceholderText("Type your message here...")
                    self.input_field.setFont(QFont('Arial', 11))
                    self.input_field.returnPressed.connect(self.send_message)
                    input_layout.addWidget(self.input_field)
                    
                    self.send_button = QPushButton("Send")
                    self.send_button.clicked.connect(self.send_message)
                    input_layout.addWidget(self.send_button)
                    
                    layout.addLayout(input_layout)
                    
                    central_widget.setLayout(layout)
                    
                    # Welcome message
                    self.add_message(
                        "System",
                        f"Welcome to C.L.A.I.R.E\n"
                        f"Conversational Language AI Responsive Entity\n\n"
                        f"I'm {self.assistant.name}, your AI assistant.\n"
                        "How can I help you today?",
                        color="blue"
                    )
                
                def send_message(self):
                    """Send user message"""
                    user_input = self.input_field.text().strip()
                    
                    if not user_input:
                        return
                    
                    # Display user message
                    self.add_message("You", user_input, color="green")
                    
                    # Clear input
                    self.input_field.clear()
                    
                    # Get response
                    try:
                        response = self.assistant.process_command(user_input)
                        self.add_message(self.assistant.name, response, color="purple")
                    except Exception as e:
                        self.add_message("Error", str(e), color="red")
                
                def add_message(self, sender: str, message: str, color: str = "black"):
                    """Add message to chat display"""
                    self.chat_display.append(
                        f'<p><b><font color="{color}">{sender}:</font></b> {message}</p>'
                    )
            
            # Create and show window
            window = MainWindow(self.assistant)
            window.show()
            
            # Run application
            sys.exit(self.app.exec())
            
        except Exception as e:
            logger.error(f"GUI error: {e}")
            print(f"❌ GUI error: {e}")
            print("Falling back to terminal mode...\n")
            
            # Fallback to terminal
            from backend.ui.terminal_ui import TerminalUI
            ui = TerminalUI(self.assistant)
            ui.run()
