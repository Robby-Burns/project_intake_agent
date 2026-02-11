from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel

class BaseAgent(ABC):
    """
    Abstract Base Class for all agents.
    Handles LLM initialization and common logic.
    """
    
    def __init__(self, name: str, role: str, model: str = "gpt-4o"):
        self.name = name
        self.role = role
        self.model_name = model
        self.llm = ChatOpenAI(
            model=model,
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    @abstractmethod
    async def run(self, input_data: Any) -> Any:
        """
        Main execution method for the agent.
        Must be implemented by subclasses.
        """
        pass

    def _create_chain(self, prompt_template: ChatPromptTemplate, output_parser: Optional[PydanticOutputParser] = None):
        """
        Helper to create a LangChain chain.
        """
        if output_parser:
            return prompt_template | self.llm | output_parser
        return prompt_template | self.llm
