# 🏗️ Application Configuration Loader
# Reference: workflow/07_CONFIGURATION_CONTROL.md
import yaml
from pydantic_settings import BaseSettings
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# --- Pydantic Models for scale.yaml structure ---

class LLMConfig(BaseModel):
    provider: str
    model: str

class LLMDetailConfig(BaseModel):
    primary: LLMConfig
    specialist: LLMConfig
    cost_efficient: LLMConfig

class DatabaseConfig(BaseModel):
    type: str

class AuditConfig(BaseModel):
    schedule_months: List[int]
    schedule_day: str
    schedule_time: str
    schedule_timezone: str
    notification_channel: str
    notification_link: str
    auto_apply: bool
    cve_check_weekly: bool

class AppConfig(BaseSettings):
    """
    Loads configuration from scale.yaml and environment variables.
    """
    deployment: dict
    context_management: dict
    orchestration: dict
    llm: LLMDetailConfig
    database: DatabaseConfig
    security: dict
    cost_controls: dict
    audit: AuditConfig

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        # FIX: Tell Pydantic to ignore extra variables from the .env file
        # that are not defined in this model.
        extra = 'ignore'

def load_config(path: str = "config/scale.yaml") -> AppConfig:
    """
    Loads the application configuration from the specified YAML file.
    """
    try:
        with open(path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        config = AppConfig(**config_data)

        # Hard safety check: auto_apply must never be True
        if config.audit.auto_apply:
            raise ValueError(
                "FATAL: audit.auto_apply is True in scale.yaml. "
                "This is forbidden. Human sign-off is mandatory."
            )
        
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at {path}. Please ensure 'config/scale.yaml' exists.")
    except Exception as e:
        raise ValueError(f"Error loading or validating configuration: {e}")

# --- Global Config Instance ---
# Load the configuration once when the module is imported
# This ensures it's available to all other modules.
config = load_config()
