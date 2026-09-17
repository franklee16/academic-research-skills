/* Yomitoki — canonical main.js
   Implements:
     1. IntersectionObserver — TOC active-section highlight + code-ref panel swap
     2. Jargon click-toggle for touch devices
     3. Pomodoro timer with localStorage persistence
     4. KaTeX auto-render no-op guard (auto-render runs via onload in HTML head)
   No external JS dependencies. Script loaded `defer` at end of body. */

// ── 1. Mermaid initialization ─────────────────────────────────────────────────
// Guard: only initialize if mermaid is available (loaded via CDN script tag).
if (typeof mermaid !== 'undefined') {
  mermaid.initialize({
    startOnLoad: true,
    theme: 'base',
    themeVariables: {
      background:         '#fff',
      primaryColor:       '#f0d8cc',
      primaryTextColor:   '#2a2622',
      primaryBorderColor: '#b8462e',
      lineColor:          '#b8462e',
      secondaryColor:     '#f4ead4',
      tertiaryColor:      '#fdfaf3',
      edgeLabelBackground:'#fff',
      fontFamily:         'Inter, sans-serif',
      fontSize:           '13px',
    }
  });
}

// ── 2. Sidebar TOC — IntersectionObserver ─────────────────────────────────────
//
// Watches every section that has a matching TOC link.
// On intersect: marks that TOC link .active (removes from all others) and
// calls updateCodeRefs() so the sidebar code-ref panel reflects the section.
(function () {
  const tocLinks = document.querySelectorAll('.toc a[data-section-id]');
  if (!tocLinks.length) return;

  const sections = Array.from(tocLinks)
    .map(a => document.getElementById(a.dataset.sectionId))
    .filter(Boolean);

  if (!sections.length) return;

  // Track which section is considered "active". We want the topmost section
  // whose top edge has entered the upper 40% of the viewport.
  let currentActive = null;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        // Only update if the section changed (avoids redundant DOM writes)
        if (id !== currentActive) {
          currentActive = id;
          tocLinks.forEach(a => {
            if (a.dataset.sectionId === id) {
              a.classList.add('active');
            } else {
              a.classList.remove('active');
            }
          });
          updateCodeRefs(id);
        }
      }
    });
  }, {
    // Trigger when the section's top crosses into the top 40% of the viewport.
    rootMargin: '0px 0px -60% 0px',
    threshold: 0
  });

  sections.forEach(s => observer.observe(s));
})();

// ── 3. Code references panel ──────────────────────────────────────────────────
//
// window.CODEREFS is expected to be set by an inline <script> in the HTML before
// this file loads. Shape:
//   { [section_id]: Array<CodeRef> }
//
// CodeRef (author repo):
//   { source: "author_repo", title, repo, path?, url?, note? }
//
// CodeRef (synthesized):
//   { source: "llm_generated", title, snippet?, repo?, url?, note? }
//
// CodeRef (web / blog):
//   { source: "web", title, url, repo?: null, path?: null, snippet?, note? }

// GitHub links read "View on GitHub"; any other link (blog, docs) reads "Read".
function refLinkLabel(url) {
  return /github\.com/i.test(url || '') ? 'View on GitHub ↗' : 'Read ↗';
}

function updateCodeRefs(sectionId) {
  const container = document.getElementById('coderefs');
  if (!container) return;

  const allRefs = window.CODEREFS || {};
  // Fall back to 'method' refs if the current section has none.
  const hasOwn = allRefs[sectionId] && allRefs[sectionId].length;
  const refs = hasOwn ? allRefs[sectionId] : (allRefs['method'] || []);
  // CRITICAL: the cards must be tagged with the section the refs ACTUALLY came
  // from, not the active section. When we fall back to 'method' refs under a
  // refless section, tagging the cards with the active id makes openModal look
  // up CODEREFS[activeSection] (undefined) and silently do nothing — the cause
  // of "clicking a card works in one section but not after scrolling to another".
  const refSection = hasOwn ? sectionId : 'method';

  if (!refs.length) {
    container.innerHTML = '<p class="empty-state">No code refs for this section.</p>';
    return;
  }

  container.innerHTML = refs.map((r, idx) => {
    const isSynth = r.source === 'llm_generated';
    const repoLine = r.repo
      ? `<p class="repo">${escapeHtml(r.repo)}</p>`
      : '';
    const metaLine = r.title
      ? `<p class="meta">${escapeHtml(r.title)}</p>`
      : '';
    const urlLine = r.url
      ? `<a href="${escapeHtml(r.url)}" target="_blank" rel="noopener">${refLinkLabel(r.url)}</a>`
      : '';
    const noteLine = r.note
      ? `<p class="meta" style="margin-top:0.3em">${escapeHtml(r.note)}</p>`
      : '';
    // Snippet preview opens the modal for the full-width view. Section + idx
    // travel with the <pre> as data attributes. The section is refSection (the
    // source of the refs), NOT the active sectionId — see note above.
    const snippetBlock = r.snippet
      ? `<pre class="code-snippet" data-coderef-section="${escapeHtml(refSection)}" data-coderef-idx="${idx}">${escapeHtml(r.snippet)}</pre>`
      : '';

    if (isSynth) {
      return `<div class="coderef-card synthesized">
        <p class="label">Synthesized snippet</p>
        ${metaLine}
        ${noteLine}
        ${snippetBlock}
      </div>`;
    }

    return `<div class="coderef-card">
      ${repoLine}
      ${metaLine}
      ${urlLine}
      ${noteLine}
      ${snippetBlock}
    </div>`;
  }).join('');

  // Snippet clicks are handled by document-level delegation below.
}

