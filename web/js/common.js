// common.js
document.addEventListener('DOMContentLoaded', () => {
    const statusBtn = document.getElementById('api-status-button');
    const modal = document.getElementById('status-modal');
    const closeBtn = document.getElementById('close-modal');
    const statusDetails = document.getElementById('status-details');

    // Initial simple check
    fetch('/api/health')
        .then(res => res.json())
        .then(data => {
            if (statusBtn) {
                statusBtn.textContent = 'API: Online';
                statusBtn.style.color = '#16a34a';
                statusBtn.style.borderColor = '#16a34a';
            }
        })
        .catch(err => {
            if (statusBtn) {
                statusBtn.textContent = 'API: Offline';
                statusBtn.style.color = '#dc2626';
                statusBtn.style.borderColor = '#dc2626';
            }
        });

    if (statusBtn && modal && closeBtn) {
        statusBtn.addEventListener('click', async () => {
            modal.classList.add('active');
            statusDetails.innerHTML = '<p>상세 상태를 불러오는 중...</p>';
            
            try {
                const res = await fetch('/api/system/status');
                if (!res.ok) throw new Error('Network error');
                const data = await res.json();
                
                let html = '';
                
                // Helper to format rows
                const row = (key, val, highlight = false) => {
                    const color = highlight ? (val.toString().toLowerCase() === 'online' || val === true ? '#16a34a' : (val.toString().toLowerCase() === 'offline' || val === false ? '#dc2626' : 'var(--text-muted)')) : 'var(--text-muted)';
                    return `<div class="status-row">
                        <span class="status-key">${key}</span>
                        <span class="status-val" style="color: ${color}; font-weight: ${highlight ? '600' : 'normal'}">${val}</span>
                    </div>`;
                };

                if (data.llm.provider.toLowerCase() === 'mock') {
                    html += '<div style="background-color: #fef08a; color: #854d0e; padding: 1rem; border-radius: 0.5rem; border: 1px solid #eab308; margin-bottom: 1rem;">';
                    html += '<strong>현재 Mock Provider입니다.</strong><br>이 상태에서는 실제 AI 분석이 아니라 개발 테스트용 응답만 생성됩니다.</div>';
                }

                html += '<h3>API 서버</h3>';
                html += row('API 상태', data.api.status, true);
                html += row('버전', data.api.version);
                html += row('Web UI', 'Online', true);

                html += '<h3 style="margin-top: 1rem;">데이터베이스 & 벡터 검색</h3>';
                html += row('PostgreSQL', data.database.status, true);
                html += row('Qdrant', data.vector_db.status, true);
                html += row('벡터 개수', data.vector_db.vector_count);

                html += '<h3 style="margin-top: 1rem;">LLM 제공자 (Provider)</h3>';
                html += row('현재 설정된 Provider', data.llm.provider, true);
                html += row('현재 모델', data.llm.model);
                
                html += '<div style="margin-top: 0.5rem; padding: 0.75rem; background-color: var(--bg-main); border-radius: 0.25rem;">';
                html += row('Google API 설정', data.llm.google_enabled ? '설정됨' : '미설정');
                html += row('OpenClaw 연동', data.llm.openclaw_enabled ? '설정됨' : '미설정');
                html += '</div>';

                html += '<h3 style="margin-top: 1rem;">기술 레퍼런스 데이터</h3>';
                html += row('등록된 소스(출처) 개수', data.reference_pipeline.source_count);
                html += row('수집된 문서 수', data.reference_pipeline.crawled_page_count);
                
                html += '<h3 style="margin-top: 1rem;">자동화 스케줄러</h3>';
                html += row('상태', data.scheduler.enabled ? '활성화됨' : '비활성화됨');
                html += row('수집 주기', `${data.scheduler.interval_hours} 시간`);

                statusDetails.innerHTML = html;

            } catch (error) {
                statusDetails.innerHTML = `<p style="color: #dc2626;">상세 상태를 불러올 수 없습니다: ${error.message}</p>`;
            }
        });

        closeBtn.addEventListener('click', () => {
            modal.classList.remove('active');
        });

        // Close on background click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
    }
});
