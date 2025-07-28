import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

@dataclass
class TwilioConfig:
    """Twilio configuration settings."""
    account_sid: str
    auth_token: str
    
    @classmethod
    def from_env(cls) -> 'TwilioConfig':
        return cls(
            account_sid=os.getenv('TWILIO_ACCOUNT_SID', ''),
            auth_token=os.getenv('TWILIO_AUTH_TOKEN', '')
        )

@dataclass
class ElevenLabsConfig:
    """ElevenLabs configuration settings."""
    api_key: str
    voice_id: Optional[str]
    
    @classmethod
    def from_env(cls) -> 'ElevenLabsConfig':
        return cls(
            api_key=os.getenv('ELEVENLABS_API_KEY', ''),
            voice_id=os.getenv('ELEVENLABS_VOICE_ID', 'drMurExmkWVIH5nW8snR')
        )

@dataclass
class OpenAIConfig:
    """OpenAI configuration settings."""
    api_key: str
    base_url: str
    model: str
    
    @classmethod
    def from_env(cls) -> 'OpenAIConfig':
        return cls(
            api_key=os.getenv('OPENAI_API_KEY', ''),
            base_url=os.getenv('OPENAI_BASE_URL', 'https://openrouter.ai/api/v1'),
            model=os.getenv('OPENAI_MODEL', 'qwen/qwen3-coder:free')
        )

@dataclass
class AppConfig:
    """Application-wide settings."""
    base_url: str
    tts_cache_dir: str
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        base = os.getenv('APP_BASE_URL', 'http://localhost:5000')
        cache_dir = os.getenv('TTS_CACHE_DIR', '/tmp/tts_cache')
        ensure_dir(cache_dir)
        return cls(
            base_url=base,
            tts_cache_dir=cache_dir
        )

@dataclass
class VoiceAgentConfig:
    """Main configuration for the voice agent."""
    twilio: TwilioConfig
    elevenlabs: ElevenLabsConfig
    openai: OpenAIConfig
    app: AppConfig
    max_conversation_context: int
    max_recording_length: int
    
    @classmethod
    def from_env(cls) -> 'VoiceAgentConfig':
        return cls(
            twilio=TwilioConfig.from_env(),
            elevenlabs=ElevenLabsConfig.from_env(),
            openai=OpenAIConfig.from_env(),
            app=AppConfig.from_env(),
            max_conversation_context=int(os.getenv('MAX_CONVERSATION_CONTEXT', '6')),
            max_recording_length=int(os.getenv('MAX_RECORDING_LENGTH', '30'))
        )

# Global configuration instance
config = VoiceAgentConfig.from_env()
