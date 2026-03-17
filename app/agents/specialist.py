# 🕵️ Specialist Agent - A domain-expert agent that analyzes user input.
# This agent acts as a "whisperer" to the main interviewer, following the multi-agent debate pattern.
# Its behavior is governed by the principles of role-playing and structured output.
# Reference: agent.md - The System Kernel for AI behavior and rules.

from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from app.agents.base import BaseAgent

class SpecialistOutput(BaseModel):
    """
    Structured output for Specialist Agents during the interview.
    """
    relevant: bool = Field(description="Is this input relevant to your domain?")
    priority_score: int = Field(description="Priority score from 1-10 (10 is critical).")
    suggested_question: Optional[str] = Field(description="The question you want to whisper to the interviewer.")
    analysis: Optional[str] = Field(description="Brief analysis of why this is important.")

class SpecialistAgent(BaseAgent):
    """
    Specialist Agent (e.g., IT, InfoSec, Marketing).
    Analyzes input and 'whispers' questions.
    """
    
    def __init__(self, name: str, role: str, domain_focus: str, model_type: str = "primary"):
        super().__init__(name, role, model_type)
        self.domain_focus = domain_focus
        self.parser = PydanticOutputParser(pydantic_object=SpecialistOutput)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are the {name} Specialist for a Credit Union Project Intake system.
            Your Role: {role}
            Your Focus: {domain_focus}
            Current Project: {project_name}
            Analyze the user's input. If it touches on your domain, suggest a CRITICAL follow-up question.
            Assign a Priority Score (1-10): 1-3 (Nice to know), 4-7 (Important), 8-10 (Critical/Blocker).
            Output must be valid JSON matching the schema.
            """),
            ("user", "{input}\n\n{format_instructions}")
        ])
        self.chain = self._create_chain(self.prompt, self.parser)

        self.summary_prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are the {name} Specialist. Your Role: {role}. Your Focus: {domain_focus}.
            Read the following project intake transcript for project: {project_name}.
            Write a concise, professional summary (3-4 sentences) specifically for {name} professionals.
            Focus ONLY on risks, requirements, and implications relevant to your domain.
            """),
            ("user", "Transcript:\n{transcript}")
        ])
        self.summary_chain = self._create_chain(self.summary_prompt, StrOutputParser())

    async def run(self, user_input: str, project_name: str = "Unknown Project") -> SpecialistOutput:
        try:
            return await self._invoke_chain(self.chain, {
                "name": self.name,
                "role": self.role,
                "domain_focus": self.domain_focus,
                "project_name": project_name,
                "input": user_input,
                "format_instructions": self.parser.get_format_instructions()
            })
        except Exception as e:
            return SpecialistOutput(relevant=False, priority_score=0, suggested_question=None, analysis=f"Error processing input: {str(e)}")

    async def generate_summary(self, transcript: str, project_name: str = "Unknown Project") -> str:
        try:
            return await self._invoke_chain(self.summary_chain, {
                "name": self.name,
                "role": self.role,
                "domain_focus": self.domain_focus,
                "project_name": project_name,
                "transcript": transcript
            })
        except Exception as e:
            return f"Could not generate summary: {str(e)}"
