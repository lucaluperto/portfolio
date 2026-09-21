// Tooltips for chart marks + entrance animations. No dependencies.
(function () {
  /* ---------- tooltip ---------- */
  var tip = document.createElement('div');
  tip.className = 'tip';
  tip.setAttribute('role', 'tooltip');
  document.body.appendChild(tip);
  function show(e) {
    var t = e.target.closest && e.target.closest('[data-tip]');
    if (!t) return;
    tip.textContent = t.getAttribute('data-tip');
    tip.style.opacity = 1;
    move(e);
  }
  function move(e) {
    var x = (e.clientX || 0) + 14, y = (e.clientY || 0) + 14;
    if (!e.clientX && e.target.getBoundingClientRect) {
      var r = e.target.getBoundingClientRect(); x = r.left; y = r.bottom + 6;
    }
    var w = tip.offsetWidth;
    if (x + w > window.innerWidth - 8) x = window.innerWidth - w - 8;
    tip.style.left = x + 'px'; tip.style.top = y + 'px';
  }
  function hide() { tip.style.opacity = 0; }
  document.addEventListener('mouseover', show);
  document.addEventListener('mousemove', function (e) { if (tip.style.opacity == 1) move(e); });
  document.addEventListener('mouseout', function (e) { if (e.target.closest && e.target.closest('[data-tip]')) hide(); });
  document.addEventListener('focusin', show);
  document.addEventListener('focusout', hide);

  /* ---------- motion ---------- */
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced || !('IntersectionObserver' in window)) {
    document.documentElement.classList.add('no-anim');
    return;
  }
  document.documentElement.classList.add('anim-ready');

  // elements that fade+rise once, with a small stagger inside a group
  var groups = [
    ['.hero h1, .hero .lede, .hero .avail', 70],
    ['.gal .tile', 60],
    ['.num-row .num', 80],
    ['.case', 0],
    ['.eyebrow, article h1, .meta, article > .lede', 60],
    ['.stats .stat', 60],
    ['figure', 0],
    ['.reels .reel', 45],
    ['.works .work', 60],
    ['article h2, article h3, article h4, article p, article ul, .insight, .todo, .brands', 0]
  ];
  var seen = new WeakSet();
  groups.forEach(function (g) {
    var els = document.querySelectorAll(g[0]);
    Array.prototype.forEach.call(els, function (el, i) {
      if (seen.has(el)) return;
      seen.add(el);
      el.classList.add('rise');
      if (g[1]) el.style.transitionDelay = Math.min(i * g[1], 320) + 'ms';
    });
  });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      en.target.classList.add('in');
      io.unobserve(en.target);
      if (en.target.tagName === 'FIGURE') animateChart(en.target);
      if (en.target.matches('.num, .stat')) countUp(en.target.querySelector('b'));
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

  document.querySelectorAll('.rise').forEach(function (el) { io.observe(el); });

  // bars grow from their baseline, staggered
  function animateChart(fig) {
    fig.querySelectorAll('svg.chart').forEach(function (svg) {
      var horizontal = svg.classList.contains('chart-h');
      svg.querySelectorAll('path.bar').forEach(function (bar, i) {
        bar.style.animationDelay = Math.min(i * 22, 500) + 'ms';
        bar.classList.add(horizontal ? 'grow-x' : 'grow-y');
      });
    });
  }

  // headline numbers count up, keeping any prefix/suffix ("32.8M", "110000€", "30+")
  function countUp(el) {
    if (!el || el.dataset.counted) return;
    var txt = el.textContent;
    var m = txt.match(/^([^\d]*)([\d.,]+)(.*)$/);
    if (!m) return;
    var raw = m[2].replace(/\./g, function (d, idx) { return d; });
    var target = parseFloat(m[2].replace(/,/g, ''));
    if (!isFinite(target)) return;
    var decimals = (m[2].split('.')[1] || '').length;
    var grouped = m[2].indexOf(',') > -1;
    el.dataset.counted = '1';
    var start = performance.now(), dur = 900;
    function frame(now) {
      var p = Math.min((now - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      var v = target * eased;
      var s = decimals ? v.toFixed(decimals) : String(Math.round(v));
      if (grouped) s = Number(s).toLocaleString('en-US');
      el.textContent = m[1] + s + m[3];
      if (p < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
})();
