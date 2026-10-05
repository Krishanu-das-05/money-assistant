#!/usr/bin/env bash
# Start the local development Postgres with Podman. Safe to run repeatedly.
set -euo pipefail

NAME=ma-postgres

if podman container exists "$NAME"; then
  podman start "$NAME"
else
  podman run -d --name "$NAME" \
    -e POSTGRES_PASSWORD=dev \
    -e POSTGRES_DB=money \
    -p 5432:5432 \
    docker.io/library/postgres:16
fi
