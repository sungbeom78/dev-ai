import re

html_content = """        <!-- Chunking Strategy -->
        <section class="card">
            <details>
                <summary style="cursor: pointer; display: flex; align-items: baseline; gap: 0.75rem; outline: none;">
                    <h2 style="margin: 0; display: inline-block;">Chunking 전략 및 개선 방향</h2>
                    <span style="font-size: 0.95rem; font-weight: 500; color: var(--text-muted);">현재 프로젝트 기반의 Chunking 아키텍처</span>
                </summary>
                <div style="margin-top: 1.5rem; animation: fadeIn 0.3s ease-in-out;">
                    <p style="margin-bottom: 1rem; line-height: 1.6;">좋아. 아래 표는 <strong>BomTS Dev AI 기준으로 어떤 chunking 전략을 언제 도입하면 좋은지</strong>를 판단하기 위한 비교표다.</p>
                    <p style="margin-bottom: 1rem; line-height: 1.6;">먼저 전제부터 잡자.<br>현재 <code>dev-ai</code>는 <strong>Character Chunking</strong>을 사용한다. 코드상 <code>CharacterChunker(chunk_size=800, chunk_overlap=100)</code>이고, <code>start</code>부터 <code>start + chunk_size</code>까지 자른 뒤 다음 시작점을 <code>chunk_size - chunk_overlap</code>만큼 이동한다. 즉 현재는 <strong>800자 단위, 100자 중복</strong> 방식이다.</p>
                    <p style="margin-bottom: 1rem; line-height: 1.6;">프로젝트 문서에서도 현재 방식은 MVP 단계에서 전체 파이프라인을 빠르게 검증하기 위한 선택이고, 향후 NLTK, spaCy, RecursiveCharacterTextSplitter, Semantic Chunking, Markdown/PDF 구조 보존 방향으로 개선할 수 있다고 정리되어 있다.</p>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">1. 전체 비교표</summary>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">표의 기준은 <code>dev-ai</code>에 적용했을 때의 상대 평가다.</p>
                        
                        <div style="overflow-x: auto; overflow-y: auto; max-height: 500px; margin-bottom: 1rem; border: 1px solid var(--border); border-radius: 0.25rem;">
                            <table style="width: 100%; border-collapse: collapse; line-height: 1.5; font-size: 0.9em; min-width: 1200px;">
                                <thead>
                                    <tr style="text-align: left;">
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">방식</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">내용</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">특징</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">장점</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">단점</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">적재 성능</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">사용 성능</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">CPU/메모리</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">디스크 사용량</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">작업 난이도</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">dev-ai 적용 우선순위</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Character Chunking</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">글자 수 기준으로 고정 길이 분할</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">`800자 + overlap 100자`처럼 단순 절단</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">구현이 매우 쉽고 빠름. 현재 구조와 잘 맞음. 디버깅 쉬움</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">문장/문단/제목/코드 중간에서 잘릴 수 있음. 의미 단위 보존 약함</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">매우 빠름</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">검색 품질은 보통</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">낮음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">overlap만큼 증가</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">매우 낮음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">이미 적용됨</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Recursive / Paragraph-aware Chunking</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">문단, 줄바꿈, 문장, 공백 순서로 자연스러운 경계를 우선 탐색</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">안 되면 더 작은 단위로 재귀 분할</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">character 방식보다 문맥 보존 좋음. 구현 대비 효과 큼</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">문서 형식이 엉망이면 완벽하지 않음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">빠름</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">검색 품질 좋아짐</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">낮음~중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">character와 비슷하거나 약간 증가</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">낮음~중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600; color: #16a34a;">1순위 개선 추천</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Token-aware Chunking</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">글자가 아니라 LLM tokenizer 기준 token 수로 분할</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">모델 context window와 비용 기준에 가까움</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">prompt 길이/embedding 입력 길이 관리에 좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">tokenizer 의존성 추가. 사람이 보는 문단 경계와 다를 수 있음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">빠름~중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">안정적. context overflow 방지</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">chunk 수에 따라 증가</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600; color: #16a34a;">2순위 추천</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Heading-aware Chunking</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">Markdown/HTML/PDF heading 구조 기준으로 분할</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">`#`, `##`, `###`, 문서 섹션 구조 활용</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">기술 문서/README/docs에 매우 좋음. 검색 결과 설명력이 좋아짐</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">heading 없는 문서에는 효과 제한. parser 필요</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">기술 문서 검색 품질 좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">metadata 추가로 약간 증가</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600; color: #16a34a;">2순위 추천</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Metadata-rich Chunking</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">chunk에 heading, source_type, category, license, published_at 등 metadata를 함께 저장</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">chunk 자체보다 검색/필터링 품질 강화</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">Qdrant payload filtering, source 추적, UI 표시, 평가 로그에 좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">metadata 설계가 필요. 잘못된 metadata는 오히려 노이즈</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">필터 검색과 RAG 설명력 크게 향상</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">metadata만큼 증가</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600; color: #9333ea;">강력 추천</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">NLTK sentence-based Chunking</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">NLTK 문장 분리기를 이용해 문장 단위로 나눈 뒤 묶음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">전통적 NLP 기반 sentence boundary detection</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">문장 중간 절단 감소. 단순 character보다 자연스러움</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">한국어/기술문서/코드/마크다운에서 한계 가능. 별도 리소스 필요</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">문장형 문서에 좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">character와 비슷</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">선택적</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">spaCy sentence/paragraph Chunking</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">spaCy pipeline 또는 Sentencizer로 문장 경계 감지</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">NLP pipeline 기반. 언어 모델 사용 가능</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">NLTK보다 pipeline 확장성 좋음. 품사/엔티티 등 확장 가능</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">모델 설치/메모리 증가. 한국어 모델 선택 고민 필요</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간~느림</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">문장 구조 보존 좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간~높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">character와 비슷</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간~높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">선택적</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Semantic Chunking</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">embedding/의미 유사도 기준으로 주제 전환 지점에서 분할</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">의미 변화 감지. 고급 RAG 전처리</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">주제 단위 보존이 가장 좋을 수 있음. 검색 품질 향상 가능</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">embedding 비용 증가. 구현 복잡. 튜닝 필요</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">느림</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">검색 품질 잠재력 높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간~높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">후순위 고급 개선</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">LLM-guided Chunking</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">LLM이 문서를 읽고 의미 단위로 나누게 함</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">가장 유연하지만 비용 큼</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">복잡한 문서에 강함. 요약/metadata 생성과 결합 가능</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">비용, 속도, 재현성, 운영 안정성 문제</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">매우 느림</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">좋을 수 있으나 비용 큼</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">API/LLM 비용 큼</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">결과에 따라 증가</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">매우 높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">지금은 비추천</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <p style="margin-top: 0.5rem; margin-bottom: 1rem; line-height: 1.6;">최근 문서 chunking 관련 연구도 chunking 전략의 효과가 “항상 하나의 정답”으로 결정되지 않고, 검색 태스크의 성격에 따라 달라진다고 보고한다. 특히 fixed-size, sentence/paragraph 기반, semantic/LLM-guided, contextualized chunking 같은 여러 축으로 나눠 평가할 필요가 있다는 점이 중요하다. (<a href="https://arxiv.org/abs/2602.16974" target="_blank" rel="noopener noreferrer">arXiv</a>)</p>
                    </details>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">2. dev-ai 기준 추천 순서</summary>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">지금 프로젝트에서는 이 순서가 가장 현실적이다.</p>
                        <div style="overflow-x: auto; margin-bottom: 1rem;">
                            <table style="width: 100%; border-collapse: collapse; line-height: 1.5; font-size: 0.9em;">
                                <thead>
                                    <tr style="background-color: var(--bg-main); text-align: left;">
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">순서</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">전략</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">이유</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">1</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Recursive / Paragraph-aware Chunking</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">현재 character 방식에서 가장 적은 수정으로 품질 개선 가능</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">2</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Metadata-rich Chunking</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">Qdrant payload, source 추적, UI 설명력, 평가 로그까지 모두 좋아짐</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">3</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Heading-aware Chunking</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">README/docs/기술문서가 많은 dev-ai에 특히 적합</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">4</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Token-aware Chunking</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">LLM context와 embedding 입력 길이 관리에 필요</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">5</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Semantic Chunking</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">고급 개선. 비용과 복잡도 때문에 나중에</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">6</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">LLM-guided Chunking</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">연구/실험용. 운영 MVP에는 아직 과함</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">즉 지금 바로 개선한다면:</p>
                        <div class="code-display" style="margin-bottom: 1rem;">CharacterChunker
  ↓
RecursiveParagraphChunker
  ↓
MetadataRichChunker
  ↓
HeadingAware + TokenAware
  ↓
SemanticChunker</div>
                        <p style="margin-bottom: 1rem; line-height: 1.6;">이 흐름이 좋다.</p>
                    </details>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">3. 상세 비교표: 품질/성능/비용 관점</summary>
                        <div style="overflow-x: auto; overflow-y: auto; max-height: 400px; margin-bottom: 1rem; border: 1px solid var(--border); border-radius: 0.25rem;">
                            <table style="width: 100%; border-collapse: collapse; line-height: 1.5; font-size: 0.9em; min-width: 800px;">
                                <thead>
                                    <tr style="text-align: left;">
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">방식</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); text-align: right; position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">검색 품질</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); text-align: right; position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">답변 품질</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); text-align: right; position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">문맥 보존</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); text-align: right; position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">중복 노이즈</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); text-align: right; position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">비용</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); text-align: right; position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">운영 안정성</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); text-align: right; position: sticky; top: 0; background-color: var(--bg-main); z-index: 1;">설명 가능성</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Character</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">보통</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">보통</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">낮음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">overlap 크면 증가</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">낮음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">보통</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Recursive/Paragraph-aware</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간~높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">적당</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">낮음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">좋음</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Token-aware</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간~좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">안정적</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">설정에 따라 다름</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">낮음~중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">보통</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Heading-aware</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">낮음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간~높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right; font-weight: 600; color: #16a34a;">매우 좋음</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Metadata-rich</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">검색 자체보다 필터 품질 향상</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">chunk 방식에 의존</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">낮출 수 있음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right; font-weight: 600; color: #16a34a;">매우 좋음</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">NLTK</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">낮음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">보통</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">spaCy</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간~좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간~좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간~높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">낮음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간~높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">좋음</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Semantic</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">좋음~매우 좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">좋음~매우 좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">낮음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">좋음</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">LLM-guided</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">매우 좋을 수 있음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">매우 좋을 수 있음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">매우 높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">낮음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right; font-weight: 600; color: #dc2626;">매우 높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">낮음~중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">좋음</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </details>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">4. 방식별 설명</summary>

                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">4-1. Character Chunking</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">현재 방식이다.</p>
                            <div class="code-display" style="margin-bottom: 0.5rem;">문서 전체를 800자 단위로 자르고,
다음 chunk는 이전 chunk의 마지막 100자를 다시 포함한다.</div>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">현재 코드가 정확히 이 방식이다. <code>chunk_text()</code>는 <code>start = 0</code>에서 시작해 <code>end = start + chunk_size</code>까지 자르고, 다음 <code>start</code>를 <code>chunk_size - chunk_overlap</code>만큼 이동시킨다.</p>
                            <div class="code-display" style="margin-bottom: 0.5rem;">예:
chunk_size = 800
overlap = 100
step = 700

Chunk 0: 0 ~ 800
Chunk 1: 700 ~ 1500
Chunk 2: 1400 ~ 2200</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">장점</h4>
                            <div class="code-display" style="margin-bottom: 0.5rem;">구현이 쉽다.
빠르다.
디버깅이 쉽다.
MVP에서 전체 pipeline 검증에 좋다.</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">단점</h4>
                            <div class="code-display" style="margin-bottom: 0.5rem;">문장 중간에서 잘릴 수 있다.
문단 중간에서 잘릴 수 있다.
Markdown heading 구조를 모른다.
코드 블록을 중간에서 자를 수 있다.
표를 망가뜨릴 수 있다.</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">평가</h4>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;"><code>dev-ai</code>의 첫 구현으로는 맞다. 하지만 계속 이 방식만 쓰면 RAG 품질이 금방 한계에 부딪힌다.</p>
                        </details>

                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">4-2. Recursive / Paragraph-aware Chunking</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">이 방식은 character chunking보다 한 단계 좋다.<br>핵심은 “무조건 800자로 자르지 말고, 자연스러운 경계를 먼저 찾자”다.</p>
                            <div class="code-display" style="margin-bottom: 0.5rem;">예상 우선순위:
1. 큰 섹션
2. 문단
3. 문장
4. 줄바꿈
5. 공백
6. 그래도 안 되면 character 기준 절단</div>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">이 방식은 LangChain의 <code>RecursiveCharacterTextSplitter</code> 계열 아이디어와 비슷하다. 프로젝트 문서에서도 향후 <code>RecursiveCharacterTextSplitter</code>처럼 의미 단위, 문단, 문장 등을 우선하는 전략을 도입할 수 있다고 정리되어 있다.</p>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">장점</h4>
                            <div class="code-display" style="margin-bottom: 0.5rem;">현재보다 문맥이 덜 깨진다.
구현 난이도가 아주 높지는 않다.
문단형 문서에 효과가 좋다.
기존 DB 구조를 거의 그대로 쓸 수 있다.</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">단점</h4>
                            <div class="code-display" style="margin-bottom: 0.5rem;">문서 구조가 지저분하면 완벽하지 않다.
Markdown heading, 코드 블록 등은 별도 처리가 필요하다.</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">dev-ai 추천</h4>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;"><strong>가장 먼저 할 개선이다.</strong><br>기존 <code>CharacterChunker</code>를 바로 없애기보다 <code>chunk_strategy = character | recursive</code> 형태로 병행하면 좋다.</p>
                        </details>

                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">4-3. Token-aware Chunking</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">Token-aware 방식은 글자 수가 아니라 LLM tokenizer 기준으로 자른다.</p>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;"><code>800 characters</code>가 아니라 <code>500 tokens</code> 같은 식이다.</p>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">왜 중요하냐면 LLM 비용과 context window는 보통 token 기준이기 때문이다.</p>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">장점</h4>
                            <div class="code-display" style="margin-bottom: 0.5rem;">LLM context window 관리에 좋다.
prompt 길이 예측이 쉬워진다.
embedding model 입력 제한을 넘길 위험이 줄어든다.</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">단점</h4>
                            <div class="code-display" style="margin-bottom: 0.5rem;">tokenizer 의존성이 생긴다.
OpenAI, Anthropic, local model마다 tokenizer 차이가 있을 수 있다.
문단 의미 경계를 보장하지는 않는다.</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">dev-ai 적용 방향</h4>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;"><code>document_chunks</code>에 <code>token_count</code>, <code>chunk_strategy</code> 필드를 추가하면 좋다.<br>Qdrant payload에도 넣으면 좋다. <code>{"chunk_strategy": "token", "token_count": 482}</code></p>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">평가</h4>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">RAG 답변 품질 자체보다 <strong>운영 안정성</strong>에 좋다. 즉 “LLM 입력 길이 관리” 측면에서 중요하다.</p>
                        </details>

                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">4-4. Heading-aware Chunking</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">Heading-aware는 Markdown, HTML, docs 구조를 활용한다.</p>
                            <div class="code-display" style="margin-bottom: 0.5rem;">예:
# BomTS Dev AI
## Architecture
### FastAPI
### PostgreSQL
### Qdrant
## RAG Pipeline
### Ingestion
### Chunking</div>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">이 구조를 기준으로 chunk를 만든다.</p>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">장점</h4>
                            <div class="code-display" style="margin-bottom: 0.5rem;">기술 문서에 매우 강하다.
README/docs/공식문서에 적합하다.
검색 결과가 설명 가능해진다.
UI에서 section 표시가 가능하다.</div>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">검색 결과를 이렇게 보여줄 수 있다.<br><code>Document: RAG Pipeline Guide<br>Section: Chunking > Overlap<br>Score: 0.82</code></p>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">단점</h4>
                            <div class="code-display" style="margin-bottom: 0.5rem;">heading이 없는 문서에는 효과가 약하다.
Markdown/HTML/PDF parser가 필요하다.
문서 구조가 잘못되어 있으면 품질도 흔들린다.</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">dev-ai 적용 방향</h4>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">PostgreSQL <code>document_chunks</code>에 <code>heading_path</code>, <code>section_title</code>, <code>chunk_strategy</code> 필드가 있으면 좋다.</p>
                            <div class="code-display" style="margin-bottom: 0.5rem;">Qdrant payload에는:
{
  "heading_path": "RAG Pipeline > Chunking",
  "section_title": "Chunking",
  "source_type": "docs"
}</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">평가</h4>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;"><code>dev-ai</code>는 README, docs, AI Reference 문서가 많기 때문에 <strong>매우 잘 맞는다</strong>.</p>
                        </details>

                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">4-5. Metadata-rich Chunking</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">이건 chunk를 어떻게 자르느냐보다, chunk에 어떤 정보를 같이 붙이느냐의 문제다.</p>
                            <div class="code-display" style="margin-bottom: 0.5rem;">예:
{
  "document_id": 3,
  "chunk_index": 7,
  "title": "LangGraph Agent Workflow",
  "source": "manual",
  "license": "private",
  "source_type": "learning_note",
  "category": "agent",
  "heading_path": "Agent > LangGraph > Workflow",
  "published_at": null,
  "chunk_strategy": "heading_recursive",
  "token_count": 438
}</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">장점</h4>
                            <div class="code-display" style="margin-bottom: 0.5rem;">검색 결과 설명이 좋아진다.
Qdrant payload filtering에 유리하다.
source/category/license 기준 검색이 가능하다.
Evaluation log 분석이 쉬워진다.
Reference Pipeline과 잘 맞는다.</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">단점</h4>
                            <div class="code-display" style="margin-bottom: 0.5rem;">metadata 설계가 필요하다.
필드가 많아지면 관리가 복잡해진다.
잘못된 metadata는 검색 품질을 오히려 해칠 수 있다.</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">적재 성능/디스크 영향</h4>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">metadata는 vector 자체에 비하면 작다. 하지만 chunk 수가 많아지면 payload도 같이 늘어난다.</p>
                            <div class="code-display" style="margin-bottom: 0.5rem;">디스크 증가:
content 중복 > vector 저장량 > metadata</div>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">보통은 metadata 추가보다 overlap으로 인한 content 중복이 더 큰 문제다.</p>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">dev-ai 추천</h4>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;"><strong>강력 추천.</strong> 특히 현재 <code>AI Engineering Reference Pipeline</code>을 키우려면 metadata-rich 구조가 필요하다.</p>
                        </details>

                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">4-6. NLTK 기반 Chunking</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">NLTK는 전통적인 NLP toolkit이다. 문장 분리, tokenization, corpus 기반 처리 등에 많이 쓰인다. NLTK 자체는 오래된 대표적인 NLP 교육/연구용 toolkit으로, 다양한 NLP 모듈과 corpus를 제공한다. (<a href="https://arxiv.org/abs/cs/0205028" target="_blank" rel="noopener noreferrer">arXiv</a>)</p>
                            <div class="code-display" style="margin-bottom: 0.5rem;">NLTK 기반 chunking은 보통 이렇게 한다.
1. 문서를 문장 단위로 분리
2. 문장들을 chunk_size 안에 들어오도록 묶음
3. 필요하면 overlap 문장 몇 개 추가</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">장점</h4>
                            <div class="code-display" style="margin-bottom: 0.5rem;">문장 중간 절단이 줄어든다.
character 방식보다 자연스럽다.
구현이 비교적 간단하다.</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">단점</h4>
                            <div class="code-display" style="margin-bottom: 0.5rem;">한국어/마크다운/코드 문서에서 정확도가 떨어질 수 있다.
문장 분리 모델/리소스 관리가 필요하다.
기술 문서의 heading 구조는 따로 처리해야 한다.</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">dev-ai 적용 평가</h4>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">문장형 블로그/아티클에는 괜찮다. 하지만 README/docs/코드 섞인 문서에는 heading-aware나 recursive 방식이 더 먼저다.</p>
                        </details>

                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">4-7. spaCy 기반 Chunking</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">spaCy는 NLP pipeline을 구성할 수 있는 라이브러리다. sentence boundary detection, tokenization, 품사/개체명 인식 같은 pipeline을 연결할 수 있다. sentence boundary detection 자체는 NLP에서 중요한 기본 전처리이며, 도메인과 언어가 복잡할수록 오류가 downstream 품질에 영향을 준다는 연구도 있다. (<a href="https://arxiv.org/abs/2305.01211" target="_blank" rel="noopener noreferrer">arXiv</a>)</p>
                            <div class="code-display" style="margin-bottom: 0.5rem;">spaCy 기반 chunking은 보통 이렇게 한다.
1. spaCy로 문장 경계 감지
2. 문장/문단을 chunk_size 기준으로 묶음
3. 필요하면 entity, noun phrase 등 metadata 추가</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">장점</h4>
                            <div class="code-display" style="margin-bottom: 0.5rem;">문장 단위 보존이 좋다.
NLP pipeline 확장이 가능하다.
엔티티/키워드 추출과 결합 가능하다.</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">단점</h4>
                            <div class="code-display" style="margin-bottom: 0.5rem;">모델 설치가 필요하다.
CPU/메모리 사용량이 character 방식보다 크다.
한국어 모델 품질과 설치 전략을 고민해야 한다.</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">dev-ai 적용 평가</h4>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">나중에 Reference 문서에서 keyword/entity 추출까지 하고 싶다면 좋다. 하지만 단순 chunk 개선만 목적이라면 Recursive/Heading-aware가 먼저다.</p>
                        </details>

                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">4-8. Semantic Chunking</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">Semantic Chunking은 문장이나 문단의 embedding을 보고, 의미가 바뀌는 지점에서 chunk를 나누는 방식이다.</p>
                            <div class="code-display" style="margin-bottom: 0.5rem;">예:
문단 1: Docker 설명
문단 2: Docker Compose 설명
문단 3: PostgreSQL 설명
문단 4: Qdrant 설명

문단 1~2는 의미가 가깝고, 문단 3부터 의미가 바뀌면:
Chunk 1: Docker + Docker Compose
Chunk 2: PostgreSQL
Chunk 3: Qdrant
처럼 나눈다.</div>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">SBERT 같은 sentence embedding 모델은 문장을 의미 있는 vector로 만들고 cosine similarity로 비교할 수 있게 해 dense retrieval/semantic similarity에 활용된다. (<a href="https://arxiv.org/abs/1908.10084" target="_blank" rel="noopener noreferrer">arXiv</a>)</p>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">장점</h4>
                            <div class="code-display" style="margin-bottom: 0.5rem;">의미 단위 보존이 좋다.
서로 다른 주제가 한 chunk에 섞이는 문제를 줄일 수 있다.
검색 품질이 좋아질 가능성이 높다.</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">단점</h4>
                            <div class="code-display" style="margin-bottom: 0.5rem;">문장/문단별 embedding 비용이 발생한다.
적재 시간이 느려진다.
구현이 복잡하다.
threshold 튜닝이 필요하다.
문서 종류별 편차가 있다.</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">리소스</h4>
                            <div class="code-display" style="margin-bottom: 0.5rem;">CPU: 중간~높음
메모리: embedding batch 크기에 따라 증가
디스크: 결과 chunk 수와 vector 수에 따라 증가
비용: OpenAI embedding 사용 시 비용 증가</div>
                            <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">dev-ai 적용 평가</h4>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">고급 개선이다. 지금 당장보다, Reference Pipeline이 어느 정도 안정된 뒤 적용하는 게 좋다.</p>
                        </details>
                    </details>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">5. 성능 관점 요약</summary>
                        <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">적재 성능, 즉 ingestion/indexing 속도</h4>
                        <div class="code-display" style="margin-bottom: 0.5rem;">빠른 순서:
Character
→ Recursive/Paragraph-aware
→ Token-aware
→ Heading-aware
→ NLTK
→ spaCy
→ Semantic
→ LLM-guided</div>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">다만 실제 속도는 구현과 문서량에 따라 달라진다. 가장 느려지는 지점은 보통 이 둘이다.</p>
                        <div class="code-display" style="margin-bottom: 0.5rem;">1. 문장/문단별 embedding을 추가로 수행하는 Semantic Chunking
2. LLM에게 chunk 분리를 맡기는 LLM-guided Chunking</div>
                        
                        <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">사용 성능, 즉 검색/Ask 시점 성능</h4>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">검색 시점 성능은 chunking 방식 자체보다 <strong>생성된 chunk 수</strong>와 <strong>Qdrant index 크기</strong>에 더 영향을 받는다.</p>
                        <div class="code-display" style="margin-bottom: 0.5rem;">chunk 수가 많다
  ↓
vector 수 증가
  ↓
검색 index 커짐
  ↓
디스크/메모리 증가
  ↓
검색 latency 증가 가능</div>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">overlap을 크게 하면 chunk 수와 중복량이 증가한다.</p>
                        <div class="code-display" style="margin-bottom: 0.5rem;">chunk_size=800, overlap=100
→ step=700

chunk_size=800, overlap=400
→ step=400
→ chunk 수 크게 증가</div>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">즉 overlap은 문맥 보존에는 좋지만, 너무 크면 비용이 늘어난다.</p>
                    </details>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">6. 디스크 사용량 관점</summary>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">디스크 사용량은 대략 이렇게 증가한다.</p>
                        <div class="code-display" style="margin-bottom: 0.5rem;">PostgreSQL:
- document_chunks.content 저장량
- overlap으로 인한 중복 content
- metadata 컬럼/json 저장량

Qdrant:
- vector 수 × vector dimension × float 크기
- payload 저장량</div>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">현재 embedding dimension이 1536이라면 vector 하나당 float32 기준 대략:</p>
                        <div class="code-display" style="margin-bottom: 0.5rem;">1536 × 4 bytes = 6144 bytes ≈ 6KB</div>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">여기에 Qdrant 내부 index와 payload overhead가 더 붙는다. 즉 chunk 수가 중요하다.</p>
                        <div style="overflow-x: auto; margin-bottom: 1rem;">
                            <table style="width: 100%; border-collapse: collapse; line-height: 1.5; font-size: 0.9em;">
                                <thead>
                                    <tr style="background-color: var(--bg-main); text-align: left;">
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">전략</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); text-align: right;">chunk 수 경향</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">디스크 영향</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">큰 Character chunk</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">적음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">낮음</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">작은 Character chunk</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">많음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">높음</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">overlap 큼</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">많아짐</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">높음</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">Paragraph-aware</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">문서 구조에 따라 보통</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">Heading-aware</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">섹션 수에 따라 보통</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">Semantic</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">threshold에 따라 변동 큼</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간~높음</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">Metadata-rich</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">payload 증가</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">약간~중간 증가</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </details>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">7. 작업 난이도 기준 상세</summary>
                        <div style="overflow-x: auto; margin-bottom: 1rem;">
                            <table style="width: 100%; border-collapse: collapse; line-height: 1.5; font-size: 0.9em;">
                                <thead>
                                    <tr style="background-color: var(--bg-main); text-align: left;">
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">단계</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">구현 내용</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border); text-align: right;">난이도</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">예상 변경 범위</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">Character 유지</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">현재 코드 유지</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">매우 낮음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">없음</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">Recursive/Paragraph-aware</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">splitter 클래스 추가</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">낮음~중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);"><code>app/rag/chunker.py</code>, 테스트</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">Token-aware</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">tokenizer 추가, token_count 저장</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">chunker, schema/model 일부</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">Heading-aware</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">Markdown parser, heading_path 저장</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">chunker, DB model, Qdrant payload, UI</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">Metadata-rich</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">metadata 설계/저장/검색 표시</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">DB, API, Qdrant payload, UI</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">NLTK</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">의존성 추가, 문장 분리</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">requirements, chunker</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">spaCy</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">모델 설치, pipeline 구성</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">중간~높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">requirements, Docker image, chunker</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">Semantic</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">embedding 기반 boundary detection</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">chunker, embedding pipeline, 비용 관리</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">LLM-guided</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">LLM 호출 기반 segmentation</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); text-align: right;">매우 높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">provider, prompt, 비용/캐시/로그</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </details>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">8. dev-ai에 바로 넣을 수 있는 설계안 & 9. 최종 추천</summary>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">지금 바로 설계한다면 chunker를 이렇게 확장하면 좋다.</p>
                        <div class="code-display" style="margin-bottom: 0.5rem;">BaseChunker
  ├─ CharacterChunker
  ├─ RecursiveParagraphChunker
  ├─ TokenAwareChunker
  ├─ HeadingAwareChunker
  └─ SemanticChunker</div>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">그리고 API에서 옵션을 받게 한다.</p>
                        <div class="code-display" style="margin-bottom: 0.5rem;">{
  "chunk_strategy": "recursive",
  "chunk_size": 800,
  "chunk_overlap": 100
}</div>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">DB에는 최소한 이 정도 추가를 추천한다.</p>
                        <div class="code-display" style="margin-bottom: 0.5rem;">document_chunks
- chunk_strategy
- token_count
- heading_path
- metadata_json</div>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">Qdrant payload에는 이 정도를 넣는다.</p>
                        <div class="code-display" style="margin-bottom: 0.5rem;">{
  "document_id": 1,
  "chunk_id": 7,
  "title": "RAG Pipeline",
  "source": "manual",
  "license": "private",
  "category": "rag",
  "heading_path": "RAG > Chunking > Overlap",
  "chunk_strategy": "heading_recursive",
  "token_count": 512,
  "content": "..."
}</div>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">이렇게 하면 나중에 UI에서 이런 식으로 보여줄 수 있다.</p>
                        <div class="code-display" style="margin-bottom: 0.5rem;">Source: RAG Pipeline
Section: RAG > Chunking > Overlap
Strategy: heading_recursive
Tokens: 512
Score: 0.84</div>
                        <p style="margin-bottom: 1rem; line-height: 1.6;">이건 포트폴리오 설명력도 확 좋아진다.</p>

                        <h4 style="margin-top: 1rem; margin-bottom: 0.25rem;">최종 추천</h4>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">지금 <code>dev-ai</code>의 다음 개선은 이렇게 가는 게 좋다.</p>
                        <div class="code-display" style="margin-bottom: 0.5rem;">1. CharacterChunker는 유지한다.
2. RecursiveParagraphChunker를 추가한다.
3. chunk_strategy를 DB에 저장한다.
4. heading_path, token_count, metadata_json을 추가한다.
5. Qdrant payload에 metadata를 함께 넣는다.
6. UI에서 chunk 전략과 heading/source/category를 보여준다.
7. 이후 Semantic Chunking은 실험 모드로 추가한다.</div>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">면접/포트폴리오 설명은 이렇게 하면 된다.</p>
                        <div class="code-display" style="margin-bottom: 0.5rem;">현재 MVP에서는 전체 RAG 파이프라인을 빠르게 검증하기 위해 character 기반 chunking을 사용했습니다.
다만 character chunking은 문장, 문단, heading, token boundary를 이해하지 못하기 때문에
향후 recursive paragraph-aware, token-aware, heading-aware, metadata-rich chunking으로 개선할 수 있습니다.

특히 dev-ai는 AI Engineering 문서와 URL reference를 다루기 때문에
문서 구조를 보존하는 heading-aware chunking과
source/category/license/heading_path를 함께 저장하는 metadata-rich chunking이 중요합니다.
Semantic chunking은 검색 품질 개선 가능성이 있지만,
embedding 비용과 구현 복잡도가 커서 후속 실험 단계로 두는 것이 적절합니다.</div>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">핵심 결론은 이거다.</p>
                        <div class="code-display" style="margin-bottom: 0.5rem;">지금은 Character Chunking으로 MVP 검증.
다음은 Recursive + Heading-aware + Metadata-rich.
Semantic Chunking은 고급 실험 단계.</div>
                    </details>

                </div>
            </details>
        </section>"""

with open("web/docs.html", "r", encoding="utf-8") as f:
    content = f.read()

# We need to replace the old <!-- Chunking Strategy --> section.
# We will find the index of "<!-- Chunking Strategy -->"
start_idx = content.find("<!-- Chunking Strategy -->")

if start_idx != -1:
    # Everything before the chunk strategy block
    content_before = content[:start_idx]
    
    # Check if </main> exists after this index
    main_end_idx = content.find("</main>", start_idx)
    if main_end_idx != -1:
        content_after = content[main_end_idx:]
        new_content = content_before + html_content + "\n\n    " + content_after
        with open("web/docs.html", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated docs.html successfully.")
    else:
        print("Could not find </main>")
else:
    print("Could not find <!-- Chunking Strategy -->")
