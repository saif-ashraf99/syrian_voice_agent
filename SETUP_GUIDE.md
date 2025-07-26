# Syrian Arabic Voice Agent - Complete Setup Guide

This comprehensive guide will walk you through setting up the Syrian Arabic Voice Agent system from scratch, including all dependencies, configurations, and testing procedures.

## 📋 Prerequisites

### System Requirements

- **Operating System**: Ubuntu 20.04+ / macOS 10.15+ / Windows 10+
- **Python**: 3.11 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 2GB free space
- **Network**: Stable internet connection for API calls

### Required Accounts and API Keys

1. **Twilio Account** (for SIP integration)

   - Sign up at [twilio.com](https://www.twilio.com)
   - Note down Account SID and Auth Token
2. **OpenAI API Key** (for intent detection)

   - Create account at [openrouter](https://openrouter.ai/)
   - Choose a model and generate API key (In my case:  "google/gemma-3n-e2b-it:free")
3. **ElevenLabs API Key** (for Syrian Arabic TTS)

   - Register at [elevenlabs.io](https://elevenlabs.io)
   - Generate API key from dashboard

## 🛠️ Installation Steps

### Step 1: Environment Setup

1. **Clone or Download the Project**

   ```bash
   cd syrian_voice_agent
   ```
2. **Navigate to Backend Directory**

   ```bash
   cd voice_agent_backend
   ```
3. **Create and Activate Virtual Environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

### Step 2: Dependencies Installation

**Install Required Packages**

```bash
pip install -r requirements.txt
```

### Step 3: Configuration

1. **Create Environment File**

   ```bash
   touch .env
   ```
2. **Add API Keys to .env**

   ```env
   # Twilio Configuration
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_auth_token_here

   # OpenAI Configuration
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

   # ElevenLabs Configuration
   ELEVENLABS_API_KEY=your_elevenlabs_key_here

   # Application Settings
   FLASK_ENV=development
   DEBUG=True
   ```
3. **Load Environment Variables**

   ```bash
   export $(cat .env | xargs)
   ```

### Step 4: Twilio SIP Configuration

1. **Purchase Phone Number**

   - Log into Twilio Console
   - Go to Phone Numbers → Manage → Buy a number
   - Choose a number with Voice capabilities
   - Complete purchase
2. **Configure Webhook**

   - In Phone Numbers section, click on your number
   - Set Webhook URL to: `https://your-domain.com/api/voice_agent/webhook/voice`
   - Set HTTP method to POST
   - Save configuration
3. **Test SIP Connection**

   ```bash
   # Test webhook endpoint
   curl -X POST http://localhost:5000/api/voice_agent/webhook/voice \
        -d "CallSid=test123&From=+1234567890&To=+0987654321"
   ```

## Running the System

### Step 1: Start the Backend Server

1. **Navigate to Backend Directory**

   ```bash
   cd voice_agent_backend
   source .venv/bin/activate
   ```
2. **Start Flask Application**

   ```bash
   python src/main.py
   ```
3. **Verify Backend is Running**

   ```bash
   curl http://localhost:5000/api/menu
   # Should return JSON menu data
   ```

### Step 2: Start the Testing Interface

1. **Open New Terminal**

   ```bash
   cd syrian_voice_agent
   ```
2. **Start Streamlit Application**

   ```bash
   streamlit run streamlit_ui.py
   ```
3. **Access the Interface**

   - Open browser to `http://localhost:8501`
   - Verify all pages load correctly

### Step 3: Test System Components

1. **Test Voice Agent API**

   ```bash
   curl -X POST http://localhost:5000/api/voice_agent/test_voice \
        -H "Content-Type: application/json" \
        -d '{"text": "مرحبا، بدي أطلب شاورما دجاج"}'
   ```
2. **Test Order Submission**

   ```bash
   curl -X POST http://localhost:5000/api/submit-order \
        -H "Content-Type: application/json" \
        -d '{
          "name": "أحمد محمد",
          "order_list": [
            {"item": "شاورما دجاج", "quantity": 2, "price": 15.00}
          ]
        }'
   ```
3. **Test Conversation Logs**

   ```bash
   curl http://localhost:5000/api/voice_agent/conversation_logs
   ```

## Testing Procedures

### Functional Testing

1. **Voice Agent Testing**

   - Open Streamlit interface
   - Navigate to "Voice Testing" page
   - Test with various Syrian Arabic phrases:
     - Orders: "بدي أطلب شاورما دجاج"
     - Questions: "شو عندكم من الأكل؟"
     - Complaints: "الأكل وصل بارد"
     - Greetings: "السلام عليكم"
2. **Intent Detection Accuracy**

   - Verify correct intent classification
   - Check confidence scores (should be > 0.7)
   - Validate entity extraction
3. **Response Quality**

   - Ensure responses are in Syrian Arabic
   - Check for cultural appropriateness
   - Verify contextual relevance

### SIP Integration Testing

1. **Local Testing**

   ```bash
   # Use ngrok to expose local server
   ngrok http 5000

   # Update Twilio webhook to ngrok URL
   # Test by calling your Twilio number
   ```
2. **Call Flow Testing**

   - Dial the Twilio number
   - Verify welcome message plays
   - Test voice recording functionality
   - Check transcription accuracy

### Performance Testing

1. **Load Testing**

   ```bash
   # Install Apache Bench
   sudo apt-get install apache2-utils

   # Test API endpoints
   ab -n 100 -c 10 http://localhost:5000/api/menu
   ```
2. **Response Time Testing**

   - Measure API response times
   - Test with various input lengths
   - Monitor memory usage

## 🔧 Troubleshooting

### Common Issues and Solutions

1. **Backend Won't Start**

   ```bash
   # Check Python version
   python --version

   # Verify virtual environment
   which python

   # Check for missing dependencies
   pip install -r requirements.txt
   ```
2. **API Key Errors**

   ```bash
   # Verify environment variables
   echo $OPENAI_API_KEY
   echo $ELEVENLABS_API_KEY
   echo $TWILIO_ACCOUNT_SID

   # Reload environment
   source .env
   export $(cat .env | xargs)
   ```
3. **Twilio Webhook Issues**

   - Verify webhook URL is accessible
   - Check SSL certificate if using HTTPS
   - Ensure POST method is configured
   - Test with ngrok for local development
4. **Arabic Text Display Issues**

   - Verify UTF-8 encoding
   - Check browser font support
   - Ensure RTL text direction is set
5. **Audio Generation Problems**

   - Verify ElevenLabs API key
   - Check voice availability
   - Test with shorter text inputs
   - Monitor API usage limits

### Debug Mode

1. **Enable Debug Logging**

   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```
2. **Check Application Logs**

   ```bash
   tail -f app.log
   ```
3. **Monitor API Calls**

   ```bash
   # Use curl with verbose output
   curl -v http://localhost:5000/api/voice_agent/test_voice
   ```

## 📊 Monitoring Setup

### Application Monitoring

1. **Log Configuration**

   ```python
   import logging
   from logging.handlers import RotatingFileHandler

   handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
   handler.setLevel(logging.INFO)
   app.logger.addHandler(handler)
   ```
2. **Performance Metrics**

   - Monitor response times
   - Track API usage
   - Monitor memory consumption
   - Check error rates

### Health Checks

1. **Create Health Check Endpoint**

   ```python
   @app.route('/health')
   def health_check():
       return jsonify({
           'status': 'healthy',
           'timestamp': datetime.now().isoformat(),
           'version': '1.0.0'
       })
   ```

## Production Deployment

### Preparation

1. **Update Configuration**

   ```env
   FLASK_ENV=production
   DEBUG=False
   ```
2. **Security Hardening**

   - Use strong secret keys
   - Enable HTTPS
   - Implement rate limiting
   - Add authentication if needed
3. **Performance Optimization**

   - Use production WSGI server (Gunicorn)
   - Configure caching
   - Optimize database queries
   - Implement CDN for static files

### Deployment Options

1. **Cloud Platforms**

   - Heroku
   - AWS Elastic Beanstalk
   - Google Cloud Run
   - Azure App Service
2. **Container Deployment**

   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "src/main.py"]
   ```
3. **Server Deployment**

   ```bash
   # Install Gunicorn
   pip install gunicorn

   # Run with Gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
   ```

## 📞 Support and Maintenance

### Regular Maintenance

1. **Update Dependencies**

   ```bash
   pip list --outdated
   pip install --upgrade package_name
   ```
2. **Monitor API Usage**

   - Check OpenAI usage dashboard
   - Monitor ElevenLabs credits
   - Review Twilio usage reports
3. **Backup Data**

   - Export conversation logs
   - Backup configuration files
   - Save order data

### Getting Help

- Check the main README.md for detailed documentation
- Review error logs for specific issues
- Test individual components in isolation
- Contact support teams for API-related issues
