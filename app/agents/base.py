# 🤖 Base Agent - The foundational blueprint for all agents in the system.
# This file enforces the "Worst-Case Coding Standard" by including tenacity for retries
# and the "Citation Law" by using the Agnostic LLM Factory.
# Reference: agent.md - The System Kernel for AI behavior and rules.

from abc import ABC, abstractmethod
from typing import Any, Optional, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from tenacity import retry, stop_after_attempt, wait_exponential
from app.factories.llm_factory import LLMFactory

class BaseAgent(ABC):
    """
    Abstract Base Class for all agents.
    Handles LLM initialization via the LLMFactory and adds retry logic.
    Reference: workflow/08_AGNOSTIC_FACTORIES.md
    Reference: workflow/02_COMPLETE_GUIDE.md (Section 5: Circuit Breakers)
    """
    
    def __init__(self, name: str, role: str, model_type: str = "primary"):
        self.name = name
        self.role = role
        self.model_type = model_type
        # Use the factory to get the LLM instance based on configuration
        self.llm = LLMFactory.get_llm(model_type)

    @abstractmethod
    async def run(self, input_data: Any) -> Any:
        """
        Main execution method for the agent.
        Must be implemented by subclasses.
        """
        pass

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True # Reraise the last exception if all retries fail
    )
    async def _invoke_chain(self, chain, input_data: Dict[str, Any]):
        """
        Helper to invoke a chain with retry logic (Circuit Breaker).
        """
        return await chain.ainvoke(input_data)

    def _create_chain(self, prompt_template: ChatPromptTemplate, output_parser: Optional[PydanticOutputParser] = None):
        """
        Helper to create a LangChain chain.
        """
        if output_parser:
            return prompt_template | self.llm | output_parser
        return prompt_template | self.llm
