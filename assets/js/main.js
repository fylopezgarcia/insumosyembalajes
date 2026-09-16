document.addEventListener('partials:loaded', function () {
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
});
