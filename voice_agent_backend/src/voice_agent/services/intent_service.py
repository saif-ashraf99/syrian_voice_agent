import json
import openai

from ..config.settings import config
from ..models.conversation import IntentData
from ..utils.logger import logger


class IntentDetectionService:
    """Handles intent detection using AI models."""
    
    def __init__(self):
        if not config.openai.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = openai.OpenAI(
            api_key=config.openai.api_key,
            base_url=config.openai.base_url
        )
        
        # Test connection on initialization
        self._test_connection()
    
    def _test_connection(self) -> None:
        """Test the connection to the API."""
        try:
            response = self.client.chat.completions.create(
                model=config.openai.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            logger.info("✅ Intent detection service connected successfully")
        except Exception as e:
            logger.warning(f"⚠️ Intent detection service connection test failed: {e}")
    
    def detect_intent(self, text: str) -> IntentData:
        """
        Detect intent from customer text using Gemma model.
        
        Args:
            text: Customer's message text
            
        Returns:
            IntentData object with detected intent and entities
        """
        try:
            messages = [
                {
                    "role": "user",
                    "content": self._build_intent_prompt(text)
                }
            ]
            
            # First try with structured response format
            response = self._try_structured_request(messages)
            
            # If structured request fails, try simple request
            if not response:
                response = self._try_simple_request(messages)
            
            if not response:
                logger.error("All intent detection attempts failed")
                return IntentData.default()
            
            content = response.choices[0].message.content or ""
            
            if not content.strip():
                logger.error("Empty response content from intent model")
                return IntentData.default()
            
            # Try to parse as JSON
            intent_data = self._parse_intent_response(content)
            
            logger.info(f"Detected intent: {intent_data}")
            return intent_data
            
        except Exception as e:
            logger.error(f"Intent detection error: {e}")
            return IntentData.default()
    
    def _try_structured_request(self, messages):
        """Try request with structured JSON schema."""
        try:
            request_params = {
                "model": config.openai.model,
                "messages": messages,
                "temperature": 0.1
            }
            
            # Add structured response format (may not be supported by all models)
            request_params["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "type": "object",
                    "properties": {
                        "intent": {"type": "string"},
                        "entities": {
                            "type": "object",
                            "properties": {
                                "food_items": {"type": "array", "items": {"type": "string"}},
                                "quantities": {"type": "array", "items": {"type": "number"}},
                                "other": {"type": "array", "items": {"type": "string"}}
                            },
                            "required": ["food_items", "quantities", "other"]
                        },
                        "confidence": {"type": "number"}
                    },
                    "required": ["intent", "entities", "confidence"],
                    "additionalProperties": False
                },
                "strict": True
            }
            
            return self.client.chat.completions.create(**request_params)
            
        except Exception as e:
            logger.warning(f"Structured request failed: {e}")
            return None
    
    def _try_simple_request(self, messages):
        """Try simple request without structured format."""
        try:
            request_params = {
                "model": config.openai.model,
                "messages": messages,
                "temperature": 0.1,
                "max_tokens": 200
            }
            
            return self.client.chat.completions.create(**request_params)
            
        except Exception as e:
            logger.error(f"Simple request failed: {e}")
            return None
    
    def _parse_intent_response(self, content: str) -> IntentData:
        """Parse intent response, handling both JSON and text formats."""
        try:
            # First try to parse as JSON
            content = content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith('```json'):
                content = content.replace('```json', '').replace('```', '').strip()
            elif content.startswith('```'):
                content = content.replace('```', '').strip()
            
            # Try to find JSON in the response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_content = content[json_start:json_end]
                intent_dict = json.loads(json_content)
                
                return IntentData(
                    intent=intent_dict.get("intent", "unknown"),
                    entities=intent_dict.get("entities", {"food_items": [], "quantities": [], "other": []}),
                    confidence=float(intent_dict.get("confidence", 0.0))
                )
            
            # If JSON parsing fails, try to extract intent from text
            return self._extract_intent_from_text(content)
            
        except json.JSONDecodeError as je:
            logger.warning(f"JSON parsing failed, trying text extraction: {je}")
            return self._extract_intent_from_text(content)
        except Exception as e:
            logger.error(f"Intent parsing error: {e}")
            return IntentData.default()
    
    def _extract_intent_from_text(self, content: str) -> IntentData:
        """Extract intent from plain text response."""
        content_lower = content.lower()
        
        # Simple keyword-based intent detection as fallback
        if any(word in content_lower for word in ['order', 'طلب', 'بدي', 'أريد', 'عايز']):
            intent = "order"
        elif any(word in content_lower for word in ['complaint', 'شكوى', 'مشكلة', 'سيء']):
            intent = "complaint"
        elif any(word in content_lower for word in ['question', 'سؤال', 'شو', 'كيف', 'وين']):
            intent = "question"
        elif any(word in content_lower for word in ['greeting', 'أهلا', 'مرحبا', 'السلام']):
            intent = "greeting"
        elif any(word in content_lower for word in ['goodbye', 'وداع', 'شكرا', 'مع السلامة']):
            intent = "goodbye"
        else:
            intent = "unknown"
        
        return IntentData(
            intent=intent,
            entities={"food_items": [], "quantities": [], "other": []},
            confidence=0.5  # Lower confidence for text-based extraction
        )
    
    def _build_intent_prompt(self, text: str) -> str:
        """Build the prompt for intent detection."""
        return (
            "You are an intent detection system for a Syrian Arabic restaurant voice agent. "
            "Analyze the customer's message and classify it into one of these intents:\n"
            "- order\n- complaint\n- question\n- greeting\n- goodbye\n"
            "Also extract any food items, quantities, or other entities.\n\n"
            "Respond in JSON format:\n"
            "{\n"
            '  "intent": "order|complaint|question|greeting|goodbye",\n'
            '  "entities": { "food_items": [], "quantities": [], "other": [] },\n'
            '  "confidence": 0.0\n'
            "}\n\n"
            f"Customer said: {text}"
        )