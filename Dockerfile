# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files
COPY requirements.txt .

# Install dependencies using uv
# We use --system to install into the system python environment (standard for Docker)
RUN uv pip install --system --no-cache -r requirements.txt

# Download Spacy Model (Default to Large for Production)
# You can override this build arg, but usually production images should have the model baked in
ARG SPACY_MODEL=en_core_web_lg
RUN python -m spacy download ${SPACY_MODEL}

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV SPACY_MODEL=${SPACY_MODEL}

# Run Streamlit
CMD ["streamlit", "run", "app/ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
