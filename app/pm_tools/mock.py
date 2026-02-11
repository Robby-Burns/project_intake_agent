from .adapter import PMToolAdapter
from typing import Optional

class MockAdapter(PMToolAdapter):
    """
    Mock Adapter for local development.
    Just prints to console.
    """
    
    def create_ticket(self, title: str, description: str, pdf_path: Optional[str] = None) -> str:
        print(f"🚀 [MOCK PM TOOL] Creating Ticket: {title}")
        print(f"📝 Description: {description[:50]}...")
        if pdf_path:
            print(f"📎 Attaching PDF: {pdf_path}")
        
        return "MOCK-TICKET-123"
