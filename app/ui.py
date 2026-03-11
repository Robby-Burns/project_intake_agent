# 🎨 Streamlit UI - The user-facing component of the agent system.
# This file adheres to the principles outlined in agent.md by providing a clear user interface
# and handling the lifecycle of the Orchestrator.
# Reference: agent.md - The System Kernel for AI behavior and rules.

import streamlit as st
import asyncio
import os
import uuid
from dotenv import load_dotenv
from app.orchestrator.orchestrator import Orchestrator

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(
    page_title="Project Intake Agent",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #f0f2f6;
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: #e8f0fe;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if "session_id" not in st.session_state:
        # Generate new session ID for persistence
        st.session_state.session_id = str(uuid.uuid4())
        
    if "messages" not in st.session_state:
        # Initial Welcome Message
        welcome_msg = (
            "👋 **Welcome to the Project Intake Assistant!**\n\n"
            "I'm here to help you define your project scope. "
            "This process will take about **10-15 minutes**.\n\n"
            "To get started, please tell me: **What is your name?**"
        )
        st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]
    
    if "orchestrator" not in st.session_state:
        # Initialize Orchestrator with the session ID for DB persistence
        st.session_state.orchestrator = Orchestrator(session_id=st.session_state.session_id)
        
    if "processing" not in st.session_state:
        st.session_state.processing = False

async def process_message(user_input: str):
    """Process user message through the orchestrator."""
    orchestrator = st.session_state.orchestrator
    try:
        response = await orchestrator.process_message(user_input)
        return response
    except Exception as e:
        st.error(f"Error processing message: {str(e)}")
        return "I encountered an error. Please try again."

def main():
    # Header
    st.title("🤖 Project Intake Agent")
    st.markdown("---")
    
    # Initialize State first
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.header("Project Details")
        
        # Display Metadata if available
        orch = st.session_state.orchestrator if "orchestrator" in st.session_state else None
        
        if orch:
            st.info(f"**Session ID:** {st.session_state.session_id}")
            st.info(f"**Status:** {orch.state}")
            
            if orch.user_name:
                st.success(f"**User:** {orch.user_name}")
            if orch.project_name:
                st.success(f"**Project:** {orch.project_name}")
            if orch.vp_number:
                st.success(f"**VP#:** {orch.vp_number}")
            
            # Turn Counter
            turns = len(orch.conversation_history)
            limit = int(os.getenv("MAX_TURNS", 15))
            st.progress(min(turns / limit, 1.0), text=f"Progress: {turns}/{limit} Turns")
        
        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.markdown("- Provide clear project goals.")
        st.markdown("- Mention any known risks.")

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process Response
        with st.chat_message("assistant"):
            with st.spinner("Consulting with specialists..."):
                # Run async orchestrator in sync Streamlit app
                response = asyncio.run(process_message(prompt))
                st.markdown(response)
                
                # Add bot response to history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Check for PDF generation success message
                if "Report generated successfully" in response:
                    # Extract filename from response
                    # Format: "Report generated successfully: filename.pdf"
                    filename = response.split(": ")[-1].split("\n")[0].strip()
                    
                    # Ensure we look in the reports directory
                    if not filename.startswith("reports"):
                        filepath = os.path.join("reports", filename)
                    else:
                        filepath = filename
                        
                    if os.path.exists(filepath):
                        with open(filepath, "rb") as pdf_file:
                            st.download_button(
                                label="📄 Download Report PDF",
                                data=pdf_file,
                                file_name=os.path.basename(filepath),
                                mime="application/pdf"
                            )

if __name__ == "__main__":
    main()
