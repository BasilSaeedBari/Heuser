(() => {
  const { icons, esc, initials, api, toast } = window.HeuserApp;

  const state = {
    student: null,
    submissions: [],
    comments: [],
    homeworks: [],
    activeSub: null,
  };

  function getStudentIDFromURL() {
    const parts = window.location.pathname.split('/').filter(Boolean);
    if (parts[0] === 'student' && parts[1]) return decodeURIComponent(parts[1]);
    return new URLSearchParams(window.location.search).get('id') || '';
  }

  function pickInitialSubmission(subs) {
    if (!subs || subs.length === 0) return null;
    // Prioritize live HW6 web game, then HW2/HW1 MakeCode, then latest HW
    return (
      subs.find((s) => s.hw_number === 6 && s.embed_url) ||
      subs.find((s) => s.hw_number === 2 && s.embed_url) ||
      subs.find((s) => s.hw_number === 1 && s.embed_url) ||
      subs[subs.length - 1]
    );
  }

  function renderHeader() {
    const st = state.student;
    document.title = `${st.name} (${st.id}) — Heuser27 Arcade`;
    document.getElementById('studentAvatar').textContent = initials(st.name);
    document.getElementById('studentName').textContent = st.name;

    const metaParts = [
      `<span class="mono tabular">${esc(st.id)}</span>`,
      st.batch ? `<span class="badge badge-batch">${esc(st.batch)}</span>` : '',
      st.starred ? `<span class="badge badge-star">${icons.star} Starred by Instructor</span>` : '',
      st.star_note ? `<span style="color:var(--heuser-gold);font-weight:600;">“${esc(st.star_note)}”</span>` : '',
    ].filter(Boolean);
    document.getElementById('studentMeta').innerHTML = metaParts.join('');

    document.getElementById('studentQuickStats').innerHTML = `
      <span class="stat-chip"><strong class="tabular">${st.submission_count}</strong> Homeworks</span>
      <span class="stat-chip"><strong class="tabular">${st.total_votes}</strong> Total Votes</span>
    `;
  }

  function renderHWTabs() {
    const byHW = new Map(state.submissions.map((s) => [s.hw_number, s]));
    const allNums = state.homeworks.length
      ? state.homeworks.map((h) => h.hw_number)
      : [1, 2, 4, 5, 6, 7, 8, 9];

    const tabsHTML = allNums.map((num) => {
      const sub = byHW.get(num);
      const isActive = state.activeSub && state.activeSub.hw_number === num;
      const meta = state.homeworks.find((h) => h.hw_number === num);
      const label = meta ? meta.kind.replace('_', ' ') : '';

      if (!sub) {
        return `
          <button type="button" class="hw-tab missing" disabled>
            <span class="hw-tab-num">HW ${num} <span style="font-size:.7rem;">—</span></span>
            <span class="hw-tab-kind">Not submitted</span>
          </button>
        `;
      }

      return `
        <button type="button" class="hw-tab ${isActive ? 'active' : ''}" data-hw="${num}">
          <span class="hw-tab-num">
            <span>HW ${num}</span>
            <span class="tabular" style="font-size:.74rem;opacity:.9;">${icons.upvote} ${sub.votes}</span>
          </span>
          <span class="hw-tab-kind">${sub.playable ? 'Playable · ' : ''}${esc(label)}</span>
        </button>
      `;
    });

    const container = document.getElementById('hwTabs');
    container.innerHTML = tabsHTML.join('');
    container.querySelectorAll('.hw-tab:not(.missing)').forEach((btn) => {
      btn.addEventListener('click', () => {
        const num = Number(btn.dataset.hw);
        state.activeSub = state.submissions.find((s) => s.hw_number === num);
        renderHWTabs();
        renderStage();
      });
    });
  }

  function safeParseJSON(str, fallback) {
    try {
      return JSON.parse(str || '') || fallback;
    } catch {
      return fallback;
    }
  }

  function renderStage() {
    const sub = state.activeSub;
    const stageGrid = document.getElementById('stageGrid');
    const noSubs = document.getElementById('noSubsState');

    if (!sub) {
      stageGrid.hidden = true;
      noSubs.hidden = false;
      return;
    }
    stageGrid.hidden = false;
    noSubs.hidden = true;

    const stageEl = document.getElementById('projectStage');
    const localFiles = safeParseJSON(sub.local_files_json, []);
    const extraURLs = safeParseJSON(sub.extra_urls_json, []);

    const actionButtons = [];
    if (sub.primary_url && !sub.is_local_only_url) {
      actionButtons.push(
        `<a class="btn btn-primary btn-sm" href="${esc(sub.primary_url)}" target="_blank" rel="noopener noreferrer">${icons.external} Open Submission</a>`
      );
    }
    if (sub.secondary_url) {
      actionButtons.push(
        `<a class="btn btn-ghost btn-sm" href="${esc(sub.secondary_url)}" target="_blank" rel="noopener noreferrer">${icons.code} View Repository / Secondary</a>`
      );
    }

    let embedSection = '';
    if (sub.embed_url) {
      embedSection = `
        <div class="arcade-frame-wrap" id="arcadeFrameWrap">
          <iframe id="arcadeIframe" src="${esc(sub.embed_url)}" title="${esc(sub.hw_title)}" allow="fullscreen; gamepad; autoplay" loading="lazy"></iframe>
        </div>
        <div style="display:flex;gap:10px;margin-top:10px;flex-wrap:wrap;align-items:center;justify-content:space-between;">
          <span style="font-size:0.8rem;color:var(--heuser-muted);">
            Interactive viewport · Click inside the game canvas to capture keyboard controls.
          </span>
          <div style="display:flex;gap:8px;">
            <button type="button" class="btn btn-ghost btn-sm" id="reloadFrameBtn">${icons.refresh} Restart</button>
            <button type="button" class="btn btn-gold btn-sm" id="fullscreenFrameBtn">Fullscreen</button>
          </div>
        </div>
      `;
    } else if (sub.hw_number >= 7 && sub.primary_url && !sub.is_local_only_url) {
      embedSection = `
        <div style="margin-top:14px;padding:18px;border-radius:12px;background:rgba(0,15,29,0.65);border:1px solid var(--heuser-border);">
          <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;">
            <div>
              <div style="font-family:var(--font-display);font-weight:700;">Live Hosted Project</div>
              <div class="mono" style="font-size:0.8rem;color:var(--heuser-muted);word-break:break-all;">${esc(sub.primary_url)}</div>
            </div>
            <div style="display:flex;gap:8px;flex-wrap:wrap;">
              <button type="button" class="btn btn-ghost btn-sm" id="inlinePreviewBtn">Try Inline Preview</button>
              <a class="btn btn-gold btn-sm" href="${esc(sub.primary_url)}" target="_blank" rel="noopener noreferrer">${icons.external} Launch Site</a>
            </div>
          </div>
          <div id="inlinePreviewHolder"></div>
        </div>
      `;
    } else if (sub.is_local_only_url) {
      embedSection = `
        <div style="margin-top:14px;padding:14px;border-radius:12px;background:rgba(218,42,53,0.14);border:1px solid rgba(218,42,53,0.4);font-size:0.86rem;">
          Student submitted a local computer path (<span class="mono">${esc(sub.primary_url)}</span>) instead of a public URL.
        </div>
      `;
    }

    let localFilesSection = '';
    if (localFiles.length > 0) {
      const fileBtns = localFiles
        .map(
          (f, idx) =>
            `<button type="button" class="pill-btn ${idx === 0 ? 'active' : ''}" data-file-idx="${idx}">${esc(f.label)}</button>`
        )
        .join('');
      localFilesSection = `
        <div style="margin-top:20px;">
          <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:10px;flex-wrap:wrap;">
            <h3 style="font-family:var(--font-display);margin:0;font-size:1rem;">Submitted Files &amp; Source Code</h3>
            <a id="downloadLocalBtn" class="btn btn-ghost btn-sm" href="#" download>${icons.download} Download File</a>
          </div>
          <div class="hw-pills" id="localFileTabs">${fileBtns}</div>
          <div class="code-viewer" id="localFileContent">Loading file...</div>
        </div>
      `;
    }

    let extraLinksHTML = '';
    if (extraURLs.length > 0) {
      const items = extraURLs
        .map((eu) => {
          const isWeb = /^https?:\/\//i.test(eu.url);
          const val = isWeb
            ? `<a href="${esc(eu.url)}" target="_blank" rel="noopener noreferrer" style="color:var(--heuser-gold);text-decoration:underline;word-break:break-all;">${esc(eu.url)}</a>`
            : `<span class="mono" style="word-break:break-all;">${esc(eu.url)}</span>`;
          return `<div style="font-size:0.82rem;"><strong>${esc(eu.label)}:</strong> ${val}</div>`;
        })
        .join('');
      extraLinksHTML = `
        <div style="margin-top:18px;padding:14px;border-radius:12px;background:rgba(0,15,29,0.55);border:1px solid var(--heuser-border);display:flex;flex-direction:column;gap:6px;">
          <div style="font-weight:700;font-size:0.84rem;color:var(--heuser-gold);">Submission Links &amp; Metadata</div>
          ${items}
          ${sub.submitted_at ? `<div style="font-size:0.78rem;color:var(--heuser-muted);">Submitted: <span class="tabular">${esc(sub.submitted_at)}</span> (Attempts: ${sub.attempt_count})</div>` : ''}
          ${sub.feedback ? `<div style="font-size:0.8rem;color:#D6E3F0;margin-top:4px;white-space:pre-wrap;">${esc(sub.feedback)}</div>` : ''}
        </div>
      `;
    }

    stageEl.innerHTML = `
      <div class="arcade-toolbar">
        <div>
          <h2 style="font-family:var(--font-display);margin:0;font-size:1.3rem;">${esc(sub.hw_title)}</h2>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
          ${actionButtons.join('')}
        </div>
      </div>
      ${embedSection}
      ${localFilesSection}
      ${extraLinksHTML}
    `;

    // Wire embed controls
    const reloadBtn = document.getElementById('reloadFrameBtn');
    const fsBtn = document.getElementById('fullscreenFrameBtn');
    const iframe = document.getElementById('arcadeIframe');
    if (reloadBtn && iframe) {
      reloadBtn.addEventListener('click', () => {
        iframe.src = iframe.src;
      });
    }
    if (fsBtn) {
      fsBtn.addEventListener('click', () => {
        const wrap = document.getElementById('arcadeFrameWrap');
        if (wrap && wrap.requestFullscreen) wrap.requestFullscreen();
      });
    }

    const previewBtn = document.getElementById('inlinePreviewBtn');
    if (previewBtn) {
      previewBtn.addEventListener('click', () => {
        const holder = document.getElementById('inlinePreviewHolder');
        holder.innerHTML = `
          <div class="arcade-frame-wrap" style="margin-top:12px;">
            <iframe src="${esc(sub.primary_url)}" title="Live Site Preview" loading="lazy"></iframe>
          </div>
          <p style="font-size:0.76rem;color:var(--heuser-muted);margin:8px 0 0;">
            If the preview stays blank, the hosting provider blocks iframe embedding — use Launch Site above.
          </p>
        `;
        previewBtn.disabled = true;
      });
    }

    // Wire local files viewer
    if (localFiles.length > 0) {
      const loadLocalFile = async (idx) => {
        const f = localFiles[idx];
        const viewer = document.getElementById('localFileContent');
        const dlBtn = document.getElementById('downloadLocalBtn');
        dlBtn.href = `/api/file?path=${encodeURIComponent(f.rel_path)}&download=1`;
        viewer.textContent = 'Loading...';
        try {
          const data = await api(`/api/file?path=${encodeURIComponent(f.rel_path)}`);
          if (data.kind === 'zip_preview') {
            const parts = (data.entries || []).map((e) => {
              return `=== ${e.name} (${e.size} bytes) ===\n${e.content || '[Binary or large file]'}\n`;
            });
            viewer.textContent = parts.join('\n') || 'Archive contains no previewable text files.';
          } else {
            viewer.textContent = data.content || '';
          }
        } catch (err) {
          viewer.textContent = `Could not load file: ${err.message}`;
        }
      };

      document.getElementById('localFileTabs').querySelectorAll('.pill-btn').forEach((btn) => {
        btn.addEventListener('click', () => {
          document.getElementById('localFileTabs').querySelectorAll('.pill-btn').forEach((b) => b.classList.remove('active'));
          btn.classList.add('active');
          loadLocalFile(Number(btn.dataset.fileIdx));
        });
      });
      loadLocalFile(0);
    }

    renderVoteAndComments();
  }

  function renderVoteAndComments() {
    const sub = state.activeSub;
    if (!sub) return;

    const voteBadge = document.getElementById('voteCountBadge');
    const voteBtn = document.getElementById('voteBtn');
    voteBadge.textContent = `${sub.votes} ${sub.votes === 1 ? 'vote' : 'votes'}`;
    voteBtn.classList.toggle('voted', !!sub.user_voted);
    voteBtn.innerHTML = sub.user_voted
      ? `${icons.upvote} Voted (${sub.votes}) · Click to Remove`
      : `${icons.upvote} Vote for HW ${sub.hw_number} (${sub.votes})`;

    const subComments = state.comments.filter((c) => c.submission_id === sub.id);
    document.getElementById('commentTotal').textContent = subComments.length;
    const listEl = document.getElementById('commentList');
    if (subComments.length === 0) {
      listEl.innerHTML = `<div style="font-size:0.84rem;color:var(--heuser-muted);padding:10px 0;">No comments on HW ${sub.hw_number} yet. Be the first!</div>`;
    } else {
      listEl.innerHTML = subComments
        .map(
          (c) => `
        <div class="comment-item">
          <div class="comment-head">
            <span>${esc(c.author_name)}</span>
            <time class="tabular">${esc(c.created_at)}</time>
          </div>
          <div class="comment-body">${esc(c.body)}</div>
        </div>
      `
        )
        .join('');
    }
  }

  document.getElementById('voteBtn').addEventListener('click', async () => {
    if (!state.activeSub) return;
    try {
      const res = await api('/api/vote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ submission_id: state.activeSub.id }),
      });
      state.activeSub.voted = res.voted;
      state.activeSub.user_voted = res.voted;
      state.activeSub.votes = res.votes;
      state.student.total_votes = state.submissions.reduce((sum, s) => sum + s.votes, 0);
      renderHeader();
      renderHWTabs();
      renderVoteAndComments();
      toast(res.voted ? 'Vote recorded for your IP!' : 'Vote removed.');
    } catch (err) {
      toast(err.message);
    }
  });

  document.getElementById('commentForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!state.activeSub) return;
    const author = document.getElementById('commentAuthor').value.trim();
    const bodyEl = document.getElementById('commentBody');
    const body = bodyEl.value.trim();
    if (!body) return;

    try {
      const res = await api('/api/comments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          submission_id: state.activeSub.id,
          author_name: author,
          body,
        }),
      });
      state.comments.unshift(res.comment);
      bodyEl.value = '';
      renderVoteAndComments();
      toast('Comment posted!');
    } catch (err) {
      toast(err.message);
    }
  });

  async function init() {
    const sid = getStudentIDFromURL();
    if (!sid) {
      document.getElementById('studentName').textContent = 'Missing student ID';
      return;
    }
    try {
      const [showcase, detail] = await Promise.all([
        api('/api/showcase'),
        api(`/api/student/${encodeURIComponent(sid)}`),
      ]);
      state.homeworks = showcase.homeworks || [];
      state.student = detail.student;
      state.submissions = detail.submissions || [];
      state.comments = detail.comments || [];
      state.activeSub = pickInitialSubmission(state.submissions);

      renderHeader();
      renderHWTabs();
      renderStage();
    } catch (err) {
      document.getElementById('studentName').textContent = 'Student Not Found';
      document.getElementById('studentMeta').textContent = err.message;
    }
  }

  init();
})();
