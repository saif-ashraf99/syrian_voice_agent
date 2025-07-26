"""Main VoiceAgent class that orchestrates all services."""
from typing import Optional, Dict, Any

from .services.speech_service import SpeechRecognitionService, TextToSpeechService
from .services.intent_service import IntentDetectionService
from .services.response_service import ResponseGenerationService
from .services.twilio_service import TwilioService
from .models.conversation import IntentData, ConversationEntry, conversation_storage
from .utils.logger import logger


class VoiceAgent:
    """Main voice agent that coordinates all services."""
    
    def __init__(self):
        """Initialize the voice agent with all required services."""
        try:
            self.speech_recognition = SpeechRecognitionService()
            self.text_to_speech = TextToSpeechService()
            self.intent_detection = IntentDetectionService()
            self.response_generation = ResponseGenerationService()
            self.twilio_service = TwilioService()
            logger.info("VoiceAgent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize VoiceAgent: {e}")
            raise
    
    def process_voice_input(
        self, 
        audio_data, 
        call_sid: str,
        language: str = 'ar-SY'
    ) -> Optional[str]:
        """
        Process voice input through the complete pipeline.
        
        Args:
            audio_data: Raw audio data
            call_sid: Call identifier
            language: Language for speech recognition
            
        Returns:
            Generated response text or None if failed
        """
        try:
            # Transcribe audio
            transcribed_text = self.speech_recognition.transcribe_audio(audio_data, language)
            if not transcribed_text:
                return None
            
            # Detect intent
            intent_data = self.intent_detection.detect_intent(transcribed_text)
            
            # Generate response
            agent_response = self.response_generation.generate_response(
                intent_data, transcribed_text
            )
            
            # Log conversation
            self._log_conversation(
                call_sid, transcribed_text, intent_data, agent_response
            )
            
            return agent_response
            
        except Exception as e:
            logger.error(f"Error processing voice input: {e}")
            return None
    
    def process_text_input(
        self, 
        text: str, 
        call_sid: str = "test",
        test_mode: bool = True
    ) -> Dict[str, Any]:
        """
        Process text input for testing purposes.
        
        Args:
            text: Input text to process
            call_sid: Call identifier (defaults to "test")
            test_mode: Whether this is a test interaction
            
        Returns:
            Dictionary with processing results including audio
        """
        try:
            # Detect intent
            intent_data = self.intent_detection.detect_intent(text)
            
            # Generate response
            agent_response = self.response_generation.generate_response(intent_data, text)
            
            # Generate audio
            audio_base64 = self.text_to_speech.generate_speech_base64(agent_response)
            
            # Log conversation
            self._log_conversation(
                call_sid, text, intent_data, agent_response, test_mode
            )
            
            return {
                'transcribed_input': text,
                'detected_intent': intent_data.intent,
                'entities': intent_data.entities,
                'confidence': intent_data.confidence,
                'agent_response': agent_response,
                'audio_base64': audio_base64
            }
            
        except Exception as e:
            logger.error(f"Error processing text input: {e}")
            return {
                'error': str(e),
                'agent_response': 'عذراً، حدث خطأ في المعالجة.',
                'audio_base64': None
            }
    
    def create_welcome_response(self) -> str:
        """Create welcome response for incoming calls."""
        welcome_message = "أهلاً وسهلاً بك في مطعم شاركو تشيكن. كيف ممكن ساعدك اليوم؟"
        return self.twilio_service.create_welcome_response(welcome_message)
    
    def create_processing_response(self) -> str:
        """Create processing response."""
        processing_message = "شكراً لك. جاري معالجة طلبك..."
        return self.twilio_service.create_processing_response(processing_message)
    
    def create_error_response(self, error_type: str = "general") -> str:
        """Create error response based on error type."""
        error_messages = {
            "general": "عذراً، حدث خطأ. يرجى المحاولة مرة أخرى.",
            "recording": "عذراً، حدث خطأ في معالجة التسجيل.",
            "transcription": "عذراً، لم أتمكن من فهم ما قلته. ممكن تعيد؟"
        }
        
        message = error_messages.get(error_type, error_messages["general"])
        return self.twilio_service.create_error_response(message)
    
    def start_call(self, call_sid: str, from_number: str, to_number: str) -> None:
        """Start tracking a new call."""
        conversation_storage.start_call(call_sid, from_number, to_number)
        logger.info(f"Started tracking call: {call_sid} from {from_number}")
    
    def end_call(self, call_sid: str) -> None:
        """End call tracking."""
        call = conversation_storage.end_call(call_sid)
        if call:
            logger.info(f"Ended call: {call_sid}, duration: {len(call.conversation)} exchanges")
    
    def reset_conversation_context(self) -> None:
        """Reset the conversation context for the response generation service."""
        self.response_generation.reset_context()
    
    def _log_conversation(
        self,
        call_sid: str,
        customer_text: str,
        intent_data: IntentData,
        agent_response: str,
        test_mode: bool = False
    ) -> None:
        """Log a conversation exchange."""
        entry = ConversationEntry.create(
            call_sid=call_sid,
            customer_text=customer_text,
            intent=intent_data.intent,
            entities=intent_data.entities,
            agent_response=agent_response,
            confidence=intent_data.confidence,
            test_mode=test_mode
        )
        
        conversation_storage.add_conversation_entry(entry)
        logger.info(f"Logged conversation entry for call {call_sid}")


# Global voice agent instance
voice_agent = VoiceAgent()