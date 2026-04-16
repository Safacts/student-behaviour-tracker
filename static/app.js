// Global Data & State
const API_BASE = window.location.origin;
const state = {
    activeTab: 'dashboard',
    charts: {},
    explorer: {
        table: '',
        offset: 0,
        limit: 15
    }
};

// Chart.js Professional Styling
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(2, 6, 23, 0.95)';
Chart.defaults.plugins.tooltip.padding = 12;
Chart.defaults.plugins.tooltip.cornerRadius = 8;
Chart.defaults.plugins.tooltip.borderWidth = 1;
Chart.defaults.plugins.tooltip.borderColor = 'rgba(255,255,255,0.1)';

// Lifecycle Setup
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initDashboard();
    initExplorer();
    initStudentDetail();
    
    // Auto-load dashboard on start
    refreshDashboard();
});

// --- Core Navigation ---
function initNavigation() {
    document.querySelectorAll('.nav-item').forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            document.querySelectorAll('.nav-item').forEach(b => b.classList.toggle('active', b === btn));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.toggle('active', c.id === tab));
            
            state.activeTab = tab;
            onTabSwitch(tab);
        });
    });
}

function onTabSwitch(tab) {
    if (tab === 'dashboard') refreshDashboard();
    if (tab === 'explorer' && !state.explorer.table) loadTableList();
}

// --- Dashboard Domain ---
async function initDashboard() {
    // Basic setup already in lifecycle
}

async function refreshDashboard() {
    try {
        const [summaryRes, topRes] = await Promise.all([
            fetch(`${API_BASE}/analytics/summary`),
            fetch(`${API_BASE}/analytics/top_students`)
        ]);
        
        const summary = await summaryRes.json();
        const topData = await topRes.json();
        
        // Update KPIs
        document.getElementById('stat-students').innerText = summary.total_students;
        document.getElementById('stat-sessions').innerText = summary.total_sessions.toLocaleString();
        document.getElementById('stat-avg-time').innerText = `${Math.round(summary.avg_time_minutes)}m`;
        
        renderSubjectDistribution(summary.subject_distribution);
        renderTopStudents(topData.top_students);
    } catch (err) {
        console.error('Dashboard synchronization failed:', err);
    }
}

function renderSubjectDistribution(data) {
    const ctx = document.getElementById('subjectChart').getContext('2d');
    if (state.charts.subject) state.charts.subject.destroy();
    
    state.charts.subject = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(d => d.subject_category.toUpperCase()),
            datasets: [{
                data: data.map(d => d.count),
                backgroundColor: ['#6366f1', '#8b5cf6', '#0ea5e9', '#10b981', '#f59e0b', '#ef4444'],
                borderWidth: 0,
                hoverOffset: 15
            }]
        },
        options: {
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: { position: 'right', labels: { usePointStyle: true, padding: 20, font: { size: 11, weight: '500' } } }
            }
        }
    });
}

function renderTopStudents(students) {
    const list = document.getElementById('top-students-list');
    list.innerHTML = '';
    
    students.forEach((s, i) => {
        const item = document.createElement('div');
        item.className = 'student-rank-item';
        item.style.display = 'flex';
        item.style.alignItems = 'center';
        item.style.gap = '16px';
        item.style.padding = '12px';
        item.style.borderRadius = '12px';
        item.style.background = 'rgba(255,255,255,0.02)';
        item.style.marginBottom = '8px';
        
        item.innerHTML = `
            <div style="font-size: 14px; font-weight: 700; color: var(--text-muted); width: 20px;">#${i+1}</div>
            <div class="avatar" style="width: 32px; height: 32px; font-size: 11px;">${s.name.substring(0, 2).toUpperCase()}</div>
            <div style="flex: 1;">
                <div style="font-size: 13px; font-weight: 600;">${s.name}</div>
                <div style="font-size: 11px; color: var(--text-muted);">Cumulative Focus: ${s.total_time}m</div>
            </div>
            <div class="badge" style="background: rgba(99, 102, 241, 0.1); color: var(--primary);">SYNCED</div>
        `;
        list.appendChild(item);
    });
}

