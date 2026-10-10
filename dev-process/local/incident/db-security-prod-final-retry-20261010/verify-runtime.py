import json
import os
import socket
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

import httpx


PROJECT_ROOT = Path(__file__).resolve().parents[4]
ROLLBACK_ENV = Path("/project/backup/bomts-ai/2026-10-09/pre-db-security/rollback/.env.before")
MONITOR_SUMMARY = Path(__file__).with_name("08-ten-minute-summary.txt")


def env_value(path: Path, key: str) -> str:
    for line in path.read_text().splitlines():
        if line.startswith(f"{key}="):
            return line.split("=", 1)[1]
    raise RuntimeError(f"missing environment key: {key}")


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=check, text=True, capture_output=True)


listeners = run("ss", "-H", "-ltn").stdout.splitlines()
listener_addresses = {line.split()[3] for line in listeners if len(line.split()) >= 4}
for port in (5432, 6333, 6334):
    assert f"127.0.0.1:{port}" in listener_addresses
    assert f"0.0.0.0:{port}" not in listener_addresses
    assert f"[::]:{port}" not in listener_addresses
    assert f"*:{port}" not in listener_addresses

roles = run(
    "docker", "exec", "bomts_db", "psql", "-U", "postgres", "-d", "bomts", "-tAc",
    "select rolname, rolsuper, rolcreatedb, rolcreaterole from pg_roles "
    "where rolname in ('postgres','bomts_app') order by 1",
).stdout.splitlines()
assert "bomts_app|f|f|f" in roles

owners = run(
    "docker", "exec", "bomts_db", "psql", "-U", "postgres", "-d", "bomts", "-tAc",
    "select tableowner, count(*) from pg_tables where schemaname='public' group by 1",
).stdout.strip()
assert owners == "bomts_app|8"

prepared_env = PROJECT_ROOT / ".env"
old_url = env_value(ROLLBACK_ENV, "DATABASE_URL")
old_password = urlsplit(old_url).password
assert old_password
new_admin_password = env_value(prepared_env, "POSTGRES_ADMIN_PASSWORD")
new_app_password = env_value(prepared_env, "POSTGRES_APP_PASSWORD")
qdrant_key = env_value(prepared_env, "QDRANT_API_KEY")

probe = (
    "import os,psycopg; "
    "c=psycopg.connect(host='db',port=5432,dbname='bomts',"
    "user=os.environ['TEST_DB_USER'],password=os.environ['TEST_DB_PASSWORD'],connect_timeout=3); "
    "c.close()"
)


def credential_result(user: str, password: str) -> int:
    env = ["-e", f"TEST_DB_USER={user}", "-e", f"TEST_DB_PASSWORD={password}"]
    return run("docker", "exec", *env, "bomts_api", "python", "-c", probe, check=False).returncode


assert credential_result("postgres", old_password) != 0
assert credential_result("postgres", new_admin_password) == 0
assert credential_result("bomts_app", new_app_password) == 0

with httpx.Client(timeout=5) as client:
    assert client.get("http://127.0.0.1:6333/collections").status_code == 401
    assert client.get(
        "http://127.0.0.1:6333/collections", headers={"api-key": qdrant_key}
    ).status_code == 200
    assert client.get("http://127.0.0.1:8000/health").status_code == 200
    search = client.post(
        "http://127.0.0.1:8000/search", json={"query": "RAG pipeline", "limit": 1}, timeout=20
    )
    assert search.status_code == 200
    payload = search.json()
    assert len(payload.get("results", payload if isinstance(payload, list) else [])) >= 1

activity = run(
    "docker", "exec", "bomts_db", "psql", "-U", "postgres", "-d", "bomts", "-tAc",
    "select count(*) from pg_stat_activity where datname='bomts' and usename='bomts_app'",
).stdout.strip()
assert int(activity) >= 1

for port in (5432, 6333):
    with socket.socket() as sock:
        sock.settimeout(2)
        assert sock.connect_ex(("192.168.50.221", port)) != 0

monitor = dict(
    line.split("=", 1) for line in MONITOR_SUMMARY.read_text().splitlines() if "=" in line
)
assert monitor["health_samples"] == "21"
assert monitor["final_search_http"] == "200"
assert int(monitor["api_log_lines"]) > 0
assert monitor["auth_connection_errors"] == "0"
assert monitor["RESULT"] == "PASS"

assert run("git", "check-ignore", "-q", ".env", check=False).returncode == 0
print(json.dumps({
    "result": "PASS",
    "listeners": "loopback_only",
    "table_owner_count": 8,
    "old_password": "rejected",
    "qdrant": {"without_key": 401, "with_key": 200},
    "health": 200,
    "search": 200,
    "lan_self_probe": {"5432": "refused", "6333": "refused"},
    "monitor_seconds": 600,
    "auth_connection_errors": 0,
}, ensure_ascii=False))
