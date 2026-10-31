(function () {
  var doc = document;
  // Mobile menu
  var btn = doc.querySelector('.menu-btn'), nav = doc.getElementById('nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  // Affiliate tag
  var tag = (window.SITE_CONFIG || {}).amazonTag;
  if (tag && tag !== 'YOURTAG-20') {
    doc.querySelectorAll('a[data-amazon]').forEach(function (a) {
      try { var u = new URL(a.href); u.searchParams.set('tag', tag); a.href = u.toString(); } catch (e) {}
    });
  }
  // Filters
  var chips = doc.querySelectorAll('.chip');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      var f = c.getAttribute('data-filter');
      chips.forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
      doc.querySelectorAll('.product').forEach(function (p) {
        p.hidden = !(f === 'all' || (' ' + p.getAttribute('data-f') + ' ').indexOf(' ' + f + ' ') > -1);
      });
    });
  });
  // Reading progress + back to top
  var bar = doc.querySelector('.progress span'), top = doc.querySelector('.to-top'), isGuide = !!doc.querySelector('.products');
  function onScroll() {
    var h = doc.documentElement, max = h.scrollHeight - h.clientHeight, y = h.scrollTop || doc.body.scrollTop;
    if (bar && isGuide) bar.style.transform = 'scaleX(' + (max > 0 ? y / max : 0) + ')';
    if (top) top.classList.toggle('show', y > 1400);
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  // Rank rail: highlight the pick in view
  var rail = doc.querySelectorAll('.rail-links a');
  if (rail.length && 'IntersectionObserver' in window) {
    var map = {}; rail.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.isIntersecting) {
          rail.forEach(function (a) { a.removeAttribute('aria-current'); });
          var a = map[en.target.id]; if (a) { a.setAttribute('aria-current', 'true'); }
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    doc.querySelectorAll('.product').forEach(function (p) { io.observe(p); });
  }
  // Holiday countdown
  var cd = doc.getElementById('countdown');
  if (cd) {
    var now = new Date(), xmas = new Date(now.getFullYear(), 11, 25);
    var days = Math.ceil((xmas - now) / 864e5);
    if (days > 1 && days < 70) cd.textContent = 'Christmas is ' + days + ' days away. Here are the 10 best gifts for everyone on your list.';
  }
  // Search
  var q = doc.getElementById('q'), out = doc.getElementById('results'), idxEl = doc.getElementById('search-index');
  if (q && out && idxEl) {
    var idx = JSON.parse(idxEl.textContent);
    function esc(t) { return t.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
    q.addEventListener('input', function () {
      var v = q.value.trim().toLowerCase();
      if (v.length < 2) { out.hidden = true; out.innerHTML = ''; return; }
      var words = v.split(/\s+/), hits = idx.filter(function (it) {
        var t = (it.t + ' ' + (it.s || '')).toLowerCase();
        return words.every(function (w) { return t.indexOf(w) > -1; });
      }).slice(0, 8);
      out.innerHTML = hits.length ? hits.map(function (it) {
        return '<li><a href="' + it.u + '"><strong>' + esc(it.t) + '</strong>' + (it.s ? '<span>' + esc(it.s) + '</span>' : '<span>Guide</span>') + '</a></li>';
      }).join('') : '<li class="none">No match yet. Try a category like “TV”, “coffee” or “gifts”.</li>';
      out.hidden = false;
    });
    q.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { var a = out.querySelector('a'); if (a) location.href = a.href; }
      if (e.key === 'Escape') { out.hidden = true; }
    });
  }
  var y = doc.getElementById('yr'); if (y) y.textContent = new Date().getFullYear();
})();
