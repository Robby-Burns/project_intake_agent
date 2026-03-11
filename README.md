# 🤖 Project Intake Agent (v1.5.0)

An intelligent, multi-agent system for automating Credit Union project intake. It uses a "Whisper Engine" architecture where 8 specialist agents analyze the conversation in real-time and guide the interviewer.

![Status](https://img.shields.io/badge/Status-Complete-green)
![Risk Level](https://img.shields.io/badge/Risk%20Level-Medium%20(8)-yellow)
![Framework](https://img.shields.io/badge/Framework-1.5.0-blue)

---

## 🚀 Features

*   **Parallel Orchestrator:** Runs 8 specialist agents (IT, InfoSec, ERM, etc.) concurrently.
*   **Agnostic Architecture:** Swap LLMs (OpenAI/Anthropic), Databases (Postgres/SQLite), and PM Tools via config (`scale.yaml`).
*   **State Persistence:** Conversation history and metadata are saved to a database, ensuring no data loss on reload.
*   **Audit System:** Mandatory bi-annual audit endpoints (`/audit/*`) for compliance and maintenance.
*   **Hybrid Security:** Circuit Breakers + PII Redaction (Regex + NLP).
*   **Professional Reporting:** Generates a PDF with Executive Summary, Key Findings, and Domain Analysis.
*   **Streamlit UI:** User-friendly chat interface with persistent session state.

---

## 🛠️ Installation

### Prerequisites
*   Python 3.12+
*   Docker & Docker Compose
*   `uv` (recommended for local dev)

### 1. Clone & Configure
```bash
git clone https://github.com/your-org/ProjectIntakeAgentThree.git
cd ProjectIntakeAgentThree

# Create .env from example
cp .env.example .env
```

**Key Variables (.env):**
*   `OPENAI_API_KEY`: Your LLM key.
*   `DATABASE_URL`: Connection string for Postgres (default provided in docker-compose).
*   `PM_TOOL_TYPE`: `jira`, `monday`, `planner`, or `mock`.

### 2. Run with Docker (Recommended)
This starts the API (Audit System), UI (Streamlit), and Database (Postgres).

```bash
docker-compose up --build
```

Access the app at `http://localhost:8501`.

### 3. Local Development (with `uv`)
```bash
# Install dependencies
uv sync

# Run the API (Audit/Health)
uv run uvicorn app.main:app --reload

# Run the UI (Streamlit)
uv run streamlit run app/ui.py
```

---

## 🏗️ Architecture

**The Whisper Engine:**
1.  **User Input** -> **Guardrails** (PII Redaction)
2.  **Orchestrator** -> **Database** (Save State)
3.  **Orchestrator** -> Broadcasts to **8 Specialists** (Async Parallel)
4.  **Specialists** -> Analyze & Whisper Questions (Priority 1-10)
5.  **Interviewer** -> Synthesizes best question -> **User**

**Components:**
*   **Factories:** `LLMFactory`, `DatabaseFactory`, `PMToolFactory` (prevents vendor lock-in).
*   **Adapters:** `PostgresAdapter`, `JiraAdapter`, etc.
*   **Audit API:** FastAPI endpoints for scheduled maintenance checks.

---

## 🛡️ Security & Compliance

*   **Risk Score:** 8 (Medium). Requires Circuit Breakers and PII Redaction.
*   **Audit Schedule:** Bi-annual audits (March & September) triggered via `POST /audit/run`.
*   **CVE Scanning:** Weekly vulnerability checks via `POST /audit/cve-check`.
*   **PII Redaction:** Configurable allow-list in `scale.yaml`.

---

## 📚 Documentation

Detailed documentation is available in the `docs/` folder:
*   [Agent Cards](docs/Agent_Cards.md) - Roster of the 8 specialist agents.
*   [Executive One-Pager](docs/Exec_One_Pager.md) - High-level summary for stakeholders.
*   [Maintenance Handoff](docs/System_Maintenance_Handoff.md) - Critical info for the client.

---

## 🧪 Testing

Run the test suite (including LLM-as-a-judge evals):

```bash
# Run all tests
pytest

# Run only evals
pytest tests/test_evals.py
```
