import openai
from typing import List, Dict, Any

from ..config.settings import config
from ..models.conversation import IntentData
from ..utils.logger import logger


class ResponseGenerationService:
    """Handles response generation using AI models."""
    
    def __init__(self):
        if not config.openai.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = openai.OpenAI(
            api_key=config.openai.api_key,
            base_url=config.openai.base_url
        )
        self.conversation_context: List[Dict[str, str]] = []
        self._instruction_in_context = False
    
    def generate_response(self, intent_data: IntentData, customer_text: str) -> str:
        """
        Generate contextual Syrian Arabic response.
        
        Args:
            intent_data: Detected intent and entities
            customer_text: Original customer message
            
        Returns:
            Generated response in Syrian Arabic
        """
        try:
            context_messages = self._build_context_messages(intent_data, customer_text)
            
            response = self.client.chat.completions.create(
                model=config.openai.model,
                messages=context_messages,
                temperature=0.7,
                max_tokens=150
            )
            
            content = response.choices[0].message.content or ""
            if not content.strip():
                logger.error("Empty response content from model")
                return "عذراً، ما وصلني رد واضح. ممكن تعيد؟"
            
            agent_response = content.strip()
            
            # Update conversation context
            self._update_context(customer_text, agent_response)
            
            logger.info(f"Generated response: {agent_response}")
            return agent_response
            
        except Exception as e:
            logger.error(f"Response generation error: {e}")
            return "عذراً، لم أفهم طلبك. ممكن تعيد؟"
    
    def _build_context_messages(
        self, 
        intent_data: IntentData, 
        customer_text: str
    ) -> List[Dict[str, str]]:
        """Build context messages for the AI model."""
        context_messages = []
        
        # Add system instruction if not already in context
        if not self._instruction_in_context:
            context_messages.append({
                "role": "user",
                "content": self._get_system_instruction()
            })
            self._instruction_in_context = True
        
        # Add recent conversation context (last 6 messages)
        max_context = config.max_conversation_context
        context_messages.extend(self.conversation_context[-max_context:])
        
        # Add current customer message with intent
        context_messages.append({
            "role": "user",
            "content": f"Customer intent: {intent_data.intent}, said: {customer_text}"
        })
        
        return context_messages
    
    def _update_context(self, customer_text: str, agent_response: str) -> None:
        """Update conversation context with new exchange."""
        self.conversation_context.append({"role": "user", "content": customer_text})
        self.conversation_context.append({"role": "assistant", "content": agent_response})
    
    def _get_system_instruction(self) -> str:
        """Get the system instruction for the AI model."""
        return (
            "You are a friendly Syrian Arabic voice agent for Charco Chicken restaurant. "
            "You must respond ONLY in Syrian Arabic dialect. "
            "Be helpful, polite, and focused on taking orders and answering questions about food. "
            "Keep responses short and conversational, suitable for phone calls. "
            "If customers want to order, ask for details. "
            "If they have complaints, be empathetic and offer solutions. "
            "Always maintain a warm, welcoming tone typical of Syrian hospitality."
        )
    
    def reset_context(self) -> None:
        """Reset conversation context."""
        self.conversation_context = []
        self._instruction_in_context = False