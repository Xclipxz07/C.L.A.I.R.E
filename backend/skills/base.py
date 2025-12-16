"""
Base Skill class for C.L.A.I.R.E plugins
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseSkill(ABC):
    """Base class for all skills"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize skill with configuration"""
        self.config = config
    
    @abstractmethod
    def can_handle(self, user_input: str) -> bool:
        """
        Check if this skill can handle the user input
        
        Args:
            user_input: User's command text
            
        Returns:
            True if this skill should handle the input
        """
        pass
    
    @abstractmethod
    def execute(self, user_input: str) -> str:
        """
        Execute the skill
        
        Args:
            user_input: User's command text
            
        Returns:
            Response text
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """
        Get skill description for help text
        
        Returns:
            Description string
        """
        pass
