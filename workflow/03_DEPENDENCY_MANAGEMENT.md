# 📦 Dependency Management - Python Setup & Reproducible Builds

**Version:** 1.5.0 | **Updated:** March 8, 2026 | **Part:** 4/10  
**Status:** Production Ready ✅  
**Purpose:** Ensure reproducible builds across Dev, Staging, and Production environments

---

## 📍 Purpose

This file teaches you to manage Python dependencies correctly so:
- Development is flexible (easy to experiment)
- Production is frozen (exact, reproducible versions)
- No "works on my machine but not production" surprises
- Security updates happen automatically in dev
- Production never breaks unexpectedly
- **Orchestration frameworks (LangGraph, CrewAI) remain optional and pluggable**

**Golden Rule:** "Development is Flexible. Production is Frozen."

**Long-term health:** Dependencies that are "frozen" today will age. The bi-annual audit in `09_AUDIT_AND_MAINTENANCE.md` ensures your lock file doesn't become a liability. This file handles the *how* of dependency management; File 09 handles the *when* of reviewing them.

---

## 🗺️ Quick Navigation

- [The Golden Rule](#-the-golden-rule)
- [File Structure](#-file-structure)
- [The 2026 Standard: uv](#-the-2026-standard-using-uv)
- [Essential Dependencies](#-essential-dependencies-for-2026)
- [Agnostic Orchestration Extras](#-agnostic-orchestration-extras)
- [Docker Integration](#-docker-integration)
- [pyproject.toml Configuration](#-projecttoml-configuration)
- [Workflow Examples](#-workflow-examples)
- [Troubleshooting](#-troubleshooting)

---

## 🔗 Related Files

**Before this:** [02_COMPLETE_GUIDE.md](./02_COMPLETE_GUIDE.md) (Deep methodology)  
**This file:** [03_DEPENDENCY_MANAGEMENT.md](./03_DEPENDENCY_MANAGEMENT.md) (You are here)  
**After this:** [04_AI_ASSISTANT_INTEGRATION.md](./04_AI_ASSISTANT_INTEGRATION.md) (AI assistant setup)  
**For production:** [06_INFRASTRUCTURE_AS_CODE.md](./06_INFRASTRUCTURE_AS_CODE.md) (Terraform + Docker)  
**For ongoing maintenance:** [09_AUDIT_AND_MAINTENANCE.md](./09_AUDIT_AND_MAINTENANCE.md) (Bi-annual audit)

---

## ⚡ The Golden Rule

> **"Development is Flexible. Production is Frozen."**

### What This Means

```text
Requirements.txt:        requirements-lock.txt:
langchain>=0.1.0         langchain==0.1.15
openai>=1.0.0            openai==1.3.7
fastapi>=0.109.0         fastapi==0.109.2

Dev: Uses latest patches  Prod: Exact versions only
Allows security updates   No surprises in production
```

---

## 🛠️ The 2026 Standard: Using `uv`

### Why `uv` Over pip?

| Feature | pip | uv | Winner |
|---------|-----|----|----|
| **Speed** | Slow (Python) | ⚡ 10-100x faster (Rust) | uv |
| **Resolution** | Sometimes errors | Smart resolver | uv |
| **Lock file** | Requires pip-tools | Built-in | uv |

**Recommendation:** Use `uv` locally, keep pip as fallback.

### Basic Workflow

```bash
# 1. Create virtual environment
uv venv

# 2. Activate it
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 3. Install from flexible requirements
uv pip install -r requirements.txt

# 4. Generate lock file (exact versions)
uv pip compile requirements.txt -o requirements-lock.txt

# 5. Production: use locked versions
uv pip install -r requirements-lock.txt
```

---

## 📋 Essential Dependencies for 2026

### Core Application
```text
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
python-dotenv>=1.0.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0 
requests>=2.31.0
aiohttp>=3.9.0 
```

### AI & LLM Providers (Agnostic)
```text
anthropic>=0.18.0
openai>=1.0.0
google-generativeai>=0.3.0
```

### Observability (Required for Production)
```text
opentelemetry-api>=1.20.0
opentelemetry-sdk>=1.20.0
opentelemetry-exporter-otlp>=1.20.0
opentelemetry-instrumentation-fastapi>=0.41b0
```

---

## 🧩 Agnostic Orchestration Extras

To support multiple agent routing paradigms (LangGraph vs. CrewAI) without bloating the base application, use optional dependencies in `pyproject.toml`.

### Structured Outputs & Evals
```text
pydantic-ai>=0.0.1
instructor>=1.0.0
```

### Multi-Agent Engines
```text
langgraph>=0.0.25
crewai>=0.11.0
```

---

## 🔧 pyproject.toml Configuration

### Modern Python Project Setup

Create `pyproject.toml`:

```toml
[project]
name = "my-ai-agent"
version = "1.0.0"
description = "Production AI Agent Framework"
requires-python = ">=3.11"

dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "anthropic>=0.18.0",
    "sqlalchemy>=2.0.0",
    "psycopg2-binary>=2.9.0",
    "redis>=5.0.0",
    "pydantic>=2.0.0",
    "python-dotenv>=1.0.0",
    "opentelemetry-api>=1.20.0",
    "opentelemetry-sdk>=1.20.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "pytest-asyncio>=0.21.0",
    "ruff>=0.1.0",
    "black>=23.0.0",
]
orchestration_langgraph = ["langgraph>=0.0.25"]
orchestration_crew = ["crewai>=0.11.0"]
structured_outputs = ["pydantic-ai>=0.0.1", "instructor>=1.0.0"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
addopts = "-v --cov=app --cov-report=term-missing:skip-covered"
```

---

## 🐳 Docker Integration

### Multi-Stage Build (Optimized)

Create `Dockerfile`:

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim AS builder
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY requirements-lock.txt .
RUN uv venv && uv pip install -r requirements-lock.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📌 File Meta

**Version:** 1.5.0  
**Released:** March 8, 2026  
**Status:** Production Ready ✅  
**Part of:** 10-Part AI Agent Framework  

**Next File:** [04_AI_ASSISTANT_INTEGRATION.md](./04_AI_ASSISTANT_INTEGRATION.md) (AI Setup)
