from pathlib import Path


incident_dir = Path(__file__).parent
apply_output = (incident_dir / "01-apply-redacted.txt").read_text()
postcheck_output = (incident_dir / "03-immediate-postchecks.txt").read_text()

required_apply_markers = ("BEGIN", "COMMIT", "ALTER TABLE")
required_postcheck_markers = (
    "127.0.0.1:5432",
    "127.0.0.1:6333",
    "127.0.0.1:6334",
    "bomts_app|f|f|f",
    "bomts_app|8",
)

missing = [marker for marker in required_apply_markers if marker not in apply_output]
missing.extend(marker for marker in required_postcheck_markers if marker not in postcheck_output)
if missing:
    raise SystemExit("missing recovery evidence markers: " + ", ".join(missing))

print("PASS: linked-sequence ownership recovery was applied and observed")
