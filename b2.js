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

// Reels in the phone frames: load when near the screen, play muted while visible,
// pause when scrolled away. A missing file shows its poster and the path to add.
(function () {
  var phones = Array.prototype.slice.call(document.querySelectorAll('.phone'));
  if (!phones.length) return;
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  phones.forEach(function (ph) {
    var v = ph.querySelector('video');
    var btn = ph.querySelector('.phone-play');
    ph._userPaused = reduced;
    ph.classList.add('paused');
    v.addEventListener('error', function () { ph.classList.add('no-video'); }, true);
    btn.addEventListener('click', function () {
      if (v.paused) { ph._userPaused = false; load(ph); v.play().catch(function () {}); }
      else { ph._userPaused = true; v.pause(); }
    });
    v.addEventListener('play', function () { ph.classList.remove('paused'); btn.setAttribute('aria-label', 'Pause video'); });
    v.addEventListener('pause', function () { ph.classList.add('paused'); btn.setAttribute('aria-label', 'Play video'); });
  });

  function load(ph) {
    var v = ph.querySelector('video');
    if (!v.getAttribute('src') && v.dataset.src) {
      v.src = v.dataset.src;
      v.addEventListener('error', function () { ph.classList.add('no-video'); });
    }
  }

  if (!('IntersectionObserver' in window)) { phones.forEach(load); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      var ph = e.target, v = ph.querySelector('video');
      if (e.isIntersecting) {
        load(ph);
        if (!ph._userPaused) v.play().catch(function () { ph.classList.add('paused'); });
      } else if (!v.paused) {
        v.pause(); ph._userPaused = false;
      }
    });
  }, { threshold: 0.15 });
  phones.forEach(function (ph) { io.observe(ph); });
})();
