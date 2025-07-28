from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

from typing import Optional
import uuid
import os

from ..services.speech_service import TextToSpeechService
from ..config.settings import config
from ..utils.logger import logger


class TwilioService:
    """Handles Twilio voice call integration."""
    
    def __init__(self):
        if not config.twilio.account_sid or not config.twilio.auth_token:
            raise ValueError("Twilio credentials are required")
        
        self.client = Client(config.twilio.account_sid, config.twilio.auth_token)
    
    def create_welcome_response(
        self,
        welcome_message: str,
        eleven_voice_id: str = None
    ) -> str:
        """
        Generate an ElevenLabs MP3 for the greeting, then <Play> it,
        <Gather> the response, and fallback/redirect if necessary.
        """
        tts_service = TextToSpeechService()
        buffer = tts_service.generate_speech(
            text=welcome_message,
            save_to_bytes=True,
            voice_id=eleven_voice_id
        )

        resp = VoiceResponse()

        # 1. Play your ElevenLabs greeting (or fallback to Polly)
        if buffer:
            file_id = str(uuid.uuid4())
            path = os.path.join(config.app.tts_cache_dir, f"{file_id}.mp3")
            with open(path, "wb") as f:
                f.write(buffer.getvalue())
            play_url = f"{config.app.base_url}/api/voice_agent/tts/{file_id}.mp3"
            resp.play(play_url)
        else:
            resp.say(welcome_message, voice="Polly.Zeina", language="ar-EG")

        # 2. Gather live speech and POST it back
        gather_url = f"{config.app.base_url}/api/voice_agent/process_speech"
        resp.gather(
            input="speech",
            language="ar-EG",
            action=gather_url,
            method="POST",
            timeout=5
        )

        # 3. Fallback if no speech was captured
        resp.say(
            "لم أسمعك، من فضلك حاول مرة أخرى.",
            voice="Polly.Zeina",
            language="ar-EG"
        )
        # 4. Redirect back to this same webhook to replay greeting+gather
        webhook_url = f"{config.app.base_url}/api/voice_agent/webhook/voice"
        resp.redirect(webhook_url, method="POST")

        return str(resp)

    def create_processing_response(self, message: str) -> str:
        """
        Create a TwiML response for processing state.
        
        Args:
            message: Processing message to speak
            
        Returns:
            TwiML response as string
        """
        response = VoiceResponse()
        response.say(
            message,
            voice='alice',
            language='ar'
        )
        response.hangup()
        return str(response)
    
    def create_error_response(self, error_message: str) -> str:
        """
        Create a TwiML response for error handling.
        
        Args:
            error_message: Error message to speak
            
        Returns:
            TwiML response as string
        """
        response = VoiceResponse()
        response.say(error_message, voice='alice', language='ar')
        response.hangup()
        return str(response)
    
    def create_agent_response(
        self,
        agent_message: str,
        continue_call: bool = True,
        eleven_voice_id: str = None
    ) -> str:
        """
        Generate TTS via ElevenLabs and return TwiML that <Play>’s it.
        """
        # 1. Generate MP3 from ElevenLabs
        tts_service = TextToSpeechService()
        buffer = tts_service.generate_speech(
            text=agent_message,
            save_to_bytes=True,
            voice_id=eleven_voice_id
        )
        if not buffer:
            # Fallback to Polly
            resp = VoiceResponse()
            resp.say(agent_message, voice="Polly.Zeina", language="ar-EG")
        else:
            # 2. Write buffer to a unique file
            file_id = str(uuid.uuid4())
            path = os.path.join(config.app.tts_cache_dir, f"{file_id}.mp3")
            with open(path, "wb") as f:
                f.write(buffer.read())

            # 3. Build TwiML that <Play>s it
            tts_url = f"{config.app.base_url}/api/voice_agent/tts/{file_id}.mp3"
            resp = VoiceResponse()
            resp.play(tts_url)

        # 4. Continue or hang up
        if continue_call:
            resp.gather(
                input="speech",
                language="ar-EG",
                action="/api/voice_agent/process_speech",
                method="POST",
                timeout=5
            )
        else:
            resp.hangup()

        return str(resp)
    
    def make_outbound_call(
        self, 
        to_number: str, 
        from_number: str, 
        webhook_url: str
    ) -> Optional[str]:
        """
        Make an outbound call using Twilio.
        
        Args:
            to_number: Number to call
            from_number: Twilio number to call from
            webhook_url: URL for call webhook
            
        Returns:
            Call SID if successful, None otherwise
        """
        try:
            call = self.client.calls.create(
                to=to_number,
                from_=from_number,
                url=webhook_url,
                method='POST'
            )
            logger.info(f"Outbound call created: {call.sid}")
            return call.sid
        except Exception as e:
            logger.error(f"Failed to create outbound call: {e}")
            return None