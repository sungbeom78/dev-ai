# Model glossary approval table

Glossary revision compared: `845342ea44c1092fa6d51341cf4c45941b0b7145`

The original reverse-engineering output used English text as Korean labels and contained plural/inflected duplicate words. The model-local word definitions were normalized before this table was produced. Physical table and column names were not changed.

| # | Full word | Existing physical token / abbreviation | Korean meaning | Action |
|---:|---|---|---|---|
| 1 | ai | ai | 인공지능 | add word |
| 2 | answer | answer | 답변 | add word |
| 3 | author | author | 작성자 | add word |
| 4 | briefing | briefings | 브리핑 | add word |
| 5 | crawl | crawled | 크롤링 | add word |
| 6 | document | documents | 문서 | add word |
| 7 | endpoint | endpoint | 엔드포인트 | add word |
| 8 | feedback | feedback | 피드백 | add word |
| 9 | it | it | 대상 | add word |
| 10 | korean | korean | 한국어 | add word |
| 11 | latency | latency | 지연시간 | add word |
| 12 | license | license | 라이선스 | add word |
| 13 | matter | matters | 중요성 | add word |
| 14 | note | note | 메모 | add word |
| 15 | quality | quality | 품질 | add word |
| 16 | question | question | 질문 | add word |
| 17 | retrieval | retrieval | 검색 | add word |
| 18 | suggest | suggested | 제안 | add word |
| 19 | tag | tags | 태그 | add abbreviation to existing word |
| 20 | title | title | 제목 | add word |
| 21 | topic | topic | 주제 | add word |
| 22 | why | why | 이유 | add word |

Comparison result: 76 model words; 54 already resolved; 22 require registration; 0 conflicts; 0 R2 violations; 0 missing compound parts.

Recommendation: approve all 22 because each maps an existing production physical-name token. The entries for `why`, `it`, and `matters` are explicitly described as legacy tokens from `why_it_matters`; approval does not endorse those names for new schema design.
