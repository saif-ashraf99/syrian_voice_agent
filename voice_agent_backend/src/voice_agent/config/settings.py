"""Configuration settings for the voice agent system."""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv
load_dotenv()


@dataclass
class TwilioConfig:
    """Twilio configuration settings."""
    account_sid: str
    auth_token: str
    
    @classmethod
    def from_env(cls) -> 'TwilioConfig':
        """Create TwilioConfig from environment variables."""
        return cls(
            account_sid=os.getenv('TWILIO_ACCOUNT_SID', ''),
            auth_token=os.getenv('TWILIO_AUTH_TOKEN', '')
        )


@dataclass
class ElevenLabsConfig:
    """ElevenLabs configuration settings."""
    api_key: str
    voice_id: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> 'ElevenLabsConfig':
        """Create ElevenLabsConfig from environment variables."""
        return cls(
            api_key=os.getenv('ELEVENLABS_API_KEY', ''),
            voice_id='drMurExmkWVIH5nW8snR',
        )


@dataclass
class OpenAIConfig:
    """OpenAI configuration settings."""
    api_key: str
    base_url: str = "https://openrouter.ai/api/v1"
    model: str = "google/gemma-3n-e2b-it:free"
    
    @classmethod
    def from_env(cls) -> 'OpenAIConfig':
        """Create OpenAIConfig from environment variables."""
        return cls(
            api_key=os.getenv('OPENAI_API_KEY', ''),
            base_url=os.getenv('OPENAI_BASE_URL', "https://openrouter.ai/api/v1"),
            model=os.getenv('OPENAI_MODEL', "google/gemma-3n-e2b-it:free")
        )


@dataclass
class VoiceAgentConfig:
    """Main configuration for the voice agent."""
    twilio: TwilioConfig
    elevenlabs: ElevenLabsConfig
    openai: OpenAIConfig
    max_conversation_context: int = 6
    max_recording_length: int = 30
    
    @classmethod
    def from_env(cls) -> 'VoiceAgentConfig':
        """Create VoiceAgentConfig from environment variables."""
        return cls(
            twilio=TwilioConfig.from_env(),
            elevenlabs=ElevenLabsConfig.from_env(),
            openai=OpenAIConfig.from_env(),
            max_conversation_context=int(os.getenv('MAX_CONVERSATION_CONTEXT', '6')),
            max_recording_length=int(os.getenv('MAX_RECORDING_LENGTH', '30'))
        )


# Global configuration instance
config = VoiceAgentConfig.from_env()