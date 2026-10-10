# Recovery investigation — pgdump-nondeterministic-noise

Collected: 2026-10-10T12:43:04.490311+00:00

## Logs and recorded failures

The initial validation was a direct preflight, so it has no sealed check-run log. The exact first discrepancy printed was `production_pg_dump_vs_generated_pg_dump_diff_lines=31`; its unified diff contained only random `\restrict`/`\unrestrict` values and the comment-only public-schema block. The persisted incident record follows.

```json
{
  "closed_at": "2026-10-10T11:33:09.814429+00:00",
  "created_at": "2026-10-10T11:31:38.643409+00:00",
  "error_signature": "schema-only dumps differ only by random restrict token and public schema comments",
  "incident_id": "pgdump-nondeterministic-noise",
  "linked_tasks": [],
  "max_rounds": 3,
  "owner_task_id": "20261010-model-baseline",
  "rounds": [
    {
      "action": "normalize dumps by excluding comments, blank lines, and restrict/unrestrict meta commands while retaining all SQL statements",
      "budget_exception": null,
      "diff_ref": null,
      "evidence": "31 diff lines; all changes are restrict/unrestrict tokens, blank lines, and public schema comment block; temporary schema counts and smoke passed",
      "expected_result": "normalized generated and production schema SQL have zero diff lines",
      "hypothesis": "pg_dump emits random restrict tokens and environment-dependent comments that are not schema statements",
      "hypothesis_hash": "bef24396ced93db8",
      "phase": "ddl-comparison",
      "proposed_by_task": "20261010-model-baseline",
      "result": "dump normalization was applied, but retry stopped before comparison because temporary server accepted connections while database bomts did not exist",
      "result_ts": "2026-10-10T11:32:02.154549+00:00",
      "round_no": 1,
      "status": "failed",
      "ts": "2026-10-10T11:31:38.956408+00:00",
      "verification_check": null,
      "verification_run_id": null,
      "verification_task": "20261010-model-baseline",
      "verified": false
    },
    {
      "action": "start the temporary server with default database, wait for postgres, then create database bomts explicitly before applying DDL",
      "budget_exception": null,
      "diff_ref": null,
      "evidence": "psql FATAL database bomts does not exist after pg_isready returned success",
      "expected_result": "temporary database exists, DDL and smoke tests pass, normalized dump diff is zero",
      "hypothesis": "pg_isready only confirms server acceptance and does not guarantee POSTGRES_DB creation completed",
      "hypothesis_hash": "bf0c76dc8feb427c",
      "phase": "ddl-comparison",
      "proposed_by_task": "20261010-model-baseline",
      "result": "explicit createdb still raced with asynchronous initdb/entrypoint initialization immediately after pg_isready",
      "result_ts": "2026-10-10T11:32:25.877922+00:00",
      "round_no": 2,
      "status": "failed",
      "ts": "2026-10-10T11:32:02.462159+00:00",
      "verification_check": null,
      "verification_run_id": null,
      "verification_task": "20261010-model-baseline",
      "verified": false
    },
    {
      "action": "poll psql SELECT 1 on postgres, check whether bomts accepts SQL, and run createdb only when it does not",
      "budget_exception": null,
      "diff_ref": null,
      "evidence": "createdb returned nonzero immediately after pg_isready; command output was captured and the temporary container was removed",
      "expected_result": "stable temporary database initialization followed by zero normalized schema diff",
      "hypothesis": "SQL readiness must be established with psql, and database creation must tolerate the entrypoint having already created bomts",
      "hypothesis_hash": "62eeaaad20bcc8da",
      "phase": "ddl-comparison",
      "proposed_by_task": "20261010-model-baseline",
      "result": "psql readiness reached the entrypoint temporary server; it shut down before createdb, so validation could not continue",
      "result_ts": "2026-10-10T11:33:09.578903+00:00",
      "round_no": 3,
      "status": "failed",
      "ts": "2026-10-10T11:32:26.199266+00:00",
      "verification_check": null,
      "verification_run_id": null,
      "verification_task": "20261010-model-baseline",
      "verified": false
    }
  ],
  "rounds_used": 3,
  "status": "blocked"
}
```

## System state

