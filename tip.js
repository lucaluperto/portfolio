// Tooltip for chart marks: any element with data-tip shows it on hover/focus.
(function () {
  var tip = document.createElement('div');
  tip.className = 'tip';
  tip.setAttribute('role', 'tooltip');
  document.body.appendChild(tip);
  function show(e) {
    var t = e.target.closest('[data-tip]');
    if (!t) return;
    tip.textContent = t.getAttribute('data-tip');
    tip.style.opacity = 1;
    move(e);
  }
  function move(e) {
    var x = (e.clientX || 0) + 14, y = (e.clientY || 0) + 14;
    if (!e.clientX) { var r = e.target.getBoundingClientRect(); x = r.left; y = r.bottom + 6; }
    var w = tip.offsetWidth;
    if (x + w > window.innerWidth - 8) x = window.innerWidth - w - 8;
    tip.style.left = x + 'px'; tip.style.top = y + 'px';
  }
  function hide() { tip.style.opacity = 0; }
  document.addEventListener('mouseover', show);
  document.addEventListener('mousemove', function (e) { if (tip.style.opacity == 1) move(e); });
  document.addEventListener('mouseout', function (e) { if (e.target.closest('[data-tip]')) hide(); });
  document.addEventListener('focusin', show);
  document.addEventListener('focusout', hide);
})();
