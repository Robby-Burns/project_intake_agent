# 🏗️ Technical Architecture: ProjectIntakeAgentThree (v1.5.0)

**Framework:** 10-Part AI Agent Framework (v1.5.0)
**Last Updated:** March 11, 2026
**Architecture Style:** Modular Monolith (FastAPI + Streamlit + Postgres)
**Orchestration:** Parallel Async ("The Whisper Engine")

---

## 🗺️ System Overview

The **Project Intake Agent** is an intelligent, multi-agent system designed to standardize project scoping. It uses a unique **"Whisper Engine"** architecture where 8 specialist agents analyze the conversation in real-time and guide the interviewer.

### High-Level Components

1.  **Frontend (UI):** Streamlit (`app/ui.py`)
    *   Handles user interaction and session state.
2.  **Backend (API):** FastAPI (`app/main.py`)
    *   Exposes Audit (`/audit/*`) and Health (`/health`) endpoints.
3.  **Orchestrator:** `app/orchestrator/orchestrator.py`
    *   Manages the conversation flow and agent execution. **Loads configuration on a per-session basis to enable hot-reloading.**
4.  **Database:** PostgreSQL (`docker-compose.yml`)
    *   Persists conversation history and metadata.
5.  **Factories:** `app/factories/`
    *   Abstracts LLMs, Databases, Storage, and PM Tools.

---

## ⚙️ Configuration: Hot-Reloading

A key feature of the architecture is **hot-reloading for configuration**.
*   The `config/scale.yaml` file is the single source of truth for application behavior (e.g., `max_turns`, LLM model names).
*   The `Orchestrator` calls `load_config()` upon initialization for every new user session.
*   **This means changes made to `scale.yaml` on disk are immediately reflected for any new user session without requiring a container restart**, enabling dynamic tuning in a running environment.

---

## 🏭 Agnostic Factory Pattern

The system is built on the **Agnostic Factory Pattern**, ensuring zero vendor lock-in.

*   **LLM Factory:** Swaps LLM providers (OpenAI, Anthropic) via `scale.yaml`.
*   **Database Factory:** Abstracts data persistence (Postgres/SQLite).
*   **Storage Factory:** Abstracts file storage (Local Disk, AWS S3, Azure Blob).
*   **PM Tool Factory:** Integrates with Jira, Monday.com, or Planner.

---

## 🗣️ The Whisper Engine (Orchestration)

The core logic resides in the `Orchestrator` class. It executes the following pipeline for every user message:

1.  **Guardrails (PII Redaction):** Input is sanitized.
2.  **State Machine:** Updates metadata (Project Name, etc.).
3.  **Parallel Execution:** Broadcasts the input to 8 Specialist Agents concurrently using `asyncio.gather`.
4.  **Whisper Ranking:** Collects and ranks "whispers" (suggested questions) from specialists.
5.  **Synthesis:** The **Interviewer Agent** formulates the next question for the user.
6.  **Persistence:** Saves the conversation turn to the database.

---

## 💾 Database Schema

**Table: `conversation_turns`**
*   `id`, `session_id`, `user_input`, `bot_response`, `timestamp`

**Table: `session_metadata`**
*   `session_id`, `metadata_json`, `updated_at`
