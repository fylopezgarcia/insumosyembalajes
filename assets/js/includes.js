/*
  Inyecta partials/header.html y partials/footer.html en cualquier página que
  tenga <div data-include="header"></div> / data-include="footer".
  Usa rutas absolutas ("/partials/...") — el sitio debe servirse desde la raíz
  del dominio (así queda al subirlo a hosting) o de un servidor local
  (npx serve . / python3 -m http.server), nunca abriendo el archivo con doble clic.
*/
(function () {
  var slots = document.querySelectorAll('[data-include]');
  var pending = slots.length;
  if (!pending) return;

  slots.forEach(function (el) {
    var name = el.getAttribute('data-include');
    fetch('/partials/' + name + '.html')
      .then(function (r) { return r.text(); })
      .then(function (html) {
        el.outerHTML = html;
      })
      .catch(function (err) {
        console.error('No se pudo cargar el partial "' + name + '":', err);
      })
      .finally(function () {
        pending -= 1;
        if (pending === 0) {
          document.dispatchEvent(new CustomEvent('partials:loaded'));
        }
      });
  });
})();
