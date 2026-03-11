# 🏭 Agnostic Factories - The "Tech Radar" Integration Pipeline

**Version:** 1.5.0 | **Updated:** March 8, 2026 | **Part:** 9/10  
**Status:** Production Ready ✅  
**Purpose:** How to safely integrate new tools discovered by the Tech Radar without rewriting your agent's core logic.

---

## 📍 Purpose

This file is the **bridge** between the "Tech Radar" (File 04) and your Codebase.

**The Problem:** The Tech Radar finds a cool new library (e.g., `pypdf-turbo`), but if you `import pypdf_turbo` directly in your agent, you are "vendor-locked" to that specific library. If it breaks next week, you have to rewrite the agent.

**The Solution:**
1. **Discover** via Tech Radar (or bi-annual audit).
2. **Encapsulate** via Adapter.
3. **Inject** via Factory.

**Core Pattern:** "One interface, many implementations. Pick at runtime."

---

## 🗺️ Quick Navigation

- [The Tech Radar Pipeline](#-the-tech-radar-pipeline-mandatory)
- [The Database Factory](#-the-database-factory)
- [The LLM Factory](#-the-llm-factory)
- [The Orchestrator Factory](#-the-orchestrator-factory)
- [The Notifier Factory](#-the-notifier-factory)
- [Best Practices](#-best-practices)

---

## 📡 The Tech Radar Pipeline (Mandatory)

This is the standard workflow for adding **ANY** new dependency to the project.

### Step 0: Scheduled Discovery (The Bi-Annual Audit)
The Tech Radar fires when you think to run it. The bi-annual audit fires whether you remember or not. Think of it as the proactive, scheduled version of Step 1. It scans `pyproject.toml`, API changelogs, and the framework guides on a fixed calendar. Anything it finds enters this same pipeline: assess → interface → adapter → factory. The audit doesn't replace the Tech Radar — it ensures the Tech Radar runs at minimum twice a year even on mature, stable projects you've stopped actively thinking about. See `09_AUDIT_AND_MAINTENANCE.md` for the full audit procedure.

### Step 1: Discovery (Tech Radar)
The AI assistant runs the `tech-radar-skill` and determines that `pypdf-turbo` is faster than `pypdf2`.

### Step 2: Define the Interface (Contract)
Create a generic interface that defines *what* we need, not *how* it's done.

```python
# app/interfaces/document_loader.py
from abc import ABC, abstractmethod

class DocumentLoader(ABC):
    @abstractmethod
    def load(self, file_path: str) -> str:
        """Loads text from a file. Must return strict string or raise Error."""
        pass
```

### Step 3: Create the Adapter (Encapsulation)
Wrap the specific library. If the library changes, only this file changes.

```python
# app/adapters/pdf_turbo_adapter.py
from app.interfaces.document_loader import DocumentLoader
import pypdf_turbo  # <--- The ONLY place this is imported

class PyPDFTurboAdapter(DocumentLoader):
    def load(self, file_path: str) -> str:
        try:
            return pypdf_turbo.extract_text(file_path)
        except Exception as e:
            # Standardize error handling (No Happy Paths)
            raise ValueError(f"PDF Turbo failed: {e}")
```

### Step 4: The Factory (Injection)
Update the factory to allow swapping between the old way and the new way via config.

```python
# app/factories/loader_factory.py
import os
from app.interfaces.document_loader import DocumentLoader

def get_document_loader() -> DocumentLoader:
    mode = os.getenv("PDF_ENGINE", "standard").lower()
    
    if mode == "turbo":
        from app.adapters.pdf_turbo_adapter import PyPDFTurboAdapter
        return PyPDFTurboAdapter()
    
    from app.adapters.standard_pdf_adapter import StandardPDFAdapter
    return StandardPDFAdapter()
```

### Step 5: Promote to Skill (When Patterns Repeat)
If you've gone through Steps 1-4 three or more times for similar tools (e.g., three different document loaders, three different notification adapters), the interface → adapter → factory pipeline itself should be extracted into a **reusable skill**.

The `/new-skill` prompt pattern in `04_AI_ASSISTANT_INTEGRATION.md` handles this. The skill automates the boilerplate: given a service name and method signature, it generates the interface, adapter stub, factory entry, and test file.

**Rule of thumb:** If the AI is copying-and-pasting factory structure from one adapter to create another, it's time for a skill. The AI should propose this during Phase 5 of the agent.md loop.

---

## 🏗️ The Database Factory

Never hardcode `psycopg2` or `qdrant_client` in your business logic.

```python
def get_database_adapter() -> DatabaseAdapter:
    """Creates the database connection based on environment settings."""
    db_type = os.getenv("DATABASE_TYPE", "postgresql").lower()
    
    if db_type == "qdrant":
        return QdrantAdapter() # Vector DB for RAG
    
    # Default to Postgres for state management
    return PostgresAdapter()   
```

---

## 🤖 The LLM Factory

Switch providers (Anthropic, OpenAI, Google) by changing a single line in `scale.yaml`.

```python
def get_llm_provider(model_type: str = "primary") -> LLMProvider:
    """Fetches the provider configured in scale.yaml."""
    provider = os.getenv("LLM_PROVIDER", "anthropic").lower()
    
    if provider == "openai":
        return OpenAILLM()
    elif provider == "google":
        return GoogleGeminiLLM()
    elif provider == "local":
        return OllamaLLM() # Great for free local testing
        
    return ClaudeLLM()
```

---

## 🎼 The Orchestrator Factory

Multi-agent orchestration frameworks change constantly. This factory isolates your business logic from the routing engine.

```python
def get_orchestrator() -> AgentOrchestrator:
    """Creates the router based on scale.yaml/env settings."""
    engine = os.getenv("ORCHESTRATION_ENGINE", "langgraph").lower()
    
    if engine == "langgraph":
        from app.adapters.langgraph_orchestrator import LangGraphOrchestrator
        return LangGraphOrchestrator()
    elif engine == "crewai":
        from app.adapters.crew_orchestrator import CrewOrchestrator
        return CrewOrchestrator()
    
    # Default: Simple linear execution for debugging
    from app.adapters.simple_orchestrator import SimpleAsyncOrchestrator
    return SimpleAsyncOrchestrator()
```

---

## 📢 The Notifier Factory

Configurable audit notification channel. Used by the bi-annual audit system to tell the human their report is ready. Notification contains a link only — never report content (security requirement).

```python
# app/factories/notifier_factory.py
import os

def get_notifier() -> AuditNotifier:
    """Returns the configured audit notification adapter.
    Channel set in scale.yaml → audit.notification_channel.
    Credentials in .env. Notification contains link only — never report content.
    """
    channel = os.getenv("AUDIT_NOTIFICATION_CHANNEL", "none").lower()

    if channel == "slack":
        from app.adapters.slack_notifier import SlackNotifier
        return SlackNotifier()
    elif channel == "email":
        from app.adapters.email_notifier import EmailNotifier
        return EmailNotifier()
    elif channel == "teams":
        from app.adapters.teams_notifier import TeamsNotifier
        return TeamsNotifier()
    elif channel == "webhook":
        from app.adapters.webhook_notifier import WebhookNotifier
        return WebhookNotifier()

    # Default: no notification. Report generated, dashboard badge set.
    from app.adapters.null_notifier import NullNotifier
    return NullNotifier()
```

---

## 💡 Best Practices

- **Lazy Imports:** Notice the imports are inside the `if` statements. This prevents loading heavy libraries (like `langgraph` or `torch`) if you aren't using them.
- **Standardized State:** Every orchestrator adapter must accept and return a standard `State` dictionary.
- **The "Local" Fallback:** Always provide a simple or local implementation that runs without API keys or complex dependencies. This allows for rapid unit testing.
- **The "None" Fallback:** For optional services like notifications, always provide a null/no-op implementation so the system doesn't crash when the service isn't configured.

---

## 📌 File Meta

**Version:** 1.5.0  
**Released:** March 8, 2026  
**Status:** Production Ready ✅  
**Part of:** 10-Part AI Agent Framework  

**Next File:** [09_AUDIT_AND_MAINTENANCE.md](./09_AUDIT_AND_MAINTENANCE.md) (Audit & Maintenance)
