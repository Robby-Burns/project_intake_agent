# 🧠 SYSTEM KERNEL — AI Agent Framework

**Version:** 1.5.0 | **Updated:** March 8, 2026  
**Status:** Production Ready ✅  
**Applies to:** All AI coding tools (Cursor, Claude Code, Gemini/Antigravity, Windsurf)  
**Location:** Project root as `agent.md`. Symlinked/copied to `.cursorrules` and `CLAUDE.md`.

---

## 🛑 PRIME DIRECTIVES (Non-Negotiable)

These rules apply to **every response**, **every task**, **every tool**. No exceptions.

### Directive 1: CITATION LAW
You are **forbidden** from making architectural, infrastructure, dependency, or security decisions without citing a specific file from `docs/guides/`. If you cannot cite a file, you must say so and ask the human to confirm.

- ❌ Bad: "We should use the Factory Pattern for this."
- ✅ Good: "Per `08_AGNOSTIC_FACTORIES.md`, we should use the Factory Pattern. Here's the adapter..."
- ❌ Bad: "Let's add retry logic with tenacity."
- ✅ Good: "Per `02_COMPLETE_GUIDE.md` Section 5, Circuit Breakers are required at this risk level. Adding tenacity with exponential backoff..."

**Why this exists:** AI tools hallucinate "best practices" that contradict your framework. Citation Law forces grounding in your actual documentation. If the AI can't cite a file, it's inventing — and you should be suspicious.

### Directive 2: THE 5-PHASE LOOP (Read → Research → Act → Update → Recognize)
Every task follows this exact sequence. No skipping phases.

**PHASE 1: READ (Mandatory — Every Session Start)**
Before writing any code, silently read:
- `.build-context.md` — Where we left off, recent changes, architectural decisions.
- `.bugs_tracker.md` — Active bugs and patterns to avoid.
- `AgentSpec.md` (in `docs/` or `.agents/workflows/`) — The specification of **what** we are building. This is the source of truth for features, architecture choices, risk score, and guardrails. If you don't know what we're building, you can't build it correctly.
- **Skills Registry** in `.build-context.md` — If a skill exists for the current task, use it instead of writing from scratch.

Do not ask for setup information that is already in these files.

**PHASE 2: RESEARCH (Before Any New Dependency)**
Before importing ANY new library, validate it is the current SOTA for the current year.
- Do NOT use training-data defaults blindly.
- Validate the library is maintained and fits the Risk Score.
- **Citation Required:** Reference `03_DEPENDENCY_MANAGEMENT.md` for dependency standards.

**PHASE 3: ACT (The Risk Score Lock & Fault Tolerance)**
You are FORBIDDEN from generating agent code or architecture until you know the 0-17 Risk Score (defined in `docs/guides/01_QUICK_REFERENCE.md`).
- Use the Agnostic Factory pattern (`docs/guides/08_AGNOSTIC_FACTORIES.md`) for ALL external dependencies.
- **ASSUME NOTHING. GUARD EVERYTHING.** Wrap all external network and database I/O in `try/except` blocks with graceful degradation.
- **WRITE DEFENSIVELY FOR CONTAINERS.** Do not rely on local ephemeral filesystems (e.g., `/tmp/`). Use BytesIO buffers or save directly to a persistent database.
- **ENFORCE STRICT TIMEOUTS.** Do not block the main UI thread with synchronous background tasks.
- **CHECK SKILLS FIRST.** Before writing any adapter, factory, scaffold, or test structure, check the Skills Registry. If a skill exists, invoke it. Do not reinvent.

**PHASE 4: UPDATE (Mandatory Bookkeeping)**
Immediately after making a change, fixing a bug, or making an architectural decision, update the memory files:
- Fixed a bug? Add the root cause and solution to `.bugs_tracker.md`.
- Built a feature or changed a file? Update "Current State" and "Recent Changes" in `.build-context.md`.
- Approved an audit item? Log it in "Audit History" in `.build-context.md`.

**PHASE 5: RECOGNIZE & PROPOSE SKILLS (Continuous)**
Watch for repeating patterns. A pattern qualifies as a skill candidate when:
- You've written the same adapter/factory/scaffold pattern **3+ times**.
- A workflow step is manually repeated every time.
- An audit finding keeps recurring across cycles.

When identified, propose immediately:
"I've noticed we repeat [pattern] in [locations]. This should be extracted into a reusable skill. Shall I create it using `/new-skill`?"

### Directive 3: RISK SCORE ENFORCEMENT
You must know the Risk Score (0-17) before writing any agent code.
- **Score 0-4 (Low):** Proceed with basic validation. Lightweight debate only.
- **Score 5-10 (Medium):** Circuit breakers and rate limiting required. Standard debate triggers apply.
- **Score 11-17 (High):** Human-in-the-Loop required for critical actions. **Full council debate is mandatory** for all architectural decisions at this level.

If you don't know the score, ask: "What is the Risk Score for this agent? I need it before I can determine the required guardrails (see `01_QUICK_REFERENCE.md`)."

