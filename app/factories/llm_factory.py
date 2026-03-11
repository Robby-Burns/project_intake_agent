# 🏭 Agnostic LLM Factory
# Reference: workflow/08_AGNOSTIC_FACTORIES.md

import os
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from app.config import config

class LLMFactory:
    """
    Factory to create LLM instances based on scale.yaml configuration.
    Allows swapping providers without changing business logic.
    """

    @staticmethod
    def get_llm(model_type: str = "primary") -> BaseChatModel:
        """
        Creates and returns an LLM instance.
        
        Args:
            model_type: "primary", "specialist", or "cost_efficient"
        """
        
        # 1. Resolve configuration based on requested type
        if model_type == "specialist":
            llm_config = config.llm.specialist
        elif model_type == "cost_efficient":
            llm_config = config.llm.cost_efficient
        else:
            llm_config = config.llm.primary
            
        provider = llm_config.provider.lower()
        model_name = llm_config.model
        
        # 2. Return the appropriate provider implementation
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is not set.")
                
            return ChatOpenAI(
                model=model_name,
                temperature=0.7, # Default temperature, can be parameterized if needed
                api_key=api_key
            )
        
        elif provider == "anthropic":
            # Lazy import to avoid dependency if not used
            from langchain_anthropic import ChatAnthropic
            
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")
                
            return ChatAnthropic(
                model=model_name,
                temperature=0.7,
                api_key=api_key
            )
            
        elif provider == "azure":
             # Placeholder for Azure OpenAI implementation
             # from langchain_openai import AzureChatOpenAI
             raise NotImplementedError("Azure OpenAI provider is not yet fully implemented.")

        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
