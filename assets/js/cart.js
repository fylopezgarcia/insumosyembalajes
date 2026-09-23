/*
  Carrito compartido entre páginas. Convierte los botones "Cotizar" de las
  tablas de especificaciones (categorías) en un selector de cantidad, igual
  al de la Tienda, y lo guarda en localStorage — así lo que se agrega en
  cualquier categoría sigue disponible al entrar a otra o a la Tienda.

  Muestra una barra flotante para enviar el pedido por WhatsApp desde
  cualquier página (se oculta sola en la Tienda, que ya tiene su propia
  barra con campos de empresa/ciudad).
*/
(function () {
  var KEY = 'ih_cart_v1';
  var WHATSAPP_NUMBER = '573017750462';

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; }
  }
  function write(cart) {
    try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch (e) {}
  }
  function totalCount(cart) {
    var n = 0;
    for (var k in cart) n += cart[k].qty;
    return n;
  }
  function notify() {
    document.dispatchEvent(new Event('ihcart:change'));
  }

  function setQty(name, qty, unit) {
    var cart = read();
    if (qty > 0) cart[name] = { qty: qty, unit: unit || (cart[name] && cart[name].unit) || '' };
    else delete cart[name];
    write(cart);
    renderBar();
    syncAll();
    notify();
  }
  function getQty(name) {
    return (read()[name] || {}).qty || 0;
  }
  function clear() {
    write({});
    renderBar();
    syncAll();
    notify();
  }

  // ---- Barra flotante ----
  var barEl;
  function renderBar() {
    var cart = read();
    var n = totalCount(cart);
    if (!barEl) {
      barEl = document.createElement('div');
      barEl.className = 'cart-bar';
      barEl.innerHTML = '<span class="cart-bar-count"></span>' +
        '<button type="button" class="cart-bar-send">Enviar pedido por WhatsApp</button>';
      document.body.appendChild(barEl);
      barEl.querySelector('.cart-bar-send').addEventListener('click', send);
    }
    if (n > 0) {
      barEl.classList.add('is-visible');
      barEl.querySelector('.cart-bar-count').textContent =
        n + (n === 1 ? ' producto seleccionado' : ' productos seleccionados');
    } else {
      barEl.classList.remove('is-visible');
    }
  }

  function send() {
    var cart = read();
    var names = Object.keys(cart);
    if (!names.length) return;
    var lines = names.map(function (name) { return '- ' + name + ': ' + cart[name].qty + ' ' + cart[name].unit; });

    var msg = 'Hola, quiero cotizar este pedido desde la página web:\n\n';
    msg += '📦 Productos:\n' + lines.join('\n') + '\n\n¿Me confirman disponibilidad y precio? Gracias.';

    if (typeof window.gtag === 'function') {
      window.gtag('event', 'order_whatsapp_click', {
        event_category: 'ecommerce',
        productos_distintos: names.length,
        productos: names.join(', '),
        page_path: location.pathname
      });
    }
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: 'order_whatsapp_click', productos_distintos: names.length,
      productos: names.join(', '), page_path: location.pathname
    });

    var url = 'https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encodeURIComponent(msg);
    var a = document.createElement('a');
    a.href = url; a.target = '_blank'; a.rel = 'noopener';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }

  // ---- Mantiene sincronizado cualquier stepper marcado con data-cart-name ----
  function syncAll() {
    document.querySelectorAll('[data-cart-name]').forEach(function (row) {
      var qtyEl = row.querySelector('.ih-qty');
      if (qtyEl) qtyEl.textContent = getQty(row.dataset.cartName);
    });
  }

  function bindStepper(row) {
    row.querySelectorAll('.ih-stepper button').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var qty = getQty(row.dataset.cartName);
        if (btn.dataset.action === 'up') qty += 1;
        if (btn.dataset.action === 'down') qty = Math.max(0, qty - 1);
        setQty(row.dataset.cartName, qty, row.dataset.cartUnit);
      });
    });
  }

  // Reduce presentaciones largas ("Rollo de 48mm x 300mts...") a una unidad
  // corta y consistente con la Tienda ("rollo(s)") para el mensaje de WhatsApp.
  function shortUnit(raw) {
    var t = (raw || '').trim();
    var m = /^Por (rollo|paquete|unidad|kilo)\b/i.exec(t);
    if (m) return m[1].toLowerCase() + '(s)';
    if (/rollo/i.test(t)) return 'rollo(s)';
    if (/paquete/i.test(t)) return 'paquete(s)';
    if (/unidad/i.test(t)) return 'unidad(es)';
    return t;
  }

  // Convierte cada botón "Cotizar" de una tabla de categoría en un stepper.
  function enhanceSpecTables() {
    document.querySelectorAll('table.spec-table tr td [data-producto]').forEach(function (link) {
      var row = link.closest('tr');
      var cell = link.closest('td');
      var nameCell = row.children[0];
      var unitCell = row.children[1];
      var unitText = unitCell ? unitCell.textContent.trim() : '';
      row.dataset.cartName = link.dataset.producto;
      row.dataset.cartUnit = shortUnit(unitText);
      // Subtítulo compacto (solo visible en celular) para no depender de la
      // columna "Presentación", que ahí se oculta para que la fila quepa
      // en una sola línea de pantalla.
      var sub = document.createElement('span');
      sub.className = 'spec-unit-mobile';
      sub.textContent = unitText;
      nameCell.appendChild(sub);
      cell.innerHTML = '<div class="ih-stepper">' +
        '<button type="button" data-action="down" aria-label="Quitar uno">–</button>' +
        '<span class="ih-qty">0</span>' +
        '<button type="button" data-action="up" aria-label="Agregar uno">+</button></div>';
      bindStepper(row);
    });
    // Filas de la Tienda: ya traen su propio stepper, solo las conectamos
    // al mismo carrito (en vez de duplicar la lógica de +/-).
    document.querySelectorAll('.ih-picker .ih-row[data-name]').forEach(function (row) {
      row.dataset.cartName = row.dataset.name;
      row.dataset.cartUnit = row.dataset.unit;
      bindStepper(row);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    enhanceSpecTables();
    syncAll();
    renderBar();
  });

  window.IHCart = { setQty: setQty, getQty: getQty, clear: clear };
})();
