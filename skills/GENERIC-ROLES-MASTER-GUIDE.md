---
file: GENERIC-ROLES-MASTER-GUIDE.md
version: 1.0.0
description: How all generic roles work together in an Antigravity agent system
framework: Antigravity (adaptable to other frameworks)
---

# 📚 GENERIC ROLES MASTER GUIDE

This document explains how your **10 core roles** work together to build and operate an Antigravity agent system.

---

## 🎯 THE 10 CORE ROLES (What You Have)

| Role | Authority | Primary Job | Blocking Power |
|------|-----------|-------------|----------------|
| **Product Manager** | Strategic | Define mission, own success metrics, go/no-go | ✅ Can block launches |
| **Architect** | Technical | Design patterns, factory enforcement, tech decisions | ✅ Can block code |
| **Database Manager** | Technical | Schema, encryption, performance, backups | ✅ Can block deployments (data risk) |
| **Infosec Lead** | Security | Audits, kill switch, breach prevention | ✅ Can block (activate kill switch) |
| **DevOps Manager** | Operations | Deployment, costs, uptime, monitoring | ✅ Can block deployments |
| **Marketing Manager** | Strategic | Brand rules, final approval, messaging | ✅ Can block publication |
| **AI Engineer** | Technical | Implement agents, write code, optimize | ⚠️ Code review blocker (if violates patterns) |
| **QA Engineer** | Technical | Tests, coverage, quality gates | ✅ Can block deployments (tests fail) |
| **Data Analyst** | Insights | Track metrics, detect anomalies, dashboards | ⚠️ Informs decisions, doesn't block |
| **Compliance Officer** | Legal | GDPR/CCPA compliance, data retention, legal risk | ✅ Can block (legal liability) |

---

## 🔄 WORKFLOW: How Roles Work Together

### PHASE 1: PLANNING (Product Manager + Architect)

```
Product Manager defines:
├─ Mission: "Our system should [do X]"
├─ Success metrics: "[Metric 1], [Metric 2], [Metric 3]"
├─ Phase gates: "Ready to launch when [criteria met]"
└─ Scope boundaries: "Include [this], exclude [that]"

Architect reviews:
├─ "Can we build this with our tech stack?"
├─ "What patterns should we use?"
├─ "Any vendor lock-in risks?"
└─ Recommendation: "Yes, with [approach]" or "No, redesign needed"

Both agree on Phase 1 success criteria

→ APPROVED TO BUILD
```

### PHASE 2: BUILD (AI Engineer + Architect)

```
AI Engineer writes:
├─ Agent code (following Architect's patterns)
├─ Use factories (LLM factory, DB adapter, etc)
├─ Write unit tests
└─ Submit PR for code review

Architect reviews:
├─ Are factories used? ✅
├─ Any hardcoded vendor choices? ✅
├─ Any anti-patterns? ✅
└─ Tests prove swappability? ✅

QA Engineer reviews:
├─ Coverage >80%? ✅
├─ Performance tests? ✅
├─ Integration tests? ✅
└─ Ready for next phase?

Both approve → CODE MERGED
```

### PHASE 3: SECURITY (Infosec Lead + Database Manager)

```
Database Manager verifies:
├─ Sensitive data encrypted? ✅
├─ Access controls enforced? ✅
├─ Backups working? ✅
└─ Schema supports audit trail? ✅

Infosec Lead verifies:
├─ PII handling correct? ✅
├─ No secrets in logs/code? ✅
├─ Audit trail complete? ✅
└─ Kill switch tested? ✅

Both approve → SECURITY CLEARED
```

### PHASE 4: QUALITY (QA Engineer + Data Analyst)

```
QA Engineer verifies:
├─ All tests passing? ✅
├─ Latency acceptable? ✅
├─ Error rate <threshold? ✅
└─ Code coverage >80%? ✅

Data Analyst verifies:
├─ Can we measure success metrics? ✅
├─ Dashboard ready? ✅
├─ Baselines established? ✅
└─ Anomaly detection working? ✅

Both approve → QUALITY GATE PASSED
```

### PHASE 5: DEPLOYMENT (DevOps Manager + Infosec Lead)

```
DevOps Manager verifies:
├─ Infrastructure ready? ✅
├─ Cost within budget? ✅
├─ Monitoring configured? ✅
├─ Rollback plan ready? ✅
└─ Team trained? ✅

Infosec Lead verifies:
├─ Kill switch works? ✅
├─ Audit trail enabled? ✅
├─ Incident response ready? ✅
└─ Emergency procedures documented? ✅

Both approve → GO FOR DEPLOYMENT
```

