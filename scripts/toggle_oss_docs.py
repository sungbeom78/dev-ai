import sys

with open("web/docs.html", "r", encoding="utf-8") as f:
    content = f.read()

target_start = "<!-- Open Source Embedding Consideration -->\n<section class=\"card\" style=\"background-color: #f8fafc; border: 1px solid var(--border);\">\n    <h2>오픈소스 Embedding 고려</h2>"

replacement_start = """<!-- Open Source Embedding Consideration -->
<section class="card" style="background-color: #f8fafc; border: 1px solid var(--border);">
    <details>
        <summary style="cursor: pointer; display: flex; align-items: baseline; gap: 0.75rem; outline: none;">
            <h2 style="margin: 0; display: inline-block;">오픈소스 Embedding 고려</h2>
            <span style="font-size: 0.95rem; font-weight: 500; color: var(--text-muted);">향후 로컬 모델 및 확장 계획</span>
        </summary>
        <div style="margin-top: 1.5rem; animation: fadeIn 0.3s ease-in-out;">"""

if target_start in content:
    content = content.replace(target_start, replacement_start)
    
    # We also need to add the closing tags before the closing </section> of this section
    # Let's find the closing section tag by looking for the next </section> after the start
    start_idx = content.find(replacement_start)
    if start_idx != -1:
        end_idx = content.find("</section>", start_idx)
        if end_idx != -1:
            content_before = content[:end_idx]
            content_after = content[end_idx:]
            # Inject closing div and details
            new_content = content_before + "        </div>\n    </details>\n" + content_after
            
            with open("web/docs.html", "w", encoding="utf-8") as f:
                f.write(new_content)
            print("Successfully wrapped open source embedding section in toggle.")
        else:
            print("Could not find closing </section>")
else:
    print("Could not find target_start.")
