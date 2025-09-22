// assets/js/mobile-drawer.js
(function(){
  // ---- safety checks
  const headerInner = document.querySelector('.header .header__inner');
  const desktopNav  = document.querySelector('.header .nav__list');
  if(!headerInner || !desktopNav){ return; }

  // ---- inject CSS once
  if(!document.getElementById('drawer-styles')){
    const css = `
/* injected by mobile-drawer.js */
.hamburger{
  display:none; appearance:none; cursor:pointer;
  border:1px solid var(--edge); background:var(--glass);
  padding:10px 12px; border-radius:10px; font-size:20px; line-height:1;
  box-shadow:var(--shadow-sm);
}
.drawer{ position:fixed; inset:0; z-index:50; pointer-events:none; }
.drawer__backdrop{ position:absolute; inset:0; background:rgba(0,0,0,.28);
  opacity:0; transition:.2s opacity ease; pointer-events:none; border:0; }
.drawer__panel{ position:absolute; top:0; bottom:0; left:0; width:min(86vw, 320px);
  background:rgba(255,255,255,.98); border-right:1px solid var(--edge);
  box-shadow:var(--shadow-lg); transform:translateX(-100%); transition: transform .25s ease;
  display:flex; flex-direction:column; }
.drawer.open{ pointer-events:auto; }
.drawer.open .drawer__panel{ transform:translateX(0); }
.drawer.open .drawer__backdrop{ opacity:1; pointer-events:auto; }
.drawer__head{ display:flex; align-items:center; justify-content:space-between; gap:12px;
  padding:14px 16px; border-bottom:1px solid var(--edge); background:var(--glass); backdrop-filter: blur(8px); }
.drawer__logo{ height:36px; width:auto; }
.drawer__close{ appearance:none; border:1px solid var(--edge); background:#fff;
  border-radius:8px; width:36px; height:36px; font-size:20px; cursor:pointer; }
.drawer__nav{ display:flex; flex-direction:column; padding:12px; gap:6px; }
.drawer__nav a{ padding:12px 12px; border-radius:10px; font-weight:700; color:#263041; }
.drawer__nav a:hover{ background:#f5f7fa; }

/* Mobile breakpoint: hide desktop nav, show hamburger */
@media (max-width: 980px){
  .nav__list{ display:none; }
  .hamburger{ display:inline-block; }
}
    `.trim();
    const style = document.createElement('style');
    style.id = 'drawer-styles';
    style.textContent = css;
    document.head.appendChild(style);
  }

  // ---- add hamburger (before existing nav)
  const burger = document.createElement('button');
  burger.className = 'hamburger';
  burger.id = 'navOpen';
  burger.setAttribute('aria-label','Open menu');
  burger.setAttribute('aria-controls','mobileDrawer');
  burger.setAttribute('aria-expanded','false');
  burger.textContent = '☰';

  // insert just before the nav element
  const navEl = headerInner.querySelector('nav');
  if(navEl){ headerInner.insertBefore(burger, navEl); } else { headerInner.appendChild(burger); }

  // ---- build the drawer (after header)
  const drawer = document.createElement('aside');
  drawer.className = 'drawer';
  drawer.id = 'mobileDrawer';
  drawer.setAttribute('aria-hidden','true');
  drawer.setAttribute('aria-label','Mobile menu');

  // nav items (match your latest order: Services • Projects • News • About • Contact)
  const links = [
    { href: 'services.html', text: 'Services' },
    { href: 'projects.html', text: 'Projects' },
    { href: 'news.html',     text: 'News' },
    { href: 'about.html',    text: 'About' },
    { href: 'contact.html',  text: 'Contact' }
  ];

  drawer.innerHTML = `
    <div class="drawer__panel">
      <div class="drawer__head">
        <img src="assets/img/uploads/tabcon-logo.jpeg" alt="Tabcon Ghana" class="drawer__logo">
        <button class="drawer__close" id="navClose" aria-label="Close menu">×</button>
      </div>
      <nav class="drawer__nav">
        ${links.map(l=>`<a href="${l.href}">${l.text}</a>`).join('')}
      </nav>
    </div>
    <button class="drawer__backdrop" id="navBackdrop" aria-hidden="true"></button>
  `;

  const header = document.querySelector('.header');
  header.insertAdjacentElement('afterend', drawer);

  // ---- wire up interactions
  const closeBtn = drawer.querySelector('#navClose');
  const backdrop = drawer.querySelector('#navBackdrop');

  function openDrawer(){
    drawer.classList.add('open');
    drawer.setAttribute('aria-hidden','false');
    burger.setAttribute('aria-expanded','true');
    closeBtn.focus();
    document.documentElement.style.overflow='hidden';
  }
  function closeDrawer(){
    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden','true');
    burger.setAttribute('aria-expanded','false');
    burger.focus();
    document.documentElement.style.overflow='';
  }

  burger.addEventListener('click', openDrawer);
  closeBtn.addEventListener('click', closeDrawer);
  backdrop.addEventListener('click', closeDrawer);
  document.addEventListener('keydown', (e)=>{ if(e.key==='Escape' && drawer.classList.contains('open')) closeDrawer(); });

  // close on link click (nice for one-page feel)
  drawer.querySelectorAll('.drawer__nav a').forEach(a=>a.addEventListener('click', closeDrawer));

  // ---- active link highlight (optional)
  try{
    const here = location.pathname.split('/').pop().toLowerCase() || 'index.html';
    drawer.querySelectorAll('.drawer__nav a').forEach(a=>{
      const href = a.getAttribute('href')?.toLowerCase();
      if(href && here.endsWith(href)){
        a.style.background = '#f0f3f7';
      }
    });
  }catch(_){}
})();
