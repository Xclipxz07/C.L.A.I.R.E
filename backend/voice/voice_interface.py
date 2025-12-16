"""
Voice interface for C.L.A.I.R.E
Handles speech-to-text and text-to-speech
"""

import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class VoiceInterface:
    """Voice input/output handler"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize voice interface"""
        self.config = config
        self.stt_enabled = False
        self.tts_enabled = False
        
        # Initialize speech recognition
        self._init_speech_recognition()
        
        # Initialize text-to-speech
        self._init_text_to_speech()
    
    def _init_speech_recognition(self):
        """Initialize speech-to-text"""
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.stt_enabled = True
            logger.info("Speech recognition initialized")
        except ImportError:
            logger.warning("speech_recognition not installed. Run: pip install SpeechRecognition")
        except Exception as e:
            logger.error(f"Failed to initialize speech recognition: {e}")
    
    def _init_text_to_speech(self):
        """Initialize text-to-speech"""
        provider = self.config.get('voice', {}).get('tts', {}).get('provider', 'pyttsx3')
        
        if provider == 'pyttsx3':
            try:
                import pyttsx3
                self.tts_engine = pyttsx3.init()
                
                # Configure voice
                rate = self.config.get('voice', {}).get('tts', {}).get('voice_rate', 150)
                volume = self.config.get('voice', {}).get('tts', {}).get('volume', 0.9)
                
                self.tts_engine.setProperty('rate', rate)
                self.tts_engine.setProperty('volume', volume)
                
                self.tts_enabled = True
                logger.info("Text-to-speech initialized")
            except ImportError:
                logger.warning("pyttsx3 not installed. Run: pip install pyttsx3")
            except Exception as e:
                logger.error(f"Failed to initialize text-to-speech: {e}")
    
    def listen(self, timeout: int = 5) -> Optional[str]:
        """
        Listen for voice input
        
        Args:
            timeout: Seconds to listen
            
        Returns:
            Recognized text or None
        """
        if not self.stt_enabled:
            logger.error("Speech recognition not available")
            return None
        
        try:
            with self.microphone as source:
                logger.info("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout)
            
            logger.info("Processing speech...")
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized: {text}")
            return text
            
        except Exception as e:
            logger.error(f"Speech recognition error: {e}")
            return None
    
    def speak(self, text: str):
        """
        Convert text to speech
        
        Args:
            text: Text to speak
        """
        if not self.tts_enabled:
            logger.error("Text-to-speech not available")
            return
        
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
    
    def is_available(self) -> bool:
        """Check if voice interface is available"""
        return self.stt_enabled and self.tts_enabled
