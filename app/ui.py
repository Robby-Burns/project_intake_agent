import streamlit as st
import asyncio
import os
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
        st.session_state.orchestrator = Orchestrator()
        
    if "processing" not in st.session_state:
        st.session_state.processing = False

async def process_message(user_input: str):
    """Process user message through the orchestrator."""
    orchestrator = st.session_state.orchestrator
    response = await orchestrator.process_message(user_input)
    return response

def main():
    # Header
    st.title("🤖 Project Intake Agent")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("Project Details")
        
        # Display Metadata if available
        orch = st.session_state.orchestrator if "orchestrator" in st.session_state else None
        
        if orch:
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
        # Removed "Generate Report" tip as persistence mode is active

    # Initialize State
    initialize_session_state()

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
                try:
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
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
