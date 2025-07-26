"""Twilio integration service for voice calls."""
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from typing import Optional

from ..config.settings import config
from ..utils.logger import logger


class TwilioService:
    """Handles Twilio voice call integration."""
    
    def __init__(self):
        if not config.twilio.account_sid or not config.twilio.auth_token:
            raise ValueError("Twilio credentials are required")
        
        self.client = Client(config.twilio.account_sid, config.twilio.auth_token)
    
    def create_welcome_response(self, welcome_message: str) -> str:
        """
        Create a TwiML response with welcome message and recording setup.
        
        Args:
            welcome_message: Message to speak to caller
            
        Returns:
            TwiML response as string
        """
        response = VoiceResponse()
        
        # Say welcome message
        response.say(
            welcome_message,
            voice='alice',
            language='ar'
        )
        
        # Set up recording
        response.record(
            action='/api/voice_agent/process_recording',
            method='POST',
            max_length=config.max_recording_length,
            finish_on_key='#',
            transcribe=True,
            transcribe_callback='/api/voice_agent/transcription'
        )
        
        return str(response)
    
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
    
    def create_agent_response(self, agent_message: str, continue_call: bool = True) -> str:
        """
        Create a TwiML response with agent message.
        
        Args:
            agent_message: Message from the agent
            continue_call: Whether to continue the call or hang up
            
        Returns:
            TwiML response as string
        """
        response = VoiceResponse()
        response.say(
            agent_message,
            voice='alice',
            language='ar'
        )
        
        if continue_call:
            # Continue conversation - record next response
            response.record(
                action='/api/voice_agent/process_recording',
                method='POST',
                max_length=config.max_recording_length,
                finish_on_key='#',
                transcribe=True,
                transcribe_callback='/api/voice_agent/transcription'
            )
        else:
            response.hangup()
        
        return str(response)
    
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