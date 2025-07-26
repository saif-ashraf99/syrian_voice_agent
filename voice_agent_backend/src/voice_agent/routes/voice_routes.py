"""Flask routes for voice agent endpoints."""
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from ..voice_agent import voice_agent
from ..models.conversation import conversation_storage
from ..utils.logger import logger

# Create blueprint
voice_agent_bp = Blueprint('voice_agent', __name__)


@voice_agent_bp.route('/webhook/voice', methods=['POST'])
@cross_origin()
def handle_voice_call():
    """Handle incoming voice calls via Twilio webhook."""
    try:
        # Get call information
        call_sid = request.form.get('CallSid')
        from_number = request.form.get('From')
        to_number = request.form.get('To')
        
        logger.info(f"Incoming call: {call_sid} from {from_number}")
        
        # Start tracking the call
        voice_agent.start_call(call_sid, from_number, to_number)
        
        # Create and return welcome response
        response = voice_agent.create_welcome_response()
        return response
        
    except Exception as e:
        logger.error(f"Voice call handling error: {e}")
        return voice_agent.create_error_response("general")


@voice_agent_bp.route('/process_recording', methods=['POST'])
@cross_origin()
def process_recording():
    """Process recorded audio from customer."""
    try:
        call_sid = request.form.get('CallSid')
        recording_url = request.form.get('RecordingUrl')
        
        logger.info(f"Processing recording for call {call_sid}: {recording_url}")
        
        # For now, return processing response
        # In production, you would:
        # 1. Download the audio from recording_url
        # 2. Process it through voice_agent.process_voice_input()
        # 3. Generate appropriate TwiML response
        
        response = voice_agent.create_processing_response()
        return response
        
    except Exception as e:
        logger.error(f"Recording processing error: {e}")
        return voice_agent.create_error_response("recording")


@voice_agent_bp.route('/transcription', methods=['POST'])
@cross_origin()
def handle_transcription():
    """Handle transcription callback from Twilio."""
    try:
        call_sid = request.form.get('CallSid')
        transcription_text = request.form.get('TranscriptionText')
        
        logger.info(f"Transcription for {call_sid}: {transcription_text}")
        
        if call_sid and transcription_text:
            # Process the transcribed text
            response_text = voice_agent.process_voice_input(
                transcription_text,  # In real implementation, this would be audio data
                call_sid
            )
            
            if response_text:
                logger.info(f"Generated response for {call_sid}: {response_text}")
        
        return jsonify({'status': 'success'})
        
    except Exception as e:
        logger.error(f"Transcription handling error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})


@voice_agent_bp.route('/test_voice', methods=['POST'])
@cross_origin()
def test_voice_agent():
    """Test endpoint for voice agent functionality."""
    try:
        data = request.get_json()
        text_input = data.get('text', '')
        
        if not text_input:
            return jsonify({'error': 'No text provided'}), 400
        
        # Process text input
        result = voice_agent.process_text_input(text_input)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Test voice agent error: {e}")
        return jsonify({'error': str(e)}), 500


@voice_agent_bp.route('/conversation_logs', methods=['GET'])
@cross_origin()
def get_conversation_logs():
    """Get conversation logs for monitoring."""
    try:
        logs_summary = conversation_storage.get_logs_summary()
        return jsonify(logs_summary)
    except Exception as e:
        logger.error(f"Get logs error: {e}")
        return jsonify({'error': str(e)}), 500


@voice_agent_bp.route('/active_calls', methods=['GET'])
@cross_origin()
def get_active_calls():
    """Get active calls information."""
    try:
        calls_summary = conversation_storage.get_active_calls_summary()
        return jsonify(calls_summary)
    except Exception as e:
        logger.error(f"Get active calls error: {e}")
        return jsonify({'error': str(e)}), 500


@voice_agent_bp.route('/reset_context', methods=['POST'])
@cross_origin()
def reset_conversation_context():
    """Reset conversation context for testing."""
    try:
        voice_agent.reset_conversation_context()
        return jsonify({'status': 'success', 'message': 'Context reset'})
    except Exception as e:
        logger.error(f"Reset context error: {e}")
        return jsonify({'error': str(e)}), 500


@voice_agent_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Health check endpoint."""
    try:
        return jsonify({
            'status': 'healthy',
            'services': {
                'speech_recognition': 'ok',
                'text_to_speech': 'ok',
                'intent_detection': 'ok',
                'response_generation': 'ok',
                'twilio': 'ok'
            }
        })
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500