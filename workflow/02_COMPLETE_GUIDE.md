# 📚 Complete Guide - AI Agent Development Framework

**Your comprehensive reference for building secure, scalable, production-ready AI agent systems**

**Version:** 1.5.0 | **Updated:** March 8, 2026 | **Part:** 3/10  
**Status:** Production Ready ✅  
**Reading Time:** 2-3 hours (reference as needed)  
**Total Content:** 12 sections, deep methodology

---

## 📍 Purpose

This file is the **deep methodology guide**. It explains:
- **Why** the framework works the way it does
- **How** to apply each pattern correctly
- **When** to use which approach
- **Real examples** of architectures, guardrails, testing strategies
- **Advanced patterns** like multi-agent orchestration, LLM Evals, and observability.

**When to use:** Deep dives on architecture, understanding tradeoffs, complex decisions.

---

## 🗺️ Quick Navigation

- [Table of Contents](#table-of-contents)
- [Section 1: Overview & Benefits](#section-1-overview--benefits)
- [Section 2: The 8-Step Process](#section-2-the-8-step-process-deep-dive)
- [Section 3: Risk Scoring System](#section-3-risk-scoring-system-0-17)
- [Section 4: Architecture Patterns](#section-4-architecture-patterns)
- [Section 5: Security & Guardrails](#section-5-security--guardrails)
- [Section 6: Testing Strategy & Evals](#section-6-testing-strategy--llm-evals)
- [Section 7: Multi-LLM Debate Pattern](#section-7-multi-llm-debate-pattern)
- [Section 8: Tooling Strategy & MCP](#section-8-tooling-strategy--mcp-integration)
- [Section 9: Infrastructure as Code](#section-9-infrastructure-as-code-iac)
- [Section 10: Deployment Strategies](#section-10-deployment-strategies)
- [Section 11: Workflows & Integration](#section-11-workflows--integration)

*(Note: Database and Agnostic Factory deep-dives have been moved to `08_AGNOSTIC_FACTORIES.md`)*  
*(Note: Bi-annual audit deep-dive lives in `09_AUDIT_AND_MAINTENANCE.md`)*

---

## 🔗 Related Files

**Before this:** [01_QUICK_REFERENCE.md](./01_QUICK_REFERENCE.md) (Formulas, matrices)  
**This file:** [02_COMPLETE_GUIDE.md](./02_COMPLETE_GUIDE.md) (You are here)  
**After this:** [03_DEPENDENCY_MANAGEMENT.md](./03_DEPENDENCY_MANAGEMENT.md) (Python setup)  
**For implementation:** [06_INFRASTRUCTURE_AS_CODE.md](./06_INFRASTRUCTURE_AS_CODE.md) (Terraform)  
**For maintenance:** [09_AUDIT_AND_MAINTENANCE.md](./09_AUDIT_AND_MAINTENANCE.md) (Audit & HITL)

---

## Table of Contents

1. [Section 1: Overview & Benefits](#section-1-overview--benefits)
2. [Section 2: The 8-Step Process (Deep Dive)](#section-2-the-8-step-process-deep-dive)
3. [Section 3: Risk Scoring System (0-17)](#section-3-risk-scoring-system-0-17)
4. [Section 4: Architecture Patterns](#section-4-architecture-patterns)
5. [Section 5: Security & Guardrails](#section-5-security--guardrails)
6. [Section 6: Testing Strategy & LLM Evals](#section-6-testing-strategy--llm-evals)
7. [Section 7: Multi-LLM Debate Pattern](#section-7-multi-llm-debate-pattern)
8. [Section 8: Tooling Strategy & MCP Integration](#section-8-tooling-strategy--mcp-integration)
9. [Section 9: Infrastructure as Code (IaC)](#section-9-infrastructure-as-code-iac)
10. [Section 10: Deployment Strategies](#section-10-deployment-strategies)
11. [Section 11: Workflows & Integration](#section-11-workflows--integration)

---

## Section 1: Overview & Benefits

### What This Framework Provides

This framework gives you everything needed to build production-ready AI agent systems:

**✅ Proven Methodology**
- 8-step discovery-to-maintenance process
- Risk-based security (not paranoid, not naive)
- Test-driven development with LLM Evals
- Production-ready from day 1

**✅ Technology Agnostic**
- Swap Orchestration (LangGraph vs CrewAI vs Simple Async)
- Swap LLM providers (1 line change)
- Swap databases (1 env var)
- **Hybrid Tooling:** Local Adapters + MCP Bridges

**✅ Time Savings**
- 30-50% faster development (after 3-4 projects)
- 80%+ code reuse across projects
- Zero security oversights (checklists prevent)
- No architecture regrets (patterns proven)

**✅ Long-Term Health**
- Bi-annual audits catch dependency rot, API drift, and stale recommendations
- HITL sign-off ensures no silent breakage from auto-applied updates
- Weekly CVE scans catch critical vulnerabilities between audits

---

## Section 2: The 8-Step Process (Deep Dive)

**ALWAYS follow this sequence. No shortcuts.**

### Step 1: DISCOVERY

**Purpose:** Understand the problem before building anything.

**Questions to Answer:**
- What problem are we solving?
- Who are the users?
- What does success look like?
- What are the risks if we fail?

**Example:**
```text
Problem: Research agents take 30+ minutes to compile reports manually
Users: 50 internal analysts
Success: Agents generate reports in <5 minutes, 90% accuracy
Constraints: <$500/month cost, data privacy required
```

---

### Step 2: RISK SCORING (0-17 Scale)

**Purpose:** Calculate risk BEFORE any architecture decisions.

**Formula:** See [01_QUICK_REFERENCE.md](./01_QUICK_REFERENCE.md) Risk Scoring Formula

**Example From Step 1:**
```text
Research Agent Risk Calculation:
Input Risk: 4 (user questions, open-ended)
Output Risk: 2 (reports, non-critical)
Data: 2 (internal data, not PII)
Model: 2 (reasoning chain, no tools)
─────────────────
TOTAL: 10 (MEDIUM) → Standard guardrails required
```

---

### Step 3: GUARDRAILS SELECTION

**Purpose:** Enable security appropriate to risk level.

**LOW (0-4):**
```text
✓ Input validation (basic type checks)
✓ Output validation (no obvious errors)
✓ Logging (info level)
```

**MEDIUM (5-10):**
```text
✓ Everything from LOW, plus:
✓ Prompt injection detection (separate LLM check)
✓ Content filtering (output scanning)
✓ Circuit breakers & rate limiting
```

**HIGH (11-17):**
```text
✓ Everything from MEDIUM, plus:
✓ Human approval (HITL) for critical actions
✓ Immutable audit logs
✓ MicroVM isolation
```

---

### Step 4: ARCHITECTURE SELECTION

**Purpose:** Choose system design that handles your scale and workflow complexity.

**Debate Trigger:** This step is a **Tier 2 Full Council** debate. The kernel in `agent.md` auto-triggers it. The Builder, Protector, and Scaler roles must weigh in before any architecture is finalized. At Risk Score 11+, this is mandatory on every sub-decision.

**Orchestration Layer (New for 2026):**
Agents rarely work alone. You must explicitly design how they coordinate:
* **Sequential Pipeline (CrewAI):** Use this when tasks are strictly ordered. Agent A gathers data -> Agent B summarizes -> Agent C formats.
* **State Graph (LangGraph):** Use this when tasks require loops or reflection. Agent A writes code -> Agent B tests it -> If fail, loop back to Agent A.

**Execution Layer:**
* **Modular Monolith:** Your orchestrator, agents, and API live in one process. 
* **Distributed Workers:** When workflows take longer than your API's 30-second timeout, move the `orchestrator.run_workflow()` call to a Celery/Redis worker.

---

### Step 5: TOOLING STRATEGY

**Purpose:** Decide when to use local code vs. external tools.

**Decision Tree:**
```text
Need to connect a tool?
│
├─ Internal / High Performance / Custom Logic
│  └─ Use: LOCAL ADAPTER (~1ms latency)
│
└─ External / Ecosystem / Standardized
   └─ Use: MCP BRIDGE (Sandboxed, safe)
```

---

### Step 6: IMPLEMENTATION

**Purpose:** Build in phases with testing integrated.

**Phase 1: Core Features + Tests (60% effort)**
- Build core agent logic and factory interfaces.
- Write unit tests and LLM Evals.
- **Identify repeating patterns early.** If you're writing the same adapter/scaffold/test structure for a third time, stop and extract it into a reusable skill using the `/new-skill` prompt pattern (see `04_AI_ASSISTANT_INTEGRATION.md`). Building skills during implementation saves compounding time in later phases and future projects.

**Phase 2: Integration + Security (20% effort)**
- Add guardrails (appropriate to risk).
- Write integration tests.

**Phase 3: Observability + Polish (20% effort)**
- Add OpenTelemetry tracing.
- Setup monitoring/alerting.
- Register all created skills in `.build-context.md` Skills Registry.

---

### Step 7: DEPLOY & MONITOR

**Purpose:** Release to production and iterate.

**Deployment Stack:**
1. **Infrastructure as Code (Terraform)**
2. **CI/CD Pipeline**
3. **Observability (OpenTelemetry)**

---

### Step 8: MAINTAIN & AUDIT

**Purpose:** Keep the system trustworthy over time. A deployed agent that is never reviewed will drift — its dependencies age, its API contracts change, and its framework recommendations become stale.

**The Bi-Annual Audit:**
Every 6 months, the system runs an automated scan and produces a report. The human reviews it and approves each change. Nothing is auto-applied.

Why this is mandatory, not optional:
- Dependencies: A library update can change behavior silently. The human needs to read "this version changes the retry logic" before approving.
- APIs: Broker and LLM providers deprecate endpoints with minimal notice. Catching this in a scheduled review is far better than discovering it during execution.
- The guides themselves: Best practices in this framework age. The audit checks whether the tooling recommendations in each guide file are still current for this year.

**HITL is required because:**
These are not mechanical changes. They require someone who understands the system to judge whether a change is safe. An automated merge of a major dependency update on a high-risk system is an unacceptable pattern.

**Configuration:** See `09_AUDIT_AND_MAINTENANCE.md` for full audit setup. Set `audit.notification_channel` in `scale.yaml` before first deploy.

---

## Section 3: Risk Scoring System (0-17)

**Full formula:** See [01_QUICK_REFERENCE.md](./01_QUICK_REFERENCE.md).

Risk scoring is the **control variable** for the entire framework. It determines guardrails, architecture, testing scope, and monitoring requirements. Do not skip this.

---

## Section 4: Architecture Patterns

### Pattern 1: Simple Monolith (MVP, <1K Users)
**When to use:** Proving concept, MVP
**Structure:** Single container FastAPI app + SQLite/Postgres. Agents execute directly in the API request cycle.

### Pattern 2: Multi-Agent Orchestration (LangGraph / CrewAI)
**When to use:** Complex tasks requiring planning, delegation, or self-reflection.
**Structure:** The API receives the request and kicks off an `AgentOrchestrator` workflow. 

### Pattern 3: Multi-Container Orchestrator + Worker Pool (10K+ Users)
**When to use:** Workflows that take > 30 seconds to complete (which will timeout standard HTTP requests).
**Components:**
1. **Orchestrator:** FastAPI, queues jobs, returns 202 Accepted.
2. **Workers:** Celery pull jobs from queue, run agent inference.
3. **Shared State:** PostgreSQL (database), Redis (cache/queue).

---

## Section 5: Security & Guardrails

### 1. Circuit Breakers (Medium-High Risk)
If an external API fails 3 times, the agent stops and reports an error, rather than hallucinating a response. Use libraries like `tenacity` with exponential backoff on all tool calls.

### 2. Output Validation (PII Redaction)
Scan output before returning to user. 
```python
def redact_pii(text: str) -> str:
    # Use regex or a small fast NLP model to strip emails, SSNs, etc.
    return safe_text
```

### 3. Human-in-the-Loop HITL (High Risk)
Physically pause code execution for human approval before dangerous actions. The orchestrator (e.g., LangGraph) must pause state, send a notification, and await an API callback before resuming.

---

## Section 6: Testing Strategy & LLM Evals

Testing non-deterministic AI agents requires a two-pronged approach. Aim for 80% coverage.

### Prong 1: Traditional Software Tests
Test the scaffolding, not the LLM.
* **Unit Tests:** Test your Pydantic schemas, routing logic, and tool adapters using mocked LLM responses.
* **Integration Tests:** Ensure the Database Factory connects and stores state correctly.

### Prong 2: LLM Evaluations (Evals) (10-15% of effort)
Traditional assertions (`assert result == "Paris"`) fail when an LLM says "The capital is Paris." You must use **LLM-as-a-judge**.

```python
@pytest.mark.asyncio
async def test_research_agent_accuracy():
    """Use a strict, separate LLM to judge the agent's output."""
    agent_output = await researcher_agent.run("What is the capital of France?")
    
    # The Judge LLM evaluates the output against a known rubric
    judge_prompt = f"""
    Fact: The capital of France is Paris.
    Agent Output: {agent_output}
    Does the Agent Output correctly state the fact without hallucinating extra cities? 
    Reply ONLY with 'PASS' or 'FAIL'.
    """
    # Use your LLM Factory to call a reliable model (e.g., Opus)
    judge_result = await get_llm_provider(model="claude-3-opus").generate(judge_prompt)
    assert "PASS" in judge_result
```
*Note: Use observability tools like LangSmith or Phoenix to trace these Eval scores over time to detect model drift.*

---

## Section 7: Multi-LLM Debate Pattern

### Why Debate Matters
Single LLMs are prone to hallucination. A debate pattern is more reliable:
* **Agent A (Optimist):** "The research shows X"
* **Agent B (Skeptic):** "But here's the counter-evidence: Y"
* **Agent C (Synthesizer):** "Combining both, the truth is: Z"

**Cost Consideration:** 3 calls = 3x cost. Worth it for financial decisions, medical advice, or High Risk scenarios.

---

## Section 8: Tooling Strategy & MCP Integration

**The Decision: Local vs. MCP**

| Feature | Local Adapter | MCP Bridge |
|---------|---------------|------------|
| **Speed** | ⚡ <1ms | 🐢 50ms+ |
| **Security**| ⚠️ Shared Process | ✅ Sandboxed |
| **Use When**| Fast DB queries, Custom internal logic | Slack, GitHub, local filesystem parsing |

---

## Section 9: Infrastructure as Code (IaC)

### Philosophy: "If It's Not in Terraform, It Doesn't Exist"
Never click buttons in cloud consoles. Define compute, database, monitoring, and secrets as code to ensure reproducible, version-controlled deployments.

**Kill Switch Patterns (Mandatory):** For Risk Score 11-17, create a specific Security Group/VPC rule in Terraform that drops all outbound traffic. In an emergency, apply this tag to blackhole the agent.

---

## Section 10: Deployment Strategies

| Platform | Best For | Resume Value | Effort |
|----------|----------|--------------|--------|
| **Railway** | MVP speed | ⭐⭐ | 30 min |
| **GCP Cloud Run** | Startup jobs | ⭐⭐⭐⭐⭐ | 1 hour |
| **Azure Container Apps** | Enterprise | ⭐⭐⭐⭐⭐ | 2 hours |
| **Fly.io** | Global users | ⭐⭐⭐ | 1 hour |

---

## Section 11: Workflows & Integration

### Daily Development Workflow
1. **Morning:** Type `/status` — AI reads `.build-context.md`, summarizes state, lists active bugs and available skills.
2. **During Work:** AI follows the 5-Phase Loop from `agent.md`. Tier 1 sanity checks happen inline. Tier 2 debates trigger at key decisions — read the verdict and confirm.
3. **Evening:** Tell AI: "Update `.build-context.md` with what we accomplished today." AI updates Current State, Recent Changes, Skills Registry, and Architectural Decisions.

---

## 📌 File Meta

**Version:** 1.5.0  
**Released:** March 8, 2026  
**Status:** Production Ready ✅  
**Part of:** 10-Part AI Agent Framework  

**Next File:** [03_DEPENDENCY_MANAGEMENT.md](./03_DEPENDENCY_MANAGEMENT.md)
