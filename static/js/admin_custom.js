// /**
//  * Palace Karimi (پالاس کریمی) - Admin UI/UX Enhancements
//  */
// document.addEventListener('DOMContentLoaded', function () {
//   'use strict';
//
//   // 1. Theme Switcher (Dark / Light Mode)
//   initThemeToggle();
//
//   // 2. Table Row Select Highlighting
//   initTableRowHighlights();
//
//   // 3. Floating Submit Bar for long forms
//   initFloatingSubmitBar();
//
//   // 4. RTL Support Detection
//   initRTLCheck();
//
//   /**
//    * Initializes theme toggling with localStorage persistence
//    */
//   function initThemeToggle() {
//     var userTools = document.getElementById('user-tools');
//     if (!userTools) return;
//
//     var toggleBtn = document.createElement('button');
//     toggleBtn.type = 'button';
//     toggleBtn.className = 'pk-theme-toggle';
//
//     var savedTheme = localStorage.getItem('pk_admin_theme') || 'light';
//     applyTheme(savedTheme);
//
//     toggleBtn.innerHTML = savedTheme === 'dark' ? '☀️ روز' : '🌙 شب';
//
//     toggleBtn.addEventListener('click', function () {
//       var currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
//       var newTheme = currentTheme === 'dark' ? 'light' : 'dark';
//       applyTheme(newTheme);
//       toggleBtn.innerHTML = newTheme === 'dark' ? '☀️ روز' : '🌙 شب';
//     });
//
//     userTools.appendChild(toggleBtn);
//   }
//
//   function applyTheme(theme) {
//     document.documentElement.setAttribute('data-theme', theme);
//     if (theme === 'dark') {
//       document.body.classList.add('theme-dark');
//     } else {
//       document.body.classList.remove('theme-dark');
//     }
//     localStorage.setItem('pk_admin_theme', theme);
//   }
//
//   /**
//    * Highlights table rows in Change List when checkboxes are toggled
//    */
//   function initTableRowHighlights() {
//     var resultList = document.getElementById('result_list');
//     if (!resultList) return;
//
//     var checkboxes = resultList.querySelectorAll('tbody input[type="checkbox"]');
//     checkboxes.forEach(function (checkbox) {
//       checkbox.addEventListener('change', function () {
//         var row = checkbox.closest('tr');
//         if (row) {
//           if (checkbox.checked) {
//             row.classList.add('selected');
//           } else {
//             row.classList.remove('selected');
//           }
//         }
//       });
//     });
//   }
//
//   /**
//    * Floating Submit Row on scroll for long forms
//    */
//   function initFloatingSubmitBar() {
//     var submitRow = document.querySelector('.submit-row');
//     if (!submitRow) return;
//
//     var observer = new IntersectionObserver(
//       function (entries) {
//         entries.forEach(function (entry) {
//           if (!entry.isIntersecting) {
//             submitRow.classList.add('is-sticky');
//           } else {
//             submitRow.classList.remove('is-sticky');
//           }
//         });
//       },
//       { threshold: 1.0 }
//     );
//
//     var sentinel = document.createElement('div');
//     sentinel.className = 'pk-submit-sentinel';
//     submitRow.parentNode.insertBefore(sentinel, submitRow);
//     observer.observe(sentinel);
//   }
//
//   /**
//    * Detects RTL and sets document direction
//    */
//   function initRTLCheck() {
//     var lang = document.documentElement.lang || 'en';
//     if (['fa', 'ar', 'he', 'ur'].includes(lang)) {
//       document.documentElement.dir = 'rtl';
//       document.body.classList.add('rtl');
//     }
//   }
// });