# Vector DB 기초

## 1. Vector DB란?
일반적인 관계형 DB가 행(Row)과 열(Column)로 데이터를 저장하고 SQL로 일치(Exact Match) 기반의 검색을 한다면, Vector DB는 데이터를 다차원 벡터 형태로 저장하고 이들 간의 거리나 각도를 기반으로 **유사도(Similarity) 검색**을 수행하는 데이터베이스입니다.

## 2. 왜 RAG에서 Vector DB가 필요한가?
RAG에서는 사용자의 "질문"과 "유사한" 문서를 찾아내는 것이 목표입니다. 
- "의미"를 담은 실수 벡터들의 바다에서 거리가 가장 가까운 벡터들을 가장 연관된 문서로 판단합니다.
- 대규모 문서 셋에서 코사인 유사도 연산을 모든 데이터에 대해 수행(Brute-force)하면 시간이 너무 오래 걸리므로, Vector DB는 ANN(Approximate Nearest Neighbor) 인덱싱 (예: HNSW)을 통해 압도적으로 빠른 검색 속도를 보장합니다.

## 3. Qdrant의 특징
- Payload 기반 필터링: 단순히 벡터 거리만 재는 것이 아니라, `document_id=1` 처럼 메타데이터 필터링을 함께 지원합니다.
- 본 프로젝트에서는 `document_id`, `chunk_index`, `title`, `content` 등의 메타데이터를 벡터와 함께 Payload에 저장하여 검색 결과만으로 문서 원문을 제공할 수 있게 합니다.
