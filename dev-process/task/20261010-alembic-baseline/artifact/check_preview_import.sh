#!/usr/bin/env bash
set -euo pipefail

cd /project/dev_ai
set -a
# Runtime credentials stay in the ignored environment file and are never printed.
. ./.env
set +a

image="bomts-api:t5-alembic-preview"
docker image inspect "$image" --format 'preview_image={{.Id}}'
docker run --rm \
  --network host \
  --entrypoint python \
  -e QDRANT_API_KEY \
  -e QDRANT_URL=http://127.0.0.1:6333 \
  -e DATABASE_URL=postgresql://unused:unused@127.0.0.1:1/unused \
  "$image" \
  -c 'from pathlib import Path; source=Path("/code/app/main.py").read_text(); assert "Base.metadata.create_all" not in source; import app.main; print("preview_import=ok create_all=absent")'