// --- Data Explorer Domain ---
function initExplorer() {
    const tableSelect = document.getElementById('table-select');
    tableSelect.addEventListener('change', (e) => {
        state.explorer.table = e.target.value;
        state.explorer.offset = 0;
        loadExplorerData();
    });
    
    document.getElementById('prev-page').onclick = () => {
        if (state.explorer.offset > 0) {
            state.explorer.offset -= state.explorer.limit;
            loadExplorerData();
        }
    };
    
    document.getElementById('next-page').onclick = () => {
        state.explorer.offset += state.explorer.limit;
        loadExplorerData();
    };
}

async function loadTableList() {
    const select = document.getElementById('table-select');
    try {
        const res = await fetch(`${API_BASE}/tables`);
        const data = await res.json();
        
        select.innerHTML = '<option value="">Select Target Table...</option>';
        data.tables.forEach(t => {
            const opt = document.createElement('option');
            opt.value = t;
            opt.innerText = t;
            select.appendChild(opt);
        });
    } catch (err) { console.error('Archive list failed:', err); }
}

async function loadExplorerData() {
    if (!state.explorer.table) return;
    try {
        const res = await fetch(`${API_BASE}/data/${state.explorer.table}?limit=${state.explorer.limit}&offset=${state.explorer.offset}`);
        const result = await res.json();
        
        renderExplorerTable(result.data);
        document.getElementById('record-count').innerText = `${result.total} entries cached`;
        document.getElementById('page-info').innerText = `${Math.floor(state.explorer.offset / state.explorer.limit) + 1} / ${Math.ceil(result.total / state.explorer.limit)}`;
    } catch (err) { console.error('Archive retrieval failed:', err); }
}

function renderExplorerTable(data) {
    const head = document.getElementById('table-head');
    const body = document.getElementById('table-body');
    head.innerHTML = '';
    body.innerHTML = '';
    
    if (!data.length) return;
    
    const columns = Object.keys(data[0]);
    columns.forEach(col => {
        const th = document.createElement('th');
        th.innerText = col;
        head.appendChild(th);
    });
    
    data.forEach(row => {
        const tr = document.createElement('tr');
        columns.forEach(col => {
            const td = document.createElement('td');
            const val = row[col];
            if (val && typeof val === 'string' && (val.startsWith('{') || val.startsWith('['))) {
                td.innerHTML = '<span class="badge" style="background:rgba(255,255,255,0.05); color:var(--text-muted)">JSON OBJECT</span>';
            } else {
                td.innerText = val !== null ? val : '---';
            }
            tr.appendChild(td);
        });
        body.appendChild(tr);
    });
}

// --- Student Intelligence Domain ---
function initStudentDetail() {
    document.getElementById('load-student-btn').addEventListener('click', () => {
        const id = document.getElementById('target-student-id').value;
        if (id) syncStudentIntelligence(id);
    });
    
    document.getElementById('generate-ai-report-btn').addEventListener('click', () => {
        const id = document.getElementById('target-student-id').value;
        if (id) generateIntelligenceAdvisory(id);
    });
    
    // Initial sync
    syncStudentIntelligence(4);
}

async function syncStudentIntelligence(id) {
    try {
        const res = await fetch(`${API_BASE}/analytics/student/${id}`);
        const data = await res.json();
        
        document.getElementById('student-name').innerText = data.student.username ? data.student.name : 'Unknown Subject';
        document.getElementById('student-id-display').innerText = `NODE_ID: ${id} • ACCESS_ROLE: ${data.student.role || 'RESTRICTED'}`;
        
        renderStudentTrajectory(data.time_series);
        renderStudentRadar(data.subject_stats);
        renderBehavioralEvents(data.recent_sessions);
        
        // Hide old report on new sync
        document.getElementById('ai-report-box').style.display = 'none';
    } catch (err) { console.error('Intelligence sync failed:', err); }
}

