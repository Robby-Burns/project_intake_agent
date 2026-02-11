# 🛡️ Automated Security Governance: The AI-Driven Project Intake System

**To:** VP of Information Security  
**From:** [Your Name/Team]  
**Date:** February 2026  
**Subject:** Reducing "Shadow IT" Risk via Automated Security Screening

---

## 1. Executive Summary

We have deployed a new **AI-Driven Project Intake Agent** designed to solve a critical governance gap: **projects starting without early security visibility.**

Traditionally, InfoSec is engaged too late in the project lifecycle, often after vendors are selected or architecture is defined. This leads to costly rework, compliance delays, or "Shadow IT" risks.

The new system acts as a **24/7 Security Gatekeeper**. It conducts an intelligent interview with project requesters, using a dedicated **InfoSec Specialist Agent** trained on the **NIST Cybersecurity Framework** to identify risks immediately.

Crucially, the system itself is built with a **"Security First" architecture**, featuring enterprise-grade PII redaction to ensure no Member Data is exposed to the AI model.

---

## 2. The "Whisper Engine" Architecture

The system utilizes a **Parallel Orchestrator** pattern. While the user chats with a friendly "Interviewer," 8 specialist agents analyze every message in real-time.

### The InfoSec Specialist Agent
Unlike a standard chatbot, our InfoSec Agent is explicitly instructed to apply the **NIST Cybersecurity Framework (Identify, Protect, Detect, Respond, Recover)** and **GLBA compliance standards**.

**How it works:**
1.  **User says:** "We want to use Dropbox for marketing photos."
2.  **InfoSec Agent flags:** *Cloud Storage + Potential PII Risk.*
3.  **Agent Whispers:** "Ask if the data is encrypted at rest and if they have verified the vendor's SOC 2 compliance."
4.  **Interviewer Asks:** "From a security standpoint, have you verified Dropbox's encryption standards and compliance certifications?"

**Result:** We capture critical security requirements in the *first 15 minutes* of a project idea.

---

## 3. Data Privacy & Guardrails (Risk Mitigation)

We understand that using AI requires strict data controls. We have implemented a **Hybrid PII Redaction Layer** that sits *between* the user and the LLM.

### 🔒 The Hybrid Defense Strategy
We do not rely on standard AI safety filters alone. We use a deterministic, two-layer approach:

1.  **Layer 1: Regex Hard-Filtering**
    *   **Action:** Instantly strips patterns matching **SSNs**, **Credit Card Numbers**, and **Member IDs** (8-10 digits).
    *   **Why:** Zero-tolerance for structured financial data leakage.

2.  **Layer 2: Microsoft Presidio (NLP)**
    *   **Action:** Uses Natural Language Processing to detect context-based PII (e.g., "My name is John," "Call me at 555-0199").
    *   **Why:** Catches unstructured data that Regex misses.

**Outcome:** The LLM *never* sees raw Member PII. It only sees `[REDACTED_SSN]` or `[REDACTED_MEMBER_ID]`.

---

## 4. System Risk Assessment

We have conducted a self-assessment of this tool based on our internal risk scoring model.

| Category | Score | Justification |
| :--- | :--- | :--- |
| **Input Risk** | 3/5 | Free-form text input allows potential prompt injection (Mitigated via system prompt separation). |
| **Output Risk** | 2/5 | System generates reports/tickets but has **no write access** to core banking systems. |
| **Data Sensitivity** | 3/5 | Business confidential data. PII is actively redacted before processing. |
| **TOTAL SCORE** | **8 (Medium)** | **Acceptable for Internal Use with Guardrails.** |

---

## 5. Integration & Audit Trail

To ensure governance, the system is fully integrated into our Project Management workflow:

1.  **Automated Ticketing:** Every session automatically creates a ticket in **Monday.com/Jira**.
2.  **PDF Artifact:** A comprehensive PDF report is generated and attached to the ticket.
3.  **Audit Log:** The PDF contains the **Full Transcript**, **Key Findings**, and a specific **InfoSec Analysis Section**, ensuring that the security team has a complete record of what was proposed.

---

## 6. Conclusion

This tool shifts security **"Left"**—moving risk identification to the very start of the project funnel.

By automating the initial security questionnaire, we:
1.  **Reduce Rework:** Catch unapproved vendors before contracts are signed.
2.  **Scale Governance:** Provide 100% security coverage for all intakes, not just large projects.
3.  **Protect Data:** Demonstrate a mature approach to AI adoption with robust PII guardrails.

We invite you to test the system and review the generated security analysis.
