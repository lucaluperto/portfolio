// The pencil: draws the marks of a block when it scrolls into view, and moves the
// little pencil along its path. No dependencies. Works with tip.js on the same page.
(function () {
  var root = document.documentElement;
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var blocks = Array.prototype.slice.call(document.querySelectorAll('[data-draw]'));

  if (reduced) { root.classList.add('no-pencil'); }

  function runPencils(block) {
    if (reduced) return;
    block.querySelectorAll('.pencil').forEach(function (g) {
      var anim = g.querySelector('animateMotion');
      var delay = parseFloat(g.getAttribute('data-delay') || '0') * 1000;
      if (!anim || typeof anim.beginElement !== 'function') return;
      setTimeout(function () {
        g.style.opacity = '1';
        anim.beginElement();
        setTimeout(function () { g.style.opacity = '0'; }, 1050);
      }, delay);
    });
  }

  function show(block) {
    if (block.classList.contains('on')) return;
    block.classList.add('on');
    runPencils(block);
  }

  if (!('IntersectionObserver' in window)) {
    blocks.forEach(show);
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { show(e.target); io.unobserve(e.target); }
    });
  }, { threshold: 0.35 });

  blocks.forEach(function (b) { io.observe(b); });
})();
