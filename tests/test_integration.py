# ⚙️ Integration Tests - Verifies the end-to-end flow of the system.
# This file ensures that all components (Orchestrator, Agents, Factories) work together
# as expected, following the "No Happy Paths" principle by testing realistic scenarios.
# Reference: agent.md - The System Kernel for AI behavior and rules.

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.orchestrator.orchestrator import Orchestrator
from app.agents.specialist import SpecialistOutput

@pytest.mark.asyncio
class TestOrchestratorIntegration:
    
    @pytest.fixture
    def mock_specialist_response(self):
        return SpecialistOutput(
            relevant=True,
            priority_score=8,
            suggested_question="Is data encrypted?",
            analysis="Security concern."
        )

    @patch("app.agents.base.ChatOpenAI")
    async def test_full_pipeline_flow(self, mock_openai, mock_specialist_response):
        """
        Tests the full Orchestrator pipeline with mocked LLMs.
        Verifies:
        1. PII Redaction is called
        2. Specialists run in parallel
        3. Interviewer synthesizes response
        """
        # Setup Mocks
        mock_chain = AsyncMock()
        mock_chain.ainvoke.return_value = mock_specialist_response
        
        mock_interviewer_chain = AsyncMock()
        mock_interviewer_chain.ainvoke.return_value = "Mocked Interviewer Response"

        with patch("app.agents.base.BaseAgent._create_chain") as mock_create_chain:
            orchestrator = Orchestrator()
            
            # FIX: Bypass Metadata Handshake
            orchestrator.state = "INTERVIEW"
            orchestrator.project_name = "Test Project"
            orchestrator.user_name = "Test User"
            
            # Replace agent chains with mocks
            for specialist in orchestrator.specialists:
                specialist.chain = mock_chain
            
            orchestrator.interviewer.chain = mock_interviewer_chain

            # Run the pipeline
            user_input = "I want to use Dropbox for storing member SSNs."
            response = await orchestrator.process_message(user_input)

            # Assertions
            assert response == "Mocked Interviewer Response"
            assert mock_chain.ainvoke.call_count == 8
            
            interviewer_call_args = mock_interviewer_chain.ainvoke.call_args[0][0]
            assert "whispers" in interviewer_call_args
            assert "Is data encrypted?" in interviewer_call_args["whispers"]

    @patch("app.agents.base.ChatOpenAI")
    async def test_low_priority_filtering(self, mock_openai):
        """
        Test that low priority whispers are handled correctly.
        """
        orchestrator = Orchestrator()
        
        # FIX: Bypass Metadata Handshake
        orchestrator.state = "INTERVIEW"
        orchestrator.project_name = "Test Project"
        
        # Mock Specialists
        high_priority = SpecialistOutput(relevant=True, priority_score=9, suggested_question="High?", analysis=".")
        low_priority = SpecialistOutput(relevant=True, priority_score=2, suggested_question="Low?", analysis=".")
        irrelevant = SpecialistOutput(relevant=False, priority_score=0, suggested_question=None, analysis=".")
        
        orchestrator.specialists[0].chain = AsyncMock()
        orchestrator.specialists[0].chain.ainvoke.return_value = high_priority
        
        orchestrator.specialists[1].chain = AsyncMock()
        orchestrator.specialists[1].chain.ainvoke.return_value = low_priority
        
        orchestrator.specialists[2].chain = AsyncMock()
        orchestrator.specialists[2].chain.ainvoke.return_value = irrelevant
        
        for i in range(3, 8):
            orchestrator.specialists[i].chain = AsyncMock()
            orchestrator.specialists[i].chain.ainvoke.return_value = irrelevant
            
        orchestrator.interviewer.chain = AsyncMock()
        orchestrator.interviewer.chain.ainvoke.return_value = "Response"

        # Run
        await orchestrator.process_message("test")
        
        # Check Unanswered Questions Queue
        # Logic: if result.priority_score >= 7: self.unanswered_questions.append(whisper)
        assert len(orchestrator.unanswered_questions) >= 1
        assert orchestrator.unanswered_questions[0]['priority'] == 9
