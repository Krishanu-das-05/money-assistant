# money-assistant
Upload a bank or UPI statement and ask questions about your spending in plain language. 

## Local development

Requirements: Python 3.12 and [Podman](https://podman.io/). The commands below are for a
POSIX shell (Linux, macOS, or Git Bash on Windows).

```bash
# 1. Create and activate a virtualenv, then install the app with dev tools
python3.12 -m venv .venv
source .venv/bin/activate          # Git Bash on Windows: source .venv/Scripts/activate
pip install -e ".[dev]"

# 2. Create your local config (never commit .env)
cp .env.example .env

# 3. Start Postgres 16 in a Podman container (safe to re-run)
./scripts/dev-db.sh

# 4. Apply migrations
python manage.py migrate

# 5. Run the dev server, then open http://localhost:8000/healthz
python manage.py runserver

# 6. Lint and test
ruff check .
ruff format --check .
pytest
```

### Container image

```bash
podman build -f Containerfile -t money-assistant .

podman run --rm -p 8000:8000 \
  -e SECRET_KEY=change-me \
  -e ALLOWED_HOSTS=localhost,127.0.0.1 \
  -e DATABASE_URL=postgres://postgres:dev@host.containers.internal:5432/money \
  money-assistant

curl http://localhost:8000/healthz   # {"status": "ok", "db": "ok"}
```

The container listens on `$PORT` (default `8000`). `host.containers.internal` lets the app
container reach the Postgres started by `scripts/dev-db.sh` on the host.
