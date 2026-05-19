import re

html_content = """        <!-- Indexing / Embedding / Qdrant -->
        <section class="card">
            <details>
                <summary style="cursor: pointer; display: flex; align-items: baseline; gap: 0.75rem; outline: none;">
                    <h2 style="margin: 0; display: inline-block;">Indexing / Embedding / Qdrant 이해</h2>
                    <span style="font-size: 0.95rem; font-weight: 500; color: var(--text-muted);">Embedding Vector, Qdrant, LLM Provider 구조 설명</span>
                </summary>
                <div style="margin-top: 1.5rem; animation: fadeIn 0.3s ease-in-out;">
                    <p style="margin-bottom: 1rem; line-height: 1.6;">현재 <code>dev-ai</code> 시스템의 RAG 구조에서 <strong>Embedding Vector, Qdrant, LLM Provider의 역할이 혼동될 수 있으므로</strong>, 이를 명확하게 설명합니다.</p>
                    <p style="margin-bottom: 1rem; line-height: 1.6; font-weight: 600; color: var(--primary);">RAG는 보통 “벡터로 AI에게 직접 조회”하는 구조가 아닙니다.<br>벡터는 Vector DB에서 관련 문서 chunk를 찾기 위한 검색 표현이고, 최종 AI 모델에는 vector가 아니라 검색된 chunk를 포함한 prompt 텍스트를 전달합니다.</p>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">1. 작업 목적 및 주요 오해 방지</summary>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">다음과 같은 흔한 오해를 방지해야 합니다.</p>
                        <div class="code-display" style="margin-bottom: 0.5rem;">오해 1. Gemma 3, Qwen 2.5, Google Gemini에 vector를 직접 보내서 검색하는 구조다.
오해 2. OpenAI embedding을 쓰면 답변 생성도 OpenAI가 해야 한다.
오해 3. Mock embedding 상태에서도 실제 의미 검색 품질이 검증된다.
오해 4. OpenClaw/Gemma/Qwen/Google Provider가 embedding에도 적용된다.</div>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;"><strong>정확한 설명은 다음과 같습니다:</strong></p>
                        <div style="background-color: #f8fafc; padding: 1rem; border-radius: 0.25rem; border: 1px solid #e2e8f0; line-height: 1.6;">
                            Embedding Provider는 질문과 chunk를 vector로 변환해 Qdrant 검색에 사용합니다.<br>
                            LLM Provider는 Qdrant에서 검색된 chunk를 prompt text로 받아 최종 답변을 생성합니다.<br><br>
                            따라서 OpenAI embedding + Qdrant + Gemma/Qwen/Google 답변 생성 조합은 완벽하게 가능하고, 이는 일반적인 RAG 구조와도 잘 맞습니다.
                        </div>
                    </details>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">2. 현재 코드 기준 사실 정리</summary>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">현재 시스템은 크게 두 레이어로 나뉩니다: <code>1. Embedding / Retrieval Layer</code>, <code>2. LLM Generation Layer</code></p>
                        
                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">2.1 Embedding / Retrieval Layer</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">현재 embedding은 <code>app/rag/embeddings.py</code>에서 처리합니다. 지원 모드는 <code>EMBEDDING_MODE=mock</code>과 <code>EMBEDDING_MODE=openai</code>입니다.</p>
                            <div class="code-display" style="margin-bottom: 0.5rem;">[mock]
- hashlib 기반 deterministic mock vector 생성
- 실제 의미 검색 품질 검증용이 아님
- 로컬 개발, 파이프라인 테스트용

[openai]
- OpenAI embedding API 사용
- model: text-embedding-3-small
- dimension: 1536
- 실제 semantic retrieval 품질 검증 가능</div>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">현재 <code>OpenClaw</code>, <code>Gemma</code>, <code>Qwen</code>, <code>Google Gemini</code>는 embedding provider가 아니며, 답변 생성 LLM Provider입니다.</p>
                        </details>

                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">2.2 Qdrant Retrieval Layer</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">Qdrant는 embedding vector를 저장하고 검색하는 역할입니다.</p>
                            <div class="code-display" style="margin-bottom: 0.5rem;">Qdrant point 저장 내용:
- id: chunk_id
- vector: chunk embedding vector
- payload: document_id, chunk_index, title, content, source</div>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">Qdrant는 AI 모델이 아닙니다. 질문 vector와 가까운 chunk vector를 찾는 semantic retrieval index입니다.</p>
                        </details>

                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">2.3 LLM Generation Layer</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">현재 답변 생성 provider는 <code>app/rag/llm_provider.py</code>에서 처리합니다.</p>
                            <div class="code-display" style="margin-bottom: 0.5rem;">FallbackLLMProvider 구조:
1. OpenClawLLMProvider (Gemma 3, Qwen 2.5 등)
2. GoogleLLMProvider (Gemini API)
3. OpenAILLMProvider (OpenAI Chat 모델)
4. MockLLMProvider (테스트 응답)</div>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">현재 LLM Provider는 embedding vector를 직접 받지 않습니다. Qdrant에서 검색된 chunk 내용과 prompt template이 결합된 <strong>최종 prompt text</strong>를 받습니다.</p>
                        </details>
                    </details>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">3. 현재 RAG 흐름 설명</summary>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">현재 시스템의 전체적인 흐름은 다음과 같습니다.</p>
                        <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                            <div class="code-display" style="flex: 1; min-width: 300px;">[Indexing Flow]

Document
  ↓
Chunking
  ↓
Embedding Provider
  - mock
  - openai
  ↓
Embedding Vector
  ↓
Qdrant Upsert
  ↓
Vector Index 저장</div>
                            <div class="code-display" style="flex: 1; min-width: 300px;">[Ask Flow]

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
  - OpenClaw / Gemma / Qwen
  - Google Gemini
  - OpenAI
  - Mock
  ↓
Answer</div>
                        </div>
                        <div style="background-color: #f8fafc; padding: 1rem; border-radius: 0.25rem; border-left: 4px solid var(--primary); margin-top: 1rem; line-height: 1.6; font-weight: 600;">
                            Embedding vector는 LLM에게 직접 전달되는 값이 아니라, Qdrant에서 관련 chunk를 찾기 위한 검색 표현입니다.<br>
                            LLM에게 전달되는 것은 vector가 아니라, 검색된 chunk를 포함한 자연어 prompt입니다.
                        </div>
                    </details>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">4. 사용자의 관점 정리</summary>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;"><strong>Q. "벡터로 AI에 직접 조회하지 않으니 완전하다고 할 순 없지만, 내부 RAG에서 벡터로 나온 결과를 chunk로 바꾸어서 다시 원래 AI에 검색/질문하는 경우는 흔할 것 같다. 현재 시스템이 어떻게 보면 더 효율적인 것 아닌가?"</strong></p>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">이 생각은 대체로 맞습니다. 일반적인 RAG 구조에서는 LLM이 vector를 직접 검색하지 않습니다. Embedding model과 Vector DB가 먼저 관련 chunk를 찾고, 그 결과를 prompt context로 만들어 최종 LLM에게 전달합니다.</p>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">따라서 OpenAI embedding으로 검색 품질을 확보하고, 답변 생성은 Gemma, Qwen, Gemini, GPT 등 여러 LLM Provider 중 하나를 사용하는 구조는 충분히 일반적이고 실용적입니다.</p>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">이 구조의 장점은 retrieval과 generation을 분리할 수 있다는 점입니다. 검색 품질은 embedding model과 Qdrant가 담당하고, 답변 품질과 문체, 추론 능력은 LLM Provider가 담당합니다.</p>
                    </details>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">5. 현재 구조가 효율적인 이유</summary>
                        
                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">5.1 Retrieval과 Generation 분리</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">검색(관련 문서 찾기, top-k chunk 반환)과 생성(검색된 context를 바탕으로 자연어 응답 생성)을 분리하면 여러 LLM을 교체하기 매우 쉽습니다.</p>
                            <div class="code-display" style="margin-bottom: 0.5rem;">예:
OpenAI embedding + Qdrant + Gemma 3
OpenAI embedding + Qdrant + Qwen 2.5
OpenAI embedding + Qdrant + Google Gemini
Local embedding + Qdrant + Local Qwen</div>
                        </details>

                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">5.2 여러 AI 모델을 같은 RAG 검색 결과에 연결 가능</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">동일한 질문에 대한 동일한 Qdrant 검색 결과를 여러 LLM에 동시에 전달할 수 있어, 향후 모델 비교나 평가 로그, 피드백 분석에 매우 유리합니다.</p>
                        </details>

                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">5.3 LLM별 context 처리 차이를 비교 가능</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">같은 chunk를 넣어도 모델마다 답변 품질과 특성이 다릅니다. 이는 모델 교체형 AI 백엔드 포트폴리오로 설명하기 아주 좋은 강점입니다.</p>
                            <ul style="list-style-position: inside; line-height: 1.8; margin-bottom: 0.5rem;">
                                <li><strong>Gemma:</strong> 로컬/온프레미스 실험에 적합</li>
                                <li><strong>Qwen:</strong> 코딩/기술 답변에 강점</li>
                                <li><strong>Gemini:</strong> API 기반의 안정적 Fallback</li>
                                <li><strong>OpenAI:</strong> 품질 비교의 기준점</li>
                            </ul>
                        </details>
                    </details>

                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">6. 현재 구조의 한계</summary>
                        
                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">6.1 Mock embedding 상태의 한계</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">Mock embedding은 실제 의미를 이해하지 않습니다. hash 기반 deterministic vector이므로 검색 파이프라인 테스트에는 유용하지만, semantic retrieval 품질 검증에는 부적합합니다.</p>
                            <div style="background-color: #fffbeb; padding: 1rem; border-radius: 0.25rem; border-left: 4px solid #b45309; line-height: 1.6; color: #92400e;">
                                <strong>주의:</strong> 현재 Mock Embedding 모드에서는 RAG 파이프라인 동작은 확인할 수 있지만, 실제 의미 검색 품질은 신뢰하기 어렵습니다. 실제 검색 품질 검증에는 OpenAI 또는 Local Embedding Provider를 사용해야 합니다.
                            </div>
                        </details>

                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">6.2 OpenClaw/Gemma/Qwen은 embedding provider가 아님</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">현재 OpenClaw는 prompt를 받아 답변을 생성하는 LLM Provider이며, embedding vector 생성에는 사용되지 않습니다. (They are generation providers, not embedding providers.)</p>
                        </details>

                        <details style="margin-bottom: 0.5rem; padding-left: 1rem; margin-top: 0.5rem;">
                            <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">6.3 Local embedding provider 부재</summary>
                            <p style="margin-bottom: 0.5rem; line-height: 1.6;">현재 local LLM 답변 생성은 가능하지만, local embedding provider는 별도로 구현되어 있지 않습니다. 향후 <code>LocalEmbeddingProvider</code> (Ollama embedding, bge-m3, multilingual-e5 등)의 추가가 필요합니다.</p>
                        </details>
                    </details>
                    
                    <details style="margin-bottom: 1rem; padding-left: 1rem;">
                        <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">7. 결론 / 요약</summary>
                        <p style="margin-bottom: 0.5rem; line-height: 1.6;">BomTS Dev AI는 검색을 위해 embedding을 사용하고, 생성을 위해 LLM을 사용하는 전형적이고 실용적인 RAG 아키텍처를 따르고 있습니다.</p>
                        <div class="code-display" style="margin-bottom: 0.5rem;">현재 구조는 맞다.
다만 mock embedding 상태라면 “잘 돌아간다”는 것은 파이프라인 기준이고,
“검색 품질까지 좋다”는 뜻은 아니다.</div>
                    </details>
                </div>
            </details>
        </section>"""

with open("web/docs.html", "r", encoding="utf-8") as f:
    original_html = f.read()

# Find the end of the Chunking Strategy section
chunk_strategy_end = original_html.find("<!-- Chunking Strategy -->")
if chunk_strategy_end != -1:
    # We need to find the closing tag of the <section class="card"> for chunking.
    # The chunking section starts at chunk_strategy_end.
    section_start = original_html.find("<section", chunk_strategy_end)
    section_end = original_html.find("</section>", section_start) + len("</section>")
    
    content_before = original_html[:section_end]
    content_after = original_html[section_end:]
    
    new_html = content_before + "\n\n" + html_content + content_after
    
    with open("web/docs.html", "w", encoding="utf-8") as f:
        f.write(new_html)
    print("Successfully added Indexing / Embedding / Qdrant section.")
else:
    print("Could not find <!-- Chunking Strategy -->")