### docker ps -a (exit 0)
```text
bomts_web	Up 5 hours	0.0.0.0:8771->80/tcp, [::]:8771->80/tcp
bomts_api	Up 5 hours	0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
bomts_db	Up 5 hours (healthy)	127.0.0.1:5432->5432/tcp
bomts_qdrant	Up 5 hours	127.0.0.1:6333-6334->6333-6334/tcp
bomts_public_website	Up 5 hours (healthy)	127.0.0.1:3001->80/tcp
bomts-mailu-fetchmail-1	Up 9 hours (healthy)	
bomts-mailu-antispam-1	Up 9 hours (healthy)	
bomts-mailu-imap-1	Up 9 hours (healthy)	
bomts-mailu-webmail-1	Up 9 hours (healthy)	
bomts-mailu-smtp-1	Up 9 hours (healthy)	
bomts-mailu-admin-1	Up 9 hours (healthy)	
bomts-mailu-front-1	Up 9 hours (healthy)	192.168.50.221:25->25/tcp, 110/tcp, 192.168.50.221:80->80/tcp, 192.168.50.221:443->443/tcp, 192.168.50.221:465->465/tcp, 192.168.50.221:587->587/tcp, 192.168.50.221:993->993/tcp, 192.168.50.221:995->995/tcp, 192.168.50.221:4190->4190/tcp, 143/tcp
bomts-mailu-redis-1	Up 9 hours	6379/tcp
bomts-mailu-resolver-1	Up 9 hours (healthy)	
bomts-mailu-antivirus-1	Up 9 hours (healthy)	3310/tcp, 7357/tcp

Temporary-name matches:
(none)
```

### TCP listeners (exit 0)
```text
LISTEN 0      4096        127.0.0.1:6334       0.0.0.0:*                                               
LISTEN 0      4096        127.0.0.1:6333       0.0.0.0:*                                               
LISTEN 0      4096        127.0.0.1:5432       0.0.0.0:*                                               
```

### Docker volumes (exit 0)
```text
DRIVER    VOLUME NAME
local     07f49dfaa842de07e6264e0831b33c6c24e84311b458fa67ad3d7f23f32fb50d
local     3050d6b0aa8da31063a529b29f1b7ec316cb14a6efae01f4cd1653443fedd1fd
local     8428d4751abd0f02f615b542d53841c5f72c264e3e4082eaa293461b9a44a51d
local     b74aac3fa41f0965627d40f0c4f7826d5e37d6b2a3dbe3485709bbe453cf557d
local     dev_ai_postgres_data
local     dev_ai_qdrant_data
```

### disk (exit 0)
```text
Filesystem                         Size  Used Avail Use% Mounted on
/dev/mapper/ubuntu--vg-ubuntu--lv   98G   28G   66G  30% /
```

### memory (exit 0)
```text
total        used        free      shared  buff/cache   available
Mem:            15Gi       3.3Gi       226Mi        38Mi        12Gi        12Gi
Swap:          4.0Gi       780Ki       4.0Gi
```

### host PostgreSQL binaries (exit 0)
```text
(no output)
```

## Recent changes

### git diff names (exit 0)
```text
M	db/01_modeling_notes.md
M	db/model.json
M	dev-process/local/upstream-requests.md
M	project.policy.yaml
```

