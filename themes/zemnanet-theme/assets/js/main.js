/* ============================================================================
   zemnanet — Interactions JS v2.1.0
   Theme toggle, search, mobile menu, category filter
   ============================================================================ */

(function () {
  'use strict';

  // ---- Theme toggle ----
  const themeBtn = document.querySelector('[data-action="theme"]');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      const html = document.documentElement;
      const current = html.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      html.classList.toggle('zn-dark', next === 'dark');
      html.classList.toggle('zn-light', next === 'light');
      try { localStorage.setItem('zn-theme', next); } catch (e) {}
    });
    // Restore saved theme
    try {
      const saved = localStorage.getItem('zn-theme');
      if (saved) {
        document.documentElement.setAttribute('data-theme', saved);
        document.documentElement.classList.toggle('zn-dark', saved === 'dark');
        document.documentElement.classList.toggle('zn-light', saved === 'light');
      }
    } catch (e) {}
  }

  // ---- Search toggle (placeholder) ----
  const searchBtn = document.querySelector('[data-action="search"]');
  if (searchBtn) {
    searchBtn.addEventListener('click', function () {
      const overlay = document.getElementById('search-overlay');
      if (overlay) overlay.classList.toggle('is-open');
    });
  }

  // ---- Mobile menu toggle ----
  const menuBtn = document.querySelector('[data-action="mobile-menu"]');
  if (menuBtn) {
    menuBtn.addEventListener('click', function () {
      const drawer = document.getElementById('mobile-drawer');
      if (drawer) drawer.classList.toggle('is-open');
    });
    const closeBtn = document.querySelector('[data-action="close-menu"]');
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        const drawer = document.getElementById('mobile-drawer');
        if (drawer) drawer.classList.remove('is-open');
      });
    }
  }

  // ---- Category filter tabs ----
  const filterGroup = document.querySelector('[data-filter-group]');
  if (filterGroup) {
    const buttons = filterGroup.querySelectorAll('.zn-filter__btn');
    const cards = document.querySelectorAll('[data-category]');

    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        // Update active button
        buttons.forEach(function (b) { b.classList.remove('is-active'); });
        btn.classList.add('is-active');

        const filter = btn.getAttribute('data-filter');

        cards.forEach(function (card) {
          if (filter === 'all') {
            card.style.display = '';
          } else {
            const category = card.getAttribute('data-category');
            card.style.display = (category === filter) ? '' : 'none';
          }
        });
      });
    });
  }

  // ---- Reading progress bar ----
  const progressBar = document.querySelector('[data-reading-progress]');
  if (progressBar) {
    function updateProgress() {
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrolled = window.scrollY;
      const percent = scrollHeight > 0 ? (scrolled / scrollHeight) * 100 : 0;
      progressBar.style.width = percent + '%';
    }
    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
  }
  // ---- Share: copy article URL ----
  const copyButtons = document.querySelectorAll('[data-copy-url]');
  copyButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      const url = btn.getAttribute('data-copy-url');
      if (!url) return;

      function markCopied() {
        const original = btn.textContent;
        btn.textContent = 'Copied';
        btn.classList.add('is-copied');
        setTimeout(function () {
          btn.textContent = original || 'Copy link';
          btn.classList.remove('is-copied');
        }, 1800);
      }

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(markCopied).catch(function () {
          window.prompt('Copy this link:', url);
        });
      } else {
        window.prompt('Copy this link:', url);
      }
    });
  });
})();
