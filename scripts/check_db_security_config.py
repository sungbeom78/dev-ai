#!/usr/bin/env python3
"""Validate security invariants without reading or printing secret values."""

import json
from pathlib import Path


root = Path(__file__).resolve().parents[1]
compose = (root / "docker-compose.yml").read_text()
gitignore = (root / ".gitignore").read_text().splitlines()
database_code = (root / "app/db/database.py").read_text()
vector_code = (root / "app/rag/vector_store.py").read_text()
health_code = (root / "app/api/health.py").read_text()
example_lines = (root / ".env.example").read_text().splitlines()
model = json.loads((root / "db/model.json").read_text())

required_bindings = {
    '"127.0.0.1:5432:5432"',
    '"127.0.0.1:6333:6333"',
    '"127.0.0.1:6334:6334"',
}
missing_bindings = sorted(binding for binding in required_bindings if binding not in compose)
assert not missing_bindings, f"missing loopback bindings: {missing_bindings}"
assert "QDRANT__SERVICE__API_KEY" in compose, "Qdrant API key is not configured"
assert "POSTGRES_APP_PASSWORD" not in compose, "application password must enter through DATABASE_URL only"
assert 'os.environ["DATABASE_URL"]' in database_code, "DATABASE_URL must be required"
assert "DATABASE_URL =" not in database_code, "DATABASE_URL must not add an unregistered module identifier"
assert "postgresql://postgres:postgres" not in database_code, "hard-coded DB credential remains"
apply_script = (root / "scripts/apply_db_security.sh").read_text()
rollback_script = (root / "scripts/rollback_db_security.sh").read_text()
assert "BEGIN;" in apply_script and "COMMIT;" in apply_script, "apply SQL must be transactional"
assert "d.deptype IN ('a', 'i')" in apply_script, "apply must skip linked sequences"
assert "DROP ROLE bomts_app" in rollback_script, "rollback must remove the task-created app role"
assert 'api_key=os.environ["QDRANT_API_KEY"]' in vector_code, "vector store does not use the API key"
assert 'api_key=os.environ["QDRANT_API_KEY"]' in health_code, "health Qdrant client does not use the API key"
assert ".env" in gitignore and ".env.*" in gitignore and "!.env.example" in gitignore
assert all("=" in line and line.endswith("=") for line in example_lines if line.strip()), ".env.example must contain key names only"
assert len(model.get("tables", [])) == 8, "model.json must contain the eight observed tables"
assert model.get("security", {}).get("owner_role") == "bomts_app"

print("PASS: DB security configuration invariants")
