# 🤖 AI Assistant Integration - Claude Code, Cursor, & Google Code Assistant

**Purpose:** Maximize AI productivity by teaching it how to work with this framework  
**Target Audience:** Developers using Claude Code, Cursor, or Google Code Assistant  
**Impact:** 50% faster development, fewer hallucinations, better code quality

---

## 🚨 The Golden Rule

**"AI assistants are only as good as their context."**

If you don't tell the AI about the framework, it will:
- Invent its own (bad) structure
- Hardcode dependencies
- Ignore security guardrails
- Forget previous decisions
- Create bugs you already fixed

**Solution:** Give it the context it needs using the System Prompt below.

---

## 🧠 System Prompt / Custom Instructions

**Copy and paste this into your AI assistant's custom instructions or system prompt:**

```markdown
You are an expert AI Agent Developer using the "AI Agent Development Framework".

CORE RULES:
1. READ FIRST: Always read /docs/01_QUICK_REFERENCE.md and .claude-context.md before starting.
2. PROCESS: Follow the 7-step process for every project (Discovery -> Risk -> Guardrails -> Architecture -> Review -> Build -> Deploy).
3. DEPENDENCIES: NEVER use '==' in requirements.txt. Use flexible versions (>=, <). Create requirements-lock.txt for production.
4. CONTEXT: Update .claude-context.md after every significant change.
5. BUGS: Check .bugs_tracker.md before writing code. Log new bugs immediately.
6. SECURITY: Implement guardrails based on Risk Score (0-14).
7. TESTING: Aim for 80% test coverage (Unit, Integration, E2E).
8. PATTERNS: Use the Database Adapter Pattern and Multi-LLM Debate Pattern where appropriate.

FILE STRUCTURE:
- /docs: Framework documentation
- /app: Application code (agents, tools, db, guardrails)
- /tests: Tests (unit, integration, e2e)
- .claude-context.md: Project state & memory
- .bugs_tracker.md: Bug tracking

WHEN WRITING CODE:
- Use Python 3.11+ type hinting.
- Use Pydantic v2 for data validation.
- Use LangChain/LangGraph for agent logic.
- Use pytest for testing.
- Docstrings for all functions/classes.

BEHAVIOR:
- Ask clarifying questions during Discovery (Step 1).
- Calculate Risk Score before suggesting architecture.
- Refuse to build without guardrails if Risk > 5.
- Proactively suggest updates to .claude-context.md.
```

---

## 🛠️ Setup Guide by Tool

### 1. Claude Code (CLI)

**Setup:**
1. Create a file named `.claude_config.md` (or similar, depending on current CLI version support for context) or simply ensure the `/docs` folder is present.
2. When starting a session, run:
   ```bash
   claude "Read /docs/01_QUICK_REFERENCE.md and .claude-context.md. Let's work on [TASK]."
   ```

**Best Practice:**
- Keep `.claude-context.md` updated.
- Use the `git` integration to let Claude see recent changes.

### 2. Cursor (IDE)

**Setup:**
1. Go to **Settings > General > Rules for AI**.
2. Paste the System Prompt from above.
3. Enable "Include .cursorrules file" if you want project-specific rules.

**Project-Specific Rules (`.cursorrules`):**
```markdown
# .cursorrules
ALWAYS read .claude-context.md at the start of a conversation.
Use the patterns defined in /docs/02_COMPLETE_GUIDE.md.
Update .bugs_tracker.md if we find a bug.
```

**Best Practice:**
- Use `@docs` to reference the documentation folder.
- Use `@.claude-context.md` to give immediate context.

### 3. Google Code Assistant (IDX / VS Code)

**Setup:**
1. Add the System Prompt to your workspace settings or user instructions if available.
2. If not, start every session with:
   "Act as an expert developer using the framework in /docs. Read 01_QUICK_REFERENCE.md first."

---

## 🗣️ Effective Prompts

### Discovery Phase
> "Let's start a new project. Read /docs/01_QUICK_REFERENCE.md and guide me through Step 1: Discovery. Ask me the 5 key questions."

### Architecture Phase
> "Based on the discovery, calculate the Risk Score using the formula in /docs/02_COMPLETE_GUIDE.md. Then suggest an architecture pattern."

### Coding Phase
> "Implement the 'Research Agent' following the pattern in /docs/02_COMPLETE_GUIDE.md section 9. Use the Database Adapter pattern. Update .claude-context.md when done."

### Debugging Phase
> "I found a bug: [DESCRIPTION]. Check .bugs_tracker.md for similar issues. Fix it, then update .bugs_tracker.md and .claude-context.md."

### Documentation Phase
> "Generate the README.md and ARCHITECTURE.md based on the current project state in .claude-context.md."

---

## 🔄 Common Workflows with AI

### 1. The "Start Right" Workflow
1. **User:** "New project. Read docs."
2. **AI:** Reads docs, asks Discovery questions.
3. **User:** Answers questions.
4. **AI:** Calculates Risk, suggests Architecture.
5. **User:** Approves.
6. **AI:** Generates file structure and config files.

### 2. The "Feature Build" Workflow
1. **User:** "Build [FEATURE]. Check .claude-context.md first."
2. **AI:** Checks context, identifies necessary files.
3. **AI:** Writes code + tests.
4. **User:** Runs tests.
5. **AI:** Fixes issues, updates .claude-context.md.

### 3. The "Bug Fix" Workflow
1. **User:** "Fix bug [ID] from .bugs_tracker.md."
2. **AI:** Reads bug details, reproduces issue.
3. **AI:** Implements fix, adds test case.
4. **AI:** Updates .bugs_tracker.md (moves to Resolved).

---

## ⚠️ Troubleshooting AI Behavior

| Issue | Cause | Solution |
|-------|-------|----------|
| **AI ignores framework** | Context window overload or didn't read docs | "Stop. Read /docs/01_QUICK_REFERENCE.md again. Follow the 7-step process." |
| **AI hardcodes versions** | Training bias towards `==` | "Check /docs/03_DEPENDENCY_MANAGEMENT.md. Use flexible versions (>=)." |
| **AI forgets project state** | .claude-context.md is stale | "Read .claude-context.md. I updated it with the latest changes." |
| **AI suggests bad security** | Ignored Risk Score | "Calculate the Risk Score again. What guardrails are required for this score?" |
| **AI writes spaghetti code** | Missed architecture patterns | "Refactor using the Modular Monolith pattern from /docs/02_COMPLETE_GUIDE.md." |

---

## 🎓 Advanced Tips

### 1. Context Optimization
AI context windows are large but not infinite.
- **Don't** paste all docs every time.
- **Do** reference specific files: "Read /docs/02_COMPLETE_GUIDE.md Section 7."

### 2. "Memory" Enforcement
If the AI keeps forgetting things:
- Ask it to **summarize** .claude-context.md at the start.
- "What is the current project phase and active task according to .claude-context.md?"

### 3. Self-Correction
Teach the AI to check its own work:
- "Before showing me the code, verify it against the rules in /docs/03_DEPENDENCY_MANAGEMENT.md."

---

## 📝 Checklist for AI Integration

- [ ] System Prompt installed/configured.
- [ ] /docs folder present in project.
- [ ] .claude-context.md created and initialized.
- [ ] .bugs_tracker.md created.
- [ ] AI confirmed it has read the docs.

---

**Remember:** The AI is a powerful engine, but **you** are the steering wheel. Use the docs to keep it on the road. 🚗💨

*Version 1.0.0 | Last Updated: February 2026*
