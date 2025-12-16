"""
Terminal UI for C.L.A.I.R.E
Simple text-based interface
"""

import sys
from typing import Optional
from backend.core.assistant import ClaireAssistant


class TerminalUI:
    """Simple terminal-based interface"""
    
    def __init__(self, assistant: ClaireAssistant):
        """Initialize terminal UI"""
        self.assistant = assistant
    
    def run(self):
        """Run the terminal interface"""
        print(f"\n{'='*60}")
        print(f"  {self.assistant.name} - Terminal Mode")
        print(f"  Type 'help' for commands, 'exit' to quit")
        print(f"{'='*60}\n")
        
        while True:
            try:
                # Get user input
                user_input = input(f"\n💬 You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    response = self.assistant.process_command(user_input)
                    print(f"\n🤖 {self.assistant.name}: {response}")
                    break
                
                # Process command
                response = self.assistant.process_command(user_input)
                
                # Display response
                print(f"\n🤖 {self.assistant.name}: {response}")
                
            except KeyboardInterrupt:
                print(f"\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    def display_message(self, message: str, prefix: str = "ℹ️"):
        """Display a message"""
        print(f"\n{prefix} {message}")
