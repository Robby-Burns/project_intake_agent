# 🔍 Audit & Maintenance - Bi-Annual Dependency Audit with HITL Sign-Off

**Version:** 1.5.0 | **Updated:** March 8, 2026 | **Part:** 10/10  
**Status:** Production Ready ✅  
**Purpose:** Keep deployed agents trustworthy over time through scheduled audits, mandatory human review, and automated CVE scanning.

---

## 📍 Purpose

A deployed agent that is never reviewed will drift. Its dependencies age, its API contracts change, and its framework recommendations become stale. This file defines the **scheduled maintenance system** that prevents silent decay.

**The Golden Rule:** "The audit proposes. The human disposes. Nothing is auto-applied. Ever."

---

## 🗺️ Quick Navigation

- [Why This Exists](#-why-this-exists)
- [Schedule & Triggers](#-schedule--triggers)
- [What It Checks (4 Layers)](#-what-it-checks-4-layers)
- [Severity Flags](#-severity-flags)
- [HITL — Why Human Sign-Off Is Mandatory](#-hitl--why-human-sign-off-is-mandatory)
- [Notification Channel Setup](#-notification-channel-setup)
- [Report Format & Sign-Off Workflow](#-report-format--sign-off-workflow)
- [API Interface Contracts](#-api-interface-contracts)
- [Setup Checklist](#-setup-checklist)

---

## 🔗 Related Files

**Depends on:** [03_DEPENDENCY_MANAGEMENT.md](./03_DEPENDENCY_MANAGEMENT.md) (What to audit)  
**Depends on:** [07_CONFIGURATION_CONTROL.md](./07_CONFIGURATION_CONTROL.md) (`scale.yaml` audit block)  
**Depends on:** [08_AGNOSTIC_FACTORIES.md](./08_AGNOSTIC_FACTORIES.md) (`get_notifier()` factory)  
**Feeds into:** [05_BUILD_CONTEXT_AND_BUGS.md](./05_BUILD_CONTEXT_AND_BUGS.md) (Audit History in `.build-context.md`)  
**Scheduled by:** [06_INFRASTRUCTURE_AS_CODE.md](./06_INFRASTRUCTURE_AS_CODE.md) (Deployment checklist)

---

## 🧠 Why This Exists

The Golden Rule of `03_DEPENDENCY_MANAGEMENT.md` is "Production is Frozen." But frozen means it was correct at the time you froze it. Without a scheduled review, you will eventually be running a dependency with a known CVE, calling a deprecated API endpoint, or relying on a library the maintainer archived two years ago. The audit is how you keep "frozen" from meaning "forgotten."

---

## 📅 Schedule & Triggers

### Primary Audit: Bi-Annual (March + September)

Runs automatically on the first Monday of March and September, at the time configured in `scale.yaml`.

```yaml
# config/scale.yaml (audit block)
audit:
  schedule_months: [3, 9]
  schedule_day: "first_monday"
  schedule_time: "06:00"
  schedule_timezone: "UTC"
```

Triggered by a scheduled task in your deployment environment (cron job, Cloud Scheduler, etc.). The scheduler calls `POST /audit/run` — the application does the scanning and report generation.

### Between Audits: Weekly CVE Scan

A lightweight weekly scan runs silently every Monday (when `cve_check_weekly: true` in `scale.yaml`). This checks only for **critical security vulnerabilities** in your current dependency tree. If a critical CVE is found, a notification fires immediately — it does not wait for the next scheduled audit.

The weekly scan calls `POST /audit/cve-check`. Non-critical findings are queued for the next bi-annual audit.

---

## 🔎 What It Checks (4 Layers)

### Layer 1: `pyproject.toml` Dependencies

Every package in your dependency tree is compared against its latest stable version:
- Changelog scanned for breaking changes
- Known CVEs flagged against current installed version
- Maintenance status checked (archived? unmaintained? last commit date?)
- License changes detected

### Layer 2: External API Contracts

Any API your system calls (LLM providers, broker APIs, data feeds, MCP servers) is checked against their published changelogs:
- Deprecated endpoints currently in your code flagged as CRITICAL
- New required parameters or auth changes flagged as WARNING
- Rate limit policy changes noted as INFO

### Layer 3: Framework Guides

Each file in `docs/guides/` is reviewed for recommendations that are no longer current:
- Tool recommendations that have been superseded
- Patterns that have known issues in newer runtime versions
- Proposed edits drafted for human review — the guides do not rewrite themselves

### Layer 4: Skills Review

Every skill registered in `.build-context.md` is reviewed for health:
- **Staleness:** Does the skill reference deprecated libraries, outdated API patterns, or superseded tools? If so, flag for update.
- **Redundancy:** Has a new library or framework feature made the skill unnecessary? If so, flag for retirement.
- **Coverage gaps:** Review `.bugs_tracker.md` and recent build history for repeating patterns that are *not* yet skills. If the same fix or scaffold has been applied 3+ times since the last audit, propose it as a new skill candidate.
- **Test health:** Do all skill test files still pass? A skill with a failing test is flagged CRITICAL.

Skills are proposed for creation, update, or retirement in the audit report alongside dependency and API findings. The human approves or rejects each proposal.

---

## 🚦 Severity Flags

```text
CRITICAL: Breaking change in new version | Known CVE | Deprecated endpoint in use
WARNING:  Soft deprecation | Minor version behind | Outdated recommendation
INFO:     Update available, no breaking changes
```

---

## 🛡️ HITL — Why Human Sign-Off Is Mandatory

The audit proposes. The human disposes.

This is not bureaucracy — it is risk management. Consider what can go wrong if a dependency update is auto-applied on a high-risk system:

- A new version of a broker library changes the order submission signature. **Auto-applied:** orders silently fail or submit with wrong parameters.
- A retry library changes its default backoff strategy. **Auto-applied:** your circuit breaker behavior changes in production without your knowledge.
- A guide recommendation changes the factory pattern. **Auto-applied:** the AI assistant follows the new pattern inconsistently across files.

A human who understands the system must read each proposed change and decide: safe to apply, defer to next quarter, or reject. That judgment cannot be delegated to automation on a system with real consequences.

`auto_apply` in `scale.yaml` is always `false`. There is no code path that sets it to `true`. The Pydantic config loader in `07_CONFIGURATION_CONTROL.md` raises a fatal error if it detects `auto_apply: true`.

---

## 📢 Notification Channel Setup

Configure where the "Audit report ready for your review" message is sent. This is set once in `scale.yaml` and uses the `get_notifier()` factory from `08_AGNOSTIC_FACTORIES.md`. Credentials go in `.env` (or your cloud's secret manager — never committed to the repo).

### Configuration

```yaml
# config/scale.yaml
audit:
  notification_channel: "slack"   # Options: slack | email | teams | webhook | none
  notification_link: "https://your-dashboard.com/audit"
```

```bash
# .env (or cloud secret manager)
# For Slack:
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...

# For Email:
SMTP_HOST=smtp.sendgrid.net
SMTP_FROM=audit@yourdomain.com
SMTP_TO=you@yourdomain.com

# For Teams:
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/...

# For generic webhook:
AUDIT_WEBHOOK_URL=https://...   # any endpoint accepting POST
```

### Channel Options

| Channel | Free at this volume? | Setup effort |
|---------|---------------------|--------------|
| Slack webhook | Yes | 5 minutes |
| Email (SendGrid/SMTP) | Yes (free tier) | 10 minutes |
| Teams webhook | Yes | 5 minutes |
| Generic webhook | Depends on endpoint | 5 minutes |
| None | N/A | Zero — report is generated, dashboard shows badge |

`none` is valid and appropriate for solo developers who prefer to check the dashboard manually or set a calendar reminder.

### Security Rule

The notification contains **only**: "Audit report ready. Review at [link]."

It **never** contains report contents. CVE details, dependency graphs, API key patterns, and endpoint lists must not be transmitted to third-party notification services. The human clicks the link and reviews the full report in the secured dashboard or local file.

---

## 📄 Report Format & Sign-Off Workflow

### Report Location

Generated at: `docs/audits/AUDIT_REPORT_[YYYY-MM-DD].md`

### Report Structure

Each item in the report has a checkbox for human decision:

```markdown
# Audit Report — [DATE]

## Summary
- Total items: [N]
- Critical: [N]
- Warning: [N]
- Info: [N]

---

## Layer 1: Dependencies

### [CRITICAL] requests 2.31.0 → 2.32.0
**Change:** New SSL verification behavior (breaking for custom cert chains)
**CVE:** None
**Recommendation:** Test with your custom CA bundle before applying.
- [ ] APPROVED
- [ ] DEFERRED (reason: _____________)
- [ ] REJECTED (reason: _____________)

### [INFO] fastapi 0.109.2 → 0.110.0
**Change:** Minor performance improvements, no breaking changes.
**CVE:** None
**Recommendation:** Safe to apply.
- [ ] APPROVED
- [ ] DEFERRED
- [ ] REJECTED

---

## Layer 2: API Contracts

### [CRITICAL] Anthropic API — /v1/complete endpoint
**Change:** Endpoint deprecated. Use /v1/messages instead.
**Impact:** Your LLM adapter calls /v1/complete in 3 locations.
**Recommendation:** Update ClaudeLLM adapter before deprecation deadline.
- [ ] APPROVED
- [ ] DEFERRED
- [ ] REJECTED

---

## Layer 3: Framework Guides

### [WARNING] 08_AGNOSTIC_FACTORIES.md — LangGraph import pattern
**Change:** LangGraph 0.1.0 changed the import path for StateGraph.
**Recommendation:** Update code example in guide and any project adapters.
- [ ] APPROVED
- [ ] DEFERRED
- [ ] REJECTED

---

## Layer 4: Skills

### [INFO] Skill: test-scaffold — Healthy
**Status:** All tests pass. No deprecated references found.
**Action:** None required.

### [WARNING] Skill: factory-generator — Stale dependency
**Issue:** Skill template imports `langgraph.graph` which moved to `langgraph.core.graph` in 0.1.0.
**Recommendation:** Update skill template to use new import path.
- [ ] APPROVED
- [ ] DEFERRED
- [ ] REJECTED

### [NEW] Proposed Skill: migration-validator
**Trigger:** Alembic migration validation has been performed manually 4 times since last audit.
**Recommendation:** Extract into a reusable skill at `/skills/migration-validator/`.
- [ ] APPROVED (create skill)
- [ ] DEFERRED
- [ ] REJECTED

---

## Sign-Off
**Reviewed by:** _______________
**Date:** _______________
**Signature:** _______________
```

### Post-Approval Workflow

1. Human reviews each item and checks APPROVED, DEFERRED, or REJECTED.
2. Human submits sign-off via dashboard (or commits the signed report file).
3. System applies **only** APPROVED items in a single batch.
4. Full test suite runs automatically post-apply.
5. **On any test failure:** full rollback to pre-audit state. The failed items are logged and flagged for the next audit.
6. Results recorded in `.build-context.md` under "Audit History" (see `05_BUILD_CONTEXT_AND_BUGS.md`).

---

## 🔌 API Interface Contracts

The audit system exposes three endpoints. These are interface contracts — the implementation lives in your application code following the factory patterns from `08_AGNOSTIC_FACTORIES.md`.

### `POST /audit/run`

**Purpose:** Triggers a full bi-annual audit scan.  
**Called by:** Scheduled task (cron, Cloud Scheduler, etc.)  
**Returns:** `202 Accepted` with a `report_id` for tracking.  
**Side effects:** Generates the report file. Sends notification via configured channel.

```json
// Response
{
  "status": "accepted",
  "report_id": "audit-2026-03-02",
  "report_path": "docs/audits/AUDIT_REPORT_2026-03-02.md",
  "notification_sent": true
}
```

### `POST /audit/cve-check`

**Purpose:** Runs the lightweight weekly CVE scan.  
**Called by:** Weekly scheduled task.  
**Returns:** `200 OK` with summary. Only sends notification if critical CVE found.

```json
// Response (no critical findings)
{
  "status": "clean",
  "packages_scanned": 47,
  "critical_cves": 0,
  "notification_sent": false
}

// Response (critical finding)
{
  "status": "alert",
  "packages_scanned": 47,
  "critical_cves": 1,
  "findings": ["requests==2.31.0: CVE-2026-XXXXX (severity: critical)"],
  "notification_sent": true
}
```

### `POST /audit/test-notify`

**Purpose:** Tests that the notification channel is configured correctly.  
**Called by:** Human, during initial setup.  
**Returns:** `200 OK` if notification delivered, `500` if configuration is broken.

```json
// Response
{
  "status": "delivered",
  "channel": "slack",
  "message": "Test notification from audit system. If you see this, setup is correct."
}
```

---

## ✅ Setup Checklist (Do This Before First Deploy)

- [ ] Set `audit.notification_channel` in `scale.yaml` (default is `none`)
- [ ] Set `audit.schedule_time` and `audit.schedule_timezone` in `scale.yaml`
- [ ] Add notification credentials to `.env` or cloud secret manager
- [ ] Schedule the bi-annual audit task in your deployment environment:
  - **Railway:** Use a Cron job service pointed at `POST /audit/run`
  - **GCP:** Cloud Scheduler → Cloud Run
  - **Azure:** Timer-triggered Function → Container App
  - **Docker:** Add a `scheduler` service to `compose.yaml`
- [ ] Schedule the weekly CVE scan: `POST /audit/cve-check` every Monday
- [ ] Confirm `audit.auto_apply: false` in `scale.yaml`
- [ ] Run `POST /audit/test-notify` to confirm notification delivery
- [ ] Verify the `docs/audits/` directory exists in your repo

---

## 📌 File Meta

**Version:** 1.5.0  
**Released:** March 8, 2026  
**Status:** Production Ready ✅  
**Part of:** 10-Part AI Agent Framework  

🏁 **THE FRAMEWORK IS COMPLETE.**
