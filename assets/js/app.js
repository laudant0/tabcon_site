(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Reveal icon font only once loaded (prevents ligature words flashing) */
  const iconsReady = () => document.documentElement.classList.add('icons-ready');
  if (document.fonts && document.fonts.load) {
    document.fonts.load('24px "Material Symbols Outlined"').then(iconsReady, iconsReady);
    setTimeout(iconsReady, 3000);
  } else iconsReady();

  /* Header: solid on scroll, mobile drawer */
  const header = $('#site-header');
  const drawer = $('#drawer');
  const toggle = $('#menu-toggle');
  const onScroll = () => header && header.classList.toggle('is-solid', scrollY > 40 || header.dataset.solid === 'true');
  onScroll();
  addEventListener('scroll', onScroll, { passive: true });

  const setDrawer = open => {
    if (!drawer || !toggle) return;
    drawer.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.classList.toggle('is-open', open);
    document.body.style.overflow = open ? 'hidden' : '';
    drawer.toggleAttribute('inert', !open);
  };
  if (toggle) {
    setDrawer(false);
    toggle.addEventListener('click', () => setDrawer(!drawer.classList.contains('is-open')));
    $$('a', drawer).forEach(a => a.addEventListener('click', () => setDrawer(false)));
    addEventListener('keydown', e => { if (e.key === 'Escape') setDrawer(false); });
    matchMedia('(min-width:1024px)').addEventListener('change', e => e.matches && setDrawer(false));
  }

  /* Footer year */
  $$('[data-year]').forEach(n => (n.textContent = new Date().getFullYear()));

  /* Reveal + count-up: scroll-position based (robust across browsers) */
  const revealEls = $$('.reveal, .reveal-img');
  const countEls = $$('[data-count]');
  const runCount = el => {
    const end = parseFloat(el.dataset.count);
    const suffix = el.dataset.suffix || '';
    if (reduce) { el.textContent = end + suffix; return; }
    const t0 = performance.now(), dur = 1800;
    const tick = t => {
      const p = Math.min((t - t0) / dur, 1);
      el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  let pendingReveal = revealEls.slice ? revealEls.slice() : Array.from(revealEls);
  let pendingCount = Array.from(countEls);
  const checkInView = () => {
    const vh = window.innerHeight || document.documentElement.clientHeight;
    pendingReveal = pendingReveal.filter(el => {
      const r = el.getBoundingClientRect();
      if (r.top < vh * 0.94 && r.bottom > 0) { el.classList.add('is-in'); return false; }
      return true;
    });
    pendingCount = pendingCount.filter(el => {
      const r = el.getBoundingClientRect();
      if (r.top < vh * 0.9 && r.bottom > 0) { runCount(el); return false; }
      return true;
    });
    if (!pendingReveal.length && !pendingCount.length) {
      window.removeEventListener('scroll', checkInView);
      window.removeEventListener('resize', checkInView);
      clearInterval(inViewTimer);
    }
  };
  const inViewTimer = setInterval(checkInView, 250);
  window.addEventListener('scroll', checkInView, { passive: true });
  window.addEventListener('resize', checkInView);
  checkInView();

  /* Hero slideshow */
  const slides = $$('.hero-slide');
  if (slides.length > 1) {
    const dots = $$('.hero-dot');
    const counter = $('#hero-counter');
    let cur = 0, timer;
    const show = i => {
      slides[cur].classList.remove('is-active');
      dots[cur] && dots[cur].classList.remove('is-active');
      cur = (i + slides.length) % slides.length;
      slides[cur].classList.add('is-active');
      dots.forEach((dot, index) => dot.setAttribute('aria-pressed', String(index === cur)));
      if (dots[cur]) { void dots[cur].offsetWidth; dots[cur].classList.add('is-active'); }
      if (counter) counter.textContent = String(cur + 1).padStart(2, '0') + ' / ' + String(slides.length).padStart(2, '0');
    };
    const start = () => { clearInterval(timer); if (!reduce && !document.hidden) timer = setInterval(() => show(cur + 1), 6000); };
    dots.forEach((d, i) => d.addEventListener('click', () => { show(i); start(); }));
    document.addEventListener('visibilitychange', () => document.hidden ? clearInterval(timer) : start());
    show(0); start();
  }

  /* Gallery filter + lightbox */
  const gallery = $('#gallery-grid');
  if (gallery) {
    const figs = $$('figure', gallery);
    const dlg = $('#lightbox');
    const img = $('#lightbox-img'), cap = $('#lightbox-cap');
    let visible = figs, idx = 0;
    $$('[data-filter]').forEach(btn => btn.addEventListener('click', () => {
      $$('[data-filter]').forEach(b => b.classList.toggle('is-active', b === btn));
      const f = btn.dataset.filter;
      figs.forEach(fg => (fg.hidden = !(f === 'all' || fg.dataset.cat === f)));
      visible = figs.filter(fg => !fg.hidden);
    }));
    const open = i => {
      idx = (i + visible.length) % visible.length;
      const fg = visible[idx];
      img.src = fg.querySelector('img').currentSrc || fg.querySelector('img').src;
      img.alt = fg.querySelector('img').alt;
      cap.textContent = fg.dataset.title + ' — ' + fg.dataset.label;
      if (!dlg.open) dlg.showModal();
    };
    figs.forEach(fg => fg.querySelector('button').addEventListener('click', () => open(visible.indexOf(fg))));
    $('#lb-close').addEventListener('click', () => dlg.close());
    $('#lb-prev').addEventListener('click', () => open(idx - 1));
    $('#lb-next').addEventListener('click', () => open(idx + 1));
    dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft') open(idx - 1);
      if (e.key === 'ArrowRight') open(idx + 1);
    });
  }

  /* News */
  const grid = $('#news-grid');
  if (grid) {
    const data = JSON.parse($('#news-data').textContent).sort((a, b) => new Date(b.date) - new Date(a.date));
    const search = $('#news-search'), more = $('#news-more'), dlg = $('#news-dialog'), empty = $('#news-empty');
    const perPage = 6;
    let cat = 'All', page = 1, list = data;
    const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const fmt = d => new Date(d + 'T00:00:00').toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
    const card = (n, i) => `
      <article class="reveal is-in lift zoom bg-white rounded-sm overflow-hidden flex flex-col shadow-sm">
        <div class="aspect-[16/10] overflow-hidden relative">
          <img src="${n.image}" alt="${esc(n.title)}" loading="lazy" class="w-full h-full object-cover">
          <span class="absolute top-4 left-4 bg-[#9FE870] text-[#101614] text-[11px] font-bold uppercase tracking-widest px-3 py-1">${esc(n.category)}</span>
        </div>
        <div class="p-7 flex flex-col gap-3 flex-1">
          <time class="text-xs font-semibold uppercase tracking-widest text-[#1c6282]">${fmt(n.date)}</time>
          <h3 class="font-display text-2xl font-extrabold leading-tight">${esc(n.title)}</h3>
          <p class="text-[#40484d] leading-relaxed text-[15px]">${esc(n.excerpt)}</p>
          <button type="button" data-read="${i}" class="mt-auto pt-4 inline-flex items-center gap-2 font-bold text-[#006e1c] hover:gap-3 transition-all self-start">Read story <span class="material-symbols-outlined text-xl">arrow_forward</span></button>
        </div>
      </article>`;
    const render = () => {
      const slice = list.slice(0, page * perPage);
      grid.innerHTML = slice.map(n => card(n, data.indexOf(n))).join('');
      more.hidden = slice.length >= list.length;
      empty.hidden = list.length > 0;
    };
    const apply = () => {
      const q = search.value.trim().toLowerCase();
      list = data.filter(n => (cat === 'All' || n.category === cat) &&
        (!q || (n.title + ' ' + n.excerpt + ' ' + n.tags.join(' ')).toLowerCase().includes(q)));
      page = 1; render();
    };
    $$('[data-news-cat]').forEach(b => b.addEventListener('click', () => {
      $$('[data-news-cat]').forEach(x => x.classList.toggle('is-active', x === b));
      cat = b.dataset.newsCat; apply();
    }));
    search.addEventListener('input', apply);
    more.addEventListener('click', () => { page++; render(); });
    grid.addEventListener('click', e => {
      const b = e.target.closest('[data-read]'); if (!b) return;
      const n = data[+b.dataset.read];
      $('#nd-img').src = n.image; $('#nd-img').alt = n.title;
      $('#nd-cat').textContent = n.category + ' · ' + fmt(n.date);
      $('#nd-title').textContent = n.title;
      $('#nd-body').innerHTML = n.body;
      dlg.showModal();
    });
    $('#nd-close').addEventListener('click', () => dlg.close());
    dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
    apply();
  }

  /* Contact form: opens the visitor's email app with the message pre-filled */
  const form = $('#contact-form');
  if (form) {
    const status = $('#form-status');
    form.addEventListener('submit', e => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const d = new FormData(form);
      const body = `Name: ${d.get('name')}\nEmail: ${d.get('email')}\nPhone: ${d.get('phone') || '-'}\nInterest: ${d.get('topic')}\n\n${d.get('message')}`;
      location.href = `mailto:${form.dataset.to}?subject=${encodeURIComponent('Website enquiry: ' + d.get('topic'))}&body=${encodeURIComponent(body)}`;
      status.hidden = false;
      status.textContent = 'Your email app should now open with your message ready to send. If it does not, write to ' + form.dataset.to + ' directly.';
    });
  }
})();
