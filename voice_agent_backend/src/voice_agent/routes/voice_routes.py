import os
import uuid

from io import BytesIO

import requests
from requests.auth import HTTPBasicAuth
import speech_recognition as sr

from flask import Blueprint, request, jsonify, Response, send_file
from flask_cors import cross_origin
from twilio.twiml.voice_response import VoiceResponse

from ..voice_agent import voice_agent
from ..models.conversation import conversation_storage
from ..utils.logger import logger
from ..config.settings import config

# Create blueprint
voice_agent_bp = Blueprint('voice_agent', __name__)


@voice_agent_bp.route('/webhook/voice', methods=['GET', 'POST'])
@cross_origin()
def handle_voice_call():
    """Handle incoming SIP call: track it, then play an ElevenLabs TTS greeting."""
    call_sid = request.values.get('CallSid')
    from_number = request.values.get('From')
    to_number = request.values.get('To')

    logger.info(f"Incoming call: {call_sid} from {from_number} to {to_number}")

    voice_agent.start_call(call_sid, from_number, to_number)

    greeting = "أهلاً وسهلاً بك في مطعم شاركو تشيكن. كيف ممكن أساعدك اليوم؟"
    twiml = voice_agent.twilio_service.create_welcome_response(
        welcome_message=greeting,
        eleven_voice_id=config.elevenlabs.voice_id
    )

    return Response(twiml, mimetype="text/xml")


@voice_agent_bp.route('/process_speech', methods=['POST'])
@cross_origin()
def process_speech():
    """
    1) Receive SpeechResult (text),
    2) Run through your text pipeline,
    3) <Play> ElevenLabs reply, then <Gather> again.
    """
    call_sid = request.form.get('CallSid')
    speech_text = (request.form.get('SpeechResult') or "").strip()
    logger.info(f"SpeechResult for {call_sid}: {speech_text}")

    result = voice_agent.process_text_input(speech_text, call_sid, test_mode=False)
    agent_text = result.get('agent_response') or "عذراً، حدث خطأ أثناء المعالجة."

    tts_service = voice_agent.text_to_speech
    buffer = tts_service.generate_speech(
        text=agent_text,
        save_to_bytes=True,
        voice_id=config.elevenlabs.voice_id
    )

    resp = VoiceResponse()
    if buffer:
        file_id = str(uuid.uuid4())
        path = os.path.join(config.app.tts_cache_dir, f"{file_id}.mp3")
        with open(path, "wb") as f:
            f.write(buffer.getvalue())
        play_url = f"{config.app.base_url}/api/voice_agent/tts/{file_id}.mp3"
        resp.play(play_url)
    else:
        resp.say(agent_text, voice="Polly.Zeina", language="ar-EG")

    gather_url = f"{config.app.base_url}/api/voice_agent/process_speech"
    resp.gather(
        input="speech",
        language="ar-EG",
        action=gather_url,
        method="POST",
        timeout=5
    )

    resp.say(
        "لم أسمعك، من فضلك حاول مرة أخرى.",
        voice="Polly.Zeina",
        language="ar-EG"
    )
    resp.redirect(f"{config.app.base_url}/api/voice_agent/webhook/voice", method="POST")

    return Response(str(resp), mimetype="text/xml")


@voice_agent_bp.route('/process_recording', methods=['POST'])
@cross_origin()
def process_recording():
    """
    1) Called by Twilio once <Record> finishes.
    2) Downloads the .wav, passes it into process_voice_input.
    3) Replies in‑call with TTS + re‑record prompt.
    """
    call_sid = request.form.get('CallSid')
    recording_url = request.form.get('RecordingUrl')
    logger.info(f"Processing recording for call {call_sid}: {recording_url}")

    wav_url = f"{recording_url}.wav"
    auth = HTTPBasicAuth(config.twilio.account_sid, config.twilio.auth_token)
    resp = requests.get(wav_url, auth=auth)
    if resp.status_code != 200:
        logger.error(f"Failed to download recording: HTTP {resp.status_code}")
        error_twiml = voice_agent.create_error_response("recording")
        return Response(error_twiml, mimetype="text/xml")

    audio_bytes = BytesIO(resp.content)
    recognizer = voice_agent.speech_recognition.recognizer
    audio_source = sr.AudioFile(audio_bytes)
    with audio_source as src:
        audio_data = recognizer.record(src)

    agent_response = voice_agent.process_voice_input(audio_data, call_sid)
    if not agent_response:
        agent_response = "عذراً، لم أتمكن من فهم ما قلته. ممكن تعيد؟"

    twiml = voice_agent.twilio_service.create_agent_response(
        agent_message=agent_response,
        continue_call=True
    )

    return Response(twiml, mimetype="text/xml")


@voice_agent_bp.route('/transcription', methods=['POST'])
@cross_origin()
def handle_transcription():
    """Handle transcription callback from Twilio."""
    try:
        call_sid = request.form.get('CallSid')
        transcription_text = request.form.get('TranscriptionText')

        logger.info(f"Transcription for {call_sid}: {transcription_text}")

        if call_sid and transcription_text:
            response_text = voice_agent.process_voice_input(
                transcription_text,
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


TTS_CACHE_DIR = "/tmp/tts_cache"
os.makedirs(TTS_CACHE_DIR, exist_ok=True)


@voice_agent_bp.route('/tts/<filename>.mp3', methods=['GET'])
def serve_tts(filename):
    """Serve a previously generated ElevenLabs MP3."""
    path = os.path.join(TTS_CACHE_DIR, f"{filename}.mp3")
    if not os.path.exists(path):
        return ("Not found", 404)
    return send_file(path, mimetype="audio/mpeg")