### model diff (exit 0)
```text
diff --git a/db/model.json b/db/model.json
index 50cf4e7..bf55e57 100644
--- a/db/model.json
+++ b/db/model.json
@@ -4,11 +4,11 @@
   "db": "postgresql",
   "db_version": "15",
   "schema": "public",
-  "source": "Reverse-engineered from the running bomts PostgreSQL database on 2026-10-09",
+  "source": "Reverse-engineered read-only from the running bomts PostgreSQL database on 2026-10-10",
   "modeling_tool": "pgModeler 1.1 compatible source of truth",
   "assumptions": [
     "This model records the existing eight-table production schema without structural redesign.",
-    "The approved target owner is bomts_app; ownership is not applied until the operational restart approval.",
+    "The current owner of all eight public application tables is bomts_app (NOSUPERUSER NOCREATEDB NOCREATEROLE).",
     "Qdrant collection structure is operational vector storage and is documented separately from relational tables."
   ],
   "open_questions": [
@@ -17,18 +17,18 @@
   ],
   "words": [
     {
-      "kor": "ai",
+      "kor": "인공지능",
       "abbr": "ai",
       "full": "ai",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: ai"
     },
     {
-      "kor": "answer",
+      "kor": "답변",
       "abbr": "answer",
       "full": "answer",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: answer"
     },
     {
       "kor": "application",
@@ -52,11 +52,11 @@
       "desc": "Existing physical-name token"
     },
     {
-      "kor": "author",
+      "kor": "작성자",
       "abbr": "author",
       "full": "author",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: author"
     },
     {
       "kor": "base",
@@ -66,11 +66,11 @@
       "desc": "Existing physical-name token"
     },
     {
-      "kor": "briefings",
+      "kor": "브리핑",
       "abbr": "briefings",
-      "full": "briefings",
+      "full": "briefing",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: briefings"
     },
     {
       "kor": "category",
@@ -150,18 +150,11 @@
       "desc": "Existing physical-name token"
     },
     {
-      "kor": "crawl",
-      "abbr": "crawl",
-      "full": "crawl",
-      "is_class": false,
-      "desc": "Existing physical-name token"
-    },
-    {
-      "kor": "crawled",
+      "kor": "크롤링",
       "abbr": "crawled",
-      "full": "crawled",
+      "full": "crawl",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: crawled"
     },
     {
       "kor": "created",
@@ -178,18 +171,11 @@
       "desc": "Existing physical-name token"
     },
     {
-      "kor": "document",
-      "abbr": "document",
-      "full": "document",
-      "is_class": false,
-      "desc": "Existing physical-name token"
-    },
-    {
-      "kor": "documents",
+      "kor": "문서",
       "abbr": "documents",
-      "full": "documents",
+      "full": "document",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: documents"
     },
     {
       "kor": "enabled",
@@ -206,11 +192,11 @@
       "desc": "Existing physical-name token"
     },
     {
-      "kor": "endpoint",
+      "kor": "엔드포인트",
       "abbr": "endpoint",
       "full": "endpoint",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: endpoint"
     },
     {
       "kor": "error",
@@ -220,11 +206,11 @@
       "desc": "Existing physical-name token"
     },
     {
-      "kor": "feedback",
+      "kor": "피드백",
       "abbr": "feedback",
       "full": "feedback",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: feedback"
     },
     {
       "kor": "freshness",
@@ -276,11 +262,11 @@
       "desc": "Existing physical-name token"
     },
     {
-      "kor": "it",
+      "kor": "대상",
       "abbr": "it",
       "full": "it",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: it"
     },
     {
       "kor": "key",
@@ -290,11 +276,11 @@
       "desc": "Existing physical-name token"
     },
     {
-      "kor": "korean",
+      "kor": "한국어",
       "abbr": "korean",
       "full": "korean",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: korean"
     },
     {
       "kor": "last",
@@ -304,18 +290,18 @@
       "desc": "Existing physical-name token"
     },
     {
-      "kor": "latency",
+      "kor": "지연시간",
       "abbr": "latency",
       "full": "latency",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: latency"
     },
     {
-      "kor": "license",
+      "kor": "라이선스",
       "abbr": "license",
       "full": "license",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: license"
     },
     {
       "kor": "log",
@@ -332,11 +318,11 @@
       "desc": "Existing physical-name token"
     },
     {
-      "kor": "matters",
+      "kor": "중요성",
       "abbr": "matters",
-      "full": "matters",
+      "full": "matter",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: matters"
     },
     {
       "kor": "message",
@@ -367,11 +353,11 @@
       "desc": "Existing physical-name token"
     },
     {
-      "kor": "note",
+      "kor": "메모",
       "abbr": "note",
       "full": "note",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: note"
     },
     {
       "kor": "or",
@@ -402,11 +388,11 @@
       "desc": "Existing physical-name token"
     },
     {
-      "kor": "quality",
+      "kor": "품질",
       "abbr": "quality",
       "full": "quality",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: quality"
     },
     {
       "kor": "query",
@@ -416,11 +402,11 @@
       "desc": "Existing physical-name token"
     },
     {
-      "kor": "question",
+      "kor": "질문",
       "abbr": "question",
       "full": "question",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: question"
     },
     {
       "kor": "rating",
@@ -437,11 +423,11 @@
       "desc": "Existing physical-name token"
     },
     {
-      "kor": "retrieval",
+      "kor": "검색",
       "abbr": "retrieval",
       "full": "retrieval",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: retrieval"
     },
     {
       "kor": "risk",
@@ -486,11 +472,11 @@
       "desc": "Existing physical-name token"
     },
     {
-      "kor": "suggested",
+      "kor": "제안",
       "abbr": "suggested",
-      "full": "suggested",
+      "full": "suggest",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: suggested"
     },
     {
       "kor": "summary",
@@ -500,11 +486,11 @@
       "desc": "Existing physical-name token"
     },
     {
-      "kor": "tags",
+      "kor": "태그",
       "abbr": "tags",
-      "full": "tags",
+      "full": "tag",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: tags"
     },
     {
       "kor": "tasks",
@@ -514,18 +500,18 @@
       "desc": "Existing physical-name token"
     },
     {
-      "kor": "title",
+      "kor": "제목",
       "abbr": "title",
       "full": "title",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: title"
     },
     {
-      "kor": "topic",
+      "kor": "주제",
       "abbr": "topic",
       "full": "topic",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: topic"
     },
     {
       "kor": "type",
@@ -556,11 +542,11 @@
       "desc": "Existing physical-name token"
     },
     {
-      "kor": "why",
+      "kor": "이유",
       "abbr": "why",
       "full": "why",
       "is_class": false,
-      "desc": "Existing physical-name token"
+      "desc": "Legacy physical-name token used by the current BOMTS AI schema: why"
     }
   ],
   "domains": [
@@ -1188,6 +1174,62 @@
       "word_path": "created>at",
       "domain": "timestamp with time zone",
       "desc": null
+    },
+    {
+      "kor": "AI 참고 브리핑",
+      "phys": "ai_reference_briefings",
+      "word_path": "ai>reference>briefings",
+      "domain": null,
+      "desc": "Reverse-engineered existing table ai_reference_briefings"
+    },
+    {
+      "kor": "질문 로그",
+      "phys": "ask_logs",
+      "word_path": "ask>logs",
+      "domain": null,
+      "desc": "Reverse-engineered existing table ask_logs"
+    },
+    {
+      "kor": "질문 출처 로그",
+      "phys": "ask_source_logs",
+      "word_path": "ask>source>logs",
+      "domain": null,
+      "desc": "Reverse-engineered existing table ask_source_logs"
+    },
+    {
+      "kor": "콘텐츠 출처",
+      "phys": "content_sources",
+      "word_path": "content>sources",
+      "domain": null,
+      "desc": "Reverse-engineered existing table content_sources"
+    },
+    {
+      "kor": "수집 페이지",
+      "phys": "crawled_pages",
+      "word_path": "crawled>pages",
+      "domain": null,
+      "desc": "Reverse-engineered existing table crawled_pages"
+    },
+    {
+      "kor": "문서 청크",
+      "phys": "document_chunks",
+      "word_path": "document>chunks",
+      "domain": null,
+      "desc": "Reverse-engineered existing table document_chunks"
+    },
+    {
+      "kor": "문서",
+      "phys": "documents",
+      "word_path": "documents",
+      "domain": null,
+      "desc": "Reverse-engineered existing table documents"
+    },
+    {
+      "kor": "피드백 로그",
+      "phys": "feedback_logs",
+      "word_path": "feedback>logs",
+      "domain": null,
+      "desc": "Reverse-engineered existing table feedback_logs"
     }
   ],
   "tables": [
@@ -1207,7 +1249,8 @@
           "nullable": false,
           "pk": true,
           "default": "nextval('ai_reference_briefings_id_seq'::regclass)",
-          "description": null
+          "description": null,
+          "domain": "integer"
         },
         {
           "name": "query",
@@ -1216,7 +1259,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(512)"
         },
         {
           "name": "clean_title",
@@ -1225,7 +1269,8 @@
           "nullable": false,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(512)"
         },
         {
           "name": "source_url",
@@ -1234,7 +1279,8 @@
           "nullable": false,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(512)"
         },
         {
           "name": "source_name",
@@ -1243,7 +1289,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(255)"
         },
         {
           "name": "topic",
@@ -1252,7 +1299,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(100)"
         },
         {
           "name": "published_at",
@@ -1261,7 +1309,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "timestamp with time zone"
         },
         {
           "name": "collected_at",
@@ -1270,7 +1319,8 @@
           "nullable": true,
           "pk": false,
           "default": "now()",
-          "description": null
+          "description": null,
+          "domain": "timestamp with time zone"
         },
         {
           "name": "freshness_status",
@@ -1279,7 +1329,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(50)"
         },
         {
           "name": "korean_summary",
@@ -1288,7 +1339,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "text"
         },
         {
           "name": "key_changes",
@@ -1297,7 +1349,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "text"
         },
         {
           "name": "why_it_matters",
@@ -1306,7 +1359,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "text"
         },
         {
           "name": "dev_ai_application_note",
@@ -1315,7 +1369,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "text"
         },
         {
           "name": "suggested_tasks",
@@ -1324,7 +1379,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "text"
         },
         {
           "name": "risk_or_caution",
@@ -1333,7 +1389,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "text"
         },
         {
           "name": "tags",
@@ -1342,7 +1399,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(512)"
         },
         {
           "name": "provider_used",
@@ -1351,7 +1409,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(100)"
         },
         {
           "name": "quality_score",
@@ -1360,7 +1419,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "double precision"
         },
         {
           "name": "status",
@@ -1369,7 +1429,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(50)"
         },
         {
           "name": "created_at",
@@ -1378,7 +1439,8 @@
           "nullable": true,
           "pk": false,
           "default": "now()",
-          "description": null
+          "description": null,
+          "domain": "timestamp with time zone"
         },
         {
           "name": "indexed_at",
@@ -1387,7 +1449,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "timestamp with time zone"
         },
         {
           "name": "document_id",
@@ -1403,7 +1466,8 @@
             "on_delete": "SET NULL",
             "on_update": "NO ACTION",
             "constraint": "ai_reference_briefings_document_id_fkey"
-          }
+          },
+          "domain": "integer"
         }
       ],
       "uniques": [],
@@ -1416,7 +1480,8 @@
           "name": "ix_ai_reference_briefings_id",
           "definition": "CREATE INDEX ix_ai_reference_briefings_id ON public.ai_reference_briefings USING btree (id)"
         }
-      ]
+      ],
+      "primary_key_constraint": "ai_reference_briefings_pkey"
     },
     {
       "name": "ask_logs",
@@ -1434,7 +1499,8 @@
           "nullable": false,
           "pk": true,
           "default": "nextval('ask_logs_id_seq'::regclass)",
-          "description": null
+          "description": null,
+          "domain": "integer"
         },
         {
           "name": "question",
@@ -1443,7 +1509,8 @@
           "nullable": false,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "text"
         },
         {
           "name": "endpoint_type",
@@ -1452,7 +1519,8 @@
           "nullable": false,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(50)"
         },
         {
           "name": "intent",
@@ -1461,7 +1529,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(50)"
         },
         {
           "name": "answer",
@@ -1470,7 +1539,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "text"
         },
         {
           "name": "provider",
@@ -1479,7 +1549,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(50)"
         },
         {
           "name": "model",
@@ -1488,7 +1559,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(100)"
         },
         {
           "name": "latency_ms",
@@ -1497,7 +1569,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "integer"
         },
         {
           "name": "retrieval_count",
@@ -1506,7 +1579,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "integer"
         },
         {
           "name": "created_at",
@@ -1515,7 +1589,8 @@
           "nullable": true,
           "pk": false,
           "default": "now()",
-          "description": null
+          "description": null,
+          "domain": "timestamp with time zone"
         }
       ],
       "uniques": [],
@@ -1528,7 +1603,8 @@
           "name": "ix_ask_logs_id",
           "definition": "CREATE INDEX ix_ask_logs_id ON public.ask_logs USING btree (id)"
         }
-      ]
+      ],
+      "primary_key_constraint": "ask_logs_pkey"
     },
     {
       "name": "ask_source_logs",
@@ -1546,7 +1622,8 @@
           "nullable": false,
           "pk": true,
           "default": "nextval('ask_source_logs_id_seq'::regclass)",
-          "description": null
+          "description": null,
+          "domain": "integer"
         },
         {
           "name": "ask_log_id",
@@ -1562,7 +1639,8 @@
             "on_delete": "CASCADE",
             "on_update": "NO ACTION",
             "constraint": "ask_source_logs_ask_log_id_fkey"
-          }
+          },
+          "domain": "integer"
         },
         {
           "name": "document_id",
@@ -1571,7 +1649,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "integer"
         },
         {
           "name": "chunk_id",
@@ -1580,7 +1659,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "integer"
         },
         {
           "name": "title",
@@ -1589,7 +1669,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(255)"
         },
         {
           "name": "content",
@@ -1598,7 +1679,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "text"
         },
         {
           "name": "score",
@@ -1607,7 +1689,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "double precision"
         },
         {
           "name": "source",
@@ -1616,7 +1699,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(255)"
         }
       ],
       "uniques": [],
@@ -1629,7 +1713,8 @@
           "name": "ix_ask_source_logs_id",
           "definition": "CREATE INDEX ix_ask_source_logs_id ON public.ask_source_logs USING btree (id)"
         }
-      ]
+      ],
+      "primary_key_constraint": "ask_source_logs_pkey"
     },
     {
       "name": "content_sources",
@@ -1647,7 +1732,8 @@
           "nullable": false,
           "pk": true,
           "default": "nextval('content_sources_id_seq'::regclass)",
-          "description": null
+          "description": null,
+          "domain": "integer"
         },
         {
           "name": "name",
@@ -1656,7 +1742,8 @@
           "nullable": false,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(255)"
         },
         {
           "name": "base_url",
@@ -1665,7 +1752,8 @@
           "nullable": false,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(255)"
         },
         {
           "name": "source_type",
@@ -1674,7 +1762,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(50)"
         },
         {
           "name": "category",
@@ -1683,7 +1772,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(50)"
         },
         {
           "name": "enabled",
@@ -1692,7 +1782,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "boolean"
         },
         {
           "name": "crawl_interval_hours",
@@ -1701,7 +1792,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "integer"
         },
         {
           "name": "last_crawled_at",
@@ -1710,7 +1802,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "timestamp with time zone"
         },
         {
           "name": "created_at",
@@ -1719,7 +1812,8 @@
           "nullable": true,
           "pk": false,
           "default": "now()",
-          "description": null
+          "description": null,
+          "domain": "timestamp with time zone"
         }
       ],
       "uniques": [],
@@ -1732,7 +1826,8 @@
           "name": "ix_content_sources_id",
           "definition": "CREATE INDEX ix_content_sources_id ON public.content_sources USING btree (id)"
         }
-      ]
+      ],
+      "primary_key_constraint": "content_sources_pkey"
     },
     {
       "name": "crawled_pages",
@@ -1750,7 +1845,8 @@
           "nullable": false,
           "pk": true,
           "default": "nextval('crawled_pages_id_seq'::regclass)",
-          "description": null
+          "description": null,
+          "domain": "integer"
         },
         {
           "name": "source_id",
@@ -1766,7 +1862,8 @@
             "on_delete": "CASCADE",
             "on_update": "NO ACTION",
             "constraint": "crawled_pages_source_id_fkey"
-          }
+          },
+          "domain": "integer"
         },
         {
           "name": "url",
@@ -1775,7 +1872,10 @@
           "nullable": false,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "unique": true,
+          "unique_constraint": "crawled_pages_url_key",
+          "domain": "character varying(512)"
         },
         {
           "name": "title",
@@ -1784,7 +1884,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(512)"
         },
         {
           "name": "content",
@@ -1793,7 +1894,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "text"
         },
         {
           "name": "summary",
@@ -1802,7 +1904,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "text"
         },
         {
           "name": "author",
@@ -1811,7 +1914,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(255)"
         },
         {
           "name": "published_at",
@@ -1820,7 +1924,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "timestamp with time zone"
         },
         {
           "name": "crawled_at",
@@ -1829,7 +1934,8 @@
           "nullable": true,
           "pk": false,
           "default": "now()",
-          "description": null
+          "description": null,
+          "domain": "timestamp with time zone"
         },
         {
           "name": "status",
@@ -1838,7 +1944,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(50)"
         },
         {
           "name": "error_message",
@@ -1847,7 +1954,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "text"
         },
         {
           "name": "document_id",
@@ -1863,17 +1971,11 @@
             "on_delete": "SET NULL",
             "on_update": "NO ACTION",
             "constraint": "crawled_pages_document_id_fkey"
-          }
-        }
-      ],
-      "uniques": [
-        {
-          "name": "crawled_pages_url_key",
-          "columns": [
-            "url"
-          ]
+          },
+          "domain": "integer"
         }
       ],
+      "uniques": [],
       "indexes": [
         {
           "name": "crawled_pages_pkey",
@@ -1887,6 +1989,15 @@
           "name": "ix_crawled_pages_id",
           "definition": "CREATE INDEX ix_crawled_pages_id ON public.crawled_pages USING btree (id)"
         }
+      ],
+      "primary_key_constraint": "crawled_pages_pkey",
+      "observed_unique_constraints": [
+        {
+          "name": "crawled_pages_url_key",
+          "columns": [
+            "url"
+          ]
+        }
       ]
     },
     {
@@ -1905,7 +2016,8 @@
           "nullable": false,
           "pk": true,
           "default": "nextval('document_chunks_id_seq'::regclass)",
-          "description": null
+          "description": null,
+          "domain": "integer"
         },
         {
           "name": "document_id",
@@ -1921,7 +2033,8 @@
             "on_delete": "CASCADE",
             "on_update": "NO ACTION",
             "constraint": "document_chunks_document_id_fkey"
-          }
+          },
+          "domain": "integer"
         },
         {
           "name": "chunk_index",
@@ -1930,7 +2043,8 @@
           "nullable": false,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "integer"
         },
         {
           "name": "content",
@@ -1939,7 +2053,8 @@
           "nullable": false,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "text"
         },
         {
           "name": "char_start",
@@ -1948,7 +2063,8 @@
           "nullable": false,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "integer"
         },
         {
           "name": "char_end",
@@ -1957,7 +2073,8 @@
           "nullable": false,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "integer"
         },
         {
           "name": "created_at",
@@ -1966,7 +2083,8 @@
           "nullable": true,
           "pk": false,
           "default": "now()",
-          "description": null
+          "description": null,
+          "domain": "timestamp with time zone"
         }
       ],
       "uniques": [],
@@ -1979,7 +2097,8 @@
           "name": "ix_document_chunks_id",
           "definition": "CREATE INDEX ix_document_chunks_id ON public.document_chunks USING btree (id)"
         }
-      ]
+      ],
+      "primary_key_constraint": "document_chunks_pkey"
     },
     {
       "name": "documents",
@@ -1997,7 +2116,8 @@
           "nullable": false,
           "pk": true,
           "default": "nextval('documents_id_seq'::regclass)",
-          "description": null
+          "description": null,
+          "domain": "integer"
         },
         {
           "name": "title",
@@ -2006,7 +2126,8 @@
           "nullable": false,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(255)"
         },
         {
           "name": "content",
@@ -2015,7 +2136,8 @@
           "nullable": false,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "text"
         },
         {
           "name": "source",
@@ -2024,7 +2146,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(255)"
         },
         {
           "name": "license",
@@ -2033,7 +2156,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(255)"
         },
         {
           "name": "created_at",
@@ -2042,7 +2166,8 @@
           "nullable": true,
           "pk": false,
           "default": "now()",
-          "description": null
+          "description": null,
+          "domain": "timestamp with time zone"
         },
         {
           "name": "updated_at",
@@ -2051,7 +2176,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "timestamp with time zone"
         }
       ],
       "uniques": [],
@@ -2064,7 +2190,8 @@
           "name": "ix_documents_id",
           "definition": "CREATE INDEX ix_documents_id ON public.documents USING btree (id)"
         }
-      ]
+      ],
+      "primary_key_constraint": "documents_pkey"
     },
     {
       "name": "feedback_logs",
@@ -2082,7 +2209,8 @@
           "nullable": false,
           "pk": true,
           "default": "nextval('feedback_logs_id_seq'::regclass)",
-          "description": null
+          "description": null,
+          "domain": "integer"
         },
         {
           "name": "ask_log_id",
@@ -2098,7 +2226,8 @@
             "on_delete": "CASCADE",
             "on_update": "NO ACTION",
             "constraint": "feedback_logs_ask_log_id_fkey"
-          }
+          },
+          "domain": "integer"
         },
         {
           "name": "rating",
@@ -2107,7 +2236,8 @@
           "nullable": false,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "character varying(50)"
         },
         {
           "name": "comment",
@@ -2116,7 +2246,8 @@
           "nullable": true,
           "pk": false,
           "default": null,
-          "description": null
+          "description": null,
+          "domain": "text"
         },
         {
           "name": "created_at",
@@ -2125,7 +2256,8 @@
           "nullable": true,
           "pk": false,
           "default": "now()",
-          "description": null
+          "description": null,
+          "domain": "timestamp with time zone"
         }
       ],
       "uniques": [],
@@ -2138,7 +2270,8 @@
           "name": "ix_feedback_logs_id",
           "definition": "CREATE INDEX ix_feedback_logs_id ON public.feedback_logs USING btree (id)"
         }
-      ]
+      ],
+      "primary_key_constraint": "feedback_logs_pkey"
     }
   ],
   "relationships": [
@@ -2156,7 +2289,9 @@
       "optional": true,
       "on_delete": "SET NULL",
       "on_update": "NO ACTION",
-      "meaning": "ai_reference_briefings references documents"
+      "meaning": "ai_reference_briefings references documents",
+      "from_col": "document_id",
+      "to_col": "id"
     },
     {
       "name": "ask_source_logs_ask_log_id_fkey",
@@ -2172,7 +2307,9 @@
       "optional": true,
       "on_delete": "CASCADE",
       "on_update": "NO ACTION",
-      "meaning": "ask_source_logs references ask_logs"
+      "meaning": "ask_source_logs references ask_logs",
+      "from_col": "ask_log_id",
+      "to_col": "id"
     },
     {
       "name": "crawled_pages_document_id_fkey",
@@ -2188,7 +2325,9 @@
       "optional": true,
       "on_delete": "SET NULL",
       "on_update": "NO ACTION",
-      "meaning": "crawled_pages references documents"
+      "meaning": "crawled_pages references documents",
+      "from_col": "document_id",
+      "to_col": "id"
     },
     {
       "name": "crawled_pages_source_id_fkey",
@@ -2204,7 +2343,9 @@
       "optional": true,
       "on_delete": "CASCADE",
       "on_update": "NO ACTION",
-      "meaning": "crawled_pages references content_sources"
+      "meaning": "crawled_pages references content_sources",
+      "from_col": "source_id",
+      "to_col": "id"
     },
     {
       "name": "document_chunks_document_id_fkey",
@@ -2220,7 +2361,9 @@
       "optional": true,
       "on_delete": "CASCADE",
       "on_update": "NO ACTION",
-      "meaning": "document_chunks references documents"
+      "meaning": "document_chunks references documents",
+      "from_col": "document_id",
+      "to_col": "id"
     },
     {
       "name": "feedback_logs_ask_log_id_fkey",
@@ -2236,7 +2379,9 @@
       "optional": true,
       "on_delete": "CASCADE",
       "on_update": "NO ACTION",
-      "meaning": "feedback_logs references ask_logs"
+      "meaning": "feedback_logs references ask_logs",
+      "from_col": "ask_log_id",
+      "to_col": "id"
     }
   ],
   "security": {
@@ -2269,6 +2414,9 @@
     "Treat free-text questions, answers, feedback comments, crawled content, and source URLs as potential personal-data carriers."
   ],
   "dq_notes": [
-    "Existing constraints and indexes are recorded as observed; no new logical constraint is applied by this security task."
-  ]
+    "Existing constraints and indexes are recorded as observed; identified issues remain separate follow-up candidates and are not applied by this baseline task."
+  ],
+  "generated_at": "2026-10-10T00:00:00Z",
+  "meta_schema": null,
+  "baseline_mode": "existing_database"
 }
```

