(() => {
  const { icons, esc, initials, tileStyleFor, api } = window.HeuserApp;

  const state = {
    students: [],
    homeworks: [],
    stats: {},
    search: '',
    batch: 'all',
    hw: 'all',
    playableOnly: false,
    sort: 'featured',
  };

  const els = {
    statStudents: document.getElementById('statStudents'),
    statSubs: document.getElementById('statSubs'),
    statPlayable: document.getElementById('statPlayable'),
    statVotes: document.getElementById('statVotes'),
    searchInput: document.getElementById('searchInput'),
    batchFilter: document.getElementById('batchFilter'),
    sortSelect: document.getElementById('sortSelect'),
    playableToggle: document.getElementById('playableToggle'),
    hwFilterBar: document.getElementById('hwFilterBar'),
    starredSection: document.getElementById('starredSection'),
    starredCount: document.getElementById('starredCount'),
    starredGrid: document.getElementById('starredGrid'),
    wallHeading: document.getElementById('wallHeading'),
    wallCount: document.getElementById('wallCount'),
    studentGrid: document.getElementById('studentGrid'),
    emptyState: document.getElementById('emptyState'),
  };

  function renderHWFilters() {
    const pills = [
      `<button type="button" class="pill-btn ${state.hw === 'all' ? 'active' : ''}" data-hw="all">All Homeworks</button>`,
      ...state.homeworks.map((h) => {
        const active = String(state.hw) === String(h.hw_number) ? 'active' : '';
        return `<button type="button" class="pill-btn ${active}" data-hw="${h.hw_number}">HW ${h.hw_number} <span class="tabular" style="opacity:.75">(${h.submission_count})</span></button>`;
      }),
    ];
    els.hwFilterBar.innerHTML = pills.join('');
    els.hwFilterBar.querySelectorAll('.pill-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        state.hw = btn.dataset.hw;
        renderHWFilters();
        renderGrids();
      });
    });
  }

  function renderTile(st, isSpotlight = false) {
    const pal = tileStyleFor(st.id);
    const submittedSet = new Set(st.submitted_hws || []);
    const hwNums = state.homeworks.map((h) => h.hw_number);

    const dotsHTML = hwNums
      .map((n) => {
        const done = submittedSet.has(n);
        const isGame = (n === 1 || n === 2 || n === 6) && done;
        return `<span class="hw-dot ${done ? 'done' : ''} ${isGame ? 'is-game' : ''}" title="HW ${n}: ${done ? 'Submitted' : 'Missing'}">${n}</span>`;
      })
      .join('');

    const hasPlayable = st.has_hw6_game || st.has_arcade_game;
    const playBadge = hasPlayable
      ? `<span class="badge badge-play">${icons.gamepad} PLAY</span>`
      : '';
    const starBadge = st.starred
      ? `<span class="badge badge-star">${icons.star} STAR</span>`
      : '';
    const batchBadge = st.batch
      ? `<span class="badge badge-batch">${esc(st.batch)}</span>`
      : '';

    const noteHTML = st.starred && st.star_note
      ? `<div class="tile-star-note">${esc(st.star_note)}</div>`
      : '';

    return `
      <a href="/student/${encodeURIComponent(st.id)}"
         class="student-tile ${st.starred ? 'is-starred' : ''}"
         style="--tile-accent: ${pal.accent}; --tile-bg: ${pal.bg};">
        <div>
          <div class="tile-top">
            <div class="tile-avatar">${esc(initials(st.name))}</div>
            <div class="tile-badges">
              ${starBadge}
              ${playBadge}
              ${!starBadge && !playBadge ? batchBadge : ''}
            </div>
          </div>

          <div class="tile-body">
            <h3 class="tile-name">${esc(st.name)}</h3>
            <div class="tile-id">${esc(st.id)}${st.batch ? ` · <span style="white-space:nowrap">${esc(st.batch)}</span>` : ''}</div>
            ${noteHTML}
          </div>
        </div>

        <div class="tile-footer">
          <div class="hw-dots">${dotsHTML}</div>
          <div class="tile-votes tabular" title="Total project votes">
            ${icons.upvote} ${st.total_votes}
          </div>
        </div>
      </a>
    `;
  }

  function filterAndSort(list) {
    const q = state.search.trim().toLowerCase();
    const filtered = list.filter((st) => {
      if (q && !st.name.toLowerCase().includes(q) && !st.id.toLowerCase().includes(q)) {
        return false;
      }
      if (state.batch !== 'all' && st.batch !== state.batch) {
        return false;
      }
      if (state.hw !== 'all' && !(st.submitted_hws || []).includes(Number(state.hw))) {
        return false;
      }
      if (state.playableOnly && !st.has_hw6_game && !st.has_arcade_game) {
        return false;
      }
      return true;
    });

    filtered.sort((a, b) => {
      if (state.sort === 'featured') {
        if (a.starred !== b.starred) return a.starred ? -1 : 1;
        if (a.total_votes !== b.total_votes) return b.total_votes - a.total_votes;
        if (a.submission_count !== b.submission_count) return b.submission_count - a.submission_count;
        return a.name.localeCompare(b.name);
      }
      if (state.sort === 'submissions') {
        if (a.submission_count !== b.submission_count) return b.submission_count - a.submission_count;
        return b.total_votes - a.total_votes;
      }
      return a.name.localeCompare(b.name);
    });

    return filtered;
  }

  function renderGrids() {
    const filtered = filterAndSort(state.students);
    const starred = filtered.filter((s) => s.starred);

    if (starred.length > 0) {
      els.starredSection.hidden = false;
      els.starredCount.textContent = `${starred.length} featured`;
      els.starredGrid.innerHTML = starred.map((s) => renderTile(s, true)).join('');
    } else {
      els.starredSection.hidden = true;
      els.starredGrid.innerHTML = '';
    }

    els.wallCount.textContent = `${filtered.length} of ${state.students.length} students`;
    if (filtered.length === 0) {
      els.studentGrid.innerHTML = '';
      els.emptyState.hidden = false;
    } else {
      els.emptyState.hidden = true;
      els.studentGrid.innerHTML = filtered.map((s) => renderTile(s, false)).join('');
    }
  }

  async function init() {
    try {
      const data = await api('/api/showcase');
      state.students = data.students || [];
      state.homeworks = data.homeworks || [];
      state.stats = data.stats || {};

      els.statStudents.textContent = state.stats.total_students ?? state.students.length;
      els.statSubs.textContent = state.stats.total_submissions ?? 0;
      els.statPlayable.textContent = state.stats.playable_games ?? 0;
      els.statVotes.textContent = state.stats.total_votes ?? 0;

      renderHWFilters();
      renderGrids();
    } catch (err) {
      els.wallCount.textContent = 'Failed to load showcase';
      els.emptyState.hidden = false;
      els.emptyState.textContent = err.message;
    }
  }

  els.searchInput.addEventListener('input', (e) => {
    state.search = e.target.value;
    renderGrids();
  });
  els.batchFilter.addEventListener('change', (e) => {
    state.batch = e.target.value;
    renderGrids();
  });
  els.sortSelect.addEventListener('change', (e) => {
    state.sort = e.target.value;
    renderGrids();
  });
  els.playableToggle.addEventListener('click', () => {
    state.playableOnly = !state.playableOnly;
    els.playableToggle.classList.toggle('active', state.playableOnly);
    renderGrids();
  });

  init();
})();
