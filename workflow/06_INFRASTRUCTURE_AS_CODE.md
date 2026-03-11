# 🏗️ Infrastructure as Code - Container-First Deployment

**Version:** 1.5.0 | **Updated:** March 8, 2026 | **Part:** 7/10  
**Status:** Production Ready ✅  
**Purpose:** Define reproducible, version-controlled cloud infrastructure using Containers and Terraform.

---

## 📍 Purpose

This file teaches you to deploy AI agents to production using **Infrastructure as Code (IaC)** and **Container-First** principles.

**The Golden Rule:** "If it doesn't run in `docker run`, it doesn't exist."

We do **not** use platform-specific builders (e.g., Vercel Python Builders, Heroku Buildpacks). We deliver a sealed artifact (Docker container) that runs identically on a laptop, a $5 VPS, or a massive Kubernetes cluster.

---

## 🗺️ Quick Navigation

- [The "Container-First" Strategy (Mandatory)](#-the-container-first-strategy-mandatory)
- [Kill Switch Patterns (Safety)](#-kill-switch-patterns-safety)
- [Docker Compose (Local Dev = Prod)](#-docker-compose-local-dev--prod)
- [The Agnostic Dockerfile Template](#-the-agnostic-dockerfile-template)
- [Terraform Basics](#-terraform-basics-infrastructure-definition)
- [Deployment Checklist](#-deployment-checklist)

---

## 🐳 The "Container-First" Strategy (Mandatory)

**The Problem:** "It works on my machine (Mac/Windows) but fails on Railway/Azure/Fly (Linux)."
**The Cause:** Relying on magic cloud builders or local environment variables.

**The Solution:**
We **NEVER** deploy code directly. We deploy a **Container**.

### Rule 1: One Dockerfile to Rule Them All
Your repository must have a single `Dockerfile` at the root. This is the **only** source of truth for dependencies, OS version, and Python runtime.

### Rule 2: Local Dev = Production
You must run your agent locally using `docker compose up`, not just `python main.py`.
* **If it works in Docker locally**, it **will** work on the cloud.
* **If it fails in Docker locally**, you fix it locally. **Never debug in the cloud.**

### Rule 3: No Platform Configs
* ❌ **Banned:** `vercel.json`, `netlify.toml`, `Procfile` (unless wrapping Docker).
* ✅ **Required:** `Dockerfile`, `compose.yaml`, `main.tf`.

---

## 🛑 Kill Switch Patterns (Safety)

For agents with a Risk Score of **11-17**, you must implement an infrastructure-level kill switch that completely isolates the agent from the outside world without deleting the database.

**Terraform Implementation (Network Isolation):**
Create a specific Security Group or VPC Network Rule that drops all **outbound** traffic.

1. **The "Red Button" Tag:**
   Define a resource tag `ProjectState = "Emergency"`.
2. **The Rule:**
   If `ProjectState == "Emergency"`, apply a Network Policy that blocks `0.0.0.0/0` outbound.
3. **Result:**
   The agent stays "on" (logs are visible), but it cannot spend money, call LLMs, or email customers.

---

## 💻 Docker Compose (Local Dev = Prod)

Always define your local multi-agent environment alongside your observability stack so you can trace agent decisions before pushing to the cloud.

**`compose.yaml`**
```yaml
version: '3.8'

services:
  # Your Agent
  agent-api:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/agents
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger:4317
      - RISK_SCORE=13
    depends_on:
      - db
      - jaeger

  # Local Database (Mirrors Production)
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=agents
    ports:
      - "5432:5432"

  # Local Observability
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686" # UI
      - "4317:4317"   # OTLP gRPC
```

---

## 📄 The Agnostic Dockerfile Template

Use this optimized template to ensure fast builds and security.

```dockerfile
# 1. Use a slim, secure base image
FROM python:3.11-slim-bookworm

# 2. Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# 3. Install system dependencies (curl for healthchecks)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Use UV for lightning-fast installs (optional but recommended)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 5. Set work directory
WORKDIR /app

# 6. Install dependencies
COPY pyproject.toml .
RUN uv pip install --system -r pyproject.toml

# 7. Copy application code
COPY . .

# 8. Create a non-root user for security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# 9. Expose the port (matches compose.yaml)
EXPOSE 8080

# 10. Healthcheck (Mandatory for Production)
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# 11. Run the application
ENTRYPOINT ["python", "-m", "app.main"]
```

---

## 🧱 Terraform Basics (Infrastructure Definition)

If using AWS, Azure, or GCP, define your container runner here.

**`main.tf` (Simplified Example)**
```terraform
# The "Container Runner" Pattern
resource "google_cloud_run_service" "agent" {
  name     = "research-agent"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/my-project/agent:latest"
        
        # Inject Secrets (Never hardcode API keys)
        env {
          name = "OPENAI_API_KEY"
          value_from {
            secret_key_ref {
              name = "openai-key"
              key  = "latest"
            }
          }
        }
      }
    }
  }
}
```

---

## ✅ Deployment Checklist

### Before Production Deployment

- [ ] **Docker Run Test:** Does `docker compose up` work cleanly on a fresh machine?
- [ ] **Secret Audit:** Are all API keys in the Secret Manager (not `.env`)?
- [ ] **Kill Switch:** Do I know exactly how to sever the network connection?
- [ ] **Health Check:** Is the `/health` endpoint returning `200 OK`?
- [ ] **Database Migration:** Have I applied the schema changes?

### Audit Scheduler Setup (Required Before Production)

- [ ] Notification channel set in `scale.yaml` (`audit.notification_channel`)
- [ ] Notification credentials in environment secrets (not `.env` committed to repo)
- [ ] Cron job or scheduled task configured to call `POST /audit/run` every 6 months (March + September)
- [ ] Weekly CVE scan scheduled: `POST /audit/cve-check` every Monday
- [ ] `POST /audit/test-notify` called to confirm notification delivery
- [ ] `audit.auto_apply: false` confirmed in `scale.yaml`

Why this is in the deployment checklist and not just the audit docs: If you deploy without scheduling the audit trigger, it will never run. The scheduler is infrastructure, not application logic.

### Troubleshooting Deployment

If a deployment fails, check in this exact order:

1. **Local Docker:** Does it run locally? (If no, fix it there).
2. **Environment Variables:** Did you forget to set a new key in the Cloud Dashboard?
3. **Logs:** "Container failed to start" usually means a missing dependency or immediate crash.
4. **Network:** Can the container reach the database? (Check VPC/Allow-list).

---

## 📌 File Meta

**Version:** 1.5.0  
**Released:** March 8, 2026  
**Status:** Production Ready ✅  
**Part of:** 10-Part AI Agent Framework  

**Next File:** [07_CONFIGURATION_CONTROL.md](./07_CONFIGURATION_CONTROL.md) (Cost & Config)
