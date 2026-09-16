document.addEventListener('DOMContentLoaded', function () {
  var root = document.querySelector('.ih-picker');
  if (!root) return;
  var WHATSAPP_NUMBER = '573017750462';

  function updateState() {
    var rows = root.querySelectorAll('.ih-row');
    var total = 0;
    rows.forEach(function (r) { total += parseInt(r.querySelector('.ih-qty').textContent, 10) || 0; });
    var notas = root.querySelector('#ih-notas').value.trim();
    root.querySelector('#ih-count-num').textContent = total;
    root.querySelector('#ih-send').disabled = !(total > 0 || notas.length > 0);
  }

  root.querySelectorAll('.ih-stepper button').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var qtyEl = btn.parentElement.querySelector('.ih-qty');
      var qty = parseInt(qtyEl.textContent, 10) || 0;
      if (btn.dataset.action === 'up') qty += 1;
      if (btn.dataset.action === 'down') qty = Math.max(0, qty - 1);
      qtyEl.textContent = qty;
      updateState();
    });
  });
  root.querySelector('#ih-notas').addEventListener('input', updateState);

  root.querySelector('#ih-send').addEventListener('click', function () {
    var empresa = root.querySelector('#ih-empresa').value.trim();
    var ciudad = root.querySelector('#ih-ciudad').value;
    var notas = root.querySelector('#ih-notas').value.trim();
    var lines = [];
    root.querySelectorAll('.ih-row').forEach(function (r) {
      var qty = parseInt(r.querySelector('.ih-qty').textContent, 10) || 0;
      if (qty > 0) lines.push('- ' + r.dataset.name + ': ' + qty + ' ' + r.dataset.unit);
    });

    var msg = 'Hola, quiero cotizar este pedido desde la página web:\n\n';
    msg += '🏢 Empresa: ' + (empresa || 'No indicado') + '\n';
    msg += '📍 Ciudad de entrega: ' + ciudad + '\n\n';
    if (lines.length) { msg += '📦 Productos:\n' + lines.join('\n') + '\n\n'; }
    if (notas) { msg += '📝 Notas: ' + notas + '\n\n'; }
    msg += '¿Me confirman disponibilidad y precio? Gracias.';

    var url = 'https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encodeURIComponent(msg);
    var a = document.createElement('a');
    a.href = url; a.target = '_blank'; a.rel = 'noopener';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  });

  updateState();
});
