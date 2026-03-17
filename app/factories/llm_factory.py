# 🏭 Agnostic LLM Factory - Creates LLM provider instances.
# This factory implements the "Agnostic Factory" pattern, a core tenet of the framework,
# allowing the system to be decoupled from a specific LLM provider (e.g., OpenAI, Anthropic).
# Reference: agent.md - The System Kernel for AI behavior and rules.
# Reference: workflow/08_AGNOSTIC_FACTORIES.md

import os
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from app.config import config # <-- Use the global config object

class LLMFactory:
    """
    Factory to create LLM instances based on the global AppConfig.
    """

    @staticmethod
    def get_llm(model_type: str = "primary") -> BaseChatModel:
        """
        Creates and returns an LLM instance.
        
        Args:
            model_type: "primary", "specialist", or "cost_efficient"
        """
        
        if model_type == "specialist":
            llm_config = config.llm.specialist
        elif model_type == "cost_efficient":
            llm_config = config.llm.cost_efficient
        else:
            llm_config = config.llm.primary
            
        provider = llm_config.provider.lower()
        model_name = llm_config.model
        
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is not set.")
            return ChatOpenAI(model=model_name, temperature=0.7, api_key=api_key)
        
        elif provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")
            return ChatAnthropic(model=model_name, temperature=0.7, api_key=api_key)
            
        elif provider == "azure":
             raise NotImplementedError("Azure OpenAI provider is not yet fully implemented.")
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
