# Database access operations

## Network boundary

PostgreSQL (`5432`) and Qdrant REST/gRPC (`6333`, `6334`) bind only to `127.0.0.1` on the Mini PC. Do not expose these ports through the router or host firewall.

## DBeaver from the LAN

Use DBeaver's SSH tunnel rather than connecting directly to the Mini PC database port.

1. Create a PostgreSQL connection whose host is `127.0.0.1`, port is `5432`, and database is `bomts`.
2. Enable **SSH Tunnel** in DBeaver.
3. Set the SSH host to the Mini PC's LAN hostname or address and port `22`.
4. Authenticate with the Mini PC SSH account and an SSH key. Do not store the PostgreSQL password in this repository.
5. Use the dedicated PostgreSQL application account only when application-equivalent access is required. Use a separately managed administrative account for maintenance.
6. Test the tunnel. A direct connection to `<MINI_PC_LAN_IP>:5432` must fail, while the SSH-tunneled connection succeeds.

Equivalent command-line tunnel:

```bash
ssh -N -L 15432:127.0.0.1:5432 <SSH_USER>@<MINI_PC_LAN_IP>
```

Connect DBeaver to `127.0.0.1:15432` when using this command-line tunnel.

## Qdrant access

Applications must send the Qdrant API key. A request without the `api-key` header must return HTTP 401 after the secured service is applied. Keep the key only in the ignored `.env` file or an external secret manager.

## Apply and rollback boundary

Do not run `scripts/apply_db_security.sh` until the service owner approves the restart. The script requires `APPLY_DB_SECURITY=YES`, changes PostgreSQL roles and ownership, and recreates the Compose services.

The pre-change Compose and `.env` files are stored outside the repository under `/project/backup/bomts-ai/2026-10-09/pre-db-security/rollback/`. Restore those files before recreating services when rolling back. PostgreSQL role passwords can be restored through the local trusted container connection; Qdrant returns to its prior no-key configuration when the previous Compose file is applied.
