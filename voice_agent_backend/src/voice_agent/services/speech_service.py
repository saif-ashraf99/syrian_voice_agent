import speech_recognition as sr
from elevenlabs import ElevenLabs, VoiceSettings
from io import BytesIO
from typing import Optional
import base64

from ..config.settings import config
from ..utils.logger import logger


class SpeechRecognitionService:
    """Handles speech-to-text conversion."""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def transcribe_audio(self, audio_data, language: str = 'ar-SY') -> Optional[str]:
        """
        Transcribe audio using speech recognition.
        
        Args:
            audio_data: Audio data to transcribe
            language: Language code for recognition
            
        Returns:
            Transcribed text or None if failed
        """
        try:
            text = self.recognizer.recognize_google(audio_data, language=language)
            logger.info(f"Transcribed text: {text}")
            return text
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            return None


class TextToSpeechService:
    """Handles text-to-speech conversion using ElevenLabs."""
    
    def __init__(self):
        if not config.elevenlabs.api_key:
            raise ValueError("ElevenLabs API key is required")
        
        self.client = ElevenLabs(api_key=config.elevenlabs.api_key)
        self.voice_id = config.elevenlabs.voice_id
    
    def generate_speech(
        self, 
        text: str, 
        save_to_bytes: bool = True,
        voice_id: Optional[str] = None
    ) -> Optional[BytesIO]:
        """
        Convert text to speech using ElevenLabs.
        
        Args:
            text: Text to convert to speech
            save_to_bytes: Whether to return audio as BytesIO
            voice_id: Voice ID to use (defaults to config voice)
            
        Returns:
            BytesIO stream of audio or None if failed
        """
        try:
            voice_id = voice_id or self.voice_id
            if not voice_id:
                raise ValueError("Voice ID is required for TTS")
            
            # Perform streaming request
            audio_iter = self.client.text_to_speech.stream(
                text=text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                optimize_streaming_latency="1",
                output_format="mp3_44100_128",
                voice_settings=VoiceSettings(
                    stability=0.75,
                    similarity_boost=0.85,
                    style=0.5,
                    use_speaker_boost=True
                )
            )
            
            if not save_to_bytes:
                # For streaming playback (not implemented in this refactor)
                logger.info("Streaming audio playback not implemented")
                return None
            
            # Collect audio chunks into BytesIO
            buffer = BytesIO()
            for chunk in audio_iter:
                if isinstance(chunk, (bytes, bytearray)):
                    buffer.write(chunk)
            buffer.seek(0)
            
            logger.info("Generated TTS audio stream as BytesIO")
            return buffer
            
        except Exception as e:
            logger.error(f"TTS streaming error: {e}")
            return None
    
    def generate_speech_base64(self, text: str) -> Optional[str]:
        """
        Generate speech and return as base64 encoded string.
        
        Args:
            text: Text to convert to speech
            
        Returns:
            Base64 encoded audio string or None if failed
        """
        audio_data = self.generate_speech(text, save_to_bytes=True)
        if audio_data:
            return base64.b64encode(audio_data.getvalue()).decode('utf-8')
        return None