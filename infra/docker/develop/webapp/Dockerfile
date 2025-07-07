FROM python:3.12-slim

# Installing dependencies
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update \
    && apt-get install -y \
        ffmpeg \
        libsm6 \
        libxext6

# Installing uv
COPY --from=ghcr.io/astral-sh/uv:0.6.1 /uv /uvx /bin/

# Change the working directory to the "nld-img-heat-map" directory
WORKDIR /usr/local/nld-img-heat-map

# Installing dependencies
COPY ./.python-version ./.python-version
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy the project into the image
COPY ./webapp ./webapp

# Copy the static files
COPY ./resources/static ./static

# Copy the config files for develop tools
COPY ./pytest.ini ./pytest.ini
COPY ./ruff.toml ./ruff.toml
COPY ./.dive-ci.yaml ./.dive-ci.yaml
COPY ./.dive-ui.yaml ./.dive-ui.yaml

# Copy the webapp config file
COPY ./infra/docker/develop/webapp/webapp-config.yml ./webapp-config.yml

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --locked

# Application entrypoint command
ENTRYPOINT [ "uv", "run" ]
