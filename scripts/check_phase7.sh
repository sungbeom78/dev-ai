#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"

echo "== BomTS Dev AI Phase 7 Check =="
echo "BASE_URL=${BASE_URL}"

echo
echo "1) Docker compose status"
docker compose ps

echo
echo "2) Health check"
HEALTH_RESPONSE="$(curl -s "${BASE_URL}/health")"
echo "${HEALTH_RESPONSE}"
echo "${HEALTH_RESPONSE}" | grep -q '"status":"ok"' || {
  echo "ERROR: health check failed"
  exit 1
}

echo
echo "3) Run previous checks if available"

if [ -x scripts/check_phase3.sh ]; then
  bash scripts/check_phase3.sh > /dev/null
fi

if [ -x scripts/check_phase4.sh ]; then
  bash scripts/check_phase4.sh > /dev/null
fi

if [ -x scripts/check_phase6.sh ]; then
  bash scripts/check_phase6.sh > /dev/null
fi

echo
echo "4) Call /agent/ask and capture ask_log_id"

AGENT_RESPONSE="$(curl -s -X POST "${BASE_URL}/agent/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is BomTS Dev AI?",
    "limit": 5
  }')"

echo "${AGENT_RESPONSE}" | python3 -m json.tool || echo "${AGENT_RESPONSE}"

ASK_LOG_ID="$(echo "${AGENT_RESPONSE}" | python3 -c 'import sys,json; data=json.load(sys.stdin); print(data.get("ask_log_id",""))')"

if [ -z "${ASK_LOG_ID}" ]; then
  echo "ERROR: ask_log_id not found in /agent/ask response"
  exit 1
fi

echo "ASK_LOG_ID=${ASK_LOG_ID}"

echo
echo "5) List ask logs"

LOGS_RESPONSE="$(curl -s "${BASE_URL}/logs/asks?limit=10")"
echo "${LOGS_RESPONSE}" | python3 -m json.tool || echo "${LOGS_RESPONSE}"
echo "${LOGS_RESPONSE}" | grep -q "${ASK_LOG_ID}" || {
  echo "ERROR: ask_log_id not found in logs list"
  exit 1
}

echo
echo "6) Get ask log detail"

DETAIL_RESPONSE="$(curl -s "${BASE_URL}/logs/asks/${ASK_LOG_ID}")"
echo "${DETAIL_RESPONSE}" | python3 -m json.tool || echo "${DETAIL_RESPONSE}"
echo "${DETAIL_RESPONSE}" | grep -q "sources" || {
  echo "ERROR: log detail does not contain sources"
  exit 1
}

echo
echo "7) Submit feedback"

FEEDBACK_RESPONSE="$(curl -s -X POST "${BASE_URL}/logs/asks/${ASK_LOG_ID}/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": "up",
    "comment": "Phase 7 check feedback."
  }')"

echo "${FEEDBACK_RESPONSE}" | python3 -m json.tool || echo "${FEEDBACK_RESPONSE}"
echo "${FEEDBACK_RESPONSE}" | grep -Eq "up|feedback|rating" || {
  echo "ERROR: feedback response does not look successful"
  exit 1
}

echo
echo "8) Verify feedback appears in detail"

DETAIL_RESPONSE_2="$(curl -s "${BASE_URL}/logs/asks/${ASK_LOG_ID}")"
echo "${DETAIL_RESPONSE_2}" | python3 -m json.tool || echo "${DETAIL_RESPONSE_2}"
echo "${DETAIL_RESPONSE_2}" | grep -q "Phase 7 check feedback" || {
  echo "ERROR: feedback not found in log detail"
  exit 1
}

echo
echo "✅ Phase 7 OK: ask logging, source logging, and feedback are working."
