FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000

WORKDIR /app

RUN useradd --create-home --uid 10001 app

COPY pyproject.toml README.md ./
RUN pip install .

COPY . .

# Throwaway values so settings load; nothing here is used at runtime.
RUN SECRET_KEY=collectstatic-only DATABASE_URL=sqlite:///:memory: \
    python manage.py collectstatic --noinput

USER app

EXPOSE 8000

CMD ["sh", "-c", "exec gunicorn config.wsgi --bind 0.0.0.0:${PORT}"]
