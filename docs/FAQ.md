# ❓ Project Intake Agent: Frequently Asked Questions (FAQ)

**Audience:** CIO, VP of IT, VP of InfoSec  
**Date:** February 2026

---

## 🏛️ Strategic & Business Value (CIO Focus)

**1. Q: Why build this instead of buying an off-the-shelf AI tool?**  
**A:** Off-the-shelf tools are generic. We built this to align specifically with our **Credit Union frameworks** (NIST, GLBA, PMI). Plus, we own the data and the guardrails, ensuring member privacy isn't outsourced to a black box.

**2. Q: How do we measure the ROI of this pilot?**  
**A:** We measure **"Time to Ticket Readiness."** Currently, it takes ~3 meetings to get a clear project scope. If this agent reduces that to 1 meeting (or zero), we save X hours of Analyst time per project.

**3. Q: Is this going to replace our Business Analysts?**  
**A:** No. It replaces the *repetitive* part of their job (gathering basic facts). It frees them to focus on complex solutioning and relationship management, which AI can't do.

**4. Q: What if the AI gives bad advice?**  
**A:** The AI doesn't give *advice*; it asks *questions*. It gathers requirements. The final output is a **Draft Report** that a human must review and approve. It’s a "force multiplier," not a decision-maker.

**5. Q: How does this fit into our long-term AI strategy?**  
**A:** This is our **"Safe AI Blueprint."** The architecture we built here (PII redaction, containerization, state machine control) is the exact foundation we'll need for future, riskier projects (like member-facing bots).

---

## 🛡️ Security & Risk (VP InfoSec Focus)

**6. Q: Does Member Data go to OpenAI?**  
**A:** **No.** We implemented a **Hybrid Guardrail System** (Regex + Presidio) that runs locally on our server. It strips SSNs, Member IDs, and Names *before* the text is ever sent to the LLM API.

**7. Q: What happens if a user tries to "jailbreak" it (Prompt Injection)?**  
**A:** We use **System Prompt Separation** and a strict **State Machine**. The AI is confined to specific steps (e.g., "Ask about Project Name"). It physically cannot execute code or access our database, limiting the blast radius of any injection attempt.

**8. Q: Is this compliant with GLBA/NCUA standards?**  
**A:** Yes. The system is designed with **Data Minimization** in mind. It doesn't store PII, and the "InfoSec Specialist Agent" is explicitly trained on NIST frameworks to *ask* about compliance early in the process.

**9. Q: Where are the chat logs stored?**  
**A:** Logs are stored locally in the `reports/` folder (or our secure database) and attached to the Monday.com ticket. We retain full auditability of every conversation.

**10. Q: Can we switch LLM providers if OpenAI becomes a risk?**  
**A:** Yes. The system uses **LangChain**, which is model-agnostic. We can swap OpenAI for Azure OpenAI, Anthropic, or even a locally hosted Llama model with minimal code changes.

**11. Q: How do you handle "Shadow IT" risks with this?**  
**A:** This tool *combats* Shadow IT. By making the intake process easy and fast, users are more likely to register their projects with IT early, rather than hiding them until the last minute.

---

## 🔧 Operations & Architecture (VP IT Focus)

**12. Q: How is this hosted?**  
**A:** It’s a standard **Docker Container**. We can deploy it to our existing Azure/AWS infrastructure or an on-prem Kubernetes cluster. It has no complex dependencies.

**13. Q: What happens if the Monday.com API changes?**  
**A:** We used the **Adapter Pattern**. The Monday.com logic is isolated in one file (`monday.py`). If their API changes, we update that one file, and the rest of the system (Agents, UI) remains untouched.

**14. Q: How much maintenance does this require?**  
**A:** Very little. It’s stateless. There’s no database to groom (unless we add one later). The main maintenance is updating the API keys if they rotate.

**15. Q: Can we customize the questions it asks?**  
**A:** Yes. The "Specialist Personas" are defined in a simple configuration file. We can tweak the "Project Manager" to ask about specific budget codes or the "IT Specialist" to ask about specific legacy systems.

**16. Q: Does it integrate with Active Directory (SSO)?**  
**A:** Not in the MVP, but the architecture supports it. We can add an SSO layer in front of the Streamlit app for the next phase.

**17. Q: What if the user types "I don't know" to everything?**  
**A:** The system has **Adaptive Logic**. If the user is vague, it simplifies the questions. If they still don't know, it captures that uncertainty in the report, flagging it as a risk for the human analyst to follow up on.

**18. Q: Can multiple people use it at once?**  
**A:** Yes. The web server (Streamlit) handles multiple concurrent sessions. Since the agents are **stateless**, User A's chat doesn't interfere with User B's.

**19. Q: How do we update the "Knowledge Base" of the agents?**  
**A:** Currently, they use general knowledge + our prompts. In Phase 3, we could add **RAG (Retrieval Augmented Generation)** to let them search our internal Wiki/SharePoint for specific policy documents.

**20. Q: What is the "Bus Factor" on this? (If you leave, who fixes it?)**  
**A:** The code is fully documented (`README.md`, `ARCHITECTURE.md`) and uses standard Python libraries. Any mid-level Python developer can pick it up. It’s not "black magic."
