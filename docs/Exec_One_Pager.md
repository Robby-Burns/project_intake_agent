# 📊 Executive One-Pager: Project Intake Agent

**Project:** ProjectIntakeAgentThree
**Risk Score:** 8 (Medium)
**Status:** COMPLETE (v1.5.0)

---

## 🎯 The Problem
Project intake is currently a manual, inconsistent process. Critical questions about security, compliance, and ROI are often missed until late in the project lifecycle, causing delays and rework.

## 💡 The Solution
We have built an **AI-powered Project Intake Assistant** that standardizes this process. It acts as an always-available interviewer that:
1.  **Orchestrates 8 Specialist Agents** (IT, InfoSec, Risk, etc.) in real-time to analyze every project proposal.
2.  **Identifies Gaps Early** by "whispering" critical questions to the interviewer based on domain expertise (e.g., "Is this PII compliant?" or "Is this budgeted as CapEx?").
3.  **Generates Professional Documentation** including an Executive Summary, Key Findings, and a PDF report instantly.

## 🏗️ Architecture & Cost
*   **Architecture:** Modular Monolith (FastAPI + Streamlit + Postgres).
*   **Cost Control:** Uses a mix of `gpt-4o` (complex reasoning) and `gpt-4o-mini` (simple tasks) to optimize token costs.
*   **Safety:** Includes PII redaction (Regex + NLP) and Circuit Breakers to prevent runaway costs or data leaks.
*   **Audit:** Mandatory bi-annual reviews (March/Sept) ensure the system remains compliant and secure.

## 🛡️ Kill Switch & Maintenance
*   **Emergency Stop:** If the agent misbehaves, setting `RISK_SCORE=17` in `scale.yaml` triggers an immediate lockdown (stops all external API calls).
*   **Audit Schedule:** Automated compliance checks run every 6 months to verify dependencies and API contracts.
*   **Data Retention:** All interview data is stored securely in a dedicated PostgreSQL database with strict access controls.

## 🚀 ROI
*   **Time Savings:** Reduces initial project scoping from 2-3 meetings to a 15-minute chat.
*   **Risk Reduction:** Catches compliance/security issues at the *start* of the project, not during implementation.
*   **Consistency:** Every project gets the same rigorous 8-point analysis, regardless of who submits it.