### PHASE 6: EXECUTION (All Roles + Marketing Manager)

```
AI Engineer deploys code

Data Analyst monitors:
├─ Success metrics hitting targets?
├─ Error rate normal?
├─ Anomalies detected?
└─ Reports to Product Manager

Marketing Manager monitors:
├─ Brand compliance maintained?
├─ Quality high?
├─ Stakeholder communication?
└─ Approval gates working?

Infosec Lead monitors:
├─ Any security incidents?
├─ Audit trail complete?
├─ Kill switch ready?
└─ Compliance maintained?

DevOps Manager monitors:
├─ Uptime good?
├─ Cost on budget?
├─ Performance acceptable?
└─ No deployment issues?

All roles report weekly to Product Manager
```

---

## 🎤 COMMUNICATION STRUCTURE

### Daily Standup (Optional, if team >6 people)
```
Participants: Project Lead (optional) + 1 rep per role
Duration: 15 minutes

Each role says:
"[Role]: Status is [good/at-risk]. Blocker: [if any]. Help needed: [if any]."

Project Lead removes blockers between roles
```

### Weekly Sync (Mandatory)
```
Participants: All 10 roles
Duration: 60 minutes

Agenda:
1. [5 min] Product Manager: Status of success metrics
2. [5 min] Architect: Any tech blockers?
3. [5 min] AI Engineer: Code status
4. [5 min] QA Engineer: Quality status
5. [5 min] Data Analyst: Dashboard insights
6. [5 min] Infosec Lead: Security posture
7. [5 min] Database Manager: Data status
8. [5 min] DevOps Manager: Infrastructure status
9. [5 min] Marketing Manager: Brand/approval status
10. [5 min] Compliance Officer: Compliance status
11. [10 min] Open discussion (blockers, conflicts, decisions)

Output: Decisions made, action items assigned, next week's priorities
```

### Ad-Hoc Escalation (When Needed)
```
Trigger: Conflict between roles OR decision needed

Example:
"Architect and QA Engineer disagree: 
Is test coverage at 75% acceptable to deploy?"

Process:
1. Roles present their cases (2 min each)
2. Product Manager decides: "Code deploys with action item for 80% coverage in Phase 2"

Result: Escalation resolved, decision documented
```

---

## 🔗 DECISION AUTHORITY MATRIX

**Who makes the final call?**

```
Decision                          | Authority        | Approvers (can block)
----------------------------------|------------------|--------------------
Deploy to production?             | Product Manager  | QA, Infosec, DevOps
New tech stack component?         | Architect        | Product Manager
Schema change?                    | Database Manager | Architect, Infosec
Activate kill switch?             | Infosec Lead     | Product Manager (notified)
Brand approval for post?          | Marketing Mgr    | None (final call)
Success metric target?            | Product Manager  | Data Analyst (feasible?)
Cost optimization strategy?       | DevOps Manager   | Product Manager (budget)
PII redaction rules?              | Infosec Lead     | Compliance Officer
Compliance requirement?           | Compliance Ofc   | Product Manager (feasible?)
Agent performance acceptable?     | AI Engineer      | QA Engineer (tests pass?)
```

---

## 📊 THE ANTIGRAVITY WORKFLOW

In **Antigravity**, this is how the roles interact:

### Agent Manager (Orchestration)

```
Agent Manager has a task:
"Build [Feature]. Success = [Metric]. Ready by [Date]"

Who runs this task? 
→ Usually the most relevant role(s)
→ E.g., "AI Engineer builds, Architect reviews, QA verifies, Data Analyst measures"

Task workflow:
1. AI Engineer: Claim task → Work on code/agents
2. Architect: Code review on PR → Approve/block
3. QA Engineer: Test review → Approve/block
4. Data Analyst: Set up metrics → Approve
5. DevOps Manager: Deploy → Approve/block
6. Product Manager: Mark complete → Celebrate

If any role blocks:
→ Task stays open
→ Blocker notified in Slack
→ Role who blocked explains why
→ Fix applied
→ Re-review
→ Continue
```

### Context Files (Documentation)

