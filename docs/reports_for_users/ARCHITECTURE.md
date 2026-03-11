# 🏗️ Technical Architecture: ProjectIntakeAgentThree (v1.5.0)

**Framework:** 10-Part AI Agent Framework (v1.5.0)
**Last Updated:** March 8, 2026
**Architecture Style:** Modular Monolith (FastAPI + Streamlit + Postgres)
**Orchestration:** Parallel Async ("The Whisper Engine")

---

## 🗺️ System Overview

The **Project Intake Agent** is an intelligent, multi-agent system designed to standardize project scoping. It uses a unique **"Whisper Engine"** architecture where 8 specialist agents (IT, InfoSec, Risk, etc.) analyze the conversation in real-time and guide the interviewer.

### High-Level Components

1.  **Frontend (UI):** Streamlit (`app/ui.py`)
    *   Handles user interaction, session state management (via `session_id`), and PDF download.
2.  **Backend (API):** FastAPI (`app/main.py`)
    *   Exposes Audit (`/audit/*`) and Health (`/health`) endpoints.
    *   Runs alongside the UI in a Docker container.
3.  **Orchestrator:** `app/orchestrator/orchestrator.py`
    *   Manages the conversation flow, state machine, and parallel execution of specialist agents.
4.  **Database:** PostgreSQL (`docker-compose.yml`)
    *   Persists conversation history and metadata to prevent data loss.
5.  **Factories:** `app/factories/`
    *   Abstracts LLM providers, Database connections, and PM Tools.

---

## 🏭 Agnostic Factory Pattern (Core Innovation)

The system is built on the **Agnostic Factory Pattern**, ensuring zero vendor lock-in.

### 1. LLM Factory (`app/factories/llm_factory.py`)
*   **Purpose:** Allows swapping LLM providers (OpenAI, Anthropic, Azure) via configuration (`scale.yaml`).
*   **Logic:**
    ```python
    def get_llm(model_type="primary"):
        provider = config.llm.primary.provider
        if provider == "openai": return ChatOpenAI(...)
        if provider == "anthropic": return ChatAnthropic(...)
    ```

### 2. Database Factory (`app/factories/database_factory.py`)
*   **Purpose:** Abstracts data persistence.
*   **Implementations:** `PostgresAdapter` (Production), `SQLiteAdapter` (Local/Dev).

### 3. PM Tool Factory (`app/factories/pm_tool_factory.py`)
*   **Purpose:** Allows plug-and-play integration with project management tools.
*   **Supported Tools:** Jira, Monday.com, Microsoft Planner, Mock (Testing).

---

## 🗣️ The Whisper Engine (Orchestration)

The core logic resides in the `Orchestrator` class. It executes the following pipeline for every user message:

1.  **Guardrails (PII Redaction):** Input is sanitized using Regex + Presidio NLP.
2.  **State Machine:** Updates metadata (Project Name, VP Number) based on conversation state.
3.  **Parallel Execution:** Broadcasts the sanitized input to **8 Specialist Agents** concurrently using `asyncio.gather`.
    *   *IT Specialist* checks for technical debt.
    *   *InfoSec Specialist* checks for PII/Compliance risks.
    *   *ERM Specialist* checks for vendor risk.
    *   *(See Agent_Cards.md for full list)*
4.  **Whisper Ranking:** Collects "whispers" (suggested questions) from specialists, filters by relevance, and ranks by priority (1-10).
5.  **Synthesis:** The **Interviewer Agent** selects the highest-priority whisper and formulates the next question for the user.
6.  **Persistence:** Saves the conversation turn to the database.

---

## 💾 Database Schema

**Table: `conversation_turns`**
*   `id`: Integer (PK)
*   `session_id`: String (UUID)
*   `user_input`: Text
*   `bot_response`: Text
*   `timestamp`: DateTime

**Table: `session_metadata`**
*   `session_id`: String (PK)
*   `metadata_json`: Text (JSON blob storing project name, VP number, etc.)
*   `updated_at`: DateTime

---

## 🛡️ Security & Compliance

*   **Risk Score:** 8 (Medium).
*   **Circuit Breakers:** `tenacity` retry logic prevents cascading failures on external API calls.
*   **Audit System:** Mandatory bi-annual security audits via `POST /audit/run`.
*   **Least Privilege:** SharePoint integration uses scoped `Sites.Selected` permissions.

---

## 🚀 Deployment

The system is deployed as a single Docker container running both the Streamlit UI and the FastAPI Audit backend.

```yaml
version: '3.8'
services:
  api:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
  ui:
    build: .
    command: streamlit run app/ui.py
  db:
    image: postgres:15-alpine
```

See `DEPLOYMENT_M365.md` for detailed instructions.
