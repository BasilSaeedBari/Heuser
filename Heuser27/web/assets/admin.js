(() => {
  const { icons, esc, api, toast } = window.HeuserApp;

  const state = {
    students: [],
    homeworks: [],
    matrix: {},
    comments: [],
    syncLogs: [],
    activeTab: 'summary',
    search: '',
    batch: 'all',
    enrollment: 'active',
    completion: 'all',
  };

  const els = {
    loginPanel: document.getElementById('loginPanel'),
    adminApp: document.getElementById('adminApp'),
    logoutBtn: document.getElementById('logoutBtn'),
    loginForm: document.getElementById('loginForm'),
    loginError: document.getElementById('loginError'),
    kpiGrid: document.getElementById('kpiGrid'),
    hwBars: document.getElementById('hwBars'),
    hwTotalNote: document.getElementById('hwTotalNote'),
    matrixHead: document.getElementById('matrixHead'),
    matrixBody: document.getElementById('matrixBody'),
    matrixCount: document.getElementById('matrixCount'),
    syncLogsList: document.getElementById('syncLogsList'),
    adminCommentsList: document.getElementById('adminCommentsList'),
    adminCommentCount: document.getElementById('adminCommentCount'),
  };

  function showTab(name) {
    state.activeTab = name;
    document.querySelectorAll('#adminTabs .pill-btn').forEach((b) => {
      b.classList.toggle('active', b.dataset.tab === name);
    });
    ['summary', 'upload', 'comments'].forEach((t) => {
      document.getElementById(`tab-${t}`).hidden = t !== name;
    });
  }

  document.querySelectorAll('#adminTabs .pill-btn').forEach((btn) => {
    btn.addEventListener('click', () => showTab(btn.dataset.tab));
  });

  async function loadSummary() {
    const data = await api('/api/admin/summary');
    state.students = data.students || [];
    state.homeworks = data.homeworks || [];
    state.matrix = data.matrix || {};
    state.comments = data.comments || [];
    state.syncLogs = data.sync_logs || [];
    renderKPIs();
    renderHWBars();
    renderMatrix();
    renderSyncLogs();
    renderComments();
  }

  function renderKPIs() {
    const enrolled = state.students.filter((s) => s.enrollment_status === 'Enrolled');
    const totalSubs = state.students.reduce((sum, s) => sum + s.submission_count, 0);
    const totalVotes = state.students.reduce((sum, s) => sum + s.total_votes, 0);
    const starred = state.students.filter((s) => s.starred).length;

    els.kpiGrid.innerHTML = `
      <div class="kpi-card">
        <div class="kpi-label">Enrolled Students</div>
        <div class="kpi-val tabular">${enrolled.length}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Total Submissions</div>
        <div class="kpi-val gold tabular">${totalSubs}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Starred Spotlight</div>
        <div class="kpi-val gold tabular">${starred}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Public Votes / Comments</div>
        <div class="kpi-val tabular">${totalVotes} / ${state.comments.length}</div>
      </div>
    `;
  }

  function renderHWBars() {
    const enrolledCount = Math.max(1, state.students.filter((s) => s.enrollment_status === 'Enrolled').length);
    els.hwTotalNote.textContent = `Out of ${enrolledCount} enrolled students`;
    els.hwBars.innerHTML = state.homeworks
      .map((h) => {
        const pct = Math.min(100, Math.round((h.submission_count / enrolledCount) * 100));
        return `
          <div class="hw-bar-card">
            <div style="display:flex;justify-content:space-between;align-items:baseline;">
              <strong style="font-family:var(--font-display);font-size:0.9rem;">HW ${h.hw_number}</strong>
              <span class="tabular" style="font-size:0.82rem;color:var(--heuser-gold);font-weight:700;">${h.submission_count} (${pct}%)</span>
            </div>
            <div style="font-size:0.73rem;color:var(--heuser-muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;" title="${esc(h.title)}">
              ${esc(h.title.replace(/^Homework \d+:\s*/, ''))}
            </div>
            <div class="hw-bar-track"><div class="hw-bar-fill" style="width:${pct}%"></div></div>
          </div>
        `;
      })
      .join('');
  }

  function filteredStudents() {
    const q = state.search.trim().toLowerCase();
    return state.students.filter((st) => {
      if (state.enrollment === 'active' && st.enrollment_status !== 'Enrolled' && st.submission_count === 0) {
        return false;
      }
      if (state.enrollment === 'enrolled' && st.enrollment_status !== 'Enrolled') {
        return false;
      }
      if (q && !st.name.toLowerCase().includes(q) && !st.id.toLowerCase().includes(q)) {
        return false;
      }
      if (state.batch !== 'all' && st.batch !== state.batch) {
        return false;
      }
      const c = st.submission_count;
      if (state.completion === 'zero' && c !== 0) return false;
      if (state.completion === '1-3' && (c < 1 || c > 3)) return false;
      if (state.completion === '4-6' && (c < 4 || c > 6)) return false;
      if (state.completion === '7+' && c < 7) return false;
      if (state.completion === 'starred' && !st.starred) return false;
      return true;
    });
  }

  function renderMatrix() {
    const hws = state.homeworks;
    const totalHWs = hws.length;

    els.matrixHead.innerHTML = `
      <tr>
        <th>Star</th>
        <th>Student</th>
        <th>ID</th>
        <th>Batch</th>
        <th>Submitted</th>
        ${hws.map((h) => `<th title="${esc(h.title)}">HW${h.hw_number}</th>`).join('')}
        <th>Votes</th>
      </tr>
    `;

    const list = filteredStudents();
    els.matrixCount.textContent = `Showing ${list.length} of ${state.students.length} records`;

    els.matrixBody.innerHTML = list
      .map((st) => {
        const cells = state.matrix[st.id] || {};
        const hwCols = hws
          .map((h) => {
            const c = cells[h.hw_number];
            if (!c) {
              return `<td><span class="cell-status miss" title="Not submitted">—</span></td>`;
            }
            const isGame = c.playable ? 'game' : '';
            const href = `/student/${encodeURIComponent(st.id)}`;
            return `<td><a href="${href}" class="cell-status ok ${isGame}" title="Submitted ${esc(c.submitted_at || '')}">✓</a></td>`;
          })
          .join('');

        return `
          <tr>
            <td>
              <button type="button"
                      class="star-toggle ${st.starred ? 'active' : ''}"
                      data-star-id="${esc(st.id)}"
                      title="${st.starred ? 'Unstar student' : 'Star student (pin to top)'}">
                ${st.starred ? icons.star : icons.starOutline}
              </button>
            </td>
            <td>
              <a href="/student/${encodeURIComponent(st.id)}" style="font-weight:700;color:#fff;text-decoration:underline;text-decoration-color:rgba(241,186,99,0.4);">
                ${esc(st.name)}
              </a>
              ${st.star_note ? `<div style="font-size:0.72rem;color:var(--heuser-gold);">${esc(st.star_note)}</div>` : ''}
            </td>
            <td class="mono tabular" style="color:var(--heuser-muted);">${esc(st.id)}</td>
            <td>${esc(st.batch || '—')}</td>
            <td class="tabular">
              <strong style="color:${st.submission_count === 0 ? '#FF7B84' : 'var(--heuser-gold)'};">${st.submission_count}</strong>
              <span style="color:var(--heuser-muted);">/ ${totalHWs}</span>
            </td>
            ${hwCols}
            <td class="tabular">${st.total_votes}</td>
          </tr>
        `;
      })
      .join('');

    els.matrixBody.querySelectorAll('[data-star-id]').forEach((btn) => {
      btn.addEventListener('click', async () => {
        const sid = btn.dataset.starId;
        const st = state.students.find((x) => x.id === sid);
        if (!st) return;
        const nextStarred = !st.starred;
        let note = st.star_note || '';
        if (nextStarred) {
          const entered = window.prompt(`Optional spotlight note for ${st.name} (leave blank for none):`, note);
          if (entered === null) return;
          note = entered.trim();
        } else {
          note = '';
        }
        try {
          await api('/api/admin/star', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ student_id: sid, starred: nextStarred, star_note: note }),
          });
          st.starred = nextStarred;
          st.star_note = note;
          state.students.sort((a, b) => (a.starred === b.starred ? a.name.localeCompare(b.name) : a.starred ? -1 : 1));
          renderKPIs();
          renderMatrix();
          toast(nextStarred ? `${st.name} starred & pinned to top!` : `${st.name} unstarred.`);
        } catch (err) {
          toast(err.message);
        }
      });
    });
  }

  function renderSyncLogs() {
    if (!state.syncLogs.length) {
      els.syncLogsList.innerHTML = `<div style="color:var(--heuser-muted);font-size:0.86rem;">No sync logs yet.</div>`;
      return;
    }
    els.syncLogsList.innerHTML = state.syncLogs
      .map(
        (l) => `
      <div class="comment-item">
        <div class="comment-head">
          <span>${esc(l.source)}</span>
          <time class="tabular">${esc(l.created_at)}</time>
        </div>
        <div class="comment-body" style="font-size:0.8rem;color:#C5D5E5;">${esc(l.notes)}</div>
      </div>
    `
      )
      .join('');
  }

  function renderComments() {
    els.adminCommentCount.textContent = `${state.comments.length} total`;
    if (!state.comments.length) {
      els.adminCommentsList.innerHTML = `<div style="color:var(--heuser-muted);font-size:0.88rem;">No visitor comments yet.</div>`;
      return;
    }
    els.adminCommentsList.innerHTML = state.comments
      .map(
        (c) => `
      <div class="comment-item" style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;">
        <div style="flex:1;">
          <div class="comment-head">
            <span>${esc(c.author_name)} → <a href="/student/${encodeURIComponent(c.student_id)}" style="text-decoration:underline;">${esc(c.student_name || c.student_id)}</a> (HW ${c.hw_number})</span>
            <time class="tabular">${esc(c.created_at)} · IP: ${esc(c.commenter_ip || '')}</time>
          </div>
          <div class="comment-body">${esc(c.body)}</div>
        </div>
        <button type="button" class="btn btn-ghost btn-sm" data-del-comment="${c.id}" title="Delete comment">${icons.trash}</button>
      </div>
    `
      )
      .join('');

    els.adminCommentsList.querySelectorAll('[data-del-comment]').forEach((btn) => {
      btn.addEventListener('click', async () => {
        const cid = btn.dataset.delComment;
        try {
          await api(`/api/admin/comments/${cid}`, { method: 'DELETE' });
          state.comments = state.comments.filter((x) => String(x.id) !== String(cid));
          renderKPIs();
          renderComments();
          toast('Comment deleted.');
        } catch (err) {
          toast(err.message);
        }
      });
    });
  }

  // Filters
  document.getElementById('adminSearch').addEventListener('input', (e) => {
    state.search = e.target.value;
    renderMatrix();
  });
  document.getElementById('adminBatch').addEventListener('change', (e) => {
    state.batch = e.target.value;
    renderMatrix();
  });
  document.getElementById('adminEnrollment').addEventListener('change', (e) => {
    state.enrollment = e.target.value;
    renderMatrix();
  });
  document.getElementById('adminCompletion').addEventListener('change', (e) => {
    state.completion = e.target.value;
    renderMatrix();
  });

  // Upload XLSX & Resync
  document.getElementById('uploadXlsxForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const hw = document.getElementById('uploadHwNum').value;
    const fileInput = document.getElementById('uploadFile');
    if (!fileInput.files.length) return;

    const fd = new FormData();
    fd.append('hw_number', hw);
    fd.append('file', fileInput.files[0]);

    try {
      const res = await fetch('/api/admin/upload-xlsx', { method: 'POST', body: fd });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Upload failed');
      toast(`Updated HW ${hw} (${data.sync.submissions_count} total submissions synced)!`);
      fileInput.value = '';
      await loadSummary();
    } catch (err) {
      toast(err.message);
    }
  });

  document.getElementById('resyncBtn').addEventListener('click', async () => {
    try {
      const res = await api('/api/admin/resync', { method: 'POST' });
      toast(`Resynced: ${res.submissions_count} submissions across ${res.homeworks_count} homeworks.`);
      await loadSummary();
    } catch (err) {
      toast(err.message);
    }
  });

  // Auth
  els.loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    els.loginError.hidden = true;
    try {
      await api('/api/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: document.getElementById('adminPassword').value }),
      });
      els.loginPanel.hidden = true;
      els.adminApp.hidden = false;
      els.logoutBtn.hidden = false;
      await loadSummary();
    } catch (err) {
      els.loginError.textContent = err.message;
      els.loginError.hidden = false;
    }
  });

  els.logoutBtn.addEventListener('click', async () => {
    await api('/api/admin/logout', { method: 'POST' });
    window.location.reload();
  });

  async function init() {
    try {
      const me = await api('/api/admin/me');
      if (me.authenticated) {
        els.loginPanel.hidden = true;
        els.adminApp.hidden = false;
        els.logoutBtn.hidden = false;
        await loadSummary();
      } else {
        els.loginPanel.hidden = false;
      }
    } catch {
      els.loginPanel.hidden = false;
    }
  }

  init();
})();
