const mockPanel = {
    isOpen: false,
    
    toggle(){
        this.isOpen ? this.close() : this.open();
    },
    
    open(){
        document.getElementById('mockPanel').classList.add('mock-panel-open');
        this.isOpen = true;
        if (!this.mocked) this.loadMocks();
    },
    
    close(){
        document.getElementById('mockPanel').classList.remove('mock-panel-open');
        this.isOpen = false;
    },
    
    async loadMocks(){
        try {
            const data = await fetch('/api/mocks').then(r => r.json());
            this.renderMocks(data.queries || []);
            this.mocked = true;
        } catch (e) {
            document.getElementById('mockList').innerHTML = '<div style="text-align:center;padding:2rem;color:#666">Failed to load</div>';
        }
    },
    
    renderMocks(queries){
        const mockList = document.getElementById('mockList');
        if (!queries.length) {
            mockList.innerHTML = '<div style="text-align:center;padding:2rem;color:#999">No issues</div>';
            return;
        }
        mockList.innerHTML = queries.map((q, i) => `
            <div class="mock-issue-item">
                <div class="mock-issue-content">
                    <span class="mock-issue-label">Mock ${i + 1}</span>
                    <p class="mock-issue-text">${this.esc(q)}</p>
                </div>
                <button onclick="mockPanel.use('${this.esc(q).replace(/'/g, "\\'")}')" class="mock-issue-copy-btn">Copy & Use</button>
            </div>
        `).join('');
    },
    
    use(query){
        document.getElementById('issue-field').value = query.replace(/\\\"/g, '"');
        document.getElementById('issue-field').focus();
        this.close();
    },
    
    esc(text){
        const map = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'};
        return text.replace(/[&<>"']/g, m => map[m]);
    }
};

document.addEventListener('click', (e) => {
    const panel = document.getElementById('mockPanel');
    const btn = document.querySelector('[onclick="mockPanel.toggle()"]');
    if (mockPanel.isOpen && !panel.contains(e.target) && !btn.contains(e.target)) {
        mockPanel.close();
    }
});