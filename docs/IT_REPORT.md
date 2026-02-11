# 🏗️ Operationalizing AI: A Controlled, Modular Architecture for Project Intake

**To:** VP of Information Technology  
**From:** [Your Name/Team]  
**Date:** February 2026  
**Subject:** Deployment Proposal for AI-Assisted Project Intake System

---

## 1. Executive Summary

We are seeking approval to deploy the **Project Intake Agent**, a system designed to solve the "Garbage In, Garbage Out" problem in our project pipeline.

We understand the risks associated with AI adoption. This system is **not** a "black box" chatbot. It is a **deterministic state machine** that utilizes LLMs strictly as processing engines within a controlled, modular architecture.

The goal is operational efficiency: converting vague user requests into **structured, standardized requirements** (PDFs & Tickets) before they ever reach an IT Analyst's desk.

---

## 2. Architecture: Built for Control & Maintainability

The system follows a **Parallel Orchestrator Pattern** ("The Whisper Engine"). This design prioritizes modularity and isolation over monolithic AI complexity.

### 🔧 Key Architectural Decisions

1.  **Stateless & Ephemeral**
    *   **Design:** The system does not retain long-term memory of user conversations. Every session is fresh.
    *   **Benefit:** Eliminates the risk of "data poisoning" or leaking context between different users.

2.  **The "Orchestrator" (State Machine)**
    *   **Control:** The AI does not control the flow; a Python-based State Machine does.
    *   **Logic:** It enforces strict steps (`GET_NAME` -> `GET_PROJECT` -> `INTERVIEW` -> `REPORT`). The AI cannot "hallucinate" its way out of this process.

3.  **Adapter Pattern for Integrations**
    *   **Flexibility:** We built a plug-and-play Adapter layer for PM tools.
    *   **Current State:** Supports **Monday.com** (via GraphQL) and **Jira** (via REST).
    *   **Future Proof:** Switching tools requires changing *one* environment variable, not rewriting code.

---

## 3. Deployment & Infrastructure

We have prioritized a "Cloud-Native" but "Infrastructure-Agnostic" approach.

*   **Containerization:** The entire application is packaged in a single **Docker** container.
    *   *Base Image:* Python 3.11 Slim (Minimal attack surface).
    *   *Dependency Mgmt:* Uses `uv` for fast, reproducible builds.
*   **Environment Config:** All secrets (API Keys, Board IDs) are managed via standard `.env` injection. **No hardcoded credentials.**
*   **Hosting:** Can run on any standard container platform (Azure Container Apps, AWS ECS, or On-Prem Kubernetes).

---

## 4. Addressing AI Risk (The "Safety Layer")

We know AI can be unpredictable. We have wrapped the LLM in a **Hybrid Guardrail System** that runs locally on our server, *before* data leaves our perimeter.

1.  **PII Redaction (Regex + NLP):** We strip SSNs, Member IDs, and Names before the LLM sees them.
2.  **Strict Personas:** The agents are grounded in specific frameworks (e.g., **TOGAF** for IT, **NIST** for Security). They are instructed to ask specific, technical questions, not to chat casually.
3.  **Human-in-the-Loop:** The AI *never* executes code or changes database records. It only generates a **Draft Report** for human review.

---

## 5. The Business Value (ROI)

Currently, IT Analysts spend hours chasing stakeholders for basic requirements ("Is this cloud or on-prem?", "Who is the vendor?").

**This system automates that discovery phase.**

*   **Standardized Output:** Every project request results in a formatted **PDF Report** attached to a **Monday/Jira Ticket**.
*   **Technical Pre-Screening:** The "IT Specialist Agent" asks about integrations and architecture *during the intake*, so the ticket arrives with technical context already captured.

## 6. Recommendation

We recommend a **Pilot Deployment** to an internal user group. The architecture is stable, secure, and designed to be a low-maintenance utility for the IT department.
