FROM python:3.13-slim-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN curl -fsSL https://ollama.com/install.sh | bash

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

COPY adapted_work /root/adapted_work
COPY requirements /root/requirements

WORKDIR /root

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"
ENV OLLAMA_MODEL=gemma3:1b

RUN uv pip install -r /root/requirements/requirements.txt --system

# Configura el comando CMD usando la sintaxis de lista de JSON
#CMD ["python", "-m", "uvicorn", "adapted_work.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["entrypoint.sh"]
