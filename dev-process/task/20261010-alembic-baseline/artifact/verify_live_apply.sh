#!/usr/bin/env bash
set -euo pipefail

cd /project/dev_ai
python3 - <<'PY'
from pathlib import Path
source = Path("app/main.py").read_text(encoding="utf-8")
assert "Base.metadata.create_all" not in source
assert "from app.db.database import engine" not in source
assert "from app.db.models import Base" not in source
print("source_check=ok create_all=absent")
PY

health_code="000"
for _ in $(seq 1 30); do
  health_code=$(curl -sS --max-time 3 -o /tmp/t5-health.json -w '%{http_code}' http://127.0.0.1:8000/health || true)
  [[ "$health_code" == "200" ]] && break
  sleep 1
done
[[ "$health_code" == "200" ]]

search_code=$(curl -sS --max-time 60 -o /tmp/t5-search.json -w '%{http_code}' \
  -H 'Content-Type: application/json' \
  --data '{"query":"RAG pipeline","limit":1}' \
  http://127.0.0.1:8000/search)
[[ "$search_code" == "200" ]]
result_count=$(python3 - <<'PY'
import json
with open('/tmp/t5-search.json', encoding='utf-8') as f:
    payload = json.load(f)
print(len(payload.get('results', [])))
PY
)
[[ "$result_count" -ge 1 ]]

docker logs --since 5m bomts_api > /tmp/t5-api-recent.log 2>&1
log_lines=$(wc -l < /tmp/t5-api-recent.log)
[[ "$log_lines" -gt 0 ]]
error_count=$(grep -Eic 'authentication failed|password authentication failed|connection refused|could not connect|OperationalError|ResponseHandlingException' /tmp/t5-api-recent.log || true)
[[ "$error_count" -eq 0 ]]

printf 'health_http=%s search_http=%s search_results=%s recent_log_lines=%s auth_connection_errors=%s\n' \
  "$health_code" "$search_code" "$result_count" "$log_lines" "$error_count"
