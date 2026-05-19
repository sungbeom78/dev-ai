import re
import os

file_path = "web/docs.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

sections_to_update = [
    {
        "old_title": "왜 이 프로젝트를 만들었는가",
        "new_title": "왜 이 프로젝트를 만들었는가",
        "subtitle": "단순 API 호출을 넘어선 실무 AI 파이프라인 설계"
    },
    {
        "old_title": "전체 시스템 구조",
        "new_title": "전체 시스템 구조",
        "subtitle": "FastAPI, Docker, Nginx 기반의 서비스 아키텍처"
    },
    {
        "old_title": "사용 기술과 역할",
        "new_title": "사용 기술과 역할",
        "subtitle": "각 컴포넌트의 도입 목적과 상세 역할"
    },
    {
        "old_title": "RAG 파이프라인 흐름",
        "new_title": "RAG 파이프라인 흐름",
        "subtitle": "문서 수집부터 의미 검색, 답변 생성까지의 단계별 처리"
    },
    {
        "old_title": "PostgreSQL과 Qdrant는 왜 둘 다 필요한가",
        "new_title": "PostgreSQL과 Qdrant는 왜 둘 다 필요한가",
        "subtitle": "데이터 영속성 관리와 의미 검색의 역할 분리"
    },
    {
        "old_title": "LangGraph Agent Workflow",
        "new_title": "LangGraph Agent Workflow",
        "subtitle": "질문 의도를 선행적으로 분류"
    },
    {
        "old_title": "AI Engineering Reference Pipeline",
        "new_title": "AI Engineering Reference Pipeline",
        "subtitle": "AI 기술 동향 브리핑"
    },
    {
        "old_title": "테스트 콘솔 사용법",
        "new_title": "테스트 콘솔 사용법",
        "subtitle": "\"테스트 콘솔\" 페이지 활용 가이드"
    },
    {
        "old_title": "면접/포트폴리오 설명 포인트",
        "new_title": "포트폴리오의 가치",
        "subtitle": "AI가 만든 시스템의 구성"
    }
]

for sec in sections_to_update:
    old_t = sec["old_title"]
    new_t = sec["new_title"]
    sub_t = sec["subtitle"]
    
    # Pattern to match:
    # <section class="card" ...>
    #     <h2 ...>old_title</h2>
    #     ... content ...
    # </section>
    # We will use a regex that matches from <section to </section>
    
    pattern = r'(<section\s+class="card"[^>]*>)\s*<h2[^>]*>' + re.escape(old_t) + r'</h2>(.*?)        </section>'
    
    def replacer(match):
        section_open = match.group(1)
        inner_content = match.group(2)
        
        # If it's the portfolio section, keep its style. The user requested keeping the green background.
        # It's already in the <section> attributes.
        
        # Wrap the inner content with details and summary
        new_html = f"""{section_open}
            <details>
                <summary style="cursor: pointer; display: flex; align-items: baseline; gap: 0.75rem; outline: none;">
                    <h2 style="margin: 0; display: inline-block;">{new_t}</h2>
                    <span style="font-size: 0.95rem; font-weight: 500; color: var(--text-muted);">{sub_t}</span>
                </summary>
                <div style="margin-top: 1.5rem; animation: fadeIn 0.3s ease-in-out;">{inner_content}                </div>
            </details>
        </section>"""
        return new_html

    content = re.sub(pattern, replacer, content, flags=re.DOTALL)

# Add keyframes for smooth fade in if not exists
if "keyframes fadeIn" not in content:
    css_to_add = """
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-5px); }
            to { opacity: 1; transform: translateY(0); }
        }
        details > summary { list-style: none; }
        details > summary::-webkit-details-marker { display: none; }
        details > summary::before { content: '▶'; display: inline-block; font-size: 0.8rem; margin-right: 0.5rem; transition: transform 0.2s; color: var(--primary); }
        details[open] > summary::before { transform: rotate(90deg); }
    """
    content = content.replace("</style>", css_to_add + "\n    </style>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully updated docs.html")
