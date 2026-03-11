# 📇 Agent Cards (The Roster)

**Project:** Project Intake Agent (ProjectIntakeAgentThree)
**Role:** Project Intake & Analysis
**Total Agents:** 9 (1 Orchestrator + 8 Specialists)
**Framework:** 1.5.0 (Agnostic Factory Pattern)

---

## 🎭 The Interviewer (Orchestrator)
**Role:** Project Intake Coordinator
**Model:** `gpt-4o` (Configurable via `scale.yaml`)
**Responsibility:** The "Face" of the system. Synthesizes user input and specialist "whispers" into a coherent conversation.
**Guardrails:**
- **PII Redaction:** Removes SSN, Credit Cards, Member IDs (unless allowed).
- **Tone Enforcement:** Professional, helpful, persistent (prevents early exit).
- **Turn Limits:** Max 15 turns to prevent infinite loops.

---

## 🕵️ The Specialist Agents (The Whisper Engine)

These agents run in parallel, analyzing every user message. They do *not* speak to the user directly; they "whisper" questions to the Interviewer.

### 1. Project Manager Specialist
**Focus:** Scope, Schedule, Cost, Quality, Resources, Risk.
**Framework:** PMI Best Practices (PMBOK).
**Critical Whisper:** "Is there a defined budget or deadline for this project?"

### 2. Product Manager Specialist
**Focus:** Outcomes, Hypotheses, Success Metrics, Member Value.
**Framework:** Hypothesis-Driven Development (HDD).
**Critical Whisper:** "How will we measure success? What is the core hypothesis?"

### 3. IT Specialist
**Focus:** Scalability, Reliability, Integration Patterns, Technical Debt.
**Framework:** Enterprise Architecture (TOGAF / AWS Well-Architected).
**Critical Whisper:** "Does this require integration with existing legacy systems?"

### 4. InfoSec Specialist
**Focus:** Data Privacy, Security Compliance, Threat Modeling.
**Framework:** NIST Cybersecurity Framework / GLBA.
**Critical Whisper:** "Will this project handle any PII or sensitive financial data?"

### 5. ERM Specialist (Enterprise Risk Management)
**Focus:** Risk Appetite, Vendor Risk, Regulatory Compliance.
**Framework:** COSO ERM Framework.
**Critical Whisper:** "Does this project involve any new third-party vendors?"

### 6. Marketing Specialist
**Focus:** Member Acquisition, Retention, Brand Alignment.
**Framework:** Marketing Mix (4Ps).
**Critical Whisper:** "How will this impact the member experience or brand perception?"
**Note:** Uses `gpt-4o-mini` for cost efficiency.

### 7. Training Specialist
**Focus:** Staff Readiness, Procedure Documentation.
**Framework:** ADDIE Model.
**Critical Whisper:** "What training will be required for staff to support this new system?"
**Note:** Uses `gpt-4o-mini` for cost efficiency.

### 8. Accounting Specialist
**Focus:** Capital vs. Expense (CapEx/OpEx), ROI, TCO.
**Framework:** GAAP & ROI Analysis.
**Critical Whisper:** "Is this budgeted as CapEx or OpEx? What is the expected ROI?"
**Note:** Uses `gpt-4o-mini` for cost efficiency.
