"""
System Control Skill for C.L.A.I.R.E
Handles system operations like opening apps, files, etc.
"""

import logging
import os
import platform
import subprocess
from typing import Dict, Any
from backend.skills.base import BaseSkill

logger = logging.getLogger(__name__)


class SystemSkill(BaseSkill):
    """Control system operations"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.allow_shutdown = config.get('allow_shutdown', False)
        self.system = platform.system()
    
    def can_handle(self, user_input: str) -> bool:
        """Check if this is a system command"""
        keywords = ['open', 'launch', 'start', 'close', 'shutdown', 'restart', 'volume']
        text_lower = user_input.lower()
        return any(keyword in text_lower for keyword in keywords)
    
    def execute(self, user_input: str) -> str:
        """Execute system command"""
        text_lower = user_input.lower()
        
        # Open application
        if 'open' in text_lower or 'launch' in text_lower or 'start' in text_lower:
            return self._open_application(user_input)
        
        # Volume control
        if 'volume' in text_lower:
            return "Volume control coming soon!"
        
        # Shutdown/Restart
        if 'shutdown' in text_lower or 'restart' in text_lower:
            if not self.allow_shutdown:
                return "Shutdown/restart commands are disabled in settings for safety."
            return "Shutdown/restart commands coming soon!"
        
        return "I'm not sure how to handle that system command yet."
    
    def _open_application(self, text: str) -> str:
        """Open an application"""
        text_lower = text.lower()
        
        # Common applications mapping
        apps = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'chrome': 'chrome.exe',
            'edge': 'msedge.exe',
            'firefox': 'firefox.exe',
            'explorer': 'explorer.exe',
            'file explorer': 'explorer.exe',
            'cmd': 'cmd.exe',
            'command prompt': 'cmd.exe',
            'powershell': 'powershell.exe',
            'terminal': 'wt.exe',  # Windows Terminal
        }
        
        # Try to find app name in text
        for app_name, executable in apps.items():
            if app_name in text_lower:
                try:
                    if self.system == 'Windows':
                        subprocess.Popen(executable, shell=True)
                    elif self.system == 'Darwin':  # macOS
                        subprocess.Popen(['open', '-a', executable])
                    else:  # Linux
                        subprocess.Popen(executable, shell=True)
                    
                    return f"Opening {app_name.title()}..."
                except Exception as e:
                    logger.error(f"Failed to open {app_name}: {e}")
                    return f"Sorry, I couldn't open {app_name}: {e}"
        
        return "I couldn't identify which application you want to open. Try: 'open notepad' or 'open chrome'"
    
    def get_description(self) -> str:
        """Get skill description"""
        return "Control system (e.g., 'open notepad', 'launch chrome')"
