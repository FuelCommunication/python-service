FROM python:3.13-slim AS base

FROM base AS builder
# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable

# Copy the project into the image
ADD app /app/app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

FROM base AS final
RUN useradd -m -u 1000 appuser

# Copy the application files into the final image
COPY --from=builder /app /app


# Add python virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Set the working directory
WORKDIR /app

USER appuser

# Expose the port the app runs on
EXPOSE 80

# Run the app with the Litestar CLI
CMD ["litestar", "--app", "app.main:app", "run", "--host", "0.0.0.0", "--port", "3002"]