```
Pinned context files in Agent Manager:
├─ .claude-context.md (current status)
├─ MISSION_AND_SUCCESS_METRICS.md (Product Manager)
├─ ARCHITECTURE.md (Architect)
├─ SECURITY_REQUIREMENTS.md (Infosec Lead)
├─ DATABASE_SCHEMA.md (Database Manager)
├─ DEPLOYMENT_CHECKLIST.md (DevOps Manager)
├─ BRAND_RULES.md (Marketing Manager)
└─ COMPLIANCE_REQUIREMENTS.md (Compliance Officer)

Each role is responsible for keeping their doc current
```

---

## 🛑 WHEN ROLES DISAGREE

**Conflict Resolution Process:**

```
Scenario: Architect and QA Engineer disagree on code review

Conflict: 
Architect: "Code uses factories correctly, ship it"
QA: "Coverage only 72%, we need 80%"

Resolution:
1. Present positions (2 min each)
2. Product Manager decides: "Can we ship with 72% and 80% goal in Phase 2?"
3. Decision: "Yes, block deployment, fix before Phase 2"
4. Action: QA writes improvement stories, Architect reviews
5. Result: Team knows decision, moves forward

Key: Product Manager breaks ties (aligns with mission)
```

---

## 📋 ONBOARDING A NEW TEAM MEMBER

**Day 1:**
- Read: MISSION_AND_SUCCESS_METRICS.md (15 min)
- Read: Their role skill (30 min)
- Read: ARCHITECTURE.md (15 min)
- Understand: Who owns what (30 min)
- Understand: How to talk to other roles (15 min)

**Day 2:**
- See: Live Agent Manager tasks
- See: Live communication in Slack
- Ask: Questions answered by their role mentor
- Ready: To contribute

**Week 1:**
- Sit in on meetings
- Review their role's responsibilities
- Run their first task
- Get feedback
- Integrate into team

---

## 🎯 SUCCESS METRICS FOR THE WHOLE TEAM

```
MISSION EXECUTION
├─ Primary metric hitting target? ✅
├─ Secondary metrics on track? ✅
├─ Phase gates passing? ✅
└─ Deadline met? ✅

TEAM HEALTH
├─ All roles happy/productive? ✅
├─ Decisions being made quickly? ✅
├─ Communication clear? ✅
├─ Conflicts resolved constructively? ✅
└─ Velocity stable/improving? ✅

TECHNICAL HEALTH
├─ Code quality high? ✅
├─ Tests comprehensive? ✅
├─ Security posture strong? ✅
├─ Infrastructure reliable? ✅
└─ Costs on budget? ✅
```

---

## 🔄 SCALING: What to Add When

| Team Size | Add | Why |
|-----------|-----|-----|
| 1-3 people | Nothing (one person multiple roles) | Too small to specialize |
| 3-5 | Keep 10 roles, rotate | Roles can overlap |
| 5-8 | Hire 1-2 people per role | Specialization helps |
| 8-15 | Full team (1 per role), add Project Lead | Coordination becomes critical |
| 15-25 | Add from "missing roles" list | More complex requirements |
| 25+ | Add middle management / domain experts | Scale challenges emerge |

---

## ✅ QUICK START: Your First Week

**Monday:** PM + Architect define Phase 1 together
**Tuesday:** AI Engineer + Architect design solution
**Wednesday:** AI Engineer builds, QA Engineer writes tests
**Thursday:** Infosec Lead + DB Manager audit, DevOps Manager plans deployment
**Friday:** Weekly sync, celebrate progress, plan next week

**Result:** By Friday, you have your first working prototype!

---

## 🚀 THE POWER OF THIS STRUCTURE

```
✅ Clear ownership (every decision has an owner)
✅ Built-in oversight (every role reviews others' work)
✅ Risk management (multiple perspectives catch issues)
✅ Scalable (structure works from 3 people to 30)
✅ Antigravity-native (works with agent paradigm)
✅ Reusable (same structure for every project)
```

---

## 🔄 HOW TO ADAPT FOR YOUR PROJECT

1. **Copy this master guide**
2. **For each role:** Customize [YOUR PROJECT] placeholders
3. **Add missing roles:** Use MISSING-ROLES-ASSESSMENT.md
4. **Define success metrics:** Product Manager fills in
5. **Define communication cadence:** Weekly sync minimum
6. **Document decisions:** Keep decision log (decision → owner → date → reasoning)

---

**This structure is your governance model. It scales from MVP to production.** 🚀
