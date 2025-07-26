# voice_agent/__init__.py
"""Voice Agent package for Syrian Arabic restaurant voice assistant."""

from .voice_agent import voice_agent
from .routes.voice_routes import voice_agent_bp

__version__ = "1.0.0"
__all__ = ["voice_agent", "voice_agent_bp"]


# voice_agent/config/__init__.py
"""Configuration module for voice agent."""

from src.voice_agent.config.settings import config, VoiceAgentConfig

__all__ = ["config", "VoiceAgentConfig"]


# voice_agent/models/__init__.py
"""Data models for voice agent."""

from src.voice_agent.models.conversation import (
    ConversationEntry,
    ActiveCall,
    IntentData,
    ConversationStorage,
    conversation_storage
)

__all__ = [
    "ConversationEntry",
    "ActiveCall", 
    "IntentData",
    "ConversationStorage",
    "conversation_storage"
]


# voice_agent/services/__init__.py
"""Services module for voice agent."""

from src.voice_agent.services.speech_service import SpeechRecognitionService, TextToSpeechService
from src.voice_agent.services.intent_service import IntentDetectionService
from src.voice_agent.services.response_service import ResponseGenerationService
from src.voice_agent.services.twilio_service import TwilioService

__all__ = [
    "SpeechRecognitionService",
    "TextToSpeechService",
    "IntentDetectionService", 
    "ResponseGenerationService",
    "TwilioService"
]


# voice_agent/routes/__init__.py
"""Routes module for voice agent."""

from src.voice_agent.routes.voice_routes import voice_agent_bp

__all__ = ["voice_agent_bp"]


# voice_agent/utils/__init__.py
"""Utilities module for voice agent."""

from src.voice_agent.utils.logger import logger, setup_logger

__all__ = ["logger", "setup_logger"]