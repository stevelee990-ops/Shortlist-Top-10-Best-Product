(function () {
  // Mobile menu
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  // Affiliate tag
  var tag = (window.SITE_CONFIG || {}).amazonTag;
  if (tag && tag !== 'YOURTAG-20') {
    document.querySelectorAll('a[data-amazon]').forEach(function (a) {
      try { var u = new URL(a.href); u.searchParams.set('tag', tag); a.href = u.toString(); } catch (e) {}
    });
  }
  // Filters
  var chips = document.querySelectorAll('.chip');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      var f = c.getAttribute('data-filter');
      chips.forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
      document.querySelectorAll('.product').forEach(function (p) {
        p.hidden = !(f === 'all' || (' ' + p.getAttribute('data-f') + ' ').indexOf(' ' + f + ' ') > -1);
      });
    });
  });
  var y = document.getElementById('yr'); if (y) y.textContent = new Date().getFullYear();
})();
