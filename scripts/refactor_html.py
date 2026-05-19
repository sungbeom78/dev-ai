import re

with open('/project/dev_ai/web/docs.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Refactor Hero Section
hero_start = html.find('<section class="card" style="border-top: 4px solid var(--primary);">')
if hero_start != -1:
    hero_end = html.find('</section>', hero_start)
    hero_content = html[hero_start:hero_end+10]
    
    new_hero = hero_content.replace(
        '<section class="card" style="border-top: 4px solid var(--primary);">\n            <h1 class="hero-title">BomTS Dev AI</h1>',
        '<details class="card" open style="border-top: 4px solid var(--primary);">\n            <summary style="cursor: pointer; outline: none;"><h1 class="hero-title" style="display: inline-block; margin-bottom: 0;">BomTS Dev AI</h1></summary>\n            <div style="margin-top: 1rem;">'
    ).replace('</section>', '            </div>\n        </details>')
    
    html = html.replace(hero_content, new_hero)

# Refactor other sections
sections = re.findall(r'(<section class="card"(.*?)>\s*<h2(.*?)>(.*?)</h2>\s*(.*?)\s*</section>)', html, re.DOTALL)

for full_match, card_attrs, h2_attrs, title, body in sections:
    new_section = f'''<details class="card"{card_attrs}>
            <summary style="cursor: pointer; outline: none;"><h2{h2_attrs} style="display: inline-block; margin: 0;">{title}</h2></summary>
            <div style="margin-top: 1.5rem;">
                {body}
            </div>
        </details>'''
    html = html.replace(full_match, new_section)

with open('/project/dev_ai/web/docs.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Refactoring done.")
