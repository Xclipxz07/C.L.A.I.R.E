"""
Core Assistant Class for C.L.A.I.R.E
Handles the main AI logic and skill orchestration
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class ClaireAssistant:
    """Main AI Assistant class"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the assistant with configuration"""
        self.config = config
        self.name = config.get('assistant', {}).get('name', 'Claire')
        self.conversation_history: List[Dict] = []
        self.max_history = config.get('assistant', {}).get('conversation_memory', 10)
        
        logger.info(f"Initializing {self.name}...")
        
        # Initialize AI provider
        self._init_ai_provider()
        
        # Initialize skills
        self._init_skills()
        
        logger.info(f"{self.name} initialized successfully")
    
    def _init_ai_provider(self):
        """Initialize the AI provider (Ollama)"""
        provider = self.config.get('ai', {}).get('provider', 'ollama')
        
        if provider == 'ollama':
            ollama_config = self.config.get('ai', {}).get('ollama', {})
            self.ollama_url = ollama_config.get('url', 'http://localhost:11434')
            self.ollama_model = ollama_config.get('model', 'llama2')
            
            # Test Ollama connection
            try:
                import requests
                response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
                if response.status_code == 200:
                    logger.info(f"Ollama connected successfully at {self.ollama_url}")
                    self.ai_client = "ollama"  # Mark as available
                else:
                    logger.warning("Ollama is not running. Start it with: ollama serve")
                    self.ai_client = None
            except Exception as e:
                logger.error(f"Cannot connect to Ollama: {e}")
                logger.info("Make sure Ollama is installed and running: https://ollama.ai")
                self.ai_client = None
        else:
            logger.warning(f"Provider '{provider}' not supported. Use 'ollama'")
            self.ai_client = None
    
    def _init_skills(self):
        """Initialize available skills/plugins"""
        self.skills = {}
        skills_config = self.config.get('skills', {})
        
        # Weather skill
        if skills_config.get('weather', {}).get('enabled', False):
            try:
                from backend.skills.weather import WeatherSkill
                self.skills['weather'] = WeatherSkill(skills_config['weather'])
                logger.info("Weather skill loaded")
            except Exception as e:
                logger.error(f"Failed to load weather skill: {e}")
        
        # System control skill
        if skills_config.get('system_control', {}).get('enabled', True):
            try:
                from backend.skills.system import SystemSkill
                self.skills['system'] = SystemSkill(skills_config.get('system_control', {}))
                logger.info("System control skill loaded")
            except Exception as e:
                logger.error(f"Failed to load system skill: {e}")
        
        logger.info(f"Loaded {len(self.skills)} skills")
    
    def process_command(self, user_input: str) -> str:
        """
        Process user command and return response
        
        Args:
            user_input: The user's text input
            
        Returns:
            Assistant's response text
        """
        logger.info(f"Processing: {user_input}")
        
        # Add to conversation history
        self.conversation_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now()
        })
        
        # Trim history if too long
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history * 2:]
        
        # Check for simple commands first
        response = self._handle_simple_commands(user_input)
        
        if response:
            self._add_to_history('assistant', response)
            return response
        
        # Check skills
        for skill_name, skill in self.skills.items():
            if skill.can_handle(user_input):
                try:
                    response = skill.execute(user_input)
                    self._add_to_history('assistant', response)
                    return response
                except Exception as e:
                    logger.error(f"Skill {skill_name} error: {e}")
                    response = f"Sorry, I encountered an error with {skill_name}: {e}"
                    self._add_to_history('assistant', response)
                    return response
        
        # Use AI if available
        if self.ai_client:
            try:
                response = self._get_ai_response(user_input)
                self._add_to_history('assistant', response)
                return response
            except Exception as e:
                logger.error(f"AI error: {e}")
                return f"Sorry, I encountered an error: {e}"
        
        # Fallback
        response = self._fallback_response(user_input)
        self._add_to_history('assistant', response)
        return response
    
    def _handle_simple_commands(self, text: str) -> Optional[str]:
        """Handle simple built-in commands"""
        text_lower = text.lower().strip()
        
        # Greetings
        if any(greeting in text_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return f"Hello! I'm {self.name}, your personal AI assistant. How can I help you today?"
        
        # Time
        if 'what time' in text_lower or 'current time' in text_lower:
            return f"The current time is {datetime.now().strftime('%I:%M %p')}"
        
        # Date
        if 'what date' in text_lower or 'today\'s date' in text_lower or 'what day' in text_lower:
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}"
        
        # Help
        if text_lower in ['help', 'what can you do', 'commands']:
            return self._get_help_text()
        
        # Exit
        if text_lower in ['exit', 'quit', 'goodbye', 'bye']:
            return f"Goodbye! Have a great day!"
        
        return None
    
    def _get_ai_response(self, user_input: str) -> str:
        """Get response from Ollama"""
        import requests
        
        temperature = self.config.get('ai', {}).get('temperature', 0.7)
        
        # Build system prompt
        system_prompt = f"""You are {self.name}, a helpful AI personal assistant running locally on the user's computer.
Your personality is {self.config.get('assistant', {}).get('personality', 'helpful and friendly')}.
Keep responses {self.config.get('assistant', {}).get('response_style', 'concise but informative')}.
Current date/time: {datetime.now().strftime('%Y-%m-%d %H:%M')}"""
        
        # Build conversation context
        context = system_prompt + "\n\n"
        recent_history = self.conversation_history[-6:]  # Last 3 exchanges
        for msg in recent_history:
            role = "User" if msg['role'] == 'user' else self.name
            context += f"{role}: {msg['content']}\n"
        
        # Make Ollama API call
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.ollama_model,
                    "prompt": context + f"User: {user_input}\n{self.name}:",
                    "stream": False,
                    "options": {
                        "temperature": temperature
                    }
                },
                timeout=(10, 180)  # (connect timeout, read timeout) - 3 minutes for read
            )
            response.raise_for_status()
            return response.json()['response'].strip()
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            raise Exception(f"Failed to get response from Ollama: {e}")
    
    def _fallback_response(self, text: str) -> str:
        """Fallback response when no AI is available"""
        return (
            f"I heard you say: '{text}'\n\n"
            f"I'm running in basic mode without AI. To enable full AI capabilities:\n"
            f"1. Install Ollama from: https://ollama.ai\n"
            f"2. Run: ollama pull llama2\n"
            f"3. Start Ollama: ollama serve\n\n"
            f"For now, try commands like:\n"
            f"- 'what time is it?'\n"
            f"- 'what's the date?'\n"
            f"- 'help'"
        )
    
    def _get_help_text(self) -> str:
        """Generate help text"""
        help_text = f"""
{self.name} - Available Commands

BASIC:
  • hello/hi - Greet me
  • what time is it? - Current time
  • what's the date? - Current date
  • help - Show this help

SKILLS:
"""
        for skill_name, skill in self.skills.items():
            help_text += f"  • {skill_name}: {skill.get_description()}\n"
        
        if self.ai_client:
            help_text += "\nAI CHAT:\n  • Ask me anything! I'm powered by AI and can help with various tasks.\n"
        
        return help_text
    
    def _add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now()
        })
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
