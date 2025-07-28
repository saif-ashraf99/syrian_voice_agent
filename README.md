# Syrian Arabic Voice Agent for Charco Chicken

A voice agent system that handles real-time phone orders in flawless Syrian Arabic dialect, featuring SIP trunk integration, advanced NLP, and a complete monitoring dashboard.

## Project Overview

This project implements a sophisticated voice agent specifically designed for Charco Chicken restaurant to automate phone order processing. The system demonstrates real-time SIP call handling, natural Syrian Arabic conversation capabilities, backend API integration, and comprehensive monitoring tools.

### Key Features

- **Real-time SIP Integration**: Handle live phone calls via Twilio SIP trunks
- **Flawless Syrian Arabic**: Native-quality speech recognition and synthesis
- **Advanced NLP**: Intent detection, entity extraction, and contextual responses
- **Order Management**: Complete order processing with ETA calculation
- **Monitoring Dashboard**: Real-time analytics and conversation logs
- **Testing Interface**: Comprehensive UI for testing and validation

## Architecture

### System Components

1. **SIP Trunk Integration** (Twilio-based)

   - Real-time call handling
   - Voice I/O with low latency
   - Webhook-based call processing
2. **Voice Agent Core**

   - Speech-to-Text (Google Speech Recognition + ElevenLabs)
   - Intent Detection (Google Gemma)
   - Text-to-Speech (ElevenLabs Syrian Arabic voices)
   - Conversation Context Management
3. **Backend API** (Flask)

   - Order submission and management
   - Menu management
   - Statistics and analytics
   - CORS-enabled for frontend integration
4. **Testing Interface** (Streamlit)

   - Text-based testing
   - Audio upload capability
   - Real-time response display
   - Conversation history
5. **Monitoring Dashboard**

   - Live conversation logs
   - Intent distribution analytics
   - Order statistics
   - Performance metrics

## Quick Start

### Prerequisites

- Python 3.11+
- Twilio Account (for SIP integration)
- OpenAI API Key ( Google Gemma)
- ElevenLabs API Key

### Installation

1. **Clone and Setup**

   ```bash
   cd syrian_voice_agent/voice_agent_backend
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. **Environment Configuration**
   Create a `.env` file in the backend directory:

   ```env
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   OPENAI_API_KEY=your_openai_api_key (Google Gemma)
   APP_BASE_URL=Your Application URL [Ngrok or Custom Domain]
   ```
3. **Start the Backend**

   ```bash
   python main.py
   ```

   The backend will be available at `http://localhost:5000`
4. **Start the Testing Interface**

   ```bash
   # In a new terminal
   cd syrian_voice_agent
   streamlit run streamlit_ui.py
   ```

   The UI will be available at `http://localhost:8501`

## 📞 SIP Configuration

### Twilio Setup

