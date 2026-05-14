# Document Ingestion과 Chunking

## 1. RAG에서 Document Ingestion이 왜 필요한가?
RAG(Retrieval-Augmented Generation) 시스템의 핵심은 LLM이 알지 못하는 외부 지식을 검색하여 답변의 근거로 활용하는 것입니다.
이를 위해서는 원본 문서(PDF, 텍스트, 웹페이지 등)를 시스템이 검색 가능한 형태(벡터 및 메타데이터)로 변환하여 저장하는 과정이 필수적이며, 이를 Document Ingestion이라고 합니다.
이는 단순한 저장이 아니라 추후 **빠르고 정확하게 검색**하기 위한 전처리 과정입니다.

## 2. Chunking과 ETL의 비교
Chunking은 문서를 일정한 크기로 자르는 과정입니다.
이 과정은 데이터 엔지니어링의 ETL(Extract, Transform, Load) 파이프라인과 매우 유사합니다.
- **Extract**: 다양한 포맷의 원본 문서에서 텍스트를 추출
- **Transform**: 추출된 텍스트를 의미가 보존되는 적절한 크기(Chunk)로 분할 (Chunking) 및 노이즈 제거
- **Load**: 생성된 Chunk를 임베딩하여 Vector DB에 적재

하나의 문서를 통째로 임베딩하면 문맥이 희석되어 정확한 검색이 어려워집니다. 따라서 의미를 담을 수 있는 최소 단위로 자르는 Transform(Chunking) 과정이 검색 성능을 좌우합니다.

## 3. 현재 Character Chunking을 선택한 이유
MVP 단계에서는 시스템의 동작을 최우선으로 검증하기 위해 가장 단순한 Character 기반 Chunking을 도입했습니다.
- **구현의 단순성**: 공백 포함 글자 수 기준으로 `chunk_size`(=800), `chunk_overlap`(=100)을 적용하여 빠르게 파이프라인을 구축할 수 있습니다.
- **직관적 동작 확인**: 복잡한 형태소 분석기나 텍스트 분리 로직 없이도 Chunking 파이프라인이 정상적으로 Document와 연결되어 DB에 저장되는지 확인하기 용이합니다.

## 4. 향후 개선 방향
- **Semantic Chunking**: 단순히 글자 수로 자르면 문장이나 문단이 중간에 끊어질 수 있습니다. 향후 NLTK나 SpaCy를 활용한 문장 단위 분리, 혹은 LangChain의 RecursiveCharacterTextSplitter처럼 의미 단위(문단, 문장 등)를 우선으로 하는 전략을 도입할 예정입니다.
- **다양한 소스 지원**: Markdown, PDF 형식 등에 특화된 파싱 로직을 추가하여 문서 구조(헤딩 등)를 메타데이터로 보존할 수 있도록 개선해야 합니다.
