# 🏗️ Application Configuration Loader
# This file loads configuration from scale.yaml, enforcing the "Configuration as Code" principle.
# It includes a hard safety check for `audit.auto_apply` as mandated by the framework.
# Reference: agent.md - The System Kernel for AI behavior and rules.
# Reference: workflow/07_CONFIGURATION_CONTROL.md

import yaml
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from typing import List, Optional

# --- Pydantic Models for scale.yaml structure ---

class DeploymentConfig(BaseModel):
    tier: str
    environment: str
    risk_score: int

class ContextManagementConfig(BaseModel):
    max_history_messages: int
    truncation_strategy: str
    rag_top_k_results: int

class LLMConfig(BaseModel):
    provider: str
    model: str

class LLMDetailConfig(BaseModel):
    primary: LLMConfig
    specialist: LLMConfig
    cost_efficient: LLMConfig

class DatabaseConfig(BaseModel):
    type: str

class OrchestrationConfig(BaseModel):
    engine: str
    max_turns: int
    soft_limit_turns: int

class SecurityConfig(BaseModel):
    pii_redaction: bool
    pii_allow_list: List[str]

class CostControlsConfig(BaseModel):
    hard_limit_usd: float
    alert_threshold_usd: float

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
    This model is now fully type-safe.
    """
    deployment: DeploymentConfig
    context_management: ContextManagementConfig
    orchestration: OrchestrationConfig
    llm: LLMDetailConfig
    database: DatabaseConfig
    security: SecurityConfig
    cost_controls: CostControlsConfig
    audit: AuditConfig

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'

def load_config(path: str = "config/scale.yaml") -> AppConfig:
    """
    Loads the application configuration from the specified YAML file.
    """
    try:
        with open(path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        config = AppConfig(**config_data)

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
config = load_config()
