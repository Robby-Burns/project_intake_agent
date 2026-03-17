# 🤖 Project Intake Agent (v1.5.0)

An intelligent, multi-agent system for automating Credit Union project intake. It uses a "Whisper Engine" architecture where 8 specialist agents analyze the conversation in real-time and guide the interviewer.

![Status](https://img.shields.io/badge/Status-Ready%20for%20Launch-green)
![Risk Level](https://img.shields.io/badge/Risk%20Level-Medium%20(8)-yellow)
![Framework](https://img.shields.io/badge/Framework-1.5.0-blue)

---

## 🚀 Features

*   **Parallel Orchestrator:** Runs 8 specialist agents (IT, InfoSec, ERM, etc.) concurrently.
*   **Agnostic Architecture:** Swap LLMs, Databases, and Storage via config (`scale.yaml`).
*   **Hot-Reloading Config:** Changes to `scale.yaml` are applied to new sessions without a server restart.
*   **State Persistence:** Conversation history is saved to a database, ensuring no data loss.
*   **Audit System:** Mandatory bi-annual audit endpoints for compliance and maintenance.
*   **Hybrid Security:** Circuit Breakers + PII Redaction.
*   **Professional Reporting:** Generates a PDF and creates tickets in Jira, Monday.com, or Planner.

---

## 🛠️ Installation

### Prerequisites
*   Python 3.12+
*   Docker & Docker Compose
*   An OpenAI API Key (or other supported LLM provider)

### 1. Clone & Configure
```bash
git clone https://github.com/Robby-Burns/project_intake_agent.git
cd project_intake_agent

# Create .env from the example file
cp .env.example .env
```
Open the new `.env` file and add your `OPENAI_API_KEY`.

### 2. Run with Docker (Recommended)
This starts the API (Audit System), UI (Streamlit), and Database (Postgres).

```bash
docker-compose up --build
```

Access the app at `http://localhost:8501`.

---

## 🏗️ Architecture

The system uses a **"Modular Monolith"** design running in Docker.
*   **UI Service:** Streamlit frontend.
*   **API Service:** FastAPI backend for health checks and the Audit System.
*   **DB Service:** PostgreSQL database for state persistence.

The core logic is built on **Agnostic Factories** to prevent vendor lock-in and a **hot-reloading configuration** (`scale.yaml`) for dynamic tuning.

---

## 📚 Documentation

Detailed documentation is available in the `docs/` folder:
*   [Agent Cards](docs/Agent_Cards.md) - Roster of the 8 specialist agents.
*   [Executive One-Pager](docs/Exec_One_Pager.md) - High-level summary for stakeholders.
*   [IT VP Report](docs/reports_for_users/IT_VP_REPORT.md) - Technical overview for IT leadership.
*   [Maintenance Handoff](docs/System_Maintenance_Handoff.md) - Critical info for the client/ops team.

---

## 🧪 Testing

Run the test suite (including LLM-as-a-judge evals):

```bash
pytest
```
