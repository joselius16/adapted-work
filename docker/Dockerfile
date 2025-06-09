FROM python:3.13-slim-bookworm

# Create group and user
RUN groupadd --gid 1000 adapted_work && \
    useradd --uid 1000 --gid adapted_work --shell /bin/bash --create-home adapted_work

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer for ollama
RUN curl -fsSL https://ollama.com/install.sh | bash

# Switch user
USER adapted_work
WORKDIR /home/adapted_work

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy folders
COPY --chown=adapted_work:adapted_work adapted_work ./adapted_work
COPY --chown=adapted_work:adapted_work requirements ./requirements
COPY --chown=adapted_work:adapted_work docker/entrypoint.sh ./entrypoint.sh

RUN chmod +x /home/adapted_work/entrypoint.sh

# Activate venv
RUN /home/adapted_work/.local/bin/uv venv .venv
ENV VIRTUAL_ENV="/home/adapted_work/.venv"
ENV PATH="/home/adapted_work/.venv/bin:/home/adapted_work/.local/bin:$PATH"
ENV OLLAMA_MODEL=gemma3:1b

# Install requirements
RUN /home/adapted_work/.local/bin/uv pip install -r /home/adapted_work/requirements/requirements.txt

# Execute entrypoint
CMD ["/home/adapted_work/entrypoint.sh"]
