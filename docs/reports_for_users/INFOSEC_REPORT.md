# 🛡️ InfoSec Report: ProjectIntakeAgentThree (v1.5.0)

**To:** Information Security Officer (ISO) / Head of Security
**From:** The Collective (Project Intake Team)
**Date:** March 8, 2026
**Subject:** Security Posture, Risk Analysis, and Compliance for v1.5.0

---

## 🎯 Executive Summary

**ProjectIntakeAgentThree** (v1.5.0) has been re-architected to meet a **Risk Score of 8 (Medium)**, aligning with the 10-Part AI Agent Framework.

This report confirms the implementation of key security controls, including:
*   **Hybrid PII Redaction:** Regex + NLP (Presidio) filtering.
*   **Circuit Breakers:** `tenacity` retry logic on all external API calls.
*   **Agnostic Factories:** Eliminates vendor lock-in and associated supply chain risks.
*   **Mandatory Audit System:** Automated bi-annual security scans with human sign-off.

---

## 📊 Risk Score Analysis (Score: 8 - Medium)

*   **Input Risk (4/5):** User input is open-ended, allowing for potential prompt injection.
*   **Output Risk (2/5):** The agent generates reports and questions, but does not execute financial transactions.
*   **Data Risk (2/4):** Handles project metadata, which may be sensitive but is not PII by default.
*   **Model Risk (0/3):** The agent uses reasoning but does not have access to external tools that could be exploited.

**Conclusion:** A Medium risk score is appropriate. The system requires robust guardrails but not full Human-in-the-Loop (HITL) for every action.

---

## 🛡️ Implemented Security Controls

### 1. PII Redaction (`app/guardrails/pii_filter.py`)
*   **Mechanism:** A hybrid approach combining Regex (for strict patterns like SSN) and NLP (Microsoft Presidio) for context-aware redaction (like names).
*   **Process:** All user input is sanitized *before* being sent to the LLM.
*   **Configuration:** The `pii_allow_list` in `config/scale.yaml` allows us to selectively permit certain entities (e.g., `PERSON` for the user's name) while blocking others.

### 2. Circuit Breakers (`app/agents/base.py`)
*   **Mechanism:** The `@retry` decorator from the `tenacity` library is applied to all LLM calls.
*   **Behavior:** If an API call fails, it will retry up to 3 times with exponential backoff. This prevents cascading failures and reduces the risk of denial-of-service from rapid retries.

### 3. Agnostic Factories (`app/factories/`)
*   **Security Benefit:** By abstracting LLM providers, we can quickly pivot away from a vendor if a major security vulnerability is discovered in their API or models. This reduces supply chain risk.

### 4. Mandatory Audit System (`app/main.py`)
*   **Frequency:** Bi-annual (March & September) + Weekly CVE scans.
*   **Process:** Automated scans check for outdated dependencies, known vulnerabilities, and deprecated API contracts.
*   **Human Sign-Off:** **No changes are ever auto-applied.** A human reviewer must approve all proposed updates, preventing silent introduction of new risks.

---

## 🔒 Data Flow & Persistence

1.  **Input:** User provides input via Streamlit UI.
2.  **Redaction:** `PIIFilter` removes sensitive data.
3.  **Processing:** Sanitized input is sent to the LLM.
4.  **Storage:** Conversation history and metadata are stored in a **PostgreSQL** database.
    *   **Encryption:** Data at rest is encrypted (handled by the cloud provider's database service).
    *   **Access:** The database is firewalled and only accessible by the application container.

---

## 🚨 Incident Response & Kill Switch

*   **Incident:** If a security incident is detected (e.g., data leak from a dependency).
*   **Kill Switch:**
    1.  **Edit `config/scale.yaml`:** Set `risk_score: 17`.
    2.  **Redeploy/Restart:** The application will enter "Emergency Mode," blocking all outbound API calls.
*   **Logging:** All application logs are sent to stdout/stderr for collection by a log aggregator (e.g., Datadog, Splunk).

---

**Conclusion:** The system's security posture is appropriate for its Medium risk score. The combination of proactive redaction, resilient architecture, and a mandatory audit schedule provides a strong defense against common AI-related threats.
