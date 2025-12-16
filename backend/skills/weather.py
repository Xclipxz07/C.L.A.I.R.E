"""
Weather Skill for C.L.A.I.R.E
Provides weather information using OpenWeatherMap API
"""

import logging
import requests
from typing import Dict, Any
from backend.skills.base import BaseSkill

logger = logging.getLogger(__name__)


class WeatherSkill(BaseSkill):
    """Get weather information"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key', '')
        self.default_location = config.get('default_location', 'New York')
        self.units = config.get('units', 'metric')
    
    def can_handle(self, user_input: str) -> bool:
        """Check if this is a weather query"""
        keywords = ['weather', 'temperature', 'forecast', 'rain', 'sunny', 'cloudy']
        text_lower = user_input.lower()
        return any(keyword in text_lower for keyword in keywords)
    
    def execute(self, user_input: str) -> str:
        """Get weather information"""
        if not self.api_key or self.api_key == 'your-openweathermap-api-key':
            return (
                "Weather service not configured. Please:\n"
                "1. Get a free API key from: https://openweathermap.org/api\n"
                "2. Add it to config.yaml under skills.weather.api_key"
            )
        
        # Extract location from input (simple version)
        location = self._extract_location(user_input) or self.default_location
        
        try:
            # Call OpenWeatherMap API
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': self.units
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Format response
            temp_unit = '°C' if self.units == 'metric' else '°F'
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            
            return (
                f"Weather in {location}:\n"
                f"• Conditions: {weather.capitalize()}\n"
                f"• Temperature: {temp:.1f}{temp_unit} (feels like {feels_like:.1f}{temp_unit})\n"
                f"• Humidity: {humidity}%"
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Weather API error: {e}")
            return f"Sorry, I couldn't fetch the weather data. Error: {e}"
        except KeyError as e:
            logger.error(f"Weather data parsing error: {e}")
            return f"Sorry, I couldn't parse the weather data for {location}"
    
    def _extract_location(self, text: str) -> str:
        """Extract location from user input (simple version)"""
        # Simple approach: look for "in [location]" or "for [location]"
        text_lower = text.lower()
        
        for prep in [' in ', ' for ', ' at ']:
            if prep in text_lower:
                parts = text_lower.split(prep)
                if len(parts) > 1:
                    location = parts[-1].strip().strip('?.,!')
                    return location.title()
        
        return None
    
    def get_description(self) -> str:
        """Get skill description"""
        return "Get weather information (e.g., 'what's the weather in Tokyo?')"
