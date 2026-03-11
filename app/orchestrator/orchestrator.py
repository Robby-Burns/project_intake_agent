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
from app.factories.pm_tool_factory import PMToolFactory # <-- CORRECT IMPORT
from app.factories.database_factory import DatabaseFactory
from app.config import config

class FinalReportOutput(BaseModel):
    executive_summary: str = Field(description="A professional executive summary of the project intake.")
    key_findings: List[str] = Field(description="A list of 3-5 key findings or takeaways from the interview.")

class Orchestrator:
    """
    The 'Whisper Engine' Orchestrator.
    Manages the parallel execution of 8 specialist agents and the interviewer.
    Refactored to use DatabaseFactory for persistence and LLMFactory (via BaseAgent).
    Reference: workflow/02_COMPLETE_GUIDE.md
    """
    
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.db_adapter = DatabaseFactory.get_adapter()

        # Initialize Interviewer
        self.interviewer = InterviewerAgent()
        
        # Initialize Specialists (Model Mixing handled by LLMFactory and config)
        self.specialists = [
            SpecialistAgent(
                "Project Manager", 
                "PMI Best Practices (PMBOK)", 
                "Scope, Schedule, Cost, Quality, Resources, and Risk Management aligned with PMI standards.",
                model_type="specialist"
            ),
            SpecialistAgent(
                "Product Manager", 
                "Hypothesis-Driven Development (HDD)", 
                "Outcomes over output. Focus on hypotheses, experiments, success metrics, and member value.",
                model_type="specialist"
            ),
            SpecialistAgent(
                "IT Specialist", 
                "Enterprise Architecture (TOGAF/AWS Well-Architected)", 
                "Scalability, reliability, integration patterns, and technical debt management.",
                model_type="specialist"
            ),
            SpecialistAgent(
                "InfoSec", 
                "NIST Cybersecurity Framework / GLBA", 
                "Identify, Protect, Detect, Respond, Recover. Focus on data privacy and financial compliance.",
                model_type="specialist"
            ),
            SpecialistAgent(
                "ERM", 
                "COSO ERM Framework", 
                "Risk appetite, vendor risk management, regulatory compliance, and governance.",
                model_type="specialist"
            ),
            SpecialistAgent(
                "Marketing", 
                "Marketing Mix (4Ps) & Member Lifecycle", 
                "Product, Price, Place, Promotion. Focus on member acquisition, retention, and brand alignment.",
                model_type="cost_efficient"
            ),
            SpecialistAgent(
                "Training", 
                "ADDIE Model", 
                "Analyze, Design, Develop, Implement, Evaluate. Focus on staff readiness and procedure documentation.",
                model_type="cost_efficient"
            ),
            SpecialistAgent(
                "Accounting", 
                "GAAP & ROI Analysis", 
                "Capital vs Expense (CapEx/OpEx), GL coding, TCO (Total Cost of Ownership), and financial reporting.",
                model_type="cost_efficient"
            ),
        ]
        
        # Load State from Database
        self.conversation_history = self.db_adapter.get_conversation_history(self.session_id)
        
        # Load Metadata from Database
        metadata = self.db_adapter.get_metadata(self.session_id)
        if metadata:
            self.vp_number = metadata.get("vp_number")
            self.user_name = metadata.get("user_name")
            self.project_name = metadata.get("project_name")
            self.stakeholders = metadata.get("stakeholders")
            self.state = metadata.get("state", "GET_NAME")
            self.unanswered_questions = metadata.get("unanswered_questions", []) # Need to parse JSON if implementing fully
        else:
            self.vp_number = None
            self.user_name = None
            self.project_name = None
            self.stakeholders = None
            self.state = "GET_NAME"
            self.unanswered_questions = []
        
        self.pdf_generator = PDFGenerator()
        # FIX: Use the new factory
        self.pm_tool = PMToolFactory.get_adapter()
        
        # Limits from config
        self.max_turns = config.orchestration.max_turns
        self.soft_limit = config.orchestration.soft_limit_turns

    def save_state(self):
        """
        Saves metadata and state to the database.
        """
        metadata = {
            "vp_number": self.vp_number,
            "user_name": self.user_name,
            "project_name": self.project_name,
            "stakeholders": self.stakeholders,
            "state": self.state,
            # For MVP, not persisting unanswered_questions fully to DB as it's complex object
            # Ideally, use a dedicated table or JSON field
        }
        self.db_adapter.save_metadata(self.session_id, metadata)

    async def process_message(self, user_input: str) -> str:
        """
        Main pipeline:
        1. Sanitize Input (Guardrails)
        2. State Machine (Metadata Collection)
        3. Broadcast to Specialists (Parallel)
        4. Synthesize Response (Interviewer)
        """
        # 1. Guardrails: PII Redaction
        allow_list = []
        if self.state in ["GET_NAME", "GET_STAKEHOLDERS", "GET_PROJECT"]:
            # Config-driven allow list
            if "PERSON" in config.security.pii_allow_list:
                allow_list.append("PERSON")
            
        sanitized_input = PIIFilter.redact(user_input, allow_list=allow_list)
        
        # 2. State Machine for Metadata
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

        # If state machine generated a response, save and return
        if response:
            self.db_adapter.save_conversation_turn(self.session_id, user_input, response)
            self.save_state()
            return response

        # Check for exit condition
        if "generate report" in sanitized_input.lower() or "end interview" in sanitized_input.lower():
            return await self.finalize_session()
            
        # Check Turn Limits
        current_turns = len(self.conversation_history)
        if current_turns >= self.max_turns:
            return await self.finalize_session()

        # 3. Parallel Execution (The Whisper Engine)
        specialist_tasks = [
            agent.run(sanitized_input, project_name=self.project_name) for agent in self.specialists
        ]
        results = await asyncio.gather(*specialist_tasks)
        
        # Filter and Rank Whispers
        active_whispers = []
        for agent, result in zip(self.specialists, results):
            if result.relevant:
                whisper = {
                    "agent_name": agent.name,
                    "priority": result.priority_score,
                    "question": result.suggested_question,
                    "analysis": result.analysis
                }
                active_whispers.append(whisper)
                self.unanswered_questions.append(whisper)

        # Sort by Priority (Highest first)
        active_whispers.sort(key=lambda x: x['priority'], reverse=True)
        
        # 4. Interviewer Synthesis
        context_summary = f"Project: {self.project_name}. User: {self.user_name}. Stakeholders: {self.stakeholders}."
        
        # Get recent history (last 3 turns)
        recent_history = "\n".join([f"User: {entry['user']}\nBot: {entry['bot']}" for entry in self.conversation_history[-3:]])
        
        # Inject "Soft Limit" warning if needed
        if current_turns >= self.soft_limit:
            context_summary += " [SYSTEM NOTE: We are approaching the time limit. Start wrapping up.]"
        
        response = await self.interviewer.run(
            user_input=sanitized_input,
            whispers=active_whispers,
            context_summary=context_summary,
            recent_history=recent_history
        )
        
        # Update History & Save
        self.conversation_history.append({"user": sanitized_input, "bot": response})
        self.db_adapter.save_conversation_turn(self.session_id, sanitized_input, response)
        self.save_state()

        return response

    async def finalize_session(self) -> str:
        """
        Generates the PDF report, creates a PM ticket, and ends the session.
        """
        # Reconstruct transcript from DB history
        transcript_text = "\n".join([f"User: {entry['user']}\nBot: {entry['bot']}" for entry in self.conversation_history])
        
        # 1. Generate Executive Summary & Key Findings (Interviewer Agent)
        parser = PydanticOutputParser(pydantic_object=FinalReportOutput)
        summary_prompt = [
            SystemMessage(content="You are an expert Project Analyst. Summarize the following project intake interview."),
            HumanMessage(content=f"""
            Project: {self.project_name}
            Transcript:
            {transcript_text}
            
            {parser.get_format_instructions()}
            """)
        ]
        
        try:
            chain = self.interviewer.llm | parser
            report_data = await chain.ainvoke(summary_prompt)
            executive_summary = report_data.executive_summary
            key_findings = report_data.key_findings
        except Exception as e:
            executive_summary = "Summary generation failed."
            key_findings = ["Error generating key findings."]
            print(f"Error generating summary: {e}")

        # 2. Generate Domain Summaries (All Specialists in Parallel)
        summary_tasks = [
            agent.generate_summary(transcript_text, project_name=self.project_name) for agent in self.specialists
        ]
        domain_summaries = await asyncio.gather(*summary_tasks)
        
        # 3. Organize Data for PDF
        specialist_data = {}
        for agent, summary in zip(self.specialists, domain_summaries):
            agent_questions = [
                q for q in self.unanswered_questions 
                if q['agent_name'] == agent.name
            ]
            agent_questions.sort(key=lambda x: x['priority'], reverse=True)
            top_5_questions = agent_questions[:5]
            
            specialist_data[agent.name] = {
                "summary": summary,
                "questions": top_5_questions
            }
        
        # 4. Generate PDF
        filename = f"{self.project_name.replace(' ', '_')}_Report.pdf"
        self.pdf_generator.filename = filename
        
        success = self.pdf_generator.generate(
            project_name=self.project_name,
            user_name=self.user_name,
            vp_number=self.vp_number,
            stakeholders=self.stakeholders,
            executive_summary=executive_summary,
            key_findings=key_findings,
            specialist_data=specialist_data,
            transcript=self.conversation_history
        )
        
        # 5. Create PM Ticket
        ticket_link = "Ticket creation failed"
        if success:
            try:
                full_pdf_path = self.pdf_generator.filename
                if not full_pdf_path.startswith("reports"):
                    full_pdf_path = os.path.join("reports", full_pdf_path)
                
                ticket_link = self.pm_tool.create_ticket(
                    title=f"Intake: {self.project_name}",
                    description=f"**Executive Summary:**\n{executive_summary}\n\n**Requester:** {self.user_name} ({self.vp_number})",
                    pdf_path=full_pdf_path
                )
            except Exception as e:
                print(f"PM Tool Tool Error: {e}")
        
        if success:
            return (f"Interview complete. Report generated successfully: {filename}\n\n"
                    f"✅ **Ticket Created:** {ticket_link}\n\n"
                    f"Thank you. Someone from the Project Team will be in touch shortly.")
        return "Interview complete, but report generation failed."
