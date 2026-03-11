# 🤖 AI Assistant Integration - Tool-Agnostic Workflows

**Version:** 1.5.0 | **Updated:** March 8, 2026 | **Part:** 5/10  
**Status:** Production Ready ✅  
**Purpose:** How to configure and interact with AI coding assistants (Cursor, Windsurf, Claude Code, Antigravity) so they follow this framework.

---

## 📍 Purpose

AI coding assistants change constantly. This file teaches you the **principles** of guiding any AI assistant so it doesn't hallucinate architectures, forget your context, or write insecure code.

**The Golden Rule of AI Assistants:** "The AI is a junior developer with infinite typing speed but zero object permanence. You must force it to read the rules and update the project memory every single time."

**How we enforce this:** The `agent.md` System Kernel at the project root. Every AI tool reads it. It contains the Prime Directives, the 5-Phase Loop, the Debate Protocol, and the Citation Law. This file (04) explains *how to use* the kernel effectively. The kernel itself lives at `agent.md`.

---

## 🗺️ Quick Navigation

- [The System Kernel (agent.md)](#-the-system-kernel-agentmd)
- [Multi-Tool Setup](#-multi-tool-setup)
- [The Debate Protocol in Practice](#-the-debate-protocol-in-practice)
- [The Worst-Case Coding Standard](#-the-worst-case-coding-standard-mandatory)
- [Context Loading Strategy](#-context-loading-strategy)
- [Enforcing the Risk Score](#-enforcing-the-risk-score)
- [Standardized Commands (Prompt Patterns)](#-standardized-commands-prompt-patterns)
- [Skill Creation & Reuse](#-skill-creation--reuse)
- [Troubleshooting AI Hallucinations](#-troubleshooting-ai-hallucinations)

---

## 🧠 The System Kernel (`agent.md`)

The kernel is the **single source of truth** for AI behavior across all tools and all team members. It lives at the project root as `agent.md`.

### What the Kernel Enforces

| Directive | What It Does | Why It Matters |
|-----------|-------------|----------------|
| **Citation Law** | AI must cite a framework file for every architectural decision | Catches hallucinations. If it can't cite, it's inventing. |
| **5-Phase Loop** | Read → Research → Act → Update → Recognize on every task | Prevents forgetting context, skipping validation, and reinventing skills |
| **Debate Protocol** | Tiered debates at key decision points | Catches bad decisions early. Scales from lightweight to full council. |
| **Risk Score Lock** | No code until the 0-17 score is known | Determines guardrails, debate intensity, and testing scope |
| **Skills Check** | AI checks Skills Registry before writing any pattern | Prevents reinventing existing solutions |
| **Worst-Case Standard** | No happy paths, KISS constraint, 8-step debug protocol | Production-grade code from day 1 |

### How to Modify the Kernel

1. Edit `agent.md` in the project root.
2. Run `./scripts/sync-kernel.sh` to propagate to all tool-specific files.
3. Commit all synced files together.
4. Notify the team.

**Rule:** Never edit `.cursorrules`, `CLAUDE.md`, or `.windsurfrules` directly. They are copies. `agent.md` is the source.

---

## 🔧 Multi-Tool Setup

Your team uses multiple AI tools. Each tool reads its rules from a different location, but they all enforce the same kernel.

### File Mapping

| AI Tool | What It Reads | Setup Method |
|---------|--------------|--------------|
| **Cursor** | `.cursorrules` at project root | Auto-synced via `sync-kernel.sh` |
| **Claude Code** | `CLAUDE.md` at project root | Auto-synced via `sync-kernel.sh` |
| **Windsurf** | `.windsurfrules` at project root | Auto-synced via `sync-kernel.sh` |
| **Antigravity** | `.agents/workflows/` + `.agents/skills/` | Auto-synced via `sync-kernel.sh` |
| **Gemini (standalone)** | Custom Instructions | Manual paste from `agent.md` |

### Initial Setup

```bash
# From project root:
chmod +x ./scripts/sync-kernel.sh
./scripts/sync-kernel.sh
```

This creates/updates all tool-specific files AND sets up Antigravity's `.agents/` folder.

### Verify It Works

Open your AI tool and type: `/status`

The AI should read `.build-context.md` and `AgentSpec.md`, then summarize the project state. If it doesn't, the kernel isn't loaded. Check:
1. Does the tool-specific file exist? (e.g., `.cursorrules` for Cursor)
2. Does it contain the kernel content? (open and check)
3. Restart the AI tool — some cache the rules file on startup.

### Google Antigravity Setup (Native Integration)

Antigravity has its own conventions for organizing AI context. The sync script maps our framework to Antigravity's native `.agents/` structure:

```text
.agents/                              # Antigravity's project-level agent config
├── workflows/                        # Step-by-step methodology (Antigravity reads these as guides)
│   ├── agent-kernel.md               # The System Kernel (debate protocol, citation law, etc.)
│   ├── AgentSpec.md                  # WHAT we're building (from /docs or project root)
│   ├── 00_START_HERE.md              # Framework guide files 00-09
│   ├── 01_QUICK_REFERENCE.md
│   ├── ...
│   └── 09_AUDIT_AND_MAINTENANCE.md
└── skills/                           # Reusable skills (Antigravity loads these semantically)
    ├── test-scaffold/
    │   └── SKILL.md                  # YAML frontmatter + instructions
    ├── factory-generator/
    │   └── SKILL.md
    └── [your-skills]/
```

**How Antigravity loads skills:** Unlike Cursor/Claude Code which read one rules file, Antigravity reads the `description` field in each skill's YAML frontmatter and decides *which skills are relevant to your prompt*. This means your `SKILL.md` descriptions must be precise and keyword-rich so the right skill triggers at the right time.

**Example SKILL.md for Antigravity:**
```yaml
---
name: test-scaffold
description: "Generate a Pytest test file with LLM-as-a-judge evaluation checks for any new AI agent. Triggers when creating tests, writing evals, or scaffolding a new agent's test suite. References 02_COMPLETE_GUIDE.md Section 6."
---

## Instructions
1. Read the agent's interface definition.
2. Create a test file at `tests/test_[agent_name].py`.
3. Include: unit tests with mocked LLM responses + LLM-as-a-judge eval test.
4. Reference: `02_COMPLETE_GUIDE.md` Section 6 (Testing Strategy & LLM Evals).
5. Register the test in `.build-context.md` Skills Registry.
```

**Syncing:** Run `./scripts/sync-kernel.sh` after any kernel, guide, or skill change. The script copies everything to `.agents/` automatically. For Gemini standalone (outside Antigravity), paste `agent.md` content into Custom Instructions manually.

---

## ⚖️ The Debate Protocol in Practice

The kernel defines three debate tiers. Here's how to work with them as a developer.

### What You'll See Day-to-Day

**Tier 1 (Sanity Checks):** These appear inline in the AI's response as small `⚖️ SANITY CHECK` blocks. They're quick — 3 lines. You don't need to do anything unless the verdict says "Escalate to Tier 2."

**Tier 2 (Full Council):** These appear as larger `⚖️ FULL COUNCIL` blocks with multiple roles debating. The AI auto-triggers these at architecture decisions, high-risk code, component swaps, and phase transitions. **Read the verdict and confirm or push back.** The AI will wait for your confirmation on Tier 2 before proceeding.

**Tier 3 (Human-Triggered):** You type `/debate [topic]`. Use this when:
- The AI's approach doesn't feel right but you can't articulate why
- You're torn between two options and want structured analysis
- A teammate disagrees with an AI suggestion and you want a tiebreaker

### When Each Tier Fires

| Trigger | Tier | What Happens |
|---------|------|-------------|
| Adding a new dependency | Tier 1 | Quick Builder + Protector check |
| Choosing between two approaches | Tier 1 | Quick comparison with risk note |
| Code touching external services | Tier 1 | Quick security + timeout check |
| Architecture decision | **Tier 2** | Full council with dissent + resolution |
| Risk Score 11+ (any code decision) | **Tier 2** | Full council — mandatory at high risk |
| Swapping a component | **Tier 2** | Full council via `/swap-component` |
| Phase transition | **Tier 2** | Full council via `/phase-check` |
| Creating or retiring a skill | **Tier 2** | Full council on reuse value |
| Audit findings requiring judgment | **Tier 2** | Full council on approve/defer/reject |
| Human types `/debate` | **Tier 3** | Full council, two approaches, human confirms |

### Tuning Debate Frequency

If debates feel too frequent for your team's pace, you can adjust in `agent.md`:
- **More debates:** Lower the Tier 2 auto-trigger threshold (e.g., trigger on Risk Score 5+ instead of 11+)
- **Fewer debates:** Raise the threshold or convert some Tier 2 triggers to Tier 1

The current defaults are calibrated for a small team building greenfield projects where getting the architecture right matters more than speed.

### When to Override a Debate Verdict

You're the human. You can always override. But:
1. Log your reasoning in `.build-context.md` under Architectural Decisions.
2. Explain *why* you're overriding (e.g., "time constraint," "client requirement").
3. The AI will respect your override in future sessions because it reads `.build-context.md`.

---

## 🛡️ THE "WORST-CASE" CODING STANDARD (Mandatory)

These rules are enforced by the kernel. They're documented here for reference.

**Rule 1: No Happy Paths.**
Assume every API call will timeout, every database connection will fail, and every user input is malicious.

- ❌ Bad: `response = api.get(url); return response.json()`
- ✅ Good: `try: response = api.get(url, timeout=5); response.raise_for_status(); ... except RequestException: handle_error()`

**Rule 2: The "KISS" Constraint (Keep It Simple, Stupid).**
Before building a "Multi-Agent RAG System with Vector Memory," ask: Can this be a 5-line Python script?

- If a simple solution works, the complex one is forbidden.
- Architect Role: You are the gatekeeper. Reject over-engineered PRs immediately.

**Rule 3: The 8-Step Debugging Protocol.**
When a bug is found, you MUST follow this exact sequence. Do not skip steps:

1. **Find:** Locate the exact line of failure.
2. **Reproduce:** Create a script that forces the error to happen.
3. **Prove (Repro):** Show the log output confirming the crash.
4. **Root Cause:** Explain why it failed (don't guess).
5. **Fix:** Write the code correction.
6. **Test:** Run the reproduction script again.
7. **Regression Check:** Run the full test suite to ensure nothing else broke.
8. **Prove (Fix):** Show the log output confirming success.

---

## 🧠 Context Loading Strategy

Because AI context windows are finite, do not dump all framework files into every prompt.

**The Optimal Context Loading Sequence:**

- **Always loaded (via kernel):** `agent.md`, `.build-context.md`, `.bugs_tracker.md`, `AgentSpec.md`.
- **On Project Start:** Have the AI read `00_START_HERE.md` and `01_QUICK_REFERENCE.md`.
- **When doing DevOps:** `@` or reference `06_INFRASTRUCTURE_AS_CODE.md` specifically.
- **When refactoring/swapping:** `@` or reference `08_AGNOSTIC_FACTORIES.md`.
- **When doing maintenance/audit:** `@` or reference `09_AUDIT_AND_MAINTENANCE.md`.

**Citation Law enforces this:** If the AI needs to cite a file it hasn't loaded, it must load it first, then cite it. No citing from memory.

---

## 🚫 Enforcing the Risk Score

If the AI tries to write code without knowing the risk score, it will guess the guardrails (usually getting them wrong).

**Your workflow when starting a new agent:**

> You: "Let's build a new agent that reads customer emails and drafts refund approvals. The Risk Score is 13 (High). Read `01_QUICK_REFERENCE.md` to see what guardrails are required, then propose the architecture."

If the AI starts coding immediately without guardrails, stop it:

> You: "Halt. You forgot the Risk Score 13 guardrails. Implement the Circuit Breaker and Human-in-the-loop HITL brake before writing the email parsing logic."

At Risk Score 11+, the kernel auto-triggers Tier 2 Full Council debates on every architectural decision. This is by design — high-risk systems deserve the extra scrutiny.

---

## 💬 Standardized Commands (Prompt Patterns)

These are defined in `agent.md` and work in any AI tool. Documented here for reference.

### `/new-agent [name] [risk-score]`

> "I want to create a new agent named [Name]. The Risk Score is [X]. Please:
> 1. Read `.build-context.md`.
> 2. Define its interface using our factory pattern.
> 3. Create a mock tool adapter for testing.
> 4. Write the Pytest file with LLM-as-a-judge Eval checks.
> Do not write the implementation until we agree on the tests."

Triggers a Tier 2 debate on architecture choice.

### `/swap-component [from] [to]`

> "We need to swap our [Database/LLM/Orchestrator] from [Current] to [New].
> Please read `08_AGNOSTIC_FACTORIES.md`. Write the new adapter class, add it to the factory, tell me what environment variable to update in `scale.yaml`, and update `.build-context.md` with this architectural decision."

Triggers a Tier 2 debate on the swap decision.

### `/run-audit`

> "Run the bi-annual audit process. Read `09_AUDIT_AND_MAINTENANCE.md` for the full procedure. Check dependencies, API contracts, framework guide recommendations, and skills. Generate the report at `docs/audits/AUDIT_REPORT_[DATE].md` and notify via the configured channel."

### `/new-skill [pattern-name]`

> "I've identified a repeating pattern: [describe the pattern and where it repeats].
> Please:
> 1. Read `.build-context.md` to check if a similar skill already exists in the Skills Registry.
> 2. Define the skill's interface (what it takes in, what it produces).
> 3. Write the skill implementation in `/skills/[skill-name]/`.
> 4. Include a `SKILL.md` with usage instructions and trigger conditions.
> 5. Add it to the Skills Registry in `.build-context.md`.
> 6. Write a test that validates the skill works in isolation."

Triggers a Tier 2 debate on whether the pattern is worth extracting.

### `/debate [topic]`

Triggers a Tier 3 Full Council debate. The AI must present two genuinely different approaches, have the Skeptic try to break both, and ask you to confirm before proceeding.

### `/status`

Reads `.build-context.md` and summarizes current state, active bugs, skills available, and upcoming audit.

### `/phase-check`

Evaluates which project phase you're in (Discovery → Build → Test → Deploy → Maintain) and whether all prerequisites for the next phase are met. Triggers a Tier 2 debate on the phase transition.

---

## 🧩 Skill Creation & Reuse

### When to Create a Skill

Skills are reusable, self-contained automation patterns that the AI assistant can invoke by name. They prevent the AI from reinventing the same solution every session.

**The "Rule of 3" trigger:** If you or the AI have written the same pattern three or more times — across features, projects, or audit cycles — it must be extracted into a skill.

**Common skill candidates:**
- Test scaffold generators (e.g., "create a Pytest file with LLM-as-a-judge for any new agent")
- Factory boilerplate (e.g., "create interface + adapter + factory for a new external service")
- Migration scripts (e.g., "generate an Alembic migration for this schema change")
- Deployment validators (e.g., "check that all env vars in scale.yaml exist in the secret manager")
- Audit sub-checks (e.g., "scan pyproject.toml for unmaintained packages")

### Skill File Structure

Each skill lives in `/skills/[skill-name]/` and contains a `SKILL.md` with YAML frontmatter (required for Antigravity compatibility) plus optional supporting files:

```text
/skills/
  /test-scaffold/
    SKILL.md          # YAML frontmatter + instructions (Antigravity-compatible)
    skill.py          # The implementation
    test_skill.py     # Validates the skill in isolation
  /factory-generator/
    SKILL.md
    skill.py
    test_skill.py
```

**SKILL.md format (all skills must follow this):**
```yaml
---
name: test-scaffold
description: "Generate a Pytest test file with LLM-as-a-judge evaluation checks for any new AI agent. Triggers when creating tests, writing evals, or scaffolding a new agent's test suite."
---

## Instructions
[Step-by-step instructions for the AI to follow]

## Examples
[Input/output examples]

## Constraints
[What the skill must NOT do]
```

The `description` field is critical — Antigravity uses it to decide when to load the skill. Make it keyword-rich and specific about trigger conditions.

### Skill Lifecycle

1. **Identify:** AI proposes during Phase 5 of the 5-Phase Loop.
2. **Create:** Use the `/new-skill` prompt pattern. AI writes the skill, test, and `SKILL.md`. Triggers Tier 2 debate.
3. **Register:** AI adds the skill to the Skills Registry in `.build-context.md`.
4. **Use:** AI invokes the skill by name in future sessions instead of rewriting the pattern.
5. **Audit:** During bi-annual audits, skills are reviewed for staleness (Layer 4 of `09_AUDIT_AND_MAINTENANCE.md`).

---

## 🔧 Troubleshooting AI Hallucinations

| Problem | AI Cause | Solution |
|---------|----------|----------|
| AI hardcodes OpenAI API calls | Default training bias | Point it to `08_AGNOSTIC_FACTORIES.md` and say "Use the LLM Factory." |
| AI forgets previous decisions | Context window pushed out | Say: "Read `.build-context.md` to refresh your memory." |
| AI writes monolithic code | Lazy generation | Say: "Refactor this into the Modular Monolith structure defined in `02_COMPLETE_GUIDE.md`." |
| AI installs random libraries | Pip hallucination | Say: "Check `pyproject.toml` and use `uv` for dependency management." |
| AI skips audit maintenance | No awareness of Step 8 | Say: "Read `09_AUDIT_AND_MAINTENANCE.md` and follow the audit checklist." |
| AI rebuilds the same pattern repeatedly | No skill awareness | Say: "We've built this 3 times. Use `/new-skill` to extract it into a reusable skill." |
| AI makes decision without citing a file | Citation Law violation | Say: "Which framework file supports that decision? Cite it or reconsider." |
| AI skips debate on a key decision | Kernel not loaded or ignored | Say: "This is an architecture decision. Run a Tier 2 Full Council debate before proceeding." |
| AI debates trivially simple tasks | Over-triggering | Adjust debate thresholds in `agent.md` — raise Tier 2 trigger level. |

---

## 📌 File Meta

**Version:** 1.5.0  
**Released:** March 8, 2026  
**Status:** Production Ready ✅  
**Part of:** 10-Part AI Agent Framework  

**Next File:** [05_BUILD_CONTEXT_AND_BUGS.md](./05_BUILD_CONTEXT_AND_BUGS.md) (Memory)
