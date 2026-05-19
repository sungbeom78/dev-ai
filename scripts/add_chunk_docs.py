import re

html_content = """
        <!-- Chunking Strategy -->
        <section class="card">
            <details>
                <summary style="cursor: pointer; display: flex; align-items: baseline; gap: 0.75rem; outline: none;">
                    <h2 style="margin: 0; display: inline-block;">Chunking 전략 및 개선 방향</h2>
                    <span style="font-size: 0.95rem; font-weight: 500; color: var(--text-muted);">현재 프로젝트 기반의 Chunking 아키텍처</span>
                </summary>
                <div style="margin-top: 1.5rem; animation: fadeIn 0.3s ease-in-out;">
                    <p style="margin-bottom: 1rem; line-height: 1.6;">RAG에서는 긴 문서를 그대로 embedding하면 여러 주제가 하나의 vector에 섞여 검색 정확도가 떨어질 수 있습니다. 그래서 문서를 검색과 LLM 입력에 적합한 작은 단위인 chunk로 나눕니다.</p>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">현재 프로젝트 기반 Chunk 설명</summary>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">현재 프로젝트에서는 MVP 단계에서 전체 파이프라인을 빠르게 검증하기 위해 character 기반 chunking을 사용했습니다.<br>
                        chunk_size는 800자로 설정했고, chunk_overlap은 100자로 설정했습니다.<br>
                        800자는 한 chunk의 최대 길이를 의미하고, overlap 100자는 chunk 경계에서 문맥이 끊기는 문제를 줄이기 위한 장치입니다.</p>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">다만 character chunking은 문장, 문단, Markdown heading, 코드 블록 같은 의미 구조를 이해하지 못하기 때문에 문맥이 중간에 끊길 수 있습니다.<br>
                        향후에는 token 기반 chunking으로 LLM context를 더 정확히 관리하고, heading 기반 chunking으로 문서 구조를 보존하며, semantic chunking으로 의미가 바뀌는 지점에서 chunk를 나누는 방향으로 개선할 수 있습니다.</p>
                        <p style="margin-bottom: 1rem; line-height: 1.6;">현재 <code>dev-ai</code>는 <strong>Character Chunking</strong>을 사용합니다. 코드상 <code>CharacterChunker(chunk_size=800, chunk_overlap=100)</code>이고, <code>start</code>부터 <code>start + chunk_size</code>까지 자른 뒤 다음 시작점을 <code>chunk_size - chunk_overlap</code>만큼 이동합니다. 즉 현재는 <strong>800자 단위, 100자 중복</strong> 방식입니다.</p>
                    </details>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">1. 전체 비교표</summary>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">표의 기준은 <code>dev-ai</code>에 적용했을 때의 상대 평가입니다.</p>
                        <div style="overflow-x: auto; margin-bottom: 1rem;">
                            <table style="width: 100%; border-collapse: collapse; line-height: 1.5; font-size: 0.9em; min-width: 800px;">
                                <thead>
                                    <tr style="background-color: var(--bg-main); text-align: left;">
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">방식</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">내용</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">특징</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">장점</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">단점</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">적재 성능</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">사용 성능</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">CPU/메모리</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">작업 난이도</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">우선순위</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Character</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">고정 길이 분할</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">단순 절단</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">구현 매우 쉬움, 빠름</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">의미 단위 보존 약함</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">매우 빠름</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">보통</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">낮음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">매우 낮음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); color: #2563eb; font-weight: 600;">적용됨</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Recursive / Paragraph</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">자연스러운 경계 우선 탐색</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">재귀 분할</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">문맥 보존 좋음, 가성비 큼</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">문서 형식 엉망이면 한계</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">빠름</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">낮음~중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">낮음~중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); color: #16a34a; font-weight: 600;">1순위 추천</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Token-aware</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">LLM token 기준 분할</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">비용/context 중심</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">입력 길이 관리에 최적</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">tokenizer 의존성</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">빠름~중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">안정적</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); color: #16a34a; font-weight: 600;">2순위 추천</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Heading-aware</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">Markdown 문서 구조 기준</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">섹션 구조 보존</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">검색 결과 설명력 높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">heading 없는 문서에 한계</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">매우 좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); color: #16a34a; font-weight: 600;">2순위 추천</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Metadata-rich</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">heading, category 함께 저장</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">검색/필터링 강화</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">payload filtering 가능</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">구조/설계 필요</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">매우 좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); color: #9333ea; font-weight: 600;">강력 추천</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Semantic Chunking</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">의미 유사도 기준 분할</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">고급 RAG 전처리</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">주제 단위 보존 최상</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">느리고 비용 높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">느림</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">잠재력 높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); color: #ea580c; font-weight: 600;">후순위 고려</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <p style="margin-top: 0.5rem; margin-bottom: 1rem; line-height: 1.6;">최근 문서 chunking 관련 연구도 chunking 전략의 효과가 “항상 하나의 정답”으로 결정되지 않고, 검색 태스크의 성격에 따라 달라진다고 보고합니다. 특히 fixed-size, sentence/paragraph 기반, semantic/LLM-guided, contextualized chunking 같은 여러 축으로 나눠 평가할 필요가 있다는 점이 중요합니다. (<a href="https://arxiv.org/abs/2602.16974" target="_blank" rel="noopener noreferrer" style="color: #3b82f6;">arXiv</a>)</p>
                    </details>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">2. dev-ai 기준 추천 순서</summary>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">지금 프로젝트에서는 이 순서가 가장 현실적입니다.</p>
                        <ol style="list-style-position: inside; line-height: 1.8; margin-bottom: 1rem;">
                            <li><strong>Recursive / Paragraph-aware Chunking</strong>: 현재 character 방식에서 가장 적은 수정으로 품질 개선 가능</li>
                            <li><strong>Metadata-rich Chunking</strong>: Qdrant payload, source 추적, UI 설명력, 평가 로그 개선</li>
                            <li><strong>Heading-aware Chunking</strong>: README/docs/기술문서가 많은 dev-ai에 특히 적합</li>
                            <li><strong>Token-aware Chunking</strong>: LLM context와 embedding 입력 길이 관리에 필요</li>
                            <li><strong>Semantic Chunking</strong>: 고급 개선. 비용과 복잡도 때문에 나중에</li>
                        </ol>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">즉 지금 바로 개선한다면 다음과 같은 흐름이 좋습니다:</p>
                        <div class="code-display" style="margin-bottom: 1rem;">CharacterChunker
  ↓
RecursiveParagraphChunker
  ↓
MetadataRichChunker
  ↓
HeadingAware + TokenAware
  ↓
SemanticChunker</div>
                    </details>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">3. 상세 비교표: 품질/성능/비용 관점</summary>
                        <div style="overflow-x: auto; margin-bottom: 1rem;">
                            <table style="width: 100%; border-collapse: collapse; line-height: 1.5; font-size: 0.9em; min-width: 600px;">
                                <thead>
                                    <tr style="background-color: var(--bg-main); text-align: left;">
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">방식</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">검색 품질</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">답변 품질</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">문맥 보존</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">비용</th>
                                        <th style="padding: 0.75rem; border-bottom: 2px solid var(--border);">설명 가능성</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Character</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">보통</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">보통</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">낮음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">낮음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">보통</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Recursive / Paragraph</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간~높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">낮음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">좋음</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Heading-aware</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">중간</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600; color: #16a34a;">매우 좋음</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); font-weight: 600;">Semantic</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">매우 좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">매우 좋음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border); color: #dc2626;">높음</td>
                                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border);">좋음</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </details>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">4. 방식별 설명</summary>
                        
                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">4-1. Character Chunking</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">현재 코드 <code>chunk_text()</code>의 방식입니다. <code>start = 0</code>에서 시작해 <code>end = start + chunk_size</code>까지 자르고, 다음 <code>start</code>를 <code>chunk_size - chunk_overlap</code>만큼 이동시킵니다.</p>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;"><strong>장점:</strong> 구현이 쉽고 빠르며 디버깅이 쉬워 MVP 전체 파이프라인 검증에 적합합니다.<br><strong>단점:</strong> 문장/문단 중간에서 잘릴 수 있으며, 마크다운 코드 블록이나 표를 망가뜨릴 수 있습니다.</p>
                        </details>
                        
                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">4-2. Recursive / Paragraph-aware Chunking</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">무조건 800자로 자르지 않고 자연스러운 경계(큰 섹션 > 문단 > 문장 > 줄바꿈)를 우선적으로 탐색합니다.</p>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;"><strong>장점:</strong> 문맥이 덜 깨지며 구현 난이도 대비 효과가 커서 가장 우선적으로 해야 할 개선 사항입니다.</p>
                        </details>

                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">4-3. Heading-aware Chunking & Metadata-rich Chunking</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">Markdown 헤딩 구조를 활용하거나 <code>source_type</code>, <code>category</code> 등의 메타데이터를 결합하는 방식입니다.</p>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">특히 <code>dev-ai</code>는 기술 문서를 다루므로 검색 결과가 매우 설명 가능해집니다. 향후 Qdrant payload 필터링과 UI 표시를 위해 매우 추천됩니다.</p>
                        </details>

                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">4-4. Semantic Chunking & LLM-guided Chunking</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">의미 유사도 기준이나 LLM 프롬프트를 통해 의미적인 경계에서 분할합니다.</p>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">주제 단위 보존이 가장 탁월하지만 embedding 비용과 적재 시간이 크게 늘어나기 때문에 고급 개선, 후속 실험으로 미루는 것이 좋습니다.</p>
                        </details>
                    </details>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">5. 현 시스템에 대한 AI 추가 설계</summary>
                        <p style="margin-bottom: 1rem; line-height: 1.6;">지금 바로 설계한다면 chunker를 다음과 같이 확장하면 좋습니다.</p>
                        <ol style="list-style-position: inside; line-height: 1.8; margin-bottom: 1rem;">
                            <li>CharacterChunker는 유지한다.</li>
                            <li>RecursiveParagraphChunker를 추가한다.</li>
                            <li><code>chunk_strategy</code>를 DB에 저장한다.</li>
                            <li><code>heading_path</code>, <code>token_count</code>, <code>metadata_json</code>을 추가한다.</li>
                            <li>Qdrant payload에 metadata를 함께 넣는다.</li>
                            <li>UI에서 chunk 전략과 heading/source/category를 보여준다.</li>
                            <li>이후 Semantic Chunking은 실험 모드로 추가한다.</li>
                        </ol>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;"><strong>포트폴리오 설명 팁:</strong></p>
                        <div style="background-color: #f8fafc; padding: 1rem; border-radius: 0.25rem; border: 1px solid #e2e8f0; line-height: 1.6;">
                            현재 MVP에서는 전체 RAG 파이프라인을 빠르게 검증하기 위해 character 기반 chunking을 사용했습니다.<br>
                            다만 character chunking은 문장, 문단, heading 경계를 이해하지 못하기 때문에 향후 recursive paragraph-aware, token-aware, heading-aware, metadata-rich chunking으로 개선할 수 있습니다.<br>
                            특히 dev-ai는 AI Engineering 문서와 URL reference를 다루기 때문에 문서 구조를 보존하는 heading-aware chunking과 source/category를 함께 저장하는 metadata-rich chunking이 중요합니다.<br>
                            Semantic chunking은 검색 품질 개선 가능성이 있지만, embedding 비용과 구현 복잡도가 커서 후속 실험 단계로 두는 것이 적절합니다.
                        </div>
                    </details>
                </div>
            </details>
        </section>
"""

with open("web/docs.html", "r", encoding="utf-8") as f:
    original = f.read()

# "문서 등록 단계" section is in a <section class="card"> ... </section> block.
# I need to insert this right after that block.
# Actually, the simplest way is to insert it right before </main>.
# Let's check where the "문서 등록 단계" section is.
# In the file, the previous edit added it just before </main>.

new_content = original.replace("</main>", html_content + "\n    </main>")

with open("web/docs.html", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Insertion complete.")
