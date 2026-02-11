import asyncio
import os
from typing import List, Dict, Optional
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from app.agents.specialist import SpecialistAgent
from app.agents.interviewer import InterviewerAgent
from app.guardrails.pii_filter import PIIFilter
from app.pdf.generator import PDFGenerator
from app.pm_tools import get_pm_tool

class FinalReportOutput(BaseModel):
    executive_summary: str = Field(description="A professional executive summary of the project intake.")
    key_findings: List[str] = Field(description="A list of 3-5 key findings or takeaways from the interview.")

class Orchestrator:
    """
    The 'Whisper Engine' Orchestrator.
    Manages the parallel execution of 8 specialist agents and the interviewer.
    """
    
    def __init__(self):
        # Initialize Interviewer
        self.interviewer = InterviewerAgent()
        
        # Initialize Specialists (Model Mixing: GPT-4o vs GPT-4o-mini)
        # Complex Agents (GPT-4o)
        self.specialists = [
            SpecialistAgent(
                "Project Manager", 
                "PMI Best Practices (PMBOK)", 
                "Scope, Schedule, Cost, Quality, Resources, and Risk Management aligned with PMI standards.", 
                model="gpt-4o"
            ),
            SpecialistAgent(
                "Product Manager", 
                "Hypothesis-Driven Development (HDD)", 
                "Outcomes over output. Focus on hypotheses, experiments, success metrics, and member value.", 
                model="gpt-4o"
            ),
            SpecialistAgent(
                "IT Specialist", 
                "Enterprise Architecture (TOGAF/AWS Well-Architected)", 
                "Scalability, reliability, integration patterns, and technical debt management.", 
                model="gpt-4o"
            ),
            SpecialistAgent(
                "InfoSec", 
                "NIST Cybersecurity Framework / GLBA", 
                "Identify, Protect, Detect, Respond, Recover. Focus on data privacy and financial compliance.", 
                model="gpt-4o"
            ),
            SpecialistAgent(
                "ERM", 
                "COSO ERM Framework", 
                "Risk appetite, vendor risk management, regulatory compliance, and governance.", 
                model="gpt-4o"
            ),
        ]
        
        # Simple Agents (GPT-4o-mini) - Cost Optimization
        self.specialists.extend([
            SpecialistAgent(
                "Marketing", 
                "Marketing Mix (4Ps) & Member Lifecycle", 
                "Product, Price, Place, Promotion. Focus on member acquisition, retention, and brand alignment.", 
                model="gpt-4o-mini"
            ),
            SpecialistAgent(
                "Training", 
                "ADDIE Model", 
                "Analyze, Design, Develop, Implement, Evaluate. Focus on staff readiness and procedure documentation.", 
                model="gpt-4o-mini"
            ),
            SpecialistAgent(
                "Accounting", 
                "GAAP & ROI Analysis", 
                "Capital vs Expense (CapEx/OpEx), GL coding, TCO (Total Cost of Ownership), and financial reporting.", 
                model="gpt-4o-mini"
            ),
        ])
        
        # State
        self.conversation_history = []
        self.unanswered_questions = [] # List of all whispers
        
        # Metadata State
        self.vp_number: Optional[str] = None
        self.user_name: Optional[str] = None
        self.project_name: Optional[str] = None
        self.stakeholders: Optional[str] = None
        self.state = "GET_NAME" # GET_NAME, GET_PROJECT, GET_VP, GET_STAKEHOLDERS, INTERVIEW
        
        self.pdf_generator = PDFGenerator()
        self.pm_tool = get_pm_tool()
        
        # Limits
        self.max_turns = int(os.getenv("MAX_TURNS", 15))
        self.soft_limit = int(os.getenv("SOFT_LIMIT_TURNS", 12))

    async def process_message(self, user_input: str) -> str:
        """
        Main pipeline:
        1. Sanitize Input (Guardrails)
        2. State Machine (Metadata Collection)
        3. Broadcast to Specialists (Parallel)
        4. Synthesize Response (Interviewer)
        """
        # 1. Guardrails: PII Redaction
        # Conditionally skip PERSON redaction for Name and Stakeholders
        allow_list = []
        if self.state in ["GET_NAME", "GET_STAKEHOLDERS", "GET_PROJECT"]:
            allow_list.append("PERSON")
            
        sanitized_input = PIIFilter.redact(user_input, allow_list=allow_list)
        
        # 2. State Machine for Metadata
        if self.state == "GET_NAME":
            self.user_name = sanitized_input
            self.state = "GET_PROJECT"
            return f"Thanks {self.user_name}. What is the name of this project?"
            
        if self.state == "GET_PROJECT":
            self.project_name = sanitized_input
            self.state = "GET_VP"
            return f"Got it. Please provide your VP Number exactly in this format **VP-123** for authorization."
            
        if self.state == "GET_VP":
            vp_input = sanitized_input.upper().strip()
            if PIIFilter.validate_vp_number(vp_input):
                self.vp_number = vp_input
                self.state = "GET_STAKEHOLDERS"
                return f"VP Number verified. Who are the key stakeholders for '{self.project_name}'?"
            else:
                return "Invalid format. Please enter your VP Number exactly in this format **VP-123**."

        if self.state == "GET_STAKEHOLDERS":
            self.stakeholders = sanitized_input
            self.state = "INTERVIEW"
            return "Thank you. Let's begin the intake. Please describe the project goals."

        # Check for exit condition
        if "generate report" in sanitized_input.lower() or "end interview" in sanitized_input.lower():
            return await self.finalize_session()
            
        # Check Turn Limits
        current_turns = len(self.conversation_history)
        if current_turns >= self.max_turns:
            return await self.finalize_session()

        # 3. Parallel Execution (The Whisper Engine)
        # Run all specialists concurrently
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
                
                # Store ALL relevant whispers for the final report
                self.unanswered_questions.append(whisper)

        # Sort by Priority (Highest first)
        active_whispers.sort(key=lambda x: x['priority'], reverse=True)
        
        # 4. Interviewer Synthesis
        context_summary = f"Project: {self.project_name}. User: {self.user_name}. Stakeholders: {self.stakeholders}."
        
        # Get recent history (last 3 turns) to avoid redundancy
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
        
        # Update History
        self.conversation_history.append({"user": sanitized_input, "bot": response})
        
        return response

    async def finalize_session(self) -> str:
        """
        Generates the PDF report, creates a PM ticket, and ends the session.
        """
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
            # Filter questions for this agent
            agent_questions = [
                q for q in self.unanswered_questions 
                if q['agent_name'] == agent.name
            ]
            # Sort by priority
            agent_questions.sort(key=lambda x: x['priority'], reverse=True)
            # Take top 5
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
                # FIX: Ensure we pass the full path including 'reports/'
                # The PDFGenerator automatically prepends 'reports/' to self.filename if needed
                # But let's be explicit to be safe
                full_pdf_path = self.pdf_generator.filename
                if not full_pdf_path.startswith("reports"):
                    full_pdf_path = os.path.join("reports", full_pdf_path)
                
                ticket_link = self.pm_tool.create_ticket(
                    title=f"Intake: {self.project_name}",
                    description=f"**Executive Summary:**\n{executive_summary}\n\n**Requester:** {self.user_name} ({self.vp_number})",
                    pdf_path=full_pdf_path
                )
            except Exception as e:
                print(f"PM Tool Error: {e}")
        
        if success:
            return (f"Interview complete. Report generated successfully: {filename}\n\n"
                    f"✅ **Ticket Created:** {ticket_link}\n\n"
                    f"Thank you. Someone from the Project Team will be in touch shortly.")
        return "Interview complete, but report generation failed."
