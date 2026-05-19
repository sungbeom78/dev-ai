import sys

html_content = """
<!-- AI Engineering Reference Pipeline -->
<section class="card" style="background-color: #f8fafc; border: 1px solid var(--border);">
    <details>
        <summary style="cursor: pointer; display: flex; align-items: baseline; gap: 0.75rem; outline: none;">
            <h2 style="margin: 0; display: inline-block;">AI Engineering Reference Pipeline</h2>
            <span style="font-size: 0.95rem; font-weight: 500; color: var(--text-muted);">개인 AI 지식 실험실로의 발전</span>
        </summary>
        <div style="margin-top: 1.5rem; animation: fadeIn 0.3s ease-in-out;">
            
            <p style="margin-bottom: 1rem; line-height: 1.6;">
                AI Engineering Reference Pipeline은 BomTS Dev AI를 개인 AI Engineering Knowledge Lab으로 발전시키기 위한 구조입니다.
            </p>

            <p style="margin-bottom: 1rem; line-height: 1.6;">
                수동 문서 등록만으로는 빠르게 변화하는 AI 개발 흐름을 따라가기 어렵습니다.<br>
                따라서 이 프로젝트는 AI 기술 블로그, 공식 문서, 모델 릴리스 노트, RAG/Agent/Local LLM 관련 자료를 source registry로 관리하고, URL fetch를 통해 본문을 수집한 뒤, raw reference로 저장합니다.
            </p>

            <p style="margin-bottom: 1rem; line-height: 1.6;">
                수집된 reference는 단순 원문 보관에 그치지 않고, 요약, 핵심 변화, 왜 중요한지, dev-ai에 어떻게 적용할 수 있는지, 후속 작업 제안, 주의사항 같은 briefing 정보로 확장될 수 있습니다.<br>
                최종적으로 reference는 공통 Document 모델로 변환되고, 기존의 Chunking, Embedding, Qdrant Indexing, Search, Ask 파이프라인을 통해 질의응답에 활용됩니다.
            </p>

            <div style="background-color: #eff6ff; padding: 1rem; border-radius: 0.25rem; border-left: 4px solid #3b82f6; line-height: 1.6; color: #1e3a8a; margin-bottom: 1.5rem;">
                <strong>이 구조를 통해 BomTS Dev AI는 단순 RAG 데모가 아니라, AI 개발 트렌드를 수집하고, 해석하고, 내 프로젝트에 적용하기 위한 개인 지식 실험실로 발전할 수 있습니다.</strong>
            </div>

            <h3 style="margin-bottom: 1rem; color: var(--primary);">단계별 의미 및 구현 상태</h3>
            
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 1rem; font-size: 0.9em; min-width: 800px;">
                    <thead>
                        <tr style="background-color: #f1f5f9; text-align: left;">
                            <th style="border: 1px solid var(--border); padding: 0.75rem;">단계</th>
                            <th style="border: 1px solid var(--border); padding: 0.75rem;">의미</th>
                            <th style="border: 1px solid var(--border); padding: 0.75rem;">현재 구현</th>
                            <th style="border: 1px solid var(--border); padding: 0.75rem;">향후 개선</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="border: 1px solid var(--border); padding: 0.75rem; font-weight: 500;">Source Registry</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">관리할 출처 등록</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;"><code>ContentSource</code> 모델/API 존재</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">source별 정책, 주기적 crawl</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid var(--border); padding: 0.75rem; font-weight: 500;">URL Fetch</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">URL에서 본문 추출</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;"><code>trafilatura</code>, <code>BeautifulSoup</code>, <code>requests</code> 사용</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">실패 처리, canonical URL, metadata 추출</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid var(--border); padding: 0.75rem; font-weight: 500;">Raw Reference</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">수집 원문/상태 저장</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;"><code>CrawledPage</code> 저장</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">author, published_at 자동 추출 강화</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid var(--border); padding: 0.75rem; font-weight: 500;">Summary</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">원문 요약</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">필드 존재</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">LLM 기반 자동 요약</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid var(--border); padding: 0.75rem; font-weight: 500;">Application Note</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">dev-ai 적용 메모</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;"><code>AIReferenceBriefing</code> 필드 존재</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">자동 생성/수동 승인 workflow</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid var(--border); padding: 0.75rem; font-weight: 500;">Document Conversion</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">RAG용 Document 변환</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">URL fetch 시 Document 생성</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">briefing도 Document화</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid var(--border); padding: 0.75rem; font-weight: 500;">Chunk/Index</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">의미 검색 가능하게 변환</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">기존 문서 파이프라인 사용 가능</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">metadata-rich indexing</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid var(--border); padding: 0.75rem; font-weight: 500;">Reference Q&A</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">수집 자료 기반 질의응답</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">기본 RAG로 가능</td>
                            <td style="border: 1px solid var(--border); padding: 0.75rem;">reference 전용 UI/filter/평가</td>
                        </tr>
                    </tbody>
                </table>
            </div>

        </div>
    </details>
</section>
"""

with open("web/docs.html", "r", encoding="utf-8") as f:
    content = f.read()

if "</main>" in content:
    new_content = content.replace("</main>", html_content + "\n    </main>")
    with open("web/docs.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully added the 'AI Engineering Reference Pipeline' section.")
else:
    print("Error: </main> not found.")