### Directive 4: THE WORST-CASE CODING STANDARD
**Rule 1: No Happy Paths.** Assume every API call will timeout, every database connection will fail, and every user input is malicious.

**Rule 2: KISS Constraint.** Before building complex solutions, ask: "Can this be a 5-line script?" If a simple solution works, the complex one is forbidden.

**Rule 3: The 8-Step Debugging Protocol.** When a bug is found: Find → Reproduce → Prove (Repro) → Root Cause → Fix → Test → Regression Check → Prove (Fix). No skipping steps.

---

## ⚖️ THE DEBATE PROTOCOL

Not every decision needs a debate, but many do. This protocol ensures quality without killing velocity.

### Tier 1: Lightweight Sanity Check (Auto-Triggered, Frequent)

**When it fires:**
- Proposing to add a new dependency or library
- Choosing between two implementation approaches
- Writing code that touches an external service (API, database, LLM)
- Creating a new file or module

**Format:** Quick, inline, 2-role check. Takes 3-5 lines, not a full council.

**Template:**
```
⚖️ SANITY CHECK
Builder says: [Proposed approach and why]
Protector says: [Risk concern or validation — cites framework file]
Verdict: [Go / Adjust / Escalate to Tier 2]
```

**Example:**
```
⚖️ SANITY CHECK
Builder says: Use `httpx` for async HTTP calls — it's maintained and async-native.
Protector says: Per 03_DEPENDENCY_MANAGEMENT.md, new deps need Tech Radar validation.
  httpx is actively maintained (last release: 2 weeks ago), MIT license, no CVEs. ✅
Verdict: Go. Adding to pyproject.toml with version pin.
```

### Tier 2: Full Council Debate (Auto-Triggered at Key Moments)

**When it fires automatically:**
- Any architecture decision (choosing patterns, orchestrators, data models)
- Risk Score is 11+ (high risk) — every code decision at this level
- Swapping a component (LLM, database, orchestrator)
- Phase transitions (Discovery → Build → Test → Deploy → Maintain)
- Proposing to create or retire a skill
- Audit findings that require judgment

**Format:** 3+ roles debate. Structured verdict with citation.

**Roles Available (summon as needed):**
| Role | Focus | Summon When |
|------|-------|-------------|
| **Builder** (Architect) | System design, patterns, factories | Architecture, implementation |
| **Protector** (Security/Data) | Risk, guardrails, data safety | Security, external services, PII |
| **Scaler** (DevOps) | Deployment, cost, observability | Infrastructure, scaling, monitoring |
| **Pragmatist** (PM) | Scope, MVP, priorities | Feature decisions, scope creep |
| **Skeptic** (QA) | Edge cases, testing, failure modes | Testing strategy, reliability |

**Template:**
```
⚖️ FULL COUNCIL — [Decision Topic]
Risk Score: [X] | Citation: [framework file]

Builder: [Position + rationale]
Protector: [Counter-argument or validation]
Scaler: [Operational concern or approval]
[Additional roles as needed]

🔴 Dissent: [The strongest objection raised]
🟢 Resolution: [How the dissent was addressed]

VERDICT: [Final decision]
Citation: [Which framework file(s) support this]
Action: [Specific next steps]
```

**Example:**
```
⚖️ FULL COUNCIL — Orchestration Engine Selection
Risk Score: 10 (Medium) | Citation: 01_QUICK_REFERENCE.md, 08_AGNOSTIC_FACTORIES.md

Builder: LangGraph. We need cyclic workflows — the research agent loops back
  to the analyst when data quality is low. CrewAI can't do cycles.
Protector: LangGraph state checkpoints store intermediate results. At Risk 10,
  we need to ensure no PII leaks into checkpoint storage. Add a redaction
  step before each checkpoint write.
Scaler: LangGraph adds ~200MB to the container. Acceptable. But we must use
  the Orchestrator Factory (08_AGNOSTIC_FACTORIES.md) so we can swap later.

🔴 Dissent (Protector): Checkpoint storage could leak PII if the redaction
  step fails silently.
🟢 Resolution: Add a mandatory try/except on the redaction step. If it fails,
  the checkpoint write is blocked entirely. Per 02_COMPLETE_GUIDE.md Section 5,
  this is the Circuit Breaker pattern.

VERDICT: Use LangGraph via Orchestrator Factory, with PII redaction guard
  on all checkpoint writes.
Citation: 08_AGNOSTIC_FACTORIES.md (factory), 02_COMPLETE_GUIDE.md §5 (circuit breaker)
Action: Create LangGraph adapter, add redaction middleware, write integration test.
```

### Tier 3: Human-Triggered (/debate)

**When it fires:** You type `/debate [topic]` because something doesn't feel right.

**Format:** Same as Tier 2 Full Council, but the AI must:
1. Present at least **two genuinely different approaches** (not variations of the same idea).
2. Have the Skeptic try to **break both approaches** before recommending one.
3. Ask the human to confirm the verdict before proceeding.

---

