/*
  Rastrea CUALQUIER clic que abra WhatsApp en el sitio (botones del header,
  hero, categorías, ciudades, footer flotante, y el enlace que arma
  order-builder.js dinámicamente) como un evento de conversión.

  Dispara, sin necesidad de configurar nada más en GTM:
  - gtag('event', 'whatsapp_click', ...)  -> aparece en GA4 como evento ya
    listo para marcar como "evento clave" (Admin > Eventos) y luego
    importar a Google Ads como conversión.
  - dataLayer.push({event:'whatsapp_click', ...}) -> por si más adelante
    quieren armar un trigger de Evento personalizado en GTM sin tocar código.
  - fbq('track', 'Contact', ...) -> "Contact" es un evento ESTÁNDAR del Meta
    Pixel (no hay que crear una conversión personalizada): ya queda
    disponible en Meta Ads Manager para optimizar campañas de inmediato.

  Usa la fase de "captura" (el 3er argumento `true`) para no perder el
  evento así algo más adelante en el DOM detenga la propagación.
*/
document.addEventListener('click', function (e) {
  var link = e.target.closest('a[href*="wa.me"], a[href*="api.whatsapp.com"]');
  if (!link) return;

  var context = document.title || location.pathname;

  if (typeof window.gtag === 'function') {
    window.gtag('event', 'whatsapp_click', {
      event_category: 'engagement',
      event_label: context,
      page_path: location.pathname
    });
  }
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ event: 'whatsapp_click', wa_context: context, wa_page: location.pathname });

  if (typeof window.fbq === 'function') {
    window.fbq('track', 'Contact', { content_name: context });
  }
}, true);