// Attach once at module load: a click on a sidebar pre.code-snippet (now or
// after any updateCodeRefs re-render) opens the matching modal.
if (!window.__yomi_snippetDelegationBound) {
  window.__yomi_snippetDelegationBound = true;
  document.addEventListener('click', function (e) {
    const pre = e.target.closest && e.target.closest('#coderefs pre.code-snippet');
    if (!pre) return;
    const sid = pre.dataset.coderefSection;
    const idx = parseInt(pre.dataset.coderefIdx || '0', 10);
    if (window.__yomi_openModal) window.__yomi_openModal(sid, idx);
  });
}

// Minimal HTML escaper — keeps injected data safe.
function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ── 4. Jargon click-toggle (touch devices) ───────────────────────────────────
//
// Hovering shows the ::after tooltip via CSS. On touch, hover doesn't fire, so
// we toggle a .open class to show the tooltip below the span instead.

(function () {
  function initJargon() {
    document.querySelectorAll('.jargon').forEach(el => {
      el.addEventListener('click', function (e) {
        e.stopPropagation();
        const isOpen = el.classList.contains('open');
        // Close all other open jargon spans first.
        document.querySelectorAll('.jargon.open').forEach(other => {
          if (other !== el) other.classList.remove('open');
        });
        el.classList.toggle('open', !isOpen);
      });
    });

    // Clicking anywhere else closes all open tooltips.
    document.addEventListener('click', function () {
      document.querySelectorAll('.jargon.open').forEach(el => {
        el.classList.remove('open');
      });
    });
  }

  // Pomodoro floating widget — collapse toggle.
  function initPomoCollapse() {
    const widget = document.getElementById('pomodoro');
    const btn = document.getElementById('pomo-collapse');
    if (!widget || !btn) return;
    btn.addEventListener('click', function () {
      widget.classList.toggle('collapsed');
    });
  }

  // Pomodoro floating widget — drag to reposition, persisted across reloads.
  function initPomoDrag() {
    const widget = document.getElementById('pomodoro');
    if (!widget) return;
    const POS_KEY = 'yomi-pomodoro-pos';

    // Clamp into the viewport so the widget can never land off-screen, then
    // switch from the default top/right anchoring to explicit left/top.
    function applyPos(left, top) {
      const maxLeft = Math.max(0, window.innerWidth - widget.offsetWidth);
      const maxTop = Math.max(0, window.innerHeight - widget.offsetHeight);
      left = Math.min(Math.max(0, left), maxLeft);
      top = Math.min(Math.max(0, top), maxTop);
      widget.style.left = left + 'px';
      widget.style.top = top + 'px';
      widget.style.right = 'auto';
      widget.style.bottom = 'auto';
    }

    // Restore a saved position.
    try {
      const saved = JSON.parse(localStorage.getItem(POS_KEY) || 'null');
      if (saved && typeof saved.left === 'number' && typeof saved.top === 'number') {
        applyPos(saved.left, saved.top);
      }
    } catch (e) { /* ignore */ }

    let dragging = false, startX = 0, startY = 0, originLeft = 0, originTop = 0, moved = false;

    widget.addEventListener('pointerdown', function (e) {
      // Let the buttons (start/pause, reset, minimize) keep working as clicks.
      if (e.target.closest('button')) return;
      const rect = widget.getBoundingClientRect();
      originLeft = rect.left; originTop = rect.top;
      startX = e.clientX; startY = e.clientY;
      dragging = true; moved = false;
      widget.classList.add('dragging');
      try { widget.setPointerCapture(e.pointerId); } catch (_) {}
    });

    widget.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      const dx = e.clientX - startX, dy = e.clientY - startY;
      if (Math.abs(dx) > 2 || Math.abs(dy) > 2) moved = true;
      applyPos(originLeft + dx, originTop + dy);
    });

    function endDrag(e) {
      if (!dragging) return;
      dragging = false;
      widget.classList.remove('dragging');
      try { widget.releasePointerCapture(e.pointerId); } catch (_) {}
      if (moved) {
        const rect = widget.getBoundingClientRect();
        try {
          localStorage.setItem(POS_KEY, JSON.stringify({ left: rect.left, top: rect.top }));
        } catch (_) {}
      }
    }
    widget.addEventListener('pointerup', endDrag);
    widget.addEventListener('pointercancel', endDrag);

    // Keep it on-screen if the window is resized.
    window.addEventListener('resize', function () {
      if (widget.style.left) applyPos(parseFloat(widget.style.left), parseFloat(widget.style.top));
    });
  }

  function initPomo() { initPomoCollapse(); initPomoDrag(); }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPomo);
  } else {
    initPomo();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initJargon);
  } else {
    initJargon();
  }
})();

