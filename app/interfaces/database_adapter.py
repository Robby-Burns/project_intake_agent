from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class DatabaseAdapter(ABC):
    """
    Interface for database operations.
    Reference: workflow/08_AGNOSTIC_FACTORIES.md
    """
    
    @abstractmethod
    def save_conversation_turn(self, session_id: str, user_input: str, bot_response: str) -> None:
        """
        Saves a single turn of conversation.
        """
        pass

    @abstractmethod
    def get_conversation_history(self, session_id: str) -> List[Dict[str, str]]:
        """
        Retrieves the full conversation history for a session.
        """
        pass
    
    @abstractmethod
    def save_metadata(self, session_id: str, metadata: Dict[str, str]) -> None:
        """
        Saves session metadata (e.g., project name, VP number).
        """
        pass

    @abstractmethod
    def get_metadata(self, session_id: str) -> Optional[Dict[str, str]]:
        """
        Retrieves session metadata.
        """
        pass
