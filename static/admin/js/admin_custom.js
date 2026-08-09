/**
 * Palace Karimi — Admin UI/UX Enhancements
 * Lightweight JavaScript for Django Admin interface improvements.
 * No frameworks. Vanilla JS only.
 *
 * Features:
 *   1. Dark / Light theme toggle with localStorage persistence
 *   2. Collapsible fieldsets (click header to toggle)
 *   3. Smart table row highlighting on checkbox selection
 *   4. Image preview lightbox for gallery inline
 *   5. Smooth transitions and micro-interactions
 */
document.addEventListener('DOMContentLoaded', function () {
  'use strict';

  /* =========================================================================
     1. Theme Toggle — Dark / Light Mode with Persistence
     ========================================================================= */

  var THEME_KEY = 'pk_admin_theme';

  function getStoredTheme() {
    try { return localStorage.getItem(THEME_KEY); } catch (e) { return null; }
  }

  function setStoredTheme(theme) {
    try { localStorage.setItem(THEME_KEY, theme); } catch (e) { /* noop */ }
  }

  function applyTheme(theme) {
    if (theme === 'light') {
      document.body.classList.remove('theme-dark');
      document.body.classList.add('theme-light');
    } else {
      document.body.classList.remove('theme-light');
      document.body.classList.add('theme-dark');
    }
    updateToggleIcon(theme);
  }

  function getCurrentTheme() {
    if (document.body.classList.contains('theme-light')) return 'light';
    return 'dark';
  }

  function toggleTheme() {
    var next = getCurrentTheme() === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    setStoredTheme(next);
  }

  function updateToggleIcon(theme) {
    var btn = document.getElementById('pk-theme-toggle');
    if (!btn) return;
    btn.textContent = theme === 'dark' ? '☀' : '☾';
    btn.title = theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
  }

  function initThemeToggle() {
    var stored = getStoredTheme();

    // Apply stored theme or default to dark
    applyTheme(stored || 'dark');

    // Create and insert toggle button into user-tools
    var userTools = document.getElementById('user-tools');
    if (userTools) {
      var btn = document.createElement('button');
      btn.id = 'pk-theme-toggle';
      btn.type = 'button';
      btn.title = 'Toggle Theme';
      btn.setAttribute('aria-label', 'Toggle dark/light theme');
      updateToggleIcon(stored || 'dark');
      btn.addEventListener('click', toggleTheme);
      userTools.appendChild(btn);
    }
  }

  initThemeToggle();


  /* =========================================================================
     2. Collapsible Fieldsets — Click to Toggle
     ========================================================================= */

  function initCollapsibleFieldsets() {
    var fieldsets = document.querySelectorAll('fieldset.module.pk-collapsible');
    fieldsets.forEach(function (fs) {
      var heading = fs.querySelector('h2');
      if (!heading) return;

      heading.style.cursor = 'pointer';

      heading.addEventListener('click', function (e) {
        // Don't collapse if user is clicking an input or link inside the header
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'A' || e.target.tagName === 'LABEL') {
          return;
        }
        fs.classList.toggle('collapsed');
      });
    });

    // Also make standard Django collapse fieldsets smoother
    var standardCollapsibles = document.querySelectorAll('fieldset.module.collapse');
    standardCollapsibles.forEach(function (fs) {
      fs.style.transition = 'all 0.3s ease';
    });
  }

  initCollapsibleFieldsets();


  /* =========================================================================
     3. Smart Row Highlighting on Checkbox Selection
     ========================================================================= */

  function initRowHighlighting() {
    var changelist = document.getElementById('result_list');
    if (!changelist) return;

    var checkboxes = changelist.querySelectorAll('tbody input[type="checkbox"]');

    checkboxes.forEach(function (checkbox) {
      checkbox.addEventListener('change', function () {
        var row = checkbox.closest('tr');
        if (!row) return;

        // Toggle selected class for background highlight
        if (checkbox.checked) {
          row.classList.add('selected');
        } else {
          row.classList.remove('selected');
        }
      });
    });

    // Handle "Select All" checkbox
    var actionToggle = changelist.querySelector('#action-toggle');
    if (actionToggle) {
      actionToggle.addEventListener('change', function () {
        var allCheckboxes = changelist.querySelectorAll('tbody input[type="checkbox"]');
        allCheckboxes.forEach(function (cb) {
          var row = cb.closest('tr');
          if (!row) return;
          if (cb.checked || actionToggle.checked) {
            row.classList.add('selected');
          } else {
            row.classList.remove('selected');
          }
        });
      });
    }
  }

  initRowHighlighting();


  /* =========================================================================
     4. ContactMessage — Unread Row Styling
     ========================================================================= */

  function initUnreadRowStyling() {
    var changelist = document.getElementById('result_list');
    if (!changelist) return;

    // Check if we're on the ContactMessage change list
    var isContactPage = window.location.href.indexOf('contactmessage') !== -1 ||
                        window.location.href.indexOf('contact_message') !== -1;
    if (!isContactPage) return;

    var rows = changelist.querySelectorAll('tbody tr');
    rows.forEach(function (row) {
      // If the row contains a "New" badge, add unread class
      var cells = row.querySelectorAll('td');
      cells.forEach(function (cell) {
        if (cell.textContent.indexOf('New') !== -1 ||
            cell.textContent.indexOf('\u062C\u062F\u06CC\u062F') !== -1) {
          row.classList.add('pk-unread');
        }
      });
    });
  }

  initUnreadRowStyling();


  /* =========================================================================
     5. Image Preview Lightbox (Gallery Inline)
     ========================================================================= */

  function initImageLightbox() {
    var gallery = document.querySelector('.inline-group');
    if (!gallery) return;

    gallery.addEventListener('click', function (e) {
      var img = e.target.closest('img');
      if (!img) return;

      // Only trigger for small thumbnails in preview columns
      var isInPreviewCell = img.closest('td').querySelector('.img_preview') ||
                            img.style.maxHeight === '70px' ||
                            img.style.height === '60px' ||
                            img.style.width === '60px';
      if (!isInPreviewCell && img.offsetHeight < 100) {
        // Small image — open lightbox
        openLightbox(img.src);
      }
    });
  }

  function openLightbox(src) {
    // Remove existing lightbox if any
    closeLightbox();

    var overlay = document.createElement('div');
    overlay.id = 'pk-lightbox';
    overlay.style.cssText =
      'position:fixed;top:0;left:0;right:0;bottom:0;' +
      'background:rgba(0,0,0,.85);z-index:100000;' +
      'display:flex;align-items:center;justify-content:center;' +
      'cursor:zoom-out;animation:fadeIn .2s ease;';

    var image = document.createElement('img');
    image.src = src;
    image.style.cssText =
      'max-width:90vw;max-height:90vh;object-fit:contain;' +
      'border-radius:8px;box-shadow:0 8px 32px rgba(0,0,0,.5);' +
      'animation:scaleIn .25s ease;';

    overlay.appendChild(image);
    document.body.appendChild(overlay);

    overlay.addEventListener('click', closeLightbox);
    document.addEventListener('keydown', lightboxKeyHandler);
  }

  function closeLightbox() {
    var existing = document.getElementById('pk-lightbox');
    if (existing) {
      existing.remove();
    }
    document.removeEventListener('keydown', lightboxKeyHandler);
  }

  function lightboxKeyHandler(e) {
    if (e.key === 'Escape' || e.key === 'Enter') {
      closeLightbox();
    }
  }

  initImageLightbox();


  /* =========================================================================
     6. Inline Form UX — Smooth Add/Remove
     ========================================================================= */

  function initInlineUX() {
    // Add smooth transition when a new inline row is added
    var observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        mutation.addedNodes.forEach(function (node) {
          if (node.nodeType === 1 && node.tagName === 'TR') {
            node.style.animation = 'fadeIn .3s ease-out';
            node.style.background = 'var(--pk-bg-hover, #1E3048)';
            setTimeout(function () {
              node.style.background = '';
              node.style.animation = '';
            }, 600);
          }
        });
      });
    });

    var inlines = document.querySelectorAll('.inline-group .tabular tbody');
    inlines.forEach(function (tbody) {
      observer.observe(tbody, { childList: true });
    });
  }

  initInlineUX();


  /* =========================================================================
     7. Accessibility — Keyboard Navigation Improvements
     ========================================================================= */

  function initAccessibility() {
    // Make fieldset headers focusable for keyboard users
    var collapsibles = document.querySelectorAll('fieldset.pk-collapsible h2');
    collapsibles.forEach(function (h2) {
      h2.setAttribute('tabindex', '0');
      h2.setAttribute('role', 'button');
      h2.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          h2.click();
        }
      });
    });
  }

  initAccessibility();


  /* =========================================================================
     8. CSS Animation Keyframes (injected once)
     ========================================================================= */

  var styleSheet = document.createElement('style');
  styleSheet.textContent =
    '@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }' +
    '@keyframes scaleIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }';
  document.head.appendChild(styleSheet);

});
