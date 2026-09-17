/*
  Se ejecuta en dos escenarios:
  1) Sitio fuente (sin construir): header/footer llegan tarde vía includes.js,
     que dispara el evento personalizado "partials:loaded".
  2) Sitio construido con build.py (dist/): header/footer ya están en el HTML
     desde el primer momento, así que basta con DOMContentLoaded normal.
  init() es idempotente (la bandera evita correrlo dos veces si ambos disparan).
*/
(function () {
  var didInit = false;

  function init() {
    if (didInit) return;
    didInit = true;

    // --- Menú móvil ---
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.querySelector('.main-nav');
    if (toggle && nav) {
      toggle.addEventListener('click', function () {
        var isOpen = nav.classList.toggle('is-open');
        toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      });
    }

    // --- Marcar el enlace de la página actual ---
    var path = window.location.pathname.replace(/\/index\.html$/, '/');
    document.querySelectorAll('.main-nav a[href]').forEach(function (a) {
      var href = a.getAttribute('href');
      if (href === path || (href !== '/' && path.indexOf(href) === 0)) {
        a.setAttribute('aria-current', 'page');
      }
    });

    // --- Año dinámico en el footer ---
    var yearEl = document.querySelector('[data-year]');
    if (yearEl) yearEl.textContent = new Date().getFullYear();

    // --- Header que se achica al hacer scroll ---
    var header = document.querySelector('.site-header');
    if (header) {
      var onScroll = function () {
        header.classList.toggle('is-scrolled', window.scrollY > 40);
      };
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    }
  }

  document.addEventListener('partials:loaded', init);
  if (document.querySelector('.site-header')) {
    // Header ya presente en el HTML (sitio construido) — no hace falta esperar.
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init);
    } else {
      init();
    }
  }
})();