// ── 5. Initialize code-ref panel on load ─────────────────────────────────────
// Show 'method' refs by default (most papers have them; nothing to observe yet).
document.addEventListener('DOMContentLoaded', function () {
  updateCodeRefs('method');
});

// ── 5b. Code anchors — body-text links to sidebar code refs ──────────────────
//
// <span class="code-anchor" data-coderef-section="method" data-coderef-idx="0">…</span>
// Clicking switches the sidebar to that section's refs, scrolls to + flashes
// the Nth card so the user can see which ref the anchor maps to.

(function () {
  // Open the full-width modal showing the entire snippet + metadata for
  // CODEREFS[sectionId][idx]. Used by both anchor clicks and sidebar
  // snippet clicks. If the ref has no snippet, falls back to flashing
  // the matching sidebar card (and opening the GitHub URL is the user's
  // own next click).
  function openModal(sectionId, idx) {
    const refs = (window.CODEREFS && window.CODEREFS[sectionId]) || [];
    if (idx >= refs.length) return;
    const ref = refs[idx];
    const modal = document.getElementById('code-modal');
    if (!modal) return;

    // Preserve current page scroll so opening the modal NEVER moves the
    // article behind it. We re-apply on close.
    const scrollY = window.scrollY;

    const isSynth = ref.source === 'llm_generated';
    let meta;
    if (isSynth) {
      meta = 'Synthesized snippet';
    } else {
      meta = `${ref.repo || ''}${ref.path ? ' · ' + ref.path : ''}`;
      if (ref.snippet_lines) meta += ` · ${ref.snippet_lines}`;
    }
    document.getElementById('code-modal-meta').textContent = meta;
    document.getElementById('code-modal-title').textContent = ref.title || '';

    const body = document.getElementById('code-modal-body');
    if (ref.snippet) {
      // Render each line wrapped in a span with its 1-indexed line number,
      // starting at snippet_start_line (or 1 by default). This gives CSS
      // counter()-driven gutter line numbers in the modal — handy when the
      // ref points at a specific line range in a real file.
      const start = parseInt(ref.snippet_start_line || '1', 10);
      const lines = ref.snippet.split('\n');
      body.innerHTML = lines.map((ln, i) => {
        const num = start + i;
        const text = escapeHtml(ln) || '&nbsp;';
        return `<span class="line" data-ln="${num}">${text}</span>`;
      }).join('');
      body.classList.remove('no-snippet');
    } else {
      body.textContent = "No inline code preview for this reference.\nClick the link below to read the source.";
      body.classList.add('no-snippet');
    }

    document.getElementById('code-modal-note').textContent = ref.note || '';
    const link = document.getElementById('code-modal-link');
    if (ref.url) {
      link.href = ref.url;
      link.textContent = refLinkLabel(ref.url);
      link.hidden = false;
    } else {
      link.hidden = true;
    }
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');

    // Lock the page from scrolling behind the modal — overflow:hidden on
    // <html> doesn't reposition any content (unlike position:fixed) so
    // there's no flicker on close. Compensate for the lost scrollbar
    // width to prevent layout shift.
    const scrollbarW = window.innerWidth - document.documentElement.clientWidth;
    document.documentElement.style.overflow = 'hidden';
    if (scrollbarW > 0) {
      document.documentElement.style.paddingRight = scrollbarW + 'px';
    }
  }

  function closeModal() {
    const modal = document.getElementById('code-modal');
    if (!modal) return;
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');

    // Release the scroll lock. No scrollTo needed because we never moved
    // the page in the first place.
    document.documentElement.style.overflow = '';
    document.documentElement.style.paddingRight = '';
  }

  function init() {
    // Code-anchor clicks use event delegation on document. Bind-once-per-node
    // (the earlier approach) silently broke when KaTeX / Mermaid / jargon
    // toggles rewrote any subtree containing a .code-anchor span — the user
    // would click and nothing happened until they scrolled enough for a
    // re-bind elsewhere to trigger. Delegation has no such failure mode.
    document.addEventListener('click', function (e) {
      const anchor = e.target.closest && e.target.closest('.code-anchor');
      if (!anchor) return;
      e.preventDefault();
      e.stopPropagation();
      const sid = anchor.dataset.coderefSection;
      const idx = parseInt(anchor.dataset.coderefIdx || '0', 10);
      openModal(sid, idx);
    });

    // Modal close handlers
    document.querySelectorAll('#code-modal [data-close]').forEach(function (el) {
      el.addEventListener('click', closeModal);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeModal();
    });
  }

  // Expose openModal for the updateCodeRefs (defined elsewhere) to wire
  // sidebar snippet clicks.
  window.__yomi_openModal = openModal;
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

// ── 6. Pomodoro timer ─────────────────────────────────────────────────────────
//
// Spec (output-structure.md — "Pomodoro JS"):
//   - 25-min focus / 5-min break
//   - Buttons: ▶/⏸ toggle, ↺ reset
//   - Auto-cycles focus → break → focus
//   - Persists across reloads (day-of state — auto-resets on new calendar day)
//   - Browser Notifications when block completes (if granted)
//   - Display: mode label + MM:SS countdown + "N pomodoros today"
(function () {
  const FOCUS_SECONDS = 25 * 60;
  const BREAK_SECONDS = 5 * 60;
  const STORAGE_KEY   = 'yomi-pomodoro';
  const today         = new Date().toISOString().slice(0, 10);

  let state      = loadState();
  let intervalId = null;

  const timeEl    = document.getElementById('pomo-time');
  const modeEl    = document.getElementById('pomo-mode');
  const statsEl   = document.getElementById('pomo-stats');
  const toggleBtn = document.getElementById('pomo-toggle');
  const resetBtn  = document.getElementById('pomo-reset');

  // Graceful no-op if the Pomodoro widget is absent in the HTML.
  if (!timeEl || !modeEl || !toggleBtn || !resetBtn) return;

  function loadState() {
    try {
      const raw  = localStorage.getItem(STORAGE_KEY);
      const data = raw ? JSON.parse(raw) : {};
      if (data.date !== today) {
        // New calendar day — reset everything.
        return { date: today, count: 0, remaining: FOCUS_SECONDS, mode: 'focus', running: false };
      }
      // Never resume a running timer across a page reload — pause at saved remaining.
      data.running = false;
      return data;
    } catch {
      return { date: today, count: 0, remaining: FOCUS_SECONDS, mode: 'focus', running: false };
    }
  }

  function saveState() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch {}
  }

  function fmt(s) {
    const m   = Math.floor(s / 60);
    const sec = s % 60;
    return `${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
  }

  function render() {
    timeEl.textContent  = fmt(state.remaining);
    modeEl.textContent  = state.mode === 'focus' ? 'Focus' : 'Break';
    if (statsEl) {
      statsEl.textContent = `${state.count} pomodoro${state.count === 1 ? '' : 's'} today`;
    }
    toggleBtn.textContent = state.running ? '⏸' : '▶';
    toggleBtn.classList.toggle('running', state.running);
  }

  function tick() {
    state.remaining -= 1;
    if (state.remaining <= 0) {
      if (state.mode === 'focus') {
        state.count   += 1;
        state.mode     = 'break';
        state.remaining = BREAK_SECONDS;
        // Gentle audio ping (silent data: URI — plays silently if autoplay blocked).
        try {
          new Audio(
            'data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA='
          ).play();
        } catch {}
        notify('Focus block done — take a break.');
      } else {
        state.mode      = 'focus';
        state.remaining = FOCUS_SECONDS;
        notify('Break over — back to it.');
      }
    }
    saveState();
    render();
  }

  function notify(msg) {
    if (typeof Notification !== 'undefined' && Notification.permission === 'granted') {
      new Notification('Yomitoki', { body: msg });
    }
  }

  toggleBtn.addEventListener('click', function () {
    state.running = !state.running;
    if (state.running) {
      // Request notification permission the first time the user starts the timer.
      if (typeof Notification !== 'undefined' && Notification.permission === 'default') {
        Notification.requestPermission();
      }
      intervalId = setInterval(tick, 1000);
    } else {
      clearInterval(intervalId);
      intervalId = null;
    }
    saveState();
    render();
  });

  resetBtn.addEventListener('click', function () {
    if (intervalId) { clearInterval(intervalId); intervalId = null; }
    state.running   = false;
    state.mode      = 'focus';
    state.remaining = FOCUS_SECONDS;
    saveState();
    render();
  });

  // Initial render (shows persisted state before any user interaction).
  render();
})();

// ── 7. KaTeX auto-render guard ────────────────────────────────────────────────
// The HTML head loads auto-render.min.js with an onload that calls
// renderMathInElement(). This file runs after that, so nothing extra is needed.
// If KaTeX is somehow unavailable, we no-op gracefully — no errors thrown.
