// The Iowan: small progressive enhancements. Every page works without this file.
(function () {
  'use strict';

  var store = {
    get: function (k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { window.localStorage.setItem(k, v); } catch (e) { /* storage unavailable */ } }
  };

  // Text size: remembered per reader.
  var sizes = ['normal', 'large', 'larger'];
  function applySize(size) {
    if (sizes.indexOf(size) === -1) size = 'normal';
    document.documentElement.setAttribute('data-text', size);
    document.querySelectorAll('[data-text-size]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-text-size') === size));
    });
  }
  applySize(store.get('iowan-text-size') || 'normal');
  document.querySelectorAll('[data-text-size]').forEach(function (b) {
    b.addEventListener('click', function () {
      var size = b.getAttribute('data-text-size');
      store.set('iowan-text-size', size);
      applySize(size);
    });
  });

  // Mobile menu.
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('primary-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
  }

  // Chip filters: <div data-filter-group="key"> chips with data-value, items with data-key="a b".
  document.querySelectorAll('[data-filter-group]').forEach(function (group) {
    var key = group.getAttribute('data-filter-group');
    var target = document.getElementById(group.getAttribute('data-target'));
    var empty = document.getElementById(group.getAttribute('data-empty'));
    var status = document.getElementById(group.getAttribute('data-status'));
    if (!target) return;
    var chips = group.querySelectorAll('.chip');

    function apply(value) {
      var shown = 0;
      chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c.getAttribute('data-value') === value)); });
      target.querySelectorAll('[data-' + key + ']').forEach(function (item) {
        var match = value === 'all' || item.getAttribute('data-' + key).split(' ').indexOf(value) !== -1;
        item.hidden = !match;
        if (match) shown++;
      });
      if (empty) empty.hidden = shown !== 0;
      if (status) status.textContent = shown + (shown === 1 ? ' result' : ' results');
      var url = new URL(window.location.href);
      if (value === 'all') url.searchParams.delete(key); else url.searchParams.set(key, value);
      window.history.replaceState(null, '', url);
    }

    chips.forEach(function (c) {
      c.addEventListener('click', function () { apply(c.getAttribute('data-value')); });
    });
    var initial = new URLSearchParams(window.location.search).get(key);
    if (initial && group.querySelector('[data-value="' + initial + '"]')) apply(initial);
  });

  // Story search: stories.html?q=word hides cards whose text doesn't match.
  var storyList = document.getElementById('story-list');
  var query = new URLSearchParams(window.location.search).get('q');
  if (storyList && query) {
    var words = query.toLowerCase().split(/\s+/).filter(Boolean);
    var shown = 0;
    storyList.querySelectorAll('article').forEach(function (a) {
      var text = a.textContent.toLowerCase();
      var match = words.every(function (w) { return text.indexOf(w) !== -1; });
      a.hidden = !match;
      if (match) shown++;
    });
    var count = document.getElementById('story-count');
    if (count) count.textContent = shown + (shown === 1 ? ' result' : ' results') + ' for \u201c' + query + '\u201d';
    var empty = document.getElementById('story-empty');
    if (empty) empty.hidden = shown !== 0;
    document.querySelectorAll('input[name="q"]').forEach(function (i) { i.value = query; });
  }

  // Subscribe page: "For me" / "As a gift".
  var giftButtons = document.querySelectorAll('[data-gift]');
  giftButtons.forEach(function (b) {
    b.addEventListener('click', function () {
      var gift = b.getAttribute('data-gift') === 'yes';
      giftButtons.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      document.querySelectorAll('[data-gift-only]').forEach(function (el) { el.hidden = !gift; });
      document.querySelectorAll('[data-gift-label]').forEach(function (el) {
        el.textContent = gift ? el.getAttribute('data-gift-label') : el.getAttribute('data-self-label');
      });
    });
  });

  // Citation tool on story pages.
  var citeBox = document.querySelector('[data-cite]');
  if (citeBox) {
    var d = citeBox.dataset;
    var out = citeBox.querySelector('.cite-out');
    var url = d.url || window.location.href;
    var formats = {
      mla: d.authorLast + ', ' + d.authorFirst + '. “' + d.title + '.” <i>The Iowan</i>, ' + d.issue + ', pp. ' + d.pages + '. ' + url + '.',
      apa: d.authorLast + ', ' + d.authorFirst.charAt(0) + '. (' + d.year + '). ' + d.title + '. <i>The Iowan</i>, ' + d.volume + '. ' + url,
      chicago: d.authorFirst + ' ' + d.authorLast + ', “' + d.title + ',” <i>The Iowan</i>, ' + d.issue + ', ' + d.pages + ', ' + url + '.'
    };
    var tabs = citeBox.querySelectorAll('[role="tab"]');
    function show(fmt) {
      tabs.forEach(function (t) { t.setAttribute('aria-selected', String(t.getAttribute('data-format') === fmt)); });
      out.innerHTML = formats[fmt];
    }
    tabs.forEach(function (t) { t.addEventListener('click', function () { show(t.getAttribute('data-format')); }); });
    show('mla');
    var copy = citeBox.querySelector('[data-copy-cite]');
    if (copy) copy.addEventListener('click', function () {
      var text = out.textContent;
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(function () { copy.textContent = 'Copied'; });
    });
  }

  var copyLink = document.querySelector('[data-copy-link]');
  if (copyLink) copyLink.addEventListener('click', function () {
    if (navigator.clipboard) navigator.clipboard.writeText(window.location.href).then(function () {
      copyLink.querySelector('span').textContent = 'Link copied';
    });
  });

  // Forms are layout only until a back end is chosen: validate, then show a confirmation.
  document.querySelectorAll('form[data-demo]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var firstInvalid = null;
      form.querySelectorAll('[required]').forEach(function (input) {
        var errId = input.id + '-error';
        var err = document.getElementById(errId);
        var bad = !input.checkValidity();
        input.setAttribute('aria-invalid', String(bad));
        if (bad) {
          if (!err) {
            err = document.createElement('p');
            err.id = errId;
            err.className = 'error';
            input.insertAdjacentElement('afterend', err);
            input.setAttribute('aria-describedby', ((input.getAttribute('aria-describedby') || '') + ' ' + errId).trim());
          }
          err.textContent = input.type === 'email' ? 'Enter an email address, like name@example.com.' : 'This field is required.';
          if (!firstInvalid) firstInvalid = input;
        } else if (err) {
          err.textContent = '';
        }
      });
      if (firstInvalid) { firstInvalid.focus(); return; }
      var msg = form.querySelector('.form-status');
      if (!msg) {
        msg = document.createElement('p');
        msg.className = 'form-status';
        msg.setAttribute('role', 'status');
        form.appendChild(msg);
      }
      msg.textContent = form.getAttribute('data-demo');
      form.querySelectorAll('button[type="submit"]').forEach(function (b) { b.disabled = true; });
    });
  });
})();
