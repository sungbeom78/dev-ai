import sys

html_content = """
<!-- Search and Ask -->
<section class="card" style="background-color: #f8fafc; border: 1px solid var(--border);">
    <details>
        <summary style="cursor: pointer; display: flex; align-items: baseline; gap: 0.75rem; outline: none;">
            <h2 style="margin: 0; display: inline-block;">Search와 Ask</h2>
            <span style="font-size: 0.95rem; font-weight: 500; color: var(--text-muted);">검색과 생성의 차이 및 디버깅 방법</span>
        </summary>
        <div style="margin-top: 1.5rem; animation: fadeIn 0.3s ease-in-out;">
            
            <details style="margin-bottom: 1rem; padding-left: 1rem;" open>
                <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">Search와 Ask는 서로 다른 목적을 가진다.</summary>
                
                <p style="margin-bottom: 0.75rem; line-height: 1.6;">
                    <strong>Search</strong>는 사용자의 질문을 embedding vector로 변환한 뒤 Qdrant에서 의미적으로 가까운 chunk를 찾는 retrieval 단계입니다.<br>
                    이 단계에서는 LLM을 호출하지 않습니다.
                </p>
                <p style="margin-bottom: 0.75rem; line-height: 1.6;">
                    <strong>Ask</strong>는 Search 결과를 context로 구성하고, PromptBuilder를 통해 최종 prompt를 만든 뒤 LLM Provider에게 답변 생성을 요청합니다.<br>
                    즉 Ask는 retrieval과 generation을 결합한 RAG 단계입니다.
                </p>
                <div style="background-color: #fffbeb; padding: 1rem; border-radius: 0.25rem; border-left: 4px solid #b45309; line-height: 1.6; color: #92400e; margin-bottom: 0.75rem;">
                    <strong>디버깅 팁:</strong> 답변이 이상할 때는 먼저 Search 결과를 확인해야 합니다.<br>
                    - Search 결과가 틀렸다면 embedding, chunking, indexing, Qdrant 데이터 문제일 가능성이 높습니다.<br>
                    - Search 결과가 맞는데 답변이 이상하다면 prompt 구성이나 LLM Provider 문제를 확인해야 합니다.
                </div>
            </details>

            <details style="margin-bottom: 1rem; padding-left: 1rem;" open>
                <summary style="font-size: 1.25rem; font-weight: 600; cursor: pointer; color: var(--primary); margin-bottom: 0.5rem;">디버깅 판단표</summary>
                
                <div style="overflow-x: auto;">
                    <table style="width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 0.9em; min-width: 600px;">
                        <thead>
                            <tr style="background-color: #f1f5f9; text-align: left;">
                                <th style="border: 1px solid var(--border); padding: 0.75rem;">증상</th>
                                <th style="border: 1px solid var(--border); padding: 0.75rem;">먼저 볼 곳</th>
                                <th style="border: 1px solid var(--border); padding: 0.75rem;">원인 후보</th>
                                <th style="border: 1px solid var(--border); padding: 0.75rem;">개선 방향</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td style="border: 1px solid var(--border); padding: 0.75rem; font-weight: 500;">Ask 답변이 엉뚱함</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">Search 결과</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">검색 chunk가 틀림</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">embedding/indexing/chunking 점검</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid var(--border); padding: 0.75rem; font-weight: 500;">Search 결과가 엉뚱함</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">Qdrant / embedding</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">mock embedding, index 누락, 테스트 데이터 섞임</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">real embedding 적용, 재색인, 필터링</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid var(--border); padding: 0.75rem; font-weight: 500;">Search 결과는 맞는데 답변이 약함</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">Prompt</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">context 지시 부족, 답변 규칙 약함</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">PromptBuilder 개선</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid var(--border); padding: 0.75rem; font-weight: 500;">답변이 너무 일반적임</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">Prompt / LLM</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">context를 안 따름</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">“context 기반 답변” 규칙 강화</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid var(--border); padding: 0.75rem; font-weight: 500;">답변이 source와 다름</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">Prompt / LLM</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">hallucination</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">모르면 모른다고 답하게 지시</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid var(--border); padding: 0.75rem; font-weight: 500;">응답이 mock처럼 보임</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">LLM Provider</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">fallback/mock 사용</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">provider/env 상태 확인</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid var(--border); padding: 0.75rem; font-weight: 500;">답변은 좋은데 source가 이상함</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">Retrieval / Logging</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">source payload 문제</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">Qdrant payload, ask_source_logs 점검</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid var(--border); padding: 0.75rem; font-weight: 500;">느림</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">Embedding / LLM</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">OpenAI API, Google API, local model latency</td>
                                <td style="border: 1px solid var(--border); padding: 0.75rem;">provider별 latency 로그 확인</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </details>

        </div>
    </details>
</section>
"""

with open("web/docs.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace </main> with html_content + </main>
if "</main>" in content:
    new_content = content.replace("</main>", html_content + "\n    </main>")
    with open("web/docs.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully added the 'Search와 Ask' section.")
else:
    print("Error: </main> not found.")
