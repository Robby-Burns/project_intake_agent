from abc import ABC, abstractmethod
from typing import Optional

class PMToolAdapter(ABC):
    """
    Abstract Base Class for Project Management Tools.
    """
    
    @abstractmethod
    def create_ticket(self, title: str, description: str, pdf_path: Optional[str] = None) -> str:
        """
        Creates a ticket/item in the PM tool.
        
        Args:
            title: The title of the ticket (e.g., Project Name).
            description: The description (e.g., Executive Summary).
            pdf_path: Path to the PDF file to attach.
            
        Returns:
            str: The ID or URL of the created ticket.
        """
        pass
