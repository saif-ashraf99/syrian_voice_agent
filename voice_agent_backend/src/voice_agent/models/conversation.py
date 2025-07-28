from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid


@dataclass
class ConversationEntry:
    """Represents a single conversation exchange."""
    call_sid: str
    timestamp: str
    customer_text: str
    intent: str
    entities: Dict[str, List[Any]]
    agent_response: str
    confidence: float
    test_mode: bool = False
    
    @classmethod
    def create(
        cls,
        call_sid: str,
        customer_text: str,
        intent: str,
        entities: Dict[str, List[Any]],
        agent_response: str,
        confidence: float,
        test_mode: bool = False
    ) -> 'ConversationEntry':
        """Create a new conversation entry with current timestamp."""
        return cls(
            call_sid=call_sid,
            timestamp=datetime.now().isoformat(),
            customer_text=customer_text,
            intent=intent,
            entities=entities,
            agent_response=agent_response,
            confidence=confidence,
            test_mode=test_mode
        )


@dataclass
class ActiveCall:
    """Represents an active phone call."""
    call_sid: str
    from_number: str
    to_number: str
    start_time: datetime
    conversation: List[ConversationEntry] = field(default_factory=list)
    
    @classmethod
    def create(cls, call_sid: str, from_number: str, to_number: str) -> 'ActiveCall':
        """Create a new active call."""
        return cls(
            call_sid=call_sid,
            from_number=from_number,
            to_number=to_number,
            start_time=datetime.now(),
            conversation=[]
        )


@dataclass
class IntentData:
    """Represents detected intent and entities."""
    intent: str
    entities: Dict[str, List[Any]]
    confidence: float
    
    @classmethod
    def default(cls) -> 'IntentData':
        """Create a default intent data object."""
        return cls(
            intent="unknown",
            entities={"food_items": [], "quantities": [], "other": []},
            confidence=0.0
        )


class ConversationStorage:
    """Manages conversation logs and active calls."""
    
    def __init__(self):
        self.conversation_logs: List[ConversationEntry] = []
        self.active_calls: Dict[str, ActiveCall] = {}
    
    def add_conversation_entry(self, entry: ConversationEntry) -> None:
        """Add a conversation entry to logs."""
        self.conversation_logs.append(entry)
        
        # Also add to active call if it exists
        if entry.call_sid in self.active_calls:
            self.active_calls[entry.call_sid].conversation.append(entry)
    
    def start_call(self, call_sid: str, from_number: str, to_number: str) -> ActiveCall:
        """Start tracking a new call."""
        call = ActiveCall.create(call_sid, from_number, to_number)
        self.active_calls[call_sid] = call
        return call
    
    def end_call(self, call_sid: str) -> Optional[ActiveCall]:
        """End an active call and return it."""
        return self.active_calls.pop(call_sid, None)
    
    def get_call(self, call_sid: str) -> Optional[ActiveCall]:
        """Get an active call by ID."""
        return self.active_calls.get(call_sid)
    
    def get_logs_summary(self) -> Dict[str, Any]:
        """Get a summary of conversation logs."""
        return {
            'logs': [entry.__dict__ for entry in self.conversation_logs],
            'total_conversations': len(self.conversation_logs),
            'active_calls': len(self.active_calls)
        }
    
    def get_active_calls_summary(self) -> Dict[str, Any]:
        """Get a summary of active calls."""
        return {
            'active_calls': {
                call_sid: {
                    'from': call.from_number,
                    'to': call.to_number,
                    'start_time': call.start_time.isoformat(),
                    'conversation_count': len(call.conversation)
                }
                for call_sid, call in self.active_calls.items()
            },
            'count': len(self.active_calls)
        }


# Global conversation storage instance
conversation_storage = ConversationStorage()