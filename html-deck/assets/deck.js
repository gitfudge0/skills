/* ================================================================
   Report deck runtime — zero deps. Copy verbatim into
   .reports/assets/deck.js and load with <script src="assets/deck.js">.

   Provides:
   - Theme toggle (persisted to localStorage; falls back to OS preference)
   - Mermaid (re)init on load and on theme switch — only if mermaid is present
   - Deck navigation: arrows / PageUp-Down / Home / End, on-screen ‹ › buttons,
     touch swipe, "f" for fullscreen, and "t" to cycle the visual style.
     Clamps at the ends — does NOT wrap.
   - Per-slide overflow detection: a slide taller than the viewport gets
     .slide-overflow so it top-aligns and scrolls instead of clipping.
   ================================================================ */
(function () {
  /* ── Theme toggle + optional Mermaid init ── */
  var root = document.documentElement;
  var btn = document.querySelector('.theme-toggle');
  var stored = localStorage.getItem('report-theme');
  if (stored) root.setAttribute('data-theme', stored);

  function isDark() {
    var t = root.getAttribute('data-theme');
    if (t) return t === 'dark';
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  }

  function toggleTheme() {
    var next = isDark() ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    localStorage.setItem('report-theme', next);
    if (typeof mermaid !== 'undefined') {
      mermaid.initialize({ startOnLoad: false, theme: next === 'dark' ? 'dark' : 'base', themeVariables: { fontSize: '13px', fontFamily: 'system-ui, sans-serif' } });
      mermaid.contentLoaded();
    }
  }

  if (btn) btn.addEventListener('click', toggleTheme);

  /* ── Visual-style cycling ── */
  // The 7 selectable styles (see SKILL.md). No data-style == the default "editorial" look.
  var STYLES = ['marginalia', 'verdant', 'blueprint', 'editorial', 'terminal', 'brutalist', 'glass'];
  var storedStyle = localStorage.getItem('report-style');
  if (storedStyle) root.setAttribute('data-style', storedStyle);

  function cycleStyle() {
    var cur = root.getAttribute('data-style') || 'editorial';
    var next = STYLES[(STYLES.indexOf(cur) + 1) % STYLES.length];
    root.setAttribute('data-style', next);
    localStorage.setItem('report-style', next);
  }

  // Bottom-left keyboard hint.
  if (!document.querySelector('.style-hint')) {
    var hint = document.createElement('div');
    hint.className = 'style-hint';
    hint.innerHTML = '<kbd>T</kbd> toggle theme';
    document.body.appendChild(hint);
  }

  // "t" cycles the visual style — ignore when a browser/OS shortcut owns the chord (e.g. Cmd+T).
  document.addEventListener('keydown', function (e) {
    if ((e.key === 't' || e.key === 'T') && !e.metaKey && !e.ctrlKey && !e.altKey) {
      cycleStyle();
    }
  });

  if (typeof mermaid !== 'undefined') {
    mermaid.initialize({ startOnLoad: true, theme: isDark() ? 'dark' : 'base', themeVariables: { fontSize: '13px', fontFamily: 'system-ui, sans-serif' } });
  }
})();

(function () {
  /* ── Deck navigation ── */
  var slides = Array.prototype.slice.call(document.querySelectorAll('.deck .slide'));
  if (!slides.length) return;
  var prevBtn = document.querySelector('.deck-prev');
  var nextBtn = document.querySelector('.deck-next');
  var progress = document.querySelector('.deck-progress');
  var current = 0;

  function clamp(i) { return Math.max(0, Math.min(slides.length - 1, i)); }

  function go(i) {
    current = clamp(i);
    slides.forEach(function (s, idx) {
      s.classList.toggle('is-active', idx === current);
      // Top-align (scroll) instead of center when content overflows.
      if (idx === current) {
        s.classList.remove('slide-overflow');
        s.scrollTop = 0;
        if (s.scrollHeight > s.clientHeight) s.classList.add('slide-overflow');
      }
    });
    if (progress) progress.style.width = ((current + 1) / slides.length * 100) + '%';
    if (prevBtn) prevBtn.disabled = current === 0;          // clamp, don't wrap
    if (nextBtn) nextBtn.disabled = current === slides.length - 1;
  }

  if (prevBtn) prevBtn.addEventListener('click', function () { go(current - 1); });
  if (nextBtn) nextBtn.addEventListener('click', function () { go(current + 1); });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight' || e.key === 'PageDown') { go(current + 1); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { go(current - 1); }
    else if (e.key === 'Home') { go(0); }
    else if (e.key === 'End') { go(slides.length - 1); }
    else if (e.key === 'f' || e.key === 'F') {
      if (!document.fullscreenElement) { document.documentElement.requestFullscreen(); }
      else { document.exitFullscreen(); }
    }
  });

  // Touch swipe.
  var x0 = null;
  document.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 40) go(current + (dx < 0 ? 1 : -1));
    x0 = null;
  }, { passive: true });

  // Re-check overflow on resize so a slide that becomes too tall scrolls.
  window.addEventListener('resize', function () { go(current); });

  go(0);
})();
