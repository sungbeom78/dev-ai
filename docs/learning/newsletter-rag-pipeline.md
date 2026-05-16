# Newsletter RAG Pipeline

이 문서는 최신 AI 개발 트렌드와 기술 문서를 주기적으로 수집하여, 개발과 학습에 활용하기 위한 파이프라인 구조를 설명합니다.

## Pipeline Overview

파이프라인은 크게 **수집 -> 번역 -> 임베딩 -> 활용** 단계로 이루어져 있습니다.

1. **Source Registry**: 크롤링 대상이 되는 블로그(Hugging Face, LangChain 등)의 엔드포인트를 등록 및 관리합니다.
2. **Fetch / Crawl**: 정해진 주기에 따라 수집을 진행하며, 크롤링된 HTML 본문을 추출합니다.
3. **Translation & Summarization**: 번역 Provider(예: Google API)를 이용해 원문을 한국어로 번역하고, 핵심 내용을 요약합니다. 이 요약은 Application Note(해당 기술이 Dev AI 프로젝트에 어떻게 활용될지)를 포함할 수 있습니다.
4. **Vector Indexing**: 번역된 본문과 요약 문구를 기반으로 Chunk를 생성하고 Vector DB(Qdrant)에 저장합니다.
5. **RAG & Agent**: 수집된 최신 정보를 바탕으로 사용자가 한국어로 질문하면, 관련 문서의 출처(Source)와 함께 답변을 생성합니다.

## Scheduler

서버 부하와 외부 사이트의 정책(Rate Limit, Robots.txt)을 고려하여 6시간 단위로 동작하는 스크립트를 크론(cron) 기반으로 등록해 사용합니다.

```bash
# 예시: 6시간 마다 수집 실행
0 */6 * * * cd /project/dev_ai && ./scripts/crawl_latest_sources.sh >> logs/crawl.log 2>&1
```

이러한 파이프라인은 단순 뉴스 구독이 아니라, 내 시스템에 적용 가능한 지식으로 승화시키는 AI Engineering 실무의 핵심 요소입니다.
