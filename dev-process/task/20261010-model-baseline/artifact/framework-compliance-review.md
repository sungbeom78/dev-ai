# Framework compliance review — model baseline

## Followed

- Resumed with `context` and `next`.
- Created a dedicated `work_type: data_model` task with the four user-provided acceptance criteria.
- Ran `prior-art` before changing the formal baseline model.
- Kept `dev-process-framework/` unchanged and changed glossary dictionary data only through the framework `model-glossary` command after the user's exact 22-term approval.
- Separated current production facts from proposed problems in `db/01_modeling_notes.md`.
- Opened a bounded recovery incident when the framework exporter failed.
- Sealed the review DBM count/XML check with `check-run` before resolving the incident.
- Did not execute DDL against the production database.

## Deviations observed

1. The first `prior-art` invocation used `--paths` instead of the documented `--files` plus required `--keywords`; it exited before recording a result and was immediately rerun correctly.
2. Recovery round 2 was registered immediately after its adapter had first been executed, rather than before the action. The action was read-only and task-local, but the event ordering did not fully follow the recovery procedure. The same command was then rerun through sealed `check-run`, recorded as confirmed+verified, and the incident was resolved.
3. The `pgdump-nondeterministic-noise` incident combined the original dump-normalization failure with a distinct Docker entrypoint initialization race discovered during recovery. This consumed all three rounds. The framework has no child-incident transition that preserves linkage without appearing to reset the retry budget, so work stopped as required instead of opening a renamed incident.

## Framework gaps found

1. `data-stance` accepted an owned `model.json` that did not satisfy the exporter/checker contract.
2. The existing-DB reverse model uses observed `column.type`, top-level relationships, named unique objects, and index definitions; the standard design exporter expects `column.domain`, inline FK objects, and list-form uniques.
3. `export_all.py` requires undocumented top-level `meta_schema` and `generated_at` values.
4. `schema=public` produces duplicate `public` schema declarations in the pgModeler output path.
5. The exporter always adds the meta catalog and FK indexes, so it cannot represent an unchanged production baseline whose current schema lacks those objects.
6. The built-in temporary PostgreSQL check has no Docker fallback when host `pg_ctl`/`initdb` binaries are absent.
7. The recovery workflow cannot split a newly discovered independent error signature into a linked child incident while retaining auditable budget semantics.

The corresponding upstream requests are recorded in `dev-process/local/upstream-requests.md`; no shared framework file was modified.

## Resume under framework 43b34f2

- Updated the framework by its own update tool and committed only the project submodule pin (`4ad2e84`).
- Reinvestigated the existing `pgdump-nondeterministic-noise` incident with all five required evidence categories.
- Classified that incident as `environment`: the official PostgreSQL image exposes an initialization server before replacing it with the final server.
- Used the new transient retry path after 30 seconds. The changed validator required a UUID container, tmpfs storage, the entrypoint completion marker, and final-database readiness. The sealed check proved 8 tables, 80 columns, 6 FKs, FK rejection, CASCADE, and normalized schema diff 0.
- Classified `model-dictionary-script-moved` as `own_change`: the project adapter retained the old framework script path after commit `40c4bab` moved it to `data-modeling-expert`. One correction round passed and the incident was resolved.
- Confirmed glossary commit `d16f5e7` contained only the approved dictionary outputs, pushed it normally to `origin/main`, and kept the project pin on that remotely reachable commit.
- No DDL was executed against the production database.
