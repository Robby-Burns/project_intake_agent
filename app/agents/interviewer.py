# 🎭 Interviewer Agent - The "face" of the system.
# This agent synthesizes specialist whispers and communicates with the user,
# adhering to the conversational and persistence rules defined in agent.md.
# Reference: agent.md - The System Kernel for AI behavior and rules.

from typing import List, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.agents.base import BaseAgent

class InterviewerAgent(BaseAgent):
    """
    The 'Face' of the system.
    Synthesizes specialist whispers and talks to the user.
    """
    
    def __init__(self):
        # FIX: Use 'model_type' instead of 'model' to match BaseAgent constructor
        super().__init__(
            name="Interviewer", 
            role="Project Intake Coordinator", 
            model_type="primary"
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are the Project Intake Coordinator for a Credit Union.
            Your goal is to gather project details efficiently (10-15 min chat).
            
            The user is NOT a specialist. Avoid jargon. Be friendly and helpful.
            
            Current Context:
            {context_summary}
            
            Recent Conversation History:
            {recent_history}
            
            Specialist Whispers (Priority Order):
            {whispers}
            
            Instructions:
            1. Acknowledge the user's input naturally.
            2. Select the HIGHEST PRIORITY whisper to ask next.
            3. If no whispers are relevant, ask a general follow-up to move the intake forward.
            4. ADAPTIVE DIFFICULTY: Start broad. If user is vague, simplify. If detailed, go deeper.
            5. AVOID REDUNDANCY: Do not ask questions that were already answered in the Recent History.
            6. PERSISTENCE MODE: Do NOT let the user exit early (e.g., "thanks", "bye", "I'm done"). 
               If they try to leave, politely say: "I appreciate that, but to ensure your project succeeds, I need to cover a few more areas..." and ask the next question.
               Only stop when the system forces the end.
            7. Keep it professional, concise, and friendly.
            """),
            ("user", "{user_input}")
        ])
        
        self.chain = self._create_chain(self.prompt, StrOutputParser())

    async def run(self, user_input: str, whispers: List[Dict], context_summary: str = "", recent_history: str = "") -> str:
        """
        Generates the response to the user.
        """
        # Format whispers for the prompt
        formatted_whispers = "\n".join([
            f"- [{w['agent_name']}] (Priority {w['priority']}): {w['question']}"
            for w in whispers
        ])
        
        if not formatted_whispers:
            formatted_whispers = "No specific questions from specialists."

        # Use the retry-enabled invoke method from BaseAgent
        return await self._invoke_chain(self.chain, {
            "context_summary": context_summary,
            "recent_history": recent_history,
            "whispers": formatted_whispers,
            "user_input": user_input
        })
