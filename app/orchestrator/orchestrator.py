# 🎼 The Orchestrator - The "Whisper Engine" of the system.
# This file implements the core logic of the 5-Phase Loop (Read, Research, Act, Update, Recognize)
# by managing agent execution, state, and final reporting.
# Reference: agent.md - The System Kernel for AI behavior and rules.

import asyncio
import os
import uuid
from typing import List, Dict, Optional
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from app.agents.specialist import SpecialistAgent
from app.agents.interviewer import InterviewerAgent
from app.guardrails.pii_filter import PIIFilter
from app.pdf.generator import PDFGenerator
from app.factories.pm_tool_factory import PMToolFactory
from app.factories.database_factory import DatabaseFactory
from app.factories.storage_factory import StorageFactory
from app.config import config # <-- Use the global config object

class FinalReportOutput(BaseModel):
    executive_summary: str = Field(description="A professional executive summary of the project intake.")
    key_findings: List[str] = Field(description="A list of 3-5 key findings or takeaways from the interview.")

class Orchestrator:
    """
    The 'Whisper Engine' Orchestrator.
    Manages agent execution, state, and final reporting using agnostic factories.
    """
    
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or str(uuid.uuid4())

        self.db_adapter = DatabaseFactory.get_adapter()
        self.storage_adapter = StorageFactory.get_adapter()
        
        self.interviewer = InterviewerAgent()
        self.specialists = [
            SpecialistAgent("Project Manager", "PMI Best Practices (PMBOK)", "Scope, Schedule, Cost...", model_type="specialist"),
            SpecialistAgent("Product Manager", "Hypothesis-Driven Development (HDD)", "Outcomes over output...", model_type="specialist"),
            SpecialistAgent("IT Specialist", "Enterprise Architecture (TOGAF/AWS Well-Architected)", "Scalability, reliability...", model_type="specialist"),
            SpecialistAgent("InfoSec", "NIST Cybersecurity Framework / GLBA", "Identify, Protect, Detect...", model_type="specialist"),
            SpecialistAgent("ERM", "COSO ERM Framework", "Risk appetite, vendor risk...", model_type="specialist"),
            SpecialistAgent("Marketing", "Marketing Mix (4Ps) & Member Lifecycle", "Product, Price, Place...", model_type="cost_efficient"),
            SpecialistAgent("Training", "ADDIE Model", "Analyze, Design, Develop...", model_type="cost_efficient"),
            SpecialistAgent("Accounting", "GAAP & ROI Analysis", "Capital vs Expense (CapEx/OpEx)...", model_type="cost_efficient"),
        ]
        
        self.conversation_history = self.db_adapter.get_conversation_history(self.session_id)
        metadata = self.db_adapter.get_metadata(self.session_id)
        if metadata:
            self.vp_number, self.user_name, self.project_name, self.stakeholders = metadata.get("vp_number"), metadata.get("user_name"), metadata.get("project_name"), metadata.get("stakeholders")
            self.state = metadata.get("state", "GET_NAME")
            self.unanswered_questions = []
        else:
            self.vp_number, self.user_name, self.project_name, self.stakeholders = None, None, None, None
            self.state = "GET_NAME"
            self.unanswered_questions = []
        
        self.pdf_generator = PDFGenerator()
        self.pm_tool = PMToolFactory.get_adapter()
        
        self.max_turns = config.orchestration.max_turns
        self.soft_limit = config.orchestration.soft_limit_turns

    def save_state(self):
        metadata = {"vp_number": self.vp_number, "user_name": self.user_name, "project_name": self.project_name, "stakeholders": self.stakeholders, "state": self.state}
        self.db_adapter.save_metadata(self.session_id, metadata)

    async def process_message(self, user_input: str) -> str:
        allow_list = []
        if self.state in ["GET_NAME", "GET_STAKEHOLDERS", "GET_PROJECT"]:
            if "PERSON" in config.security.pii_allow_list:
                allow_list.append("PERSON")
        sanitized_input = PIIFilter.redact(user_input, allow_list=allow_list)
        
        response = None
        if self.state == "GET_NAME":
            self.user_name = sanitized_input
            self.state = "GET_PROJECT"
            response = f"Thanks {self.user_name}. What is the name of this project?"
        elif self.state == "GET_PROJECT":
            self.project_name = sanitized_input
            self.state = "GET_VP"
            response = f"Got it. Please provide your VP Number exactly in this format **VP-123** for authorization."
        elif self.state == "GET_VP":
            vp_input = sanitized_input.upper().strip()
            if PIIFilter.validate_vp_number(vp_input):
                self.vp_number = vp_input
                self.state = "GET_STAKEHOLDERS"
                response = f"VP Number verified. Who are the key stakeholders for '{self.project_name}'?"
            else:
                response = "Invalid format. Please enter your VP Number exactly in this format **VP-123**."
        elif self.state == "GET_STAKEHOLDERS":
            self.stakeholders = sanitized_input
            self.state = "INTERVIEW"
            response = "Thank you. Let's begin the intake. Please describe the project goals."
        
        if response:
            self.db_adapter.save_conversation_turn(self.session_id, user_input, response)
            self.save_state()
            return response

        if "generate report" in sanitized_input.lower() or "end interview" in sanitized_input.lower():
            return await self.finalize_session()
            
        current_turns = len(self.conversation_history)
        if current_turns >= self.max_turns:
            return await self.finalize_session()

        specialist_tasks = [agent.run(sanitized_input, project_name=self.project_name) for agent in self.specialists]
        results = await asyncio.gather(*specialist_tasks)
        
        active_whispers = [
            {"agent_name": agent.name, "priority": result.priority_score, "question": result.suggested_question, "analysis": result.analysis}
            for agent, result in zip(self.specialists, results) if result.relevant
        ]
        for whisper in active_whispers: self.unanswered_questions.append(whisper)
        active_whispers.sort(key=lambda x: x['priority'], reverse=True)
        
        context_summary = f"Project: {self.project_name}. User: {self.user_name}. Stakeholders: {self.stakeholders}."
        recent_history = "\n".join([f"User: {entry['user']}\nBot: {entry['bot']}" for entry in self.conversation_history[-3:]])
        if current_turns >= self.max_turns:
            context_summary += " [SYSTEM NOTE: We are approaching the time limit. Start wrapping up.]"
        
        response = await self.interviewer.run(user_input=sanitized_input, whispers=active_whispers, context_summary=context_summary, recent_history=recent_history)
        
        self.conversation_history.append({"user": sanitized_input, "bot": response})
        self.db_adapter.save_conversation_turn(self.session_id, sanitized_input, response)
        self.save_state()
        
        return response

    async def finalize_session(self) -> str:
        transcript_text = "\n".join([f"User: {entry['user']}\nBot: {entry['bot']}" for entry in self.conversation_history])
        
        parser = PydanticOutputParser(pydantic_object=FinalReportOutput)
        summary_prompt = [SystemMessage(content="..."), HumanMessage(content=f"Project: {self.project_name}\nTranscript:\n{transcript_text}\n\n{parser.get_format_instructions()}")]
        
        try:
            report_data = await (self.interviewer.llm | parser).ainvoke(summary_prompt)
            executive_summary, key_findings = report_data.executive_summary, report_data.key_findings
        except Exception as e:
            executive_summary, key_findings = "Summary generation failed.", [f"Error: {e}"]

        summary_tasks = [agent.generate_summary(transcript_text, project_name=self.project_name) for agent in self.specialists]
        domain_summaries = await asyncio.gather(*summary_tasks)
        
        specialist_data = {}
        for agent, summary in zip(self.specialists, domain_summaries):
            agent_questions = sorted([q for q in self.unanswered_questions if q['agent_name'] == agent.name], key=lambda x: x['priority'], reverse=True)
            specialist_data[agent.name] = {"summary": summary, "questions": agent_questions[:5]}
        
        try:
            file_name = f"{self.project_name.replace(' ', '_')}_Report.pdf"
            pdf_bytes = self.pdf_generator.generate(project_name=self.project_name, user_name=self.user_name, vp_number=self.vp_number, stakeholders=self.stakeholders, executive_summary=executive_summary, key_findings=key_findings, specialist_data=specialist_data, transcript=self.conversation_history)
            
            saved_path = self.storage_adapter.save(file_name, pdf_bytes)
            
            ticket_link = self.pm_tool.create_ticket(title=f"Intake: {self.project_name}", description=f"**Executive Summary:**\n{executive_summary}\n\n**Requester:** {self.user_name} ({self.vp_number})", pdf_path=saved_path)
            
            return (f"Interview complete. Report generated successfully and saved to {saved_path}\n\n"
                    f"✅ **Ticket Created:** {ticket_link}\n\n"
                    f"Thank you. Someone from the Project Team will be in touch shortly.")
        except Exception as e:
            print(f"Finalization Error: {e}")
            return f"Interview complete, but report finalization failed. Error: {e}"