1. **Create a Twilio Account**

   - Sign up at [twilio.com](https://www.twilio.com)
   - Get your Account SID and Auth Token
2. **Configure Phone Number**

   - Purchase a phone number in Twilio Console
   - Set webhook URL to: `https://your-domain.com/api/voice_agent/webhook/voice`
3. **SIP Trunk Configuration**

   ```python
   # The system automatically handles SIP calls via Twilio webhooks
   # No additional SIP configuration required
   ```

### Alternative SIP Providers

The system can be adapted for other SIP providers:

- **Asterisk**: Modify webhook endpoints
- **Vonage**: Update authentication methods
- **Custom SIP**: Implement SIP protocol handlers

## API Documentation

### Voice Agent Endpoints

#### POST `/api/voice_agent/webhook/voice`

Handles incoming SIP calls from Twilio.

**Request**: Twilio webhook format
**Response**: TwiML for call handling

#### POST `/api/voice_agent/test_voice`

Test endpoint for voice agent functionality.

**Request**:

```json
{
  "text": "مرحبا، بدي أطلب شاورما دجاج"
}
```

**Response**:

```json
{
  "transcribed_input": "مرحبا، بدي أطلب شاورما دجاج",
  "detected_intent": "order",
  "entities": {
    "food_items": ["شاورما دجاج"],
    "quantities": [],
    "other": []
  },
  "confidence": 0.95,
  "agent_response": "أهلاً وسهلاً! شاورما دجاج، اختيار ممتاز. كم قطعة بدك؟",
  "audio_base64": "base64_encoded_audio_data"
}
```

#### GET `/api/voice_agent/conversation_logs`

Retrieve conversation logs for monitoring.

**Response**:

```json
{
  "logs": [...],
  "total_conversations": 25,
  "active_calls": 2
}
```

### Order Management Endpoints

#### POST `/api/submit-order`

Submit a new order.

**Request**:

```json
{
  "name": "أحمد محمد",
  "order_list": [
    {"item": "شاورما دجاج", "quantity": 2, "price": 15.00},
    {"item": "حمص", "quantity": 1, "price": 8.00}
  ],
  "phone": "+963123456789",
  "notes": "Extra sauce"
}
```

**Response**:

```json
{
  "order_id": "A1B2C3D4",
  "eta": "14:30",
  "eta_minutes": 25,
  "total_price": 38.00,
  "status": "confirmed",
  "message": "شكراً أحمد! تم تأكيد طلبك. رقم الطلب: A1B2C3D4. سيكون جاهز خلال 25 دقيقة."
}
```

#### GET `/api/orders`

Retrieve orders with optional filtering.

**Query Parameters**:

- `status`: Filter by order status
- `customer_name`: Filter by customer name
- `limit`: Limit number of results

#### GET `/api/menu`

Get restaurant menu.

#### GET `/api/stats`

Get order statistics and analytics.

## Testing Guide

### Using the Streamlit Interface

1. **Voice Testing Page**

   - Enter Syrian Arabic text
   - View intent detection results
   - Listen to generated audio responses
   - Review conversation history
2. **Order Management Page**

   - Create new orders
   - View recent orders
   - Monitor order status
3. **Conversation Logs Page**

   - Filter by intent or mode
   - View detailed conversation analysis
   - Export conversation data
4. **Monitoring Dashboard**

   - Real-time metrics
   - Intent distribution charts
   - Order statistics
   - Performance analytics

### Test Scenarios

#### 1. Order Placement

```
Input: "مرحبا، بدي أطلب شاورما دجاج وحمص"
Expected Intent: order
Expected Response: Confirmation and quantity questions
```

#### 2. Menu Inquiry

```
Input: "شو عندكم من الأكل؟"
Expected Intent: question
Expected Response: Menu description
```

#### 3. Complaint Handling

```
Input: "الأكل وصل بارد"
Expected Intent: complaint
Expected Response: Empathetic response and solution
```

#### 4. Greeting

```
Input: "السلام عليكم"
Expected Intent: greeting
Expected Response: Warm welcome
```

## Syrian Arabic Accent Implementation

### Voice Selection

The system uses ElevenLabs' Arabic voices:

1. **Phonetic Accuracy**

   - Proper pronunciation of Syrian-specific phonemes
   - Correct stress patterns and intonation
   - Natural rhythm and prosody
2. **Cultural Authenticity**

   - Use of Syrian expressions and greetings
   - Appropriate formality levels
   - Regional vocabulary preferences
3. **Technical Implementation**

   ```python
   voice_settings = VoiceSettings(
       stability=0.75,        # Consistent pronunciation
       similarity_boost=0.85, # Maintain accent characteristics
       style=0.5,            # Natural conversational style
       use_speaker_boost=True # Enhanced clarity
   )
   ```

## 📊 Monitoring and Analytics

### Key Metrics

1. **Conversation Metrics**

   - Total conversations
   - Intent distribution
   - Confidence scores
   - Response times
2. **Order Metrics**

   - Total orders
   - Revenue tracking
   - Popular items
   - Order status distribution
3. **Performance Metrics**

   - Call success rate
   - Audio quality scores
   - System uptime
   - Error rates

### Dashboard Features

- Real-time conversation monitoring
- Interactive charts and graphs
- Exportable reports
- Alert system for issues

## Configuration

### Environment Variables

```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token

# AI Services
OPENAI_API_KEY=your_openai_key (Google Gemma)
ELEVENLABS_API_KEY=your_elevenlabs_key

APP_BASE_URL=Your Application URL [Ngrok or Custom Domain]
 
# Application Settings
FLASK_ENV=production
DEBUG=False
```

### Voice Agent Settings

```python
# Intent Detection Configuration
INTENT_CONFIDENCE_THRESHOLD = 0.7
MAX_CONVERSATION_CONTEXT = 6

# TTS Configuration
VOICE_STABILITY = 0.75
VOICE_SIMILARITY = 0.85

# Order Processing
DEFAULT_ETA_RANGE = (15, 45)  # minutes
CURRENCY = "USD"
```

## Deployment

### Local Development

```bash
# Backend
cd voice_agent_backend
source .venv/bin/activate
python src/main.py

# Frontend
streamlit run streamlit_ui.py
```

### Production Deployment

1. **Backend Deployment**

   ```bash
   # Update requirements
   pip freeze > requirements.txt

   # Deploy to cloud platform
   # (Heroku, AWS, Google Cloud, etc.)
   ```
2. **SIP Configuration**

   - Update Twilio webhook URLs
   - Configure SSL certificates
   - Set up monitoring
3. **Environment Setup**

   - Set production environment variables
   - Configure logging
   - Set up backup systems

## Troubleshooting

### Common Issues

1. **SIP Connection Problems**

   - Verify Twilio credentials
   - Check webhook URL accessibility
   - Confirm SSL certificate validity
2. **Audio Quality Issues**

   - Adjust ElevenLabs voice settings
   - Check network latency
   - Verify audio codec compatibility
3. **Intent Detection Accuracy**

   - Review training examples
   - Adjust confidence thresholds
   - Update context management
4. **Arabic Text Display**

   - Ensure UTF-8 encoding
   - Configure RTL text support
   - Verify font compatibility

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance Optimization

### Response Time Optimization

1. **Caching Strategies**

   - Cache frequent responses
   - Pre-load menu data
   - Store conversation context efficiently
2. **API Optimization**

   - Implement request pooling
   - Use async processing where possible
   - Optimize database queries
3. **Audio Processing**

   - Stream audio data
   - Compress audio files

### Scalability Considerations

- Implement load balancing
- Use message queues for high volume
- Consider microservices architecture
- Implement database clustering

## 🔒 Security

### Data Protection

- Encrypt sensitive customer data
- Implement secure API authentication
- Use HTTPS for all communications
- Regular security audits

### Privacy Compliance

- GDPR compliance for EU customers
- Data retention policies
- Customer consent management
- Secure data deletion

## Development Guidelines

1. Follow PEP 8 for Python code
2. Use meaningful commit messages
3. Add tests for new features
4. Update documentation

## 📞 Support

For technical support or questions:

- Create an issue in the repository
- Contact the development team
- Check the troubleshooting guide

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

---

**Built for Charco Chicken Restaurant**
*Bringing authentic Syrian hospitality to automated phone ordering*