async function generateIntelligenceAdvisory(id) {
    const btn = document.getElementById('generate-ai-report-btn');
    const box = document.getElementById('ai-report-box');
    const textZone = document.getElementById('report-text');
    
    btn.innerHTML = '<span>⚡</span> Processing Neural Patterns...';
    btn.disabled = true;
    
    try {
        const res = await fetch(`${API_BASE}/analytics/generate_report/${id}`);
        const data = await res.json();
        
        document.getElementById('report-date').innerText = `ANALYSIS PERIOD: ${data.period.start} → ${data.period.end}`;
        
        // Advanced Parsing for structured report
        textZone.innerHTML = parseStructuredReport(data.report);
        
        box.style.display = 'block';
        box.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (err) {
        alert('Neural processing failed. Verify student activity logs exist for the requested period.');
    } finally {
        btn.innerHTML = '<span>✨</span> Generate Intelligence Report';
        btn.disabled = false;
    }
}

function parseStructuredReport(text) {
    const tag = '[INTELLIGENCE_SUMMARY]';
    let content = text;
    
    if (text.includes(tag)) {
        content = text.split(tag)[1].trim();
    }
    
    return `
        <div class="report-section" style="position: relative; padding-left: 56px;">
            <div style="position: absolute; left: 12px; top: 16px; font-size: 24px;">🧠</div>
            <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; color: var(--primary); margin-bottom: 8px; letter-spacing: 1px;">Insight Summary</div>
            <div style="font-size: 15px; color: var(--text-primary); line-height: 1.8; opacity: 0.95;">${content}</div>
        </div>
    `;
}

function renderStudentTrajectory(series) {
    const ctx = document.getElementById('studentTimeSeriesChart').getContext('2d');
    if (state.charts.trajectory) state.charts.trajectory.destroy();
    
    state.charts.trajectory = new Chart(ctx, {
        type: 'line',
        data: {
            labels: series.map(s => s.log_date),
            datasets: [{
                label: 'Focus Intensity (Minutes)',
                data: series.map(s => s.total_minutes),
                borderColor: '#6366f1',
                backgroundColor: (context) => {
                    const chart = context.chart;
                    const {ctx, chartArea} = chart;
                    if (!chartArea) return null;
                    const gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
                    gradient.addColorStop(0, 'rgba(99, 102, 241, 0)');
                    gradient.addColorStop(1, 'rgba(99, 102, 241, 0.1)');
                    return gradient;
                },
                fill: true,
                tension: 0.4,
                borderWidth: 3,
                pointRadius: 4,
                pointBackgroundColor: '#6366f1'
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { display: false } },
                y: { grid: { color: 'rgba(255,255,255,0.03)' }, beginAtZero: true }
            }
        }
    });
}

function renderStudentRadar(stats) {
    const ctx = document.getElementById('studentSubjectChart').getContext('2d');
    if (state.charts.radar) state.charts.radar.destroy();
    
    state.charts.radar = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: stats.map(s => s.subject_category.toUpperCase()),
            datasets: [{
                label: 'Competency Mapping',
                data: stats.map(s => s.avg_minutes),
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                borderColor: '#6366f1',
                borderWidth: 2,
                pointBackgroundColor: '#6366f1',
                pointRadius: 3
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                r: {
                    angleLines: { color: 'rgba(255,255,255,0.05)' },
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    pointLabels: { font: { size: 10, weight: '600' } },
                    ticks: { display: false }
                }
            }
        }
    });
}

function renderBehavioralEvents(sessions) {
    const zone = document.getElementById('student-activities');
    zone.innerHTML = '';
    
    sessions.forEach(s => {
        const item = document.createElement('div');
        item.style.padding = '16px';
        item.style.borderBottom = '1px solid var(--border-subtle)';
        item.style.display = 'flex';
        item.style.justifyContent = 'space-between';
        
        // Data sanitization for lesson name
        let displayTitle = s.lesson_name || 'Generic Module';
        if (displayTitle.includes(':') && displayTitle.includes(',')) {
            // It's a complex item list, extract names
            displayTitle = displayTitle.split(',').map(p => p.split(':')[1] || p).join(', ');
        }
        
        item.innerHTML = `
            <div>
                <div style="font-size: 13px; font-weight: 600;">${displayTitle}</div>
                <div style="font-size: 10px; color: var(--text-muted); margin-top: 4px;">SEC_KEY: ${s.subject_category.toUpperCase()}</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 12px; font-weight: 700;">${s.time_spent_minutes}m</div>
                <div style="font-size: 10px; color: var(--text-muted); margin-top: 4px;">${s.log_date}</div>
            </div>
        `;
        zone.appendChild(item);
    });
}
