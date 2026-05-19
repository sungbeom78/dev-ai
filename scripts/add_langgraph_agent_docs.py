import sys

html_content = """
<!-- LangGraph Agent -->
<section class="card" style="background-color: #f8fafc; border: 1px solid var(--border);">
    <details>
        <summary style="cursor: pointer; display: flex; align-items: baseline; gap: 0.75rem; outline: none;">
            <h2 style="margin: 0; display: inline-block;">LangGraph Agent</h2>
            <span style="font-size: 0.95rem; font-weight: 500; color: var(--text-muted);">질문 의도 분류 및 조건부 라우팅 구조</span>
        </summary>
        <div style="margin-top: 1.5rem; animation: fadeIn 0.3s ease-in-out;">
            
            <p style="margin-bottom: 1rem; line-height: 1.6;">
                LangGraph Agent는 단순 RAG를 실제 서비스형 AI Workflow로 확장하기 위한 구조입니다.
            </p>
            
            <p style="margin-bottom: 1rem; line-height: 1.6;">
                기본 RAG는 모든 질문을 검색 후 답변 생성 흐름으로 처리합니다. 하지만 실제 AI 서비스에서는 질문 유형에 따라 다른 처리 경로가 필요합니다. 예를 들어 시스템 상태 질문, 사용법 질문, 범위 외 질문, 모호한 질문은 문서 검색 기반 RAG와 다른 방식으로 처리하는 것이 적절합니다.
            </p>

            <p style="margin-bottom: 1.5rem; line-height: 1.6;">
                이 프로젝트는 <strong>LangGraph</strong>를 사용해 질문 처리 흐름을 여러 단계로 나누어 구성합니다. 먼저 사용자의 질문이 들어오면 <code>classify_intent</code> 단계에서 질문 의도를 분류합니다. 그리고 분류 결과에 따라 <code>rag_answer</code>, <code>system_status_answer</code>, <code>how_to_use_answer</code>, <code>out_of_scope_answer</code>, <code>clarification_answer</code> 중 적절한 처리 단계로 이동합니다. 실제 코드에서도 <code>classify_intent</code>를 시작점으로 두고, intent 값에 따라 각 답변 node로 분기하는 구조를 사용합니다.
            </p>

            <div style="margin-bottom: 1.5rem;">
                <h4 style="margin-bottom: 0.75rem; color: var(--text-main);">이 흐름을 구성하기 위해 LangGraph에서는 State, Node, Edge라는 개념을 사용합니다.</h4>
                
                <details style="margin-bottom: 0.5rem; padding-left: 1rem;" open>
                    <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">State</summary>
                    <p style="margin-bottom: 0.5rem; line-height: 1.6;">
                        <code>State</code>는 질문 처리 과정에서 유지되는 작업 데이터입니다. 단순히 원본 질문만 의미하는 것이 아니라, 질문을 처리하면서 생기는 중간 결과와 실행 정보를 함께 담습니다. 예를 들어 <code>question</code>, <code>intent</code>, <code>answer</code>, <code>sources</code>, <code>provider</code>, <code>model</code>, <code>workflow_steps</code> 같은 값이 State에 담깁니다.
                    </p>
                </details>

                <details style="margin-bottom: 0.5rem; padding-left: 1rem;" open>
                    <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">Node</summary>
                    <p style="margin-bottom: 0.5rem; line-height: 1.6;">
                        <code>Node</code>는 State를 받아 특정 작업을 수행하는 처리 단계입니다. 예를 들어 <code>classify_intent</code> node는 질문 의도를 판단해 <code>intent</code> 값을 채우고, <code>rag_answer</code> node는 RAG 검색과 답변 생성을 수행하며, <code>out_of_scope_answer</code> node는 범위 밖 질문에 대한 안내 응답을 만듭니다.
                    </p>
                </details>

                <details style="margin-bottom: 0.5rem; padding-left: 1rem;" open>
                    <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">Edge</summary>
                    <p style="margin-bottom: 0.5rem; line-height: 1.6;">
                        <code>Edge</code>는 Node와 Node 사이의 이동 경로입니다. 일반적인 Edge는 한 단계가 끝난 뒤 다음 단계로 이동하게 하고, 조건이 있는 Edge는 State에 담긴 값에 따라 다음 Node를 선택합니다. 이 프로젝트에서는 <code>classify_intent</code> 단계에서 결정된 <code>intent</code> 값을 기준으로 어떤 답변 node로 이동할지 결정합니다.
                    </p>
                </details>
            </div>

            <div style="background-color: #f0fdf4; padding: 1rem; border-radius: 0.25rem; border-left: 4px solid #16a34a; line-height: 1.6; color: #166534;">
                이 구조 덕분에 AI Agent의 처리 흐름을 하나의 거대한 함수로 만들지 않고, 질문 분류, RAG 답변, 사용법 안내, 시스템 상태 응답, 범위 외 질문 처리처럼 관찰 가능하고 확장 가능한 단계들의 조합으로 표현할 수 있습니다.
            </div>

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
    print("Successfully added the 'LangGraph Agent' section.")
else:
    print("Error: </main> not found.")
