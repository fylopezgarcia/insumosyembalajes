/*
  Rastrea otras acciones de interés comercial, además del clic a WhatsApp
  (ese lo cubre whatsapp-tracking.js). Todo llega a GA4 vía gtag y al
  dataLayer, listo para verse en Looker Studio sin configurar nada más.

  Eventos:
  - phone_click      -> tocó el número de teléfono (header o footer)
  - map_click        -> tocó el enlace a Google Maps
  - category_click   -> entró a una categoría desde una tarjeta ("cat-card")
*/
document.addEventListener('click', function (e) {
  var page = location.pathname;

  var tel = e.target.closest('a[href^="tel:"]');
  if (tel) return fire('phone_click', { event_category: 'engagement', page_path: page });

  var map = e.target.closest('a[href*="maps.app.goo.gl"], a[href*="google.com/maps"]');
  if (map) return fire('map_click', { event_category: 'engagement', page_path: page });

  var cat = e.target.closest('a.cat-card');
  if (cat) {
    var name = cat.querySelector('h3');
    return fire('category_click', {
      event_category: 'navigation',
      event_label: name ? name.textContent.trim() : cat.href,
      page_path: page
    });
  }
}, true);

function fire(name, params) {
  if (typeof window.gtag === 'function') window.gtag('event', name, params);
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push(Object.assign({ event: name }, params));
}