### DDL diff (exit 0)
```text
(no output)
```

### validator diff (exit 0)
```text
(no output)
```

### Regeneration check
```text
export_exit=0
exported=/tmp/tmpanv63j09 tables=8 columns=80 relationships=6
generated_ddl_equals_db_out=true
```

## Data changes

- Temporary validators used `docker run --rm`; `docker ps -a` has no matching stopped container.
- Temporary output directories were Python `TemporaryDirectory` instances and were removed.
- `/tmp/bomts-prod-schema.sql` is the earlier read-only production schema dump; no production data file was written or changed.
- Docker anonymous volumes are listed above; the prior script did not assign a named volume or reuse one.

## Search and implementation evidence

The installed official image entrypoint starts a temporary server, stops it, prints initialization complete, and only then execs the final server. A readiness probe can therefore succeed against the temporary server that is about to stop.

```text
entrypoint_exit=0
290: docker_temp_server_start() {
309: docker_temp_server_stop() {
360: 			docker_temp_server_start "$@"
365: 			docker_temp_server_stop
370: 				PostgreSQL init process complete; ready for start up.
382: 	exec "$@"
```

Local search of the persisted incident shows the same sequence: first DDL/FK/CASCADE success, then database-missing and server-shutdown failures during Docker initialization. No prior project incident with this exact Docker entrypoint race exists outside this task.
