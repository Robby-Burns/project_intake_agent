# 🏗️ Production-Grade Dockerfile for ProjectIntakeAgentThree
# This file implements the "Container-First" strategy, ensuring a reproducible build environment.
# It follows the principles of security (non-root user) and efficiency (multi-stage build).
# Reference: agent.md - The System Kernel for AI behavior and rules.
# Reference: workflow/06_INFRASTRUCTURE_AS_CODE.md

# Stage 1: Builder (Install dependencies)
FROM python:3.12-slim AS builder
WORKDIR /app

# Install system dependencies (curl, build-essential)
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files
COPY pyproject.toml .

# Install dependencies using uv
RUN uv pip install --system --no-cache -r pyproject.toml

# FIX: Download the spaCy model data into this builder stage
# Default to the small model for faster builds; can be overridden.
ARG SPACY_MODEL=en_core_web_sm
RUN python -m spacy download ${SPACY_MODEL}

# Stage 2: Runtime (Slim production image)
FROM python:3.12-slim
WORKDIR /app

# Copy installed dependencies and spaCy model from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Create a non-root user for security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose Streamlit port
EXPOSE 8501

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Healthcheck (Mandatory for Production)
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "app/ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
