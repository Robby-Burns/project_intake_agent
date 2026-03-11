# ❓ Frequently Asked Questions (v1.5.0)

**Project:** ProjectIntakeAgentThree
**Framework:** 10-Part AI Agent Framework (1.5.0)
**Last Updated:** March 8, 2026

---

## 🤖 General Questions

### Q: What does this agent actually do?
**A:** It acts as an intelligent "Project Intake Coordinator." It interviews users about their project ideas while 8 specialist AI agents (IT, InfoSec, Risk, etc.) listen in real-time. These specialists "whisper" critical follow-up questions to the interviewer to ensure no important details are missed. Finally, it generates a professional PDF report and creates a ticket in your PM tool.

### Q: Is my data safe?
**A:** Yes. We use a hybrid security model:
1.  **PII Redaction:** All input is scanned (Regex + NLP) to redact sensitive data like SSNs and credit card numbers *before* it leaves your network.
2.  **Zero Training:** Your data is NOT used to train public AI models.
3.  **Audit System:** We run mandatory security audits every 6 months to ensure compliance.

### Q: Can I use this for non-technical projects?
**A:** Absolutely. The "Specialist Agents" cover Marketing, Training, and Accounting, not just IT. The system adapts its questions based on the project type.

---

## 🛠️ Technical Questions

### Q: Why do you use "Agnostic Factories"?
**A:** This prevents "vendor lock-in." If OpenAI raises prices or changes their API, we can switch to Anthropic or Azure OpenAI by changing one line in `config/scale.yaml`. No code rewriting is required.

### Q: What happens if the internet goes down during an interview?
**A:** The system now uses a **PostgreSQL Database** to save every turn of the conversation. If you refresh the page or lose connection, your session history is preserved and you can pick up right where you left off.

### Q: How do you control AI costs?
**A:** We use a "Model Mixing" strategy. Complex reasoning (like the Project Manager agent) uses `gpt-4o`, while simpler tasks (like the Marketing agent) use `gpt-4o-mini`. This reduces costs by ~40% without sacrificing quality.

### Q: How do I change the interview questions?
**A:** You don't edit code. You edit the agent prompts in `app/agents/`. The system is designed to be prompt-driven.

---

## 🚀 Deployment & Maintenance

### Q: How often is the system updated?
**A:** The core framework is stable. We run a mandatory **Bi-Annual Audit** (March & September) to check for security vulnerabilities and outdated dependencies.

### Q: Can I host this on-premise?
**A:** Yes. The entire system is containerized (Docker). You can run it on any server that supports Docker, including on-premise Kubernetes clusters or private clouds.

### Q: What if the agent "hallucinates" (makes things up)?
**A:** We use "Circuit Breakers" and "LLM-as-a-judge" testing to minimize this. However, AI is probabilistic. Always review the final PDF report before submitting it for funding approval.