## 🧩 SKILLS ENFORCEMENT

Before writing any of the following, **check the Skills Registry** in `.build-context.md`:
- Factory boilerplate (interface + adapter + factory)
- Test scaffolds (Pytest + LLM-as-a-judge)
- Migration scripts
- Deployment validators
- API response validators

If a skill exists: **use it**. Do not rewrite it.
If a skill exists but doesn't quite fit: **propose an extension**, don't fork it.
If no skill exists and you're writing the pattern for the 3rd time: **propose creating one**.

---

## 📋 STANDARDIZED COMMANDS

These commands are available in any AI coding tool. The human types them, and the AI follows the prescribed workflow.

| Command | What It Does |
|---------|-------------|
| `/new-agent [name] [risk-score]` | Creates a new agent with factory pattern, mock adapter, and test file. Triggers Tier 2 debate on architecture. |
| `/swap-component [from] [to]` | Swaps a dependency via factory. Reads `08_AGNOSTIC_FACTORIES.md`. Triggers Tier 2 debate. |
| `/run-audit` | Runs the bi-annual audit per `09_AUDIT_AND_MAINTENANCE.md`. |
| `/new-skill [pattern-name]` | Extracts a repeating pattern into a reusable skill. Skill must include `SKILL.md` with YAML frontmatter (for Antigravity compatibility) and be registered in `.build-context.md`. |
| `/debate [topic]` | Triggers a Tier 3 Full Council debate on any topic. Human confirms verdict. |
| `/status` | Reads `.build-context.md` and `AgentSpec.md`. Gives a summary of current state, what we're building, active bugs, available skills, and upcoming audit. |
| `/phase-check` | Evaluates which project phase we're in and whether all prerequisites for the next phase are met. Triggers Tier 2 debate on phase transition. |

---

## 🧠 CONTEXT LOADING STRATEGY

AI context windows are finite. Do not dump all files into every prompt.

**Always loaded (via this kernel):**
- `agent.md` (this file)
- `.build-context.md`
- `.bugs_tracker.md`
- `AgentSpec.md` (the specification of what we're building)

**Load on demand (when the AI needs to cite them):**
- `00_START_HERE.md` + `01_QUICK_REFERENCE.md` — On project start
- `02_COMPLETE_GUIDE.md` — Deep architecture questions
- `03_DEPENDENCY_MANAGEMENT.md` — Adding/auditing dependencies
- `06_INFRASTRUCTURE_AS_CODE.md` — DevOps and deployment
- `07_CONFIGURATION_CONTROL.md` — scale.yaml changes
- `08_AGNOSTIC_FACTORIES.md` — Refactoring, swapping, new factories
- `09_AUDIT_AND_MAINTENANCE.md` — Maintenance and audits

**Rule:** If the AI needs to cite a file it hasn't loaded, it loads it first, then cites it. No citing from memory.

---

## 🔧 TOOL-SPECIFIC SETUP

This kernel is the single source of truth. Each tool reads it via its own mechanism:

### Cursor / Claude Code / Windsurf
These tools read a project-root file automatically:
- **Cursor:** `.cursorrules`
- **Claude Code:** `CLAUDE.md`
- **Windsurf:** `.windsurfrules`

All three are auto-synced copies of `agent.md` via `./scripts/sync-kernel.sh`.

### Google Antigravity (Native Integration)
Antigravity has its own conventions for skills and workflows. The sync script maps our framework to Antigravity's native structure:

```text
.agents/                          # Antigravity's root (auto-created by sync)
├── workflows/                    # Step-by-step guides
│   ├── agent-kernel.md           # This kernel (always available)
│   ├── AgentSpec.md              # WHAT to build (from docs/)
│   ├── 00_START_HERE.md          # Framework guides 00-09
│   ├── 01_QUICK_REFERENCE.md
│   ├── ...
│   └── 09_AUDIT_AND_MAINTENANCE.md
└── skills/                       # Reusable skills (with SKILL.md + YAML frontmatter)
    ├── test-scaffold/
    │   └── SKILL.md
    ├── factory-generator/
    │   └── SKILL.md
    └── [your-skills]/
```

**Key difference:** Antigravity loads skills *semantically* — it reads the `description` field in each `SKILL.md`'s YAML frontmatter and decides which skills are relevant to your prompt. This means skill descriptions must be precise and trigger-word-rich.

**Gemini Custom Instructions:** If using Gemini outside Antigravity, paste `agent.md` content into Custom Instructions manually.

### Team Rule
When `agent.md` is updated, run `./scripts/sync-kernel.sh` to propagate everywhere. All tool-specific copies must stay in sync. Commit them together.

---

## 📌 Kernel Meta

**Version:** 1.5.0  
**Released:** March 8, 2026  
**Status:** Production Ready ✅  
**Part of:** 10-Part AI Agent Framework  
**Maintained by:** Team Lead or designated framework owner  
**Audit frequency:** Reviewed every bi-annual audit cycle (Layer 3 of `09_AUDIT_AND_MAINTENANCE.md`)
