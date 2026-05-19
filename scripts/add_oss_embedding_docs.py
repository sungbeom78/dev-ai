import sys

html_content = """
<!-- Open Source Embedding Consideration -->
<section class="card" style="background-color: #f8fafc; border: 1px solid var(--border);">
    <h2>오픈소스 Embedding 고려</h2>

    <p style="margin-bottom: 1rem; line-height: 1.6;">
        현재 BomTS Dev AI는 RAG 파이프라인에서 Embedding Provider와 LLM Provider를 분리하는 구조를 사용합니다.
        Embedding Provider는 질문과 문서 chunk를 vector로 변환해 Qdrant에서 관련 chunk를 찾는 역할을 하고,
        LLM Provider는 검색된 chunk를 prompt text로 받아 최종 답변을 생성합니다.
    </p>

    <div class="code-display" style="margin-bottom: 1.5rem;">
User Question
  ↓
Embedding Provider
  ↓
Query Vector
  ↓
Qdrant Semantic Search
  ↓
Relevant Chunks
  ↓
Prompt Builder
  ↓
LLM Provider
  - Gemma 3
  - Qwen 2.5
  - Google Gemini
  - OpenAI
  ↓
Answer
    </div>

    <p style="margin-bottom: 1rem; line-height: 1.6;">
        중요한 점은 LLM이 vector를 직접 받는 것이 아니라는 점입니다.
        Vector는 Qdrant에서 관련 chunk를 찾기 위한 검색 표현이고,
        최종 LLM에는 검색된 chunk가 포함된 자연어 prompt가 전달됩니다.
    </p>

    <div class="info-card" style="margin-bottom: 1.5rem;">
        <h4>Mock Embedding의 의미</h4>
        <p style="font-size: 0.95em; color: var(--text-muted); line-height: 1.6;">
            Mock embedding은 무작위라기보다는 deterministic fake embedding입니다.
            같은 입력에는 항상 같은 vector를 반환하지만, 문장의 의미를 이해하는 모델은 아닙니다.
            따라서 문서 등록, chunk 생성, Qdrant upsert, search/ask API 흐름 확인에는 유용하지만,
            실제 semantic retrieval 품질 검증에는 적합하지 않습니다.
        </p>
        <p style="font-size: 0.95em; color: #991b1b; line-height: 1.6; margin-top: 0.75rem;">
            Mock embedding 상태에서 “시스템이 동작한다”는 것은 파이프라인 연결이 정상이라는 뜻이지,
            검색 품질이 좋다는 뜻은 아닙니다.
        </p>
    </div>

    <div class="info-card" style="margin-bottom: 1.5rem;">
        <h4>OpenAI Embedding의 의미</h4>
        <p style="font-size: 0.95em; color: var(--text-muted); line-height: 1.6;">
            OpenAI embedding은 실제 의미 기반 vector를 생성하므로 Qdrant semantic search 품질을 확인하는 데 적합합니다.
            현재 dev-ai는 EMBEDDING_MODE=openai일 때 OpenAI text-embedding-3-small 모델을 사용하는 구조입니다.
            다만 OpenAI embedding은 유료 API이므로 API Key, 비용, latency, rate limit, 외부 API 장애,
            입력 텍스트가 외부 API로 전달된다는 점을 고려해야 합니다.
        </p>
    </div>

    <div class="info-card" style="margin-bottom: 1.5rem;">
        <h4>Gemma / Qwen / Google과 Embedding의 역할 구분</h4>
        <p style="font-size: 0.95em; color: var(--text-muted); line-height: 1.6;">
            현재 dev-ai에서 OpenClaw 기반 Gemma 3, Qwen 2.5, Google Gemini는 답변 생성 LLM Provider로 사용됩니다.
            이들은 Qdrant 검색용 embedding vector를 생성하는 provider가 아닙니다.
            RAG 구조에서는 embedding model이 먼저 관련 chunk를 찾고,
            그 결과를 prompt text로 만들어 LLM에게 전달합니다.
        </p>
    </div>

    <h3 style="margin-top: 1.5rem;">오픈소스 Embedding 후보</h3>
    <table style="width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 0.9em;">
        <thead>
            <tr style="background-color: #f1f5f9;">
                <th style="border: 1px solid var(--border); padding: 0.75rem;">모델</th>
                <th style="border: 1px solid var(--border); padding: 0.75rem;">특징</th>
                <th style="border: 1px solid var(--border); padding: 0.75rem;">한국어/다국어</th>
                <th style="border: 1px solid var(--border); padding: 0.75rem;">리소스 부담</th>
                <th style="border: 1px solid var(--border); padding: 0.75rem;">dev-ai 추천도</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">BAAI bge-m3</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">다국어 RAG 검색에 강한 embedding 모델. dense/sparse/multi-vector 검색 확장 가능</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">좋음</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">중간</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">1순위 추천</td>
            </tr>
            <tr>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">multilingual-e5-large / instruct</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">다국어 semantic retrieval에서 널리 사용되는 embedding 계열</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">좋음</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">중간</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">추천</td>
            </tr>
            <tr>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">jina-embeddings-v3</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">다국어, long-context, 1024 dimension 기반 embedding. dimension 축소 옵션도 고려 가능</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">좋음</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">중간</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">추천</td>
            </tr>
            <tr>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">nomic-embed-text</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">Ollama 등 로컬 환경에서 사용하기 쉬운 embedding 모델</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">영어 중심 성격이 강함</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">낮음~중간</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">가벼운 테스트 추천</td>
            </tr>
            <tr>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">mxbai-embed-large</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">로컬 embedding 실험에서 자주 거론되는 모델</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">영어권 평가 중심</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">중간</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">비교 후보</td>
            </tr>
            <tr>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">Qwen embedding / reranker 계열</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">Qwen 계열의 별도 embedding 또는 reranker 모델. 답변 생성용 Qwen 2.5와는 역할이 다름</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">모델별 확인 필요</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">중간~높음</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">후순위 고급 실험</td>
            </tr>
        </tbody>
    </table>

    <h3 style="margin-top: 1.5rem;">리소스 관점</h3>
    <table style="width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 0.9em;">
        <thead>
            <tr style="background-color: #f1f5f9;">
                <th style="border: 1px solid var(--border); padding: 0.75rem;">모델 규모</th>
                <th style="border: 1px solid var(--border); padding: 0.75rem;">예시</th>
                <th style="border: 1px solid var(--border); padding: 0.75rem;">CPU 실행</th>
                <th style="border: 1px solid var(--border); padding: 0.75rem;">GPU 필요성</th>
                <th style="border: 1px solid var(--border); padding: 0.75rem;">속도</th>
                <th style="border: 1px solid var(--border); padding: 0.75rem;">비고</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">Small</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">MiniLM, small e5</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">가능</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">필수 아님</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">빠름</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">품질은 제한적일 수 있음</td>
            </tr>
            <tr>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">Base</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">bge-base, e5-base, LaBSE</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">가능</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">있으면 좋음</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">보통</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">개인 RAG에 현실적</td>
            </tr>
            <tr>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">Large</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">bge-m3, multilingual-e5-large, jina-v3</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">가능하지만 느릴 수 있음</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">권장</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">중간</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">품질과 비용의 균형이 좋음</td>
            </tr>
            <tr>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">2B 이상</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">Qwen embedding 계열 일부</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">느림</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">권장</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">느림~중간</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">고급 실험용</td>
            </tr>
            <tr>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">8B급</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">대형 embedding / multimodal embedding 계열</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">비현실적</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">강력 권장</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">무거움</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">현재 dev-ai 첫 적용 대상으로는 과함</td>
            </tr>
        </tbody>
    </table>

    <h3 style="margin-top: 1.5rem;">OpenAI Embedding vs 오픈소스 Local Embedding</h3>
    <table style="width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 0.9em;">
        <thead>
            <tr style="background-color: #f1f5f9;">
                <th style="border: 1px solid var(--border); padding: 0.75rem;">구분</th>
                <th style="border: 1px solid var(--border); padding: 0.75rem;">OpenAI Embedding</th>
                <th style="border: 1px solid var(--border); padding: 0.75rem;">Open-source / Local Embedding</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">비용</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">API 비용 발생</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">로컬 실행 시 API 비용 없음</td>
            </tr>
            <tr>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">속도</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">네트워크 latency 있음</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">로컬 하드웨어 성능에 의존</td>
            </tr>
            <tr>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">품질</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">안정적이고 빠르게 품질 확인 가능</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">모델 선택에 따라 편차 있음</td>
            </tr>
            <tr>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">운영</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">API Key, rate limit, 비용 관리 필요</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">모델 다운로드, 서빙, 리소스 관리 필요</td>
            </tr>
            <tr>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">프라이버시</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">텍스트가 외부 API로 전달됨</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">로컬 처리 가능</td>
            </tr>
            <tr>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">dev-ai 학습 가치</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">실제 semantic retrieval 품질 기준점 확보</td>
                <td style="border: 1px solid var(--border); padding: 0.75rem;">온프레미스 AI 포트폴리오 가치가 큼</td>
            </tr>
        </tbody>
    </table>

    <h3 style="margin-top: 1.5rem;">권장 발전 방향</h3>
    <p style="margin-bottom: 1rem; line-height: 1.6;">
        dev-ai의 다음 단계는 단순히 Local LLM 답변 생성을 붙이는 것이 아니라,
        Local Embedding Provider를 추가하는 것입니다.
        Gemma/Qwen/Google은 답변 생성용으로 유지하고,
        검색 품질을 담당하는 embedding model은 bge-m3 같은 오픈소스 모델로 분리하는 방향이 적절합니다.
    </p>

    <div class="code-display" style="margin-bottom: 1.5rem;">
현재 구조:
Embedder
  ├─ mock
  └─ openai

권장 구조:
EmbeddingProvider
  ├─ MockEmbeddingProvider
  ├─ OpenAIEmbeddingProvider
  ├─ LocalSentenceTransformerEmbeddingProvider
  ├─ OllamaEmbeddingProvider
  └─ OpenAICompatibleEmbeddingProvider
    </div>

    <div class="code-display" style="margin-bottom: 1.5rem;">
환경변수 예시:

EMBEDDING_PROVIDER=local
EMBEDDING_MODEL=BAAI/bge-m3
EMBEDDING_DIMENSION=1024

또는

EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=bge-m3
EMBEDDING_BASE_URL=http://localhost:11434
EMBEDDING_DIMENSION=1024
    </div>

    <div class="info-card" style="margin-bottom: 1.5rem;">
        <h4>Qdrant Collection Dimension 주의사항</h4>
        <p style="font-size: 0.95em; color: var(--text-muted); line-height: 1.6;">
            Embedding 모델을 바꾸면 vector dimension이 달라질 수 있습니다.
            현재 dev-ai는 OpenAI text-embedding-3-small 기준으로 1536 dimension을 사용합니다.
            하지만 bge-m3, jina, e5, nomic 등은 dimension이 다를 수 있습니다.
            Qdrant collection은 생성 시 vector dimension이 고정되므로,
            embedding model을 바꿀 때는 collection도 분리하거나 재생성해야 합니다.
        </p>
        <div class="code-display" style="margin-top: 1rem;">
documents_mock_1536
documents_openai_1536
documents_bge_m3_1024
documents_jina_v3_1024
documents_nomic_768
        </div>
    </div>

    <p style="line-height: 1.6; font-weight: 500;">
        결론적으로 현재 dev-ai의 RAG 구조는 올바른 방향입니다.
        Embedding Provider는 검색 품질을 담당하고,
        LLM Provider는 검색된 context를 바탕으로 답변 생성을 담당합니다.
        Mock embedding은 파이프라인 검증용이고,
        OpenAI embedding은 실제 품질 확인용이며,
        오픈소스 Local embedding은 온프레미스 AI Lab으로 발전하기 위한 다음 단계입니다.
    </p>
</section>
"""

with open("web/docs.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace </main> with html_content + </main>
if "</main>" in content:
    new_content = content.replace("</main>", html_content + "\n    </main>")
    with open("web/docs.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully added the open source embedding consideration section.")
else:
    print("Error: </main> not found.")

