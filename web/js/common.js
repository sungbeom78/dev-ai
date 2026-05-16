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

                html += '<h3>API Server</h3>';
                html += row('Status', data.api.status, true);
                html += row('Version', data.api.version);
                html += row('Web UI', 'Online', true);

                html += '<h3 style="margin-top: 1rem;">Database & Vector Store</h3>';
                html += row('PostgreSQL', data.database.status, true);
                html += row('Qdrant', data.vector_db.status, true);
                html += row('Vector Count', data.vector_db.vector_count);

                html += '<h3 style="margin-top: 1rem;">LLM Provider</h3>';
                html += row('Current Provider', data.llm.provider);
                html += row('Current Model', data.llm.model);
                
                html += '<div style="margin-top: 0.5rem; padding: 0.75rem; background-color: var(--bg-main); border-radius: 0.25rem;">';
                html += '<p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.5rem;"><strong>OpenClaw 연동:</strong> 개인 데스크탑에서 실행 중인 모델을 활용하기 위한 선택 기능입니다. 항상 연결 가능한 운영 의존성은 아닙니다.</p>';
                html += row('OpenClaw Enabled', data.llm.openclaw_enabled ? 'Configured' : 'Not Configured');
                html += row('Google Provider Enabled', data.llm.google_enabled ? 'Configured' : 'Not Configured');
                html += '</div>';

                html += '<h3 style="margin-top: 1rem;">Reference Pipeline</h3>';
                html += row('Source Count', data.reference_pipeline.source_count);
                html += row('Crawled Pages', data.reference_pipeline.crawled_page_count);
                
                html += '<h3 style="margin-top: 1rem;">Scheduler</h3>';
                html += row('Enabled', data.scheduler.enabled);
                html += row('Interval', `${data.scheduler.interval_hours} Hours`);

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
