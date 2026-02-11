# 🤖 Project Intake Agent (ProjectIntakeAgentTwo)

An intelligent, multi-agent system for automating Credit Union project intake. It uses a "Whisper Engine" architecture where 8 specialist agents analyze the conversation in real-time and guide the interviewer.

![Status](https://img.shields.io/badge/Status-Complete-green)
![Risk Level](https://img.shields.io/badge/Risk%20Level-Medium%20(8)-yellow)

---

## 🚀 Features

*   **Parallel Orchestrator:** Runs 8 specialist agents (IT, InfoSec, ERM, etc.) concurrently.
*   **Framework-Aligned Agents:** Specialists use industry standards (PMI, NIST, TOGAF, COSO).
*   **Hybrid Security:** Combines Regex + Microsoft Presidio (NLP) for robust PII redaction.
*   **Professional Reporting:** Generates a PDF with Executive Summary, Key Findings, and Domain Analysis.
*   **PM Tool Integration:** Automatically creates tickets in **Monday.com** or **Jira** with PDF attachment.
*   **Streamlit UI:** User-friendly chat interface.

---

## 🛠️ Installation

### Prerequisites
*   Python 3.11+
*   OpenAI API Key
*   Monday.com API Key (Optional)

### 1. Clone & Install
```bash
# Install dependencies
pip install -r requirements.txt

# Download NLP Model (Small for local dev)
python -m spacy download en_core_web_sm
```

### 2. Configuration
Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

**Key Variables:**
*   `OPENAI_API_KEY`: Your LLM key.
*   `PM_TOOL`: Set to `monday`, `jira`, or `mock`.
*   `MONDAY_FILES_COLUMN_ID`: The ID of your files column (default: `file`).
*   `SPACY_MODEL`: `en_core_web_sm` (Local) or `en_core_web_lg` (Prod).

---

## ▶️ Running the App

```bash
python -m streamlit run app/ui.py
```

The app will open in your browser at `http://localhost:8501`.

**Note:** Generated reports are saved in the `reports/` directory.

---

## 🧪 Testing

Run the test suite to verify security and logic:

```bash
pytest
```

---

## 🐳 Docker Deployment

Build and run the container:

```bash
docker-compose up --build
```

**Note:** The Dockerfile defaults to the **Large** Spacy model (`en_core_web_lg`) for production accuracy. If building locally with limited space, edit `docker-compose.yml` to use `en_core_web_sm`.

---

## 🏗️ Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the detailed design.

**The Whisper Engine:**
1.  **User Input** -> **Guardrails** (PII Redaction)
2.  **Orchestrator** -> Broadcasts to **8 Specialists** (Async)
3.  **Specialists** -> Analyze & Whisper Questions (Priority 1-10)
4.  **Interviewer** -> Synthesizes best question -> **User**

---

## 🛡️ Security

See [docs/GUARDRAILS.md](docs/GUARDRAILS.md).

*   **PII Redaction:** SSN, Credit Cards, Member IDs, Names.
*   **Stateless:** No data leakage between sessions.
*   **Validation:** Strict VP Number format (`VP-\d{3}`).
