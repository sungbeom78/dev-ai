import sys

html_content = """
<!-- Logs / Feedback / Evaluation -->
<section class="card" style="background-color: #f8fafc; border: 1px solid var(--border);">
    <details>
        <summary style="cursor: pointer; display: flex; align-items: baseline; gap: 0.75rem; outline: none;">
            <h2 style="margin: 0; display: inline-block;">Logs / Feedback / Evaluation</h2>
            <span style="font-size: 0.95rem; font-weight: 500; color: var(--text-muted);">관찰하고 개선할 수 있는 AI 시스템의 핵심</span>
        </summary>
        <div style="margin-top: 1.5rem; animation: fadeIn 0.3s ease-in-out;">
            
            <div style="background-color: #f0fdf4; padding: 1rem; border-radius: 0.25rem; border-left: 4px solid #16a34a; line-height: 1.6; color: #166534; margin-bottom: 1.5rem;">
                Logs / Feedback / Evaluation은 BomTS Dev AI가 단순한 RAG 데모가 아니라, 관찰하고 개선할 수 있는 AI 시스템이 되기 위한 핵심 구조입니다.
            </div>

            <p style="margin-bottom: 1rem; line-height: 1.6;">
                AI 답변은 단순한 함수 결과가 아닙니다. 사용자 질문이 들어온 뒤, 질문 의도 분류, embedding 생성, Qdrant 검색, source chunk 선택, prompt 구성, LLM Provider 호출, 답변 생성, 사용자 피드백까지 여러 단계를 거쳐 만들어집니다.
            </p>

            <p style="margin-bottom: 1rem; line-height: 1.6;">
                따라서 최종 답변만 저장해서는 충분하지 않습니다. 질문, 답변, endpoint type, intent, provider, model, latency뿐 아니라, 어떤 source chunk가 검색되었고, 그 score가 얼마였으며, 사용자가 그 답변을 어떻게 평가했는지까지 함께 남겨야 합니다.
            </p>

            <ul style="margin-bottom: 1.5rem; line-height: 1.6; padding-left: 1.5rem; color: var(--text-main);">
                <li><strong>Ask log</strong>는 질문과 답변의 기본 실행 기록입니다.</li>
                <li><strong>Source log</strong>는 RAG 답변이 어떤 문서 chunk를 근거로 생성되었는지 추적하기 위한 기록입니다.</li>
                <li><strong>Feedback log</strong>는 사용자의 평가와 의견을 저장합니다.</li>
            </ul>

            <p style="margin-bottom: 1.5rem; line-height: 1.6;">
                이 세 가지가 연결되면 하나의 평가 데이터가 됩니다. 예를 들어 어떤 답변이 down 평가를 받았을 때, 검색된 source가 엉뚱했다면 retrieval 문제이고, source는 적절했지만 답변이 부족했다면 prompt 또는 LLM Provider 문제일 수 있습니다. provider와 model, latency 기록을 함께 보면 어떤 모델이 더 좋은 답변을 만드는지, 어떤 provider가 느리거나 불안정한지도 분석할 수 있습니다.<br>
                <strong>즉 Logs / Source Logs / Feedback은 RAG 품질 개선을 위한 관찰 데이터이자, 향후 AI가 스스로 답변 품질을 분석하고 개선 방향을 제안하기 위한 평가 데이터셋의 출발점입니다.</strong>
            </p>

            <h3 style="margin-bottom: 1rem; color: var(--primary);">상세 기록 및 아키텍처 철학</h3>
            
            <details style="margin-bottom: 0.5rem; padding-left: 1rem;">
                <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">1. 왜 로그가 필요한가</summary>
                <p style="margin-bottom: 0.5rem; line-height: 1.6;">
                    AI 답변이 만들어지기까지 여러 단계가 관여하므로, 답변이 좋았는지 나빴는지를 판단하려면 최종 답변이 아닌 <strong>과정 전체</strong>를 남겨야 합니다. 이를 통해 사용자가 문제를 제기했을 때 답변을 <strong>재검토</strong>하고, <strong>근거를 추적</strong>하며, <strong>검색 문제와 생성 문제를 분리</strong>하고, <strong>모델과 provider를 비교</strong>하며, 궁극적으로 사용자 평가를 단순 감상이 아닌 <strong>데이터</strong>로 만들 수 있습니다.
                </p>
            </details>

            <details style="margin-bottom: 0.5rem; padding-left: 1rem;">
                <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">2. 현재 dev-ai에서 남기는 로그</summary>
                <div style="margin-bottom: 0.5rem;">
                    <p style="line-height: 1.6; margin-bottom: 0.5rem;"><strong>ask_logs</strong>: 질문, 의도(intent), 답변, provider, model, latency, retrieval_count 등을 담습니다. 누가 무엇을 물었고 어떤 모델이 답했는지 확인합니다.</p>
                    <p style="line-height: 1.6; margin-bottom: 0.5rem;"><strong>ask_source_logs</strong>: 답변에 사용된 검색 근거(문서 ID, chunk ID, 내용, score, 출처)를 저장합니다. RAG 답변이 이상할 때 가장 먼저 봐야 할 핵심 데이터입니다.</p>
                    <p style="line-height: 1.6; margin-bottom: 0.5rem;"><strong>feedback_logs</strong>: 사용자의 평가(up/down/neutral)와 의견을 저장합니다. 이 피드백 하나는 단순한 점수가 아니라, 앞서 쌓인 질문, 답변, source, latency 등의 로그 전체와 연결되어 평가 데이터셋을 이룹니다.</p>
                </div>
            </details>

            <details style="margin-bottom: 0.5rem; padding-left: 1rem;">
                <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">3. Source log와 Feedback의 결합이 만드는 가치</summary>
                <p style="margin-bottom: 0.5rem; line-height: 1.6;">
                    RAG 품질은 Retrieval(검색)과 Generation(생성) 두 축으로 결정됩니다. 답변이 이상할 때 Source log가 없다면 이유가 검색 문제인지, 생성 문제인지 구분할 수 없습니다.<br>
                    사용자가 남긴 "검색 결과는 맞는데 답변이 부족하다"는 Feedback은 Source log와 결합되어, "해당 의도(intent)에서 특정 Provider의 Prompt를 보강해야 한다"는 명확한 개선 지표로 탈바꿈합니다. 즉, AI가 스스로 분석하고 개선 방향을 도출할 수 있는 기반이 됩니다.
                </p>
            </details>

            <details style="margin-bottom: 0.5rem; padding-left: 1rem;">
                <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">4. Latency와 Provider/Model 기록의 중요성</summary>
                <p style="margin-bottom: 0.5rem; line-height: 1.6;">
                    Latency는 단순 성능이 아닌 사용자 경험, 비용, 안정성을 나타내는 지표입니다. 향후 Embedding, 검색, LLM 호출 등 단계별로 Latency를 세분화하면 어떤 구간이 병목인지 파악할 수 있습니다.<br>
                    또한 OpenClaw 내 여러 모델(Gemma, Qwen 등) 및 Google, OpenAI, Mock 등 다양한 Provider 환경에서 실제로 어떤 모델이 답했는지(혹은 Fallback 되었는지) 기록함으로써 성능 및 비용 효율성을 정확히 비교할 수 있습니다.
                </p>
            </details>

            <details style="margin-bottom: 0.5rem; padding-left: 1rem;">
                <summary style="font-size: 1.1rem; font-weight: 600; cursor: pointer; color: var(--text-main); margin-bottom: 0.5rem;">5. 향후 발전 방향 (추가 기록 항목 제안)</summary>
                <ul style="line-height: 1.6; padding-left: 1.5rem; color: var(--text-muted);">
                    <li><strong>Agent Workflow</strong>: 각 Node 통과 내역 및 Intent 분류 이유 명시</li>
                    <li><strong>Embedding & Retrieval 상세</strong>: Embedding Provider/Model, Qdrant Collection명, 필터 제외 사유 등</li>
                    <li><strong>Source 상세 토글화</strong>: Token 수, Prompt 실제 포함 여부 등을 상세 토글로 관리</li>
                    <li><strong>Prompt & LLM</strong>: Prompt Version, Fallback 이유, Token Count 기록</li>
                    <li><strong>Feedback 사유 분류</strong>: 사용자가 구체적 사유(잘못된 출처, 짧은 길이, 환각 등)를 체크할 수 있는 UI 도입</li>
                </ul>
            </details>

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
    print("Successfully added the 'Logs / Feedback / Evaluation' section.")
else:
    print("Error: </main> not found.")
