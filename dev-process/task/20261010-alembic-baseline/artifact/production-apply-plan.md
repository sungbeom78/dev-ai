# T5 production apply plan

- Preflight health: HTTP 200
- API container: `running 2026-10-10T07:54:16.318755992Z restart=0`
- Command: `["uvicorn","app.main:app","--host","0.0.0.0","--port","8000","--reload"]`
- Bind mount: `/project/dev_ai/app -> /code/app rw=true`
- Exact live source change: remove the two unused engine/model imports and `Base.metadata.create_all(bind=engine)` from `app/main.py`.
- Database action: none. No `alembic upgrade`, `alembic stamp`, DDL, container recreation, or image replacement.
- Expected interruption: one uvicorn reload caused by the bind-mounted source edit, normally a few seconds; verification window is five minutes.
- Backup: `/project/backup/bomts-ai/20261010T125746Z-t5-alembic-baseline/app-main.py` with `/project/backup/bomts-ai/20261010T125746Z-t5-alembic-baseline/SHA256SUMS`.
- Rollback: atomically restore the backup to `app/main.py`, allow one reload, then repeat health and real-query checks.
- Prepared preview: image `sha256:a34c452be588c76bacba5c8dc671cc6918e264a99c230b9d5b02a240e826ad2c`; static check, image import, Qdrant authentication, and empty-PostgreSQL Alembic schema comparison passed.
