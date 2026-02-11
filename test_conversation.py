import asyncio
import os
from dotenv import load_dotenv
from app.orchestrator.orchestrator import Orchestrator

# Load environment variables from .env file
load_dotenv()

async def run_mock_conversation():
    """
    Simulates a chat session to test the Whisper Engine.
    """
    print("🚀 Initializing Orchestrator...")
    orchestrator = Orchestrator()
    
    print("\n--- STARTING MOCK INTERVIEW ---\n")
    
    # Mock User Inputs (Flow: Name -> Project -> VP -> Chat -> End)
    inputs = [
        "John Doe",  # Name
        "Marketing Cloud Migration",  # Project
        "VP-123",  # VP Number
        "Hi, I want to implement a new cloud storage system for our marketing team.",
        "We are thinking of using Dropbox. It will store some member photos and maybe some contract drafts.",
        "No, we haven't talked to IT yet. We just need it fast.",
        "Generate report"  # Trigger PDF
    ]
    
    for i, user_msg in enumerate(inputs):
        print(f"\n👤 User: {user_msg}")
        
        # Run the pipeline
        response = await orchestrator.process_message(user_msg)
        
        print(f"🤖 Bot: {response}")
        print("-" * 50)

if __name__ == "__main__":
    # Check API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not set. Please set it in your environment.")
    else:
        asyncio.run(run_mock_conversation())
