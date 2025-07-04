FROM python:3.12-slim-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        ffmpeg \
        libsm6 \
        libxext6

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /usr/local/lwglg/nld-img-heat-map

# Copy the necessary project files
COPY ./.python-version ./.python-version
COPY ./pyproject.toml ./pyproject.toml
COPY ./uv.lock ./uv.lock
COPY ./src ./src

# Sync the project into a new environment, installing only non-dev packages, using the frozen lockfile
RUN uv sync --frozen --no-dev

# Application startup command
CMD [ "uv", "run", "python", "-m", "src" ]

