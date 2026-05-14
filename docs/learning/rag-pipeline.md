# RAG 파이프라인 기초

RAG(Retrieval-Augmented Generation) 파이프라인은 외부 지식을 검색(Retrieval)하여 LLM의 생성(Generation)을 증강(Augmented)하는 구조입니다.
Phase 4를 통해 본 프로젝트의 최소 RAG 흐름이 모두 완성되었습니다.

## 1. 단계별 흐름
1. **문서 입력 및 청킹(Ingestion & Chunking)**: 긴 문서를 적절한 크기로 분할하여 의미 단위의 조각으로 만듭니다.
2. **임베딩 및 인덱싱(Embedding & Indexing)**: 분할된 텍스트 조각을 다차원 실수 벡터로 변환하고 Qdrant와 같은 Vector DB에 저장합니다.
3. **검색(Search)**: 사용자의 질문(Question) 역시 동일한 임베딩 모델을 통해 벡터로 변환한 뒤, 코사인 유사도 등을 바탕으로 가장 관련된 문서 청크를 찾습니다.
4. **프롬프트 빌딩(Prompt Building)**: 시스템 메시지, 사용자 질문, 그리고 검색된 문서 내용(Context)을 하나로 조립하여 LLM에게 전달할 지시문을 구성합니다.
5. **응답 생성(Answer Generation)**: 최종 프롬프트를 받은 LLM이 주어진 Context 안에서 근거를 찾고 답변 텍스트를 생성하여 반환합니다.
