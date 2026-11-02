"""Generates the Tabcon static pages. Run from the repo root: python tools/build.py"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = "assets/img/uploads/"
PARTNERS = "assets/img/partners/Partners/"

PHONE_MAIN = ("+233 (0)20 811 6401", "+233208116401")
PHONE_OFFICE = ("050 989 5777", "+233509895777")
EMAIL_MAIN = "info@tabcongh.com"
EMAIL_OFFICE = "Office@tabcongh.com"

NAV = [
    ("index.html", "Home"),
    ("services.html", "Services"),
    ("projects.html", "Projects"),
    ("news.html", "News"),
    ("about_us.html", "About"),
]

PARTNER_FILES = [
    ("Bui-power-authority.jpg", "Bui Power Authority"),
    ("Voith.jpg", "Voith"),
    ("stanbic.jpg", "Stanbic Bank"),
    ("Wenco.jpg", "Wenco"),
    ("LVS.jpg", "LVS"),
    ("SF.JPG", "SF"),
    ("OIP.jpg", "Partner"),
    ("OIP1.jpg", "Partner"),
    ("R.jpg", "Partner"),
]


def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#101614">
<link rel="icon" href="{IMG}tabcon-logo.webp">
<script>document.documentElement.classList.add('js')</script>
<script src="https://cdn.tailwindcss.com"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&display=swap" rel="stylesheet">
<script>
tailwind.config = {{ theme: {{ extend: {{ colors: {{ ink:'#101614', brand:'#1c6282', leaf:'#006e1c', lime:'#9FE870', paper:'#fbf9f8', stone:'#f1edec', mute:'#40484d' }} }} }} }}
</script>
<link rel="stylesheet" href="assets/css/app.css">
</head>
<body class="bg-paper text-ink">
<a href="#main" class="sr-only focus:not-sr-only focus:fixed focus:z-[100] focus:top-3 focus:left-3 focus:bg-lime focus:text-ink focus:px-4 focus:py-2">Skip to content</a>
"""


def header(active, solid=False):
    links = "".join(
        '<a class="nav-link" href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == active else "", t)
        for h, t in NAV
    )
    drawer = "".join(
        f'<a class="drawer-link font-display text-4xl font-extrabold text-white py-2" style="transition-delay:{i*60+120}ms" href="{h}">{t}</a>'
        for i, (h, t) in enumerate(NAV)
    )
    return f"""<header id="site-header" data-solid="{str(solid).lower()}" class="fixed top-0 inset-x-0 z-50">
  <div class="max-w-7xl mx-auto px-6 lg:px-8 h-20 flex items-center justify-between">
    <a href="index.html" class="font-display font-extrabold text-3xl tracking-tight leading-none" aria-label="Tabcon home">TABCON</a>
    <nav class="hidden lg:flex items-center gap-8" aria-label="Primary">{links}</nav>
    <a href="contact.html" class="hidden lg:inline-flex btn btn-lime !py-3 !px-6 !text-sm">Get in touch</a>
    <button id="menu-toggle" class="lg:hidden w-11 h-11 grid place-items-center" aria-label="Menu" aria-expanded="false" aria-controls="drawer"><span class="burger" aria-hidden="true"><i></i><i></i><i></i></span></button>
  </div>
</header>
<div id="drawer" class="fixed inset-0 z-40 bg-ink blueprint lg:hidden" inert>
  <div class="h-full flex flex-col justify-center px-8 pt-20">
    {drawer}
    <a class="drawer-link btn btn-lime self-start mt-8" style="transition-delay:560ms" href="contact.html">Get in touch</a>
  </div>
</div>
<main id="main">
"""


def footer():
    quick = "".join(f'<li><a class="hover:text-lime transition-colors" href="{h}">{t}</a></li>' for h, t in NAV)
    return f"""</main>
<footer class="bg-ink text-white relative overflow-hidden">
  <div class="blueprint absolute inset-0 opacity-60"></div>
  <div class="relative max-w-7xl mx-auto px-6 lg:px-8 pt-20 pb-10">
    <div class="grid gap-14 md:grid-cols-12">
      <div class="md:col-span-5">
        <p class="font-display font-extrabold text-4xl tracking-tight mb-6">TABCON</p>
        <p class="text-white/65 leading-relaxed max-w-md">Infrastructure, engineering and renewable energy consultants delivering sustainable development across Ghana and Africa since 1983.</p>
        <a href="contact.html" class="btn btn-lime mt-8">Start a conversation <span class="material-symbols-outlined">arrow_forward</span></a>
      </div>
      <div class="md:col-span-3">
        <h4 class="text-xs font-bold tracking-[.25em] uppercase text-lime mb-6">Explore</h4>
        <ul class="space-y-3 text-white/75">{quick}<li><a class="hover:text-lime transition-colors" href="track-record.html">Track Record</a></li><li><a class="hover:text-lime transition-colors" href="gallery.html">Gallery</a></li><li><a class="hover:text-lime transition-colors" href="tain-project.html">Tain Project</a></li><li><a class="hover:text-lime transition-colors" href="partners.html">Partners</a></li></ul>
      </div>
      <div class="md:col-span-4">
        <h4 class="text-xs font-bold tracking-[.25em] uppercase text-lime mb-6">Head office</h4>
        <ul class="space-y-4 text-white/75">
          <li class="flex gap-3"><span class="material-symbols-outlined text-lime">location_on</span><span>Accra, Greater Accra Region<br>Ghana</span></li>
          <li class="flex gap-3"><span class="material-symbols-outlined text-lime">call</span><span><a class="hover:text-lime" href="tel:{PHONE_MAIN[1]}">{PHONE_MAIN[0]}</a><br><a class="hover:text-lime" href="tel:{PHONE_OFFICE[1]}">{PHONE_OFFICE[0]}</a></span></li>
          <li class="flex gap-3"><span class="material-symbols-outlined text-lime">mail</span><span><a class="hover:text-lime" href="mailto:{EMAIL_MAIN}">{EMAIL_MAIN}</a><br><a class="hover:text-lime" href="mailto:{EMAIL_OFFICE}">{EMAIL_OFFICE}</a></span></li>
        </ul>
      </div>
    </div>
    <div class="font-display font-extrabold outline-text text-[22vw] leading-none mt-16 -mb-4 select-none pointer-events-none" aria-hidden="true">TABCON</div>
    <div class="border-t border-white/10 mt-6 pt-6 text-sm text-white/50">© <span data-year>2025</span> Tabcon Development Consultants. All rights reserved.<br><span class="text-white/35 text-xs">Some photos via Wikimedia Commons (CC BY / CC BY-SA): Esthee2010, Wtshymanski, Joseph Archibald Whadji and the Pokuase Interchange photographer.</span></div>
  </div>
</footer>
<script src="assets/js/app.js" defer></script>
</body>
</html>
"""


def eyebrow(text, cls="text-brand"):
    return f'<span class="eyebrow {cls}">{text}</span>'


def page_hero(img, kicker, title, lead, crumb, h="min-h-[78svh]", actions="", pos="center"):
    return f"""<section class="page-hero relative {h} flex items-end overflow-hidden bg-ink text-white">
  <img class="hero-img absolute inset-0 w-full h-full object-cover" style="object-position:{pos}" src="{IMG}{img}" alt="">
  <div class="hero-shade absolute inset-0"></div>
  <div class="relative max-w-7xl mx-auto w-full px-6 lg:px-8 pb-16 md:pb-24 pt-36">
    <p class="text-sm text-white/60 mb-6"><a class="hover:text-lime" href="index.html">Home</a> <span class="mx-2">/</span> {crumb}</p>
    <div>{eyebrow(kicker, "text-lime")}</div>
    <h1 class="font-display font-extrabold text-5xl sm:text-6xl md:text-8xl leading-[.92] mt-6 max-w-4xl">{title}</h1>
    <p class="mt-8 text-lg md:text-xl text-white/80 max-w-2xl leading-relaxed">{lead}</p>{actions}
  </div>
</section>
"""


def cta(kicker, title, text, img="backgg2.jpg"):
    return f"""<section class="relative overflow-hidden bg-ink text-white py-28 md:py-40">
  <img class="absolute inset-0 w-full h-full object-cover opacity-35" src="{IMG}{img}" alt="" loading="lazy">
  <div class="absolute inset-0 bg-gradient-to-t from-ink via-ink/60 to-ink/40"></div>
  <div class="relative max-w-5xl mx-auto px-6 lg:px-8 text-center">
    <div class="reveal">{eyebrow(kicker, "text-lime")}</div>
    <h2 class="reveal font-display font-extrabold text-5xl md:text-8xl leading-[.95] mt-6" style="--d:.1s">{title}</h2>
    <p class="reveal mt-8 text-lg md:text-xl text-white/75 max-w-2xl mx-auto" style="--d:.2s">{text}</p>
    <div class="reveal mt-12 flex flex-wrap justify-center gap-4" style="--d:.3s"><a class="btn btn-lime" href="contact.html">Start a conversation <span class="material-symbols-outlined">arrow_forward</span></a><a class="btn btn-ghost" href="projects.html">See our projects</a></div>
  </div>
</section>
"""


def stat(count, suffix, label):
    return f"""<div class="reveal border-t border-white/15 pt-6"><p class="font-display font-extrabold text-6xl md:text-8xl tracking-tighter text-lime"><span data-count="{count}" data-suffix="{suffix}">0{suffix}</span></p><p class="mt-4 text-xs md:text-sm uppercase tracking-[.2em] font-bold text-white/65">{label}</p></div>"""


def dark_stats(*stats, pad="py-24 md:py-32", bg=None):
    photo = f'<img class="absolute inset-0 w-full h-full object-cover opacity-[.18]" src="{IMG}{bg}" alt="" loading="lazy">' if bg else ""
    return f"""<section class="relative bg-ink text-white {pad} overflow-hidden">{photo}<div class="blueprint absolute inset-0"></div>
  <div class="relative max-w-7xl mx-auto px-6 lg:px-8 grid grid-cols-2 lg:grid-cols-{len(stats)} gap-x-8 gap-y-14">{"".join(stats)}</div></section>
"""


def write(name, html):
    (ROOT / name).write_text(html, encoding="utf-8", newline="\n")


# ---------------------------------------------------------------- HOME
def home():
    hero_imgs = ["gh-solar-rooftop.jpg", "gh-hydro-dam.jpg", "gh-interchange.jpg", "R.jPG", "oooo.jpg"]
    slides = "".join(
        '<div class="hero-slide"><img src="%s%s" alt=""%s></div>' % (IMG, i, "" if k == 0 else ' loading="lazy"')
        for k, i in enumerate(hero_imgs)
    )
    dots = "".join(f'<button class="hero-dot" aria-label="Show slide {k+1}"><i></i></button>' for k in range(len(hero_imgs)))
    ticker_items = ["Highways & Roads", "Rural Water Systems", "Solar PV", "Hydropower", "Battery Storage", "Feasibility Studies", "PPP Advisory", "Construction Supervision"]
    ticker = "".join(f'<span class="font-display font-extrabold text-3xl md:text-5xl px-8 whitespace-nowrap">{t}</span><span class="text-3xl md:text-5xl">✦</span>' for t in ticker_items) * 2
    svc = [
        ("3.jpg", "01", "Engineering & Infrastructure", "Highways, water systems, transport networks and structural developments designed to last."),
        ("SOLARINST.jpg", "02", "Renewable Energy", "Solar, hydro and storage systems for energy security and industrial growth."),
        ("WORKERS.jpg", "03", "Project Delivery", "Feasibility to commissioning: planning, procurement and supervision under one roof."),
    ]
    svc_html = "".join(
        f"""<a href="services.html" class="reveal lift zoom group block relative h-[28rem] overflow-hidden bg-ink text-white" style="--d:{k*.12}s">
      <img class="absolute inset-0 w-full h-full object-cover" src="{IMG}{im}" alt="" loading="lazy">
      <div class="absolute inset-0 bg-gradient-to-t from-ink via-ink/30 to-transparent"></div>
      <div class="absolute inset-x-0 bottom-0 p-8"><span class="font-display text-lime text-lg font-bold">{n}</span><h3 class="font-display font-extrabold text-3xl mt-2 leading-tight">{t}</h3><p class="mt-3 text-white/75 text-[15px] leading-relaxed">{d}</p><span class="mt-5 inline-flex items-center gap-2 font-bold text-lime">Explore <span class="material-symbols-outlined transition-transform group-hover:translate-x-1">arrow_forward</span></span></div>
    </a>"""
        for k, (im, n, t, d) in enumerate(svc)
    )
    proj = [
        ("pic13.jpg", "Urban Road Expansion", "Mobility, logistics and urban connectivity."),
        ("ROADCONS.jpg", "Accra–Kumasi Highway", "Road infrastructure for regional growth."),
        ("viii.jPG", "Renewable Energy Systems", "Utility-scale solar for resilient power."),
    ]
    proj_html = "".join(
        f"""<a href="projects.html" class="reveal lift zoom block bg-white overflow-hidden" style="--d:{k*.12}s"><div class="aspect-[4/3] overflow-hidden"><img class="w-full h-full object-cover" src="{IMG}{im}" alt="{t}" loading="lazy"></div><div class="p-7"><h3 class="font-display font-extrabold text-2xl">{t}</h3><p class="mt-2 text-mute">{d}</p></div></a>"""
        for k, (im, t, d) in enumerate(proj)
    )
    logos = "".join(
        f'<div class="logo-tile h-24 bg-white grid place-items-center p-5"><img class="max-h-full max-w-full object-contain" src="{PARTNERS}{f}" alt="{n}" loading="lazy"></div>'
        for f, n in PARTNER_FILES[:6]
    )
    return (
        head("Tabcon Ghana | Infrastructure, Engineering & Renewable Energy", "Tabcon Development Consultants delivers roads, solar systems, hydropower and infrastructure projects across Ghana and Africa since 1983.")
        + header("index.html")
        + f"""<section class="relative min-h-[100svh] flex items-end overflow-hidden bg-ink text-white">
  <div class="absolute inset-0">{slides}</div>
  <div class="hero-shade absolute inset-0"></div>
  <div class="relative max-w-7xl mx-auto w-full px-6 lg:px-8 pb-28 md:pb-32 pt-40">
    <div>{eyebrow("Since 1983 · Accra, Ghana", "text-lime")}</div>
    <h1 class="font-display font-extrabold text-[2.9rem] sm:text-6xl md:text-8xl lg:text-[8.5rem] leading-[.9] mt-6 max-w-5xl">Building Africa's future, <span class="text-lime">sustainably.</span></h1>
    <p class="mt-8 text-lg md:text-xl text-white/80 max-w-2xl leading-relaxed">Roads, solar, hydropower and engineering solutions shaping the continent's next era of growth.</p>
    <div class="mt-10 flex flex-wrap gap-4"><a class="btn btn-lime" href="projects.html">Explore our projects <span class="material-symbols-outlined">arrow_forward</span></a><a class="btn btn-ghost" href="track-record.html">Track record</a></div>
  </div>
  <div class="absolute bottom-8 inset-x-0"><div class="max-w-7xl mx-auto px-6 lg:px-8 flex items-center justify-between"><div class="flex gap-2">{dots}</div><span id="hero-counter" class="font-display font-bold text-white/70 text-sm tracking-widest">01 / 05</span></div></div>
</section>

<section class="bg-lime text-ink py-5 overflow-hidden" aria-hidden="true"><div class="marquee">{ticker}</div></section>

<section class="py-28 md:py-40">
  <div class="max-w-7xl mx-auto px-6 lg:px-8 grid lg:grid-cols-12 gap-16 items-center">
    <div class="lg:col-span-6 relative">
      <div class="reveal-img overflow-hidden"><img class="w-full aspect-[4/5] object-cover" src="{IMG}ix.jpg" alt="Engineer inspecting solar panels" loading="lazy"></div>
      <div class="reveal-img absolute -top-8 -right-2 md:-right-10 w-40 md:w-56 border-8 border-paper shadow-2xl overflow-hidden" style="--d:.2s"><img class="w-full aspect-square object-cover" src="{IMG}newpic3.jpg" alt="Field team installing equipment" loading="lazy"></div>
      <div class="reveal absolute -bottom-8 left-6 md:left-8 bg-ink text-white p-8 shadow-2xl max-w-[16rem]"><p class="font-display font-extrabold text-6xl text-lime">40+</p><p class="text-sm uppercase tracking-widest font-bold mt-2 text-white/70">Years of engineering across Africa</p></div>
    </div>
    <div class="lg:col-span-6 lg:pl-8">
      <div class="reveal">{eyebrow("About Tabcon")}</div>
      <h2 class="reveal font-display font-extrabold text-4xl md:text-6xl leading-[1] mt-6" style="--d:.1s">Engineering development with African vision.</h2>
      <p class="reveal mt-8 text-lg text-mute leading-relaxed" style="--d:.15s">Tabcon Development Consultants focuses on infrastructure, consulting, renewable energy and engineering projects across Ghana and Africa.</p>
      <p class="reveal mt-5 text-mute leading-relaxed" style="--d:.2s">From solar systems and highways to modern structural developments, we combine innovation, execution and long-term thinking.</p>
      <a class="reveal btn btn-dark mt-10" style="--d:.25s" href="about_us.html">Our story <span class="material-symbols-outlined">arrow_forward</span></a>
    </div>
  </div>
</section>

{dark_stats(stat(40, "+", "Years building infrastructure"), stat(250, "+", "KM of highways built"), stat(300, "+", "Rural water supply systems"), stat(12, "", "African nations"), bg="pic10.jpg")}

<section class="py-28 md:py-36 bg-stone">
  <div class="max-w-7xl mx-auto px-6 lg:px-8">
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-8 mb-16">
      <div><div class="reveal">{eyebrow("What we do")}</div><h2 class="reveal font-display font-extrabold text-4xl md:text-6xl leading-[1] mt-6 max-w-2xl" style="--d:.1s">Capabilities built for scale.</h2></div>
      <a class="reveal font-bold text-brand border-b-2 border-leaf pb-1 hover:text-leaf transition-colors self-start md:self-auto" href="services.html">All services →</a>
    </div>
    <div class="grid md:grid-cols-3 gap-6">{svc_html}</div>
  </div>
</section>

<section class="relative bg-ink text-white overflow-hidden">
  <div class="grid lg:grid-cols-2 min-h-[34rem]">
    <div class="relative min-h-[22rem] reveal-img overflow-hidden"><img class="absolute inset-0 w-full h-full object-cover object-[30%_75%]" src="{IMG}AREA.jpg" alt="Floating solar beside a hydropower reservoir" loading="lazy"><div class="absolute inset-0 bg-gradient-to-r from-transparent to-ink/80 hidden lg:block"></div></div>
    <div class="relative px-6 lg:px-16 py-20 md:py-28 flex flex-col justify-center">
      <div class="reveal">{eyebrow("Flagship · Tabcon Energy Limited", "text-lime")}</div>
      <h2 class="reveal font-display font-extrabold text-4xl md:text-6xl leading-[1] mt-6" style="--d:.1s">Tain Hybrid <span class="text-lime">Hydro-Solar</span> Energy Project</h2>
      <p class="reveal mt-8 text-white/75 text-lg leading-relaxed max-w-xl" style="--d:.15s">Hydropower reliability with solar scale: 70 MW of clean, dispatchable power for the Bono Region and the national grid.</p>
      <div class="reveal mt-10 flex gap-10" style="--d:.2s"><div><p class="font-display font-extrabold text-5xl text-lime">70 MW</p><p class="text-xs uppercase tracking-widest text-white/60 mt-1">Total capacity</p></div><div><p class="font-display font-extrabold text-5xl text-lime">2</p><p class="text-xs uppercase tracking-widest text-white/60 mt-1">Development phases</p></div></div>
      <a class="reveal btn btn-lime mt-12 self-start" style="--d:.25s" href="tain-project.html">Discover the project <span class="material-symbols-outlined">arrow_forward</span></a>
    </div>
  </div>
</section>

<section class="py-28 md:py-36">
  <div class="max-w-7xl mx-auto px-6 lg:px-8">
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-8 mb-16">
      <div><div class="reveal">{eyebrow("Featured work")}</div><h2 class="reveal font-display font-extrabold text-4xl md:text-6xl leading-[1] mt-6" style="--d:.1s">Projects that move nations.</h2></div>
      <a class="reveal font-bold text-brand border-b-2 border-leaf pb-1 hover:text-leaf transition-colors self-start md:self-auto" href="projects.html">View all projects →</a>
    </div>
    <div class="grid md:grid-cols-3 gap-6">{proj_html}</div>
  </div>
</section>

<section class="py-28 md:py-36 bg-stone">
  <div class="max-w-7xl mx-auto px-6 lg:px-8 grid lg:grid-cols-12 gap-12 lg:gap-16 items-center">
    <div class="lg:col-span-5 order-2 lg:order-1">
      <div class="reveal">{eyebrow("Beyond infrastructure")}</div>
      <h2 class="reveal font-display font-extrabold text-4xl md:text-6xl leading-[1] mt-6" style="--d:.1s">Clean water. Reliable power. <span class="text-leaf">Real lives.</span></h2>
      <p class="reveal mt-8 text-lg text-mute leading-relaxed" style="--d:.15s">Every road, borehole and solar array we deliver is measured by what it changes for the communities around it: safer journeys, safe drinking water and energy that keeps clinics, schools and businesses running.</p>
      <div class="reveal mt-10 grid grid-cols-2 gap-8" style="--d:.2s"><div class="border-t-2 border-leaf pt-4"><p class="font-display font-extrabold text-5xl text-ink">300+</p><p class="text-sm text-mute mt-1">Rural water systems</p></div><div class="border-t-2 border-leaf pt-4"><p class="font-display font-extrabold text-5xl text-ink">250+</p><p class="text-sm text-mute mt-1">KM of highways built</p></div></div>
      <a class="reveal btn btn-green mt-10" style="--d:.25s" href="track-record.html">See the track record <span class="material-symbols-outlined">arrow_forward</span></a>
    </div>
    <div class="lg:col-span-7 order-1 lg:order-2 grid grid-cols-12 gap-4 md:gap-6">
      <div class="reveal-img col-span-7 row-span-2 overflow-hidden"><img class="w-full h-full min-h-[26rem] object-cover" src="{IMG}Picture1.jpg" alt="Clean water flowing from a community tap" loading="lazy"></div>
      <div class="reveal-img col-span-5 overflow-hidden" style="--d:.15s"><img class="w-full h-full aspect-square object-cover" src="{IMG}Picture8.jpg" alt="Child drinking from a standpipe" loading="lazy"></div>
      <div class="reveal-img col-span-5 overflow-hidden" style="--d:.3s"><img class="w-full h-full aspect-square object-cover" src="{IMG}backgg2.jpg" alt="Hands under flowing water" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="bg-ink">
  <div class="grid grid-cols-2 md:grid-cols-4">
    <div class="reveal-img relative h-56 md:h-72 overflow-hidden"><img class="absolute inset-0 w-full h-full object-cover" src="{IMG}newpic4.jpg" alt="Floating solar on a reservoir" loading="lazy"></div>
    <div class="reveal-img relative h-56 md:h-72 overflow-hidden" style="--d:.1s"><img class="absolute inset-0 w-full h-full object-cover" src="{IMG}newpic6.jpg" alt="Road crew at work" loading="lazy"></div>
    <div class="reveal-img relative h-56 md:h-72 overflow-hidden" style="--d:.2s"><img class="absolute inset-0 w-full h-full object-cover" src="{IMG}workkk.jpg" alt="Technicians fitting solar panels" loading="lazy"></div>
    <div class="reveal-img relative h-56 md:h-72 overflow-hidden" style="--d:.3s"><img class="absolute inset-0 w-full h-full object-cover" src="{IMG}picture9.jpg" alt="Road roller on a new highway" loading="lazy"></div>
  </div>
</section>

<section class="py-28 md:py-36 bg-ink text-white relative overflow-hidden">
  <div class="blueprint absolute inset-0"></div>
  <div class="relative max-w-7xl mx-auto px-6 lg:px-8">
    <div class="max-w-3xl mb-14"><div class="reveal">{eyebrow("Solar in Ghana", "text-lime")}</div><h2 class="reveal font-display font-extrabold text-4xl md:text-6xl leading-[1] mt-6" style="--d:.1s">Ghana is powering up.</h2><p class="reveal mt-6 text-white/70 text-lg leading-relaxed" style="--d:.15s">From rooftop arrays on city buildings to solar-powered street lighting, clean energy is already at work across Ghana. This is the future Tabcon is engineering.</p></div>
    <div class="grid md:grid-cols-12 gap-4 md:gap-6">
      <figure class="reveal-img md:col-span-7 relative overflow-hidden group"><img class="w-full h-full min-h-[22rem] object-cover transition-transform duration-700 group-hover:scale-105" src="{IMG}gh-solar-house.jpg" alt="Rooftop solar panels on a building in Ghana" loading="lazy"><figcaption class="absolute inset-x-0 bottom-0 p-6 bg-gradient-to-t from-ink/90 to-transparent"><p class="font-display font-extrabold text-2xl">Rooftop solar</p><p class="text-sm text-white/70">Clean power for institutions and homes</p></figcaption></figure>
      <figure class="reveal-img md:col-span-5 relative overflow-hidden group" style="--d:.15s"><img class="w-full h-full min-h-[22rem] object-cover transition-transform duration-700 group-hover:scale-105" src="{IMG}gh-solar-streetlight.jpg" alt="Solar-powered street light in Ghana" loading="lazy"><figcaption class="absolute inset-x-0 bottom-0 p-6 bg-gradient-to-t from-ink/90 to-transparent"><p class="font-display font-extrabold text-2xl">Solar street lighting</p><p class="text-sm text-white/70">Safer streets, off the grid</p></figcaption></figure>
      <figure class="reveal-img md:col-span-12 relative overflow-hidden group" style="--d:.3s"><img class="w-full h-72 md:h-[26rem] object-cover transition-transform duration-700 group-hover:scale-105" src="{IMG}gh-solar-panel.jpg" alt="Commercial rooftop solar arrays in Accra, Ghana" loading="lazy"><figcaption class="absolute inset-x-0 bottom-0 p-6 bg-gradient-to-t from-ink/90 to-transparent"><p class="font-display font-extrabold text-2xl">Commercial solar arrays</p><p class="text-sm text-white/70">Large-scale rooftop generation in the city</p></figcaption></figure>
    </div>
    <p class="mt-6 text-xs text-white/40">Photos: Esthee2010 via Wikimedia Commons (CC BY 4.0 / CC BY-SA 4.0).</p>
  </div>
</section>

<section class="py-20 bg-stone">
  <div class="max-w-7xl mx-auto px-6 lg:px-8">
    <div class="flex items-end justify-between mb-10"><div class="reveal">{eyebrow("Trusted by")}</div><a class="font-bold text-brand hover:text-leaf" href="partners.html">All partners →</a></div>
    <div class="reveal grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">{logos}</div>
  </div>
</section>
"""
        + cta("Work with Tabcon", "Let's build what matters.", "Infrastructure is civilisation in physical form. Tell us about your next project.", "newpic5.jpg")
        + footer()
    )


# ---------------------------------------------------------------- ABOUT
def about():
    pillars = [
        ("visibility", "Vision", "To become one of Africa's defining infrastructure and development consultancy firms shaping sustainable growth."),
        ("flag", "Mission", "Delivering engineering excellence, strategic advisory and clean energy systems through innovation, discipline and execution."),
        ("psychology", "Philosophy", "Africa's future will not be imported. It will be engineered, financed and built from within."),
    ]
    cards = "".join(
        f"""<div class="reveal lift bg-white p-10 border-t-4 border-leaf" style="--d:{k*.12}s"><span class="material-symbols-outlined text-5xl text-brand">{i}</span><h3 class="font-display font-extrabold text-3xl mt-6">{t}</h3><p class="mt-4 text-mute leading-relaxed">{d}</p></div>"""
        for k, (i, t, d) in enumerate(pillars)
    )
    return (
        head("About Us | Tabcon Ghana", "Tabcon is a development consultancy focused on infrastructure, engineering, renewable energy and strategic project delivery across Africa.")
        + header("about_us.html")
        + page_hero("Dl66b83XgAE3LX0.jpg", "About Tabcon", "Building <span class='text-lime'>futures.</span>", "Chancellor Angela Merkel and Vice President Dr Mahamudu Bawumia at the Germany-Ghana Business Cooperation forum, Accra, 30 August 2018. Tabcon engineers systems, infrastructure and energy solutions that move nations forward.", "About", pos="center 30%")
        + f"""<section class="py-28 md:py-40">
  <div class="max-w-7xl mx-auto px-6 lg:px-8 grid lg:grid-cols-12 gap-16">
    <div class="lg:col-span-5"><div class="reveal">{eyebrow("Who we are")}</div><h2 class="reveal font-display font-extrabold text-4xl md:text-6xl leading-[1] mt-6" style="--d:.1s">Infrastructure with purpose.</h2></div>
    <div class="lg:col-span-7 space-y-6 text-lg text-mute leading-relaxed">
      <p class="reveal">Tabcon is a development consultancy focused on infrastructure, engineering, renewable energy and strategic project delivery across Africa.</p>
      <p class="reveal text-ink text-2xl md:text-3xl font-display font-bold leading-snug">We believe infrastructure is not just construction. It is economics. Energy. Water. Mobility. The architecture of national transformation.</p>
    </div>
  </div>
</section>
<section class="pb-28 md:pb-40"><div class="max-w-7xl mx-auto px-6 lg:px-8 grid md:grid-cols-3 gap-6">{cards}</div></section>

<section class="relative bg-ink text-white py-28 md:py-36 overflow-hidden">
  <div class="blueprint absolute inset-0"></div>
  <div class="relative max-w-7xl mx-auto px-6 lg:px-8 grid lg:grid-cols-2 gap-16 items-center">
    <div>
      <div class="reveal">{eyebrow("Our journey", "text-lime")}</div>
      <h2 class="reveal font-display font-extrabold text-4xl md:text-6xl leading-[1] mt-6" style="--d:.1s">From Lesotho to the continent.</h2>
      <p class="reveal mt-8 text-white/75 text-lg leading-relaxed" style="--d:.15s">Established in 1983 in Lesotho and later, in 1988, in Ghana as Tabcon Limited, our firm has evolved into a premier consultancy driving sustainable development across the continent.</p>
      <div class="reveal mt-12 grid grid-cols-2 gap-8" style="--d:.2s"><div class="border-t border-lime pt-4"><p class="font-display font-extrabold text-5xl text-lime">1983</p><p class="text-sm text-white/60 mt-1">Founded in Lesotho</p></div><div class="border-t border-lime pt-4"><p class="font-display font-extrabold text-5xl text-lime">1988</p><p class="text-sm text-white/60 mt-1">Tabcon Limited, Ghana</p></div></div>
    </div>
    <div class="reveal-img overflow-hidden"><img class="w-full aspect-[4/3] object-cover" src="{IMG}pic11.jpeg" alt="Tabcon engineering project" loading="lazy"></div>
  </div>
</section>

<section class="py-28 md:py-36 text-center">
  <div class="max-w-4xl mx-auto px-6"><div class="reveal">{eyebrow("Core philosophy")}</div><p class="reveal font-display font-extrabold text-3xl md:text-5xl leading-[1.1] mt-8" style="--d:.1s">“Engineering isn't just about structures; it's about building the framework for a sustainable future for every community we touch.”</p></div>
</section>
"""
        + cta("The future", "Engineering the next African era.", "From transport and water infrastructure to renewable energy and advisory, we are building frameworks for the next generation of growth.", "roadd.jpg")
        + footer()
    )


# ---------------------------------------------------------------- SERVICES
def mini(icon, t, d, k):
    return f"""<div class="reveal lift bg-white p-8" style="--d:{k*.1}s"><span class="material-symbols-outlined text-4xl text-leaf">{icon}</span><h4 class="font-display font-extrabold text-2xl mt-5">{t}</h4><p class="mt-3 text-mute leading-relaxed">{d}</p></div>"""


def services():
    blocks = [
        ("gh-tamale-highway.jpg", "01", "Engineering & Infrastructure", "Designing resilient infrastructure systems including highways, water systems, transport networks and structural developments.", ["Highways & roads", "Water systems", "Transport networks", "Structural developments"]),
        ("TOPFLOOR.jpg", "02", "Renewable Energy", "Clean energy systems engineered for sustainable development, grid optimisation and long-term energy security for heavy industrial companies.", ["Solar PV", "Hydropower", "Battery storage", "Grid optimisation"]),
    ]
    rows = ""
    for k, (im, n, t, d, tags) in enumerate(blocks):
        flip = " lg:order-2" if k % 2 else ""
        pills = "".join(f'<li class="px-4 py-2 border border-ink/15 text-sm font-semibold">{x}</li>' for x in tags)
        rows += f"""<div class="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center mb-28 last:mb-0">
      <div class="reveal-img overflow-hidden{flip}"><img class="w-full aspect-[4/3] object-cover" src="{IMG}{im}" alt="{t}" loading="lazy"></div>
      <div><span class="reveal block font-display font-extrabold text-8xl text-ink/10 leading-none">{n}</span><h3 class="reveal font-display font-extrabold text-4xl md:text-5xl leading-tight -mt-4">{t}</h3><p class="reveal mt-6 text-lg text-mute leading-relaxed">{d}</p><ul class="reveal mt-8 flex flex-wrap gap-3">{pills}</ul></div>
    </div>"""
    dev = "".join(mini(*x, k) for k, x in enumerate([("query_stats", "Feasibility Studies", "Technical assessments and development planning."), ("engineering", "Construction Supervision", "Oversight and quality assurance during execution."), ("account_balance", "Financial Structuring", "Capital strategy and infrastructure investment planning.")]))
    adv = "".join(mini(*x, k) for k, x in enumerate([("handshake", "PPP Advisory", "Public-private partnership development and transaction advisory."), ("eco", "Environmental Studies", "Sustainability assessments and environmental impact analysis."), ("gavel", "Regulatory Consulting", "Frameworks and policy guidance for infrastructure systems.")]))
    afr = """<div class="reveal border-t border-white/15 pt-6"><p class="font-display font-extrabold text-6xl md:text-8xl tracking-tighter text-lime">AFR</p><p class="mt-4 text-xs md:text-sm uppercase tracking-[.2em] font-bold text-white/65">Africa-centred vision</p></div>"""
    return (
        head("Services | Tabcon Ghana", "Engineering, renewable energy, project development and advisory services from Tabcon Development Consultants.")
        + header("services.html")
        + page_hero("gh-paving.jpg", "Engineering · Energy · Development", "Technical <span class='text-lime'>precision.</span>", "Large-scale infrastructure, engineering and renewable energy solutions built for long-term African transformation.", "Services")
        + f"""<section class="py-28 md:py-40"><div class="max-w-7xl mx-auto px-6 lg:px-8">
  <div class="max-w-3xl mb-24"><div class="reveal">{eyebrow("Expert capabilities")}</div><h2 class="reveal font-display font-extrabold text-4xl md:text-6xl leading-[1] mt-6" style="--d:.1s">Infrastructure built with vision.</h2><p class="reveal mt-8 text-lg text-mute leading-relaxed" style="--d:.15s">We combine engineering expertise, project management, renewable energy systems and strategic consulting to execute impactful projects across Ghana and Africa.</p></div>
  {rows}
</div></section>
<section class="py-28 bg-stone"><div class="max-w-7xl mx-auto px-6 lg:px-8">
  <div class="reveal">{eyebrow("Project development")}</div><h2 class="reveal font-display font-extrabold text-4xl md:text-6xl leading-[1] mt-6 mb-6" style="--d:.1s">End-to-end project management.</h2><p class="reveal text-lg text-mute max-w-2xl mb-14">From feasibility studies and engineering concepts to procurement, supervision and commissioning, Tabcon manages projects through every phase.</p>
  <div class="grid md:grid-cols-3 gap-6">{dev}</div>
  <div class="mt-28"><div class="reveal">{eyebrow("Advisory & policy")}</div><h2 class="reveal font-display font-extrabold text-4xl md:text-6xl leading-[1] mt-6 mb-6" style="--d:.1s">Strategic counsel.</h2><p class="reveal text-lg text-mute max-w-2xl mb-14">Consulting for governments, institutions and developers navigating energy, water and transport systems.</p></div>
  <div class="grid md:grid-cols-3 gap-6">{adv}</div>
</div></section>
{dark_stats(stat(740, "+", "KM of infrastructure planning"), stat(20, "+", "Development concepts"), stat(100, "%", "Sustainability focused"), afr, pad="py-24")}
"""
        + cta("Build with Tabcon", "Engineering Africa's next era.", "Infrastructure is economic movement. Energy is national growth. Development is the future.", "newpic7.jpg")
        + footer()
    )


# ---------------------------------------------------------------- PROJECTS
def projects():
    items = [
        ("ghana-body.jpg", "Energy", "Tain Hybrid Hydro-Solar Project", "Renewable infrastructure concept integrating hydro and solar generation to support sustainable power expansion in Ghana.", "tain-project.html"),
        ("gh-motorway.jpg", "Roads", "Urban Road Expansion", "Transportation and road engineering designed to improve mobility, logistics efficiency and urban connectivity.", None),
        ("gh-earthworks.jpg", "Planning", "Development Planning", "Long-term engineering consultancy and planning support for future-focused infrastructure and investment strategies.", None),
        ("gh-road-works.jpg", "Roads", "Highway Construction", "Modern road infrastructure focused on economic growth, mobility expansion and regional development.", None),
        ("JYT.jpg", "Energy", "Renewable Energy Systems", "Smart solar deployment supporting sustainable power generation and infrastructure resilience.", None),
        ("PPP.JPG", "Structures", "Structural Development", "Engineering execution combining precision planning, technical expertise and modern development systems.", None),
    ]
    cards = ""
    for k, (im, tag, t, d, link) in enumerate(items):
        more = f'<a class="mt-6 inline-flex items-center gap-2 font-bold text-leaf" href="{link}">View project <span class="material-symbols-outlined">arrow_forward</span></a>' if link else ""
        big = " md:col-span-2" if k == 0 else ""
        aspect = "aspect-[16/9]" if k == 0 else "aspect-[4/3]"
        cards += f"""<article class="reveal lift zoom bg-white overflow-hidden{big}"><div class="{aspect} overflow-hidden relative"><img class="w-full h-full object-cover" src="{IMG}{im}" alt="{t}" loading="lazy"><span class="absolute top-5 left-5 bg-lime text-ink text-[11px] font-bold uppercase tracking-widest px-3 py-1">{tag}</span></div><div class="p-8 md:p-10"><h3 class="font-display font-extrabold text-3xl">{t}</h3><p class="mt-3 text-mute leading-relaxed max-w-xl">{d}</p>{more}</div></article>"""
    return (
        head("Projects | Tabcon Ghana", "Featured developments from Tabcon: renewable energy, highways, urban roads and structural engineering.")
        + header("projects.html")
        + page_hero("gh-crane-site.jpg", "Projects", "Over 40 years of <span class='text-lime'>excellence.</span>", "From the highlands of Lesotho to the growing landscapes of Ghana, Tabcon has been a cornerstone of engineering innovation since 1983.", "Projects", actions='<div class="mt-10 flex flex-wrap gap-4"><a class="btn btn-lime" href="track-record.html">View our track record <span class="material-symbols-outlined">arrow_forward</span></a><a class="btn btn-ghost" href="gallery.html">Project gallery</a></div>')
        + dark_stats(stat(20, "+", "Infrastructure concepts"), stat(10, "+", "Engineering partnerships"), stat(5, "+", "Renewable initiatives"), stat(100, "%", "African-focused vision"), pad="py-20")
        + f"""<section class="py-28 md:py-36"><div class="max-w-7xl mx-auto px-6 lg:px-8">
  <div class="mb-16 max-w-3xl"><div class="reveal">{eyebrow("Featured developments")}</div><h2 class="reveal font-display font-extrabold text-4xl md:text-6xl leading-[1] mt-6" style="--d:.1s">Strategic projects designed for long-term impact.</h2></div>
  <div class="grid md:grid-cols-2 gap-6">{cards}</div>
</div></section>
"""
        + cta("Build the future", "Infrastructure that shapes nations.", "Engineering, sustainability and African development thinking, delivered as transformational projects.", "gh-labour.jpg")
        + footer()
    )


# ---------------------------------------------------------------- TRACK RECORD
def track():
    steps = [
        ("backgg1.jpg", "1983", "Lesotho Highlands Hydroelectric Scheme", "Feasibility studies, engineering design and supervision for one of Africa's major hydroelectric projects."),
        ("gh-accra-kumasi.jpg", "Roads", "Accra–Kumasi Highway Dualization", "Large-scale transportation corridor engineering improving logistics and national mobility."),
        ("Picture3.jpg", "Water", "Sustainable Rural Water Systems", "Community water systems, boreholes and sanitation infrastructure across Ghana."),
        ("iii.JPG", "Energy", "Tain Hybrid Hydro–Solar Project", "Integrating hydro, solar and battery technologies into Africa's sustainable energy future."),
    ]
    tl = ""
    for k, (im, tag, t, d) in enumerate(steps):
        flip = " md:order-2" if k % 2 else ""
        tl += f"""<div class="relative grid md:grid-cols-2 gap-8 md:gap-16 items-center mb-20 last:mb-0 pl-12 md:pl-0">
      <span class="absolute left-[11px] md:left-1/2 md:-translate-x-1/2 top-2 w-[18px] h-[18px] rounded-full bg-lime ring-4 ring-ink z-10"></span>
      <div class="reveal-img overflow-hidden{flip}"><img class="w-full aspect-[16/10] object-cover" src="{IMG}{im}" alt="{t}" loading="lazy"></div>
      <div class="reveal"><span class="font-display font-extrabold text-lime text-xl">0{k+1} · {tag}</span><h3 class="font-display font-extrabold text-3xl md:text-4xl mt-3 leading-tight">{t}</h3><p class="mt-4 text-white/70 text-lg leading-relaxed">{d}</p></div>
    </div>"""
    return (
        head("Track Record | Tabcon Ghana", "Four decades of engineering across Africa: hydroelectric schemes, highways, rural water systems and renewable energy.")
        + header("projects.html")
        + page_hero("gh-bui-construction.jpg", "Tabcon track record", "Decades of engineering <span class='text-lime'>across Africa.</span>", "Infrastructure, energy, transportation, water systems and large-scale development projects shaping the next era of African growth.", "Track record")
        + f"""<section class="relative bg-ink text-white py-24 md:py-32 overflow-hidden"><div class="blueprint absolute inset-0"></div>
  <div class="relative max-w-7xl mx-auto px-6 lg:px-8 grid md:grid-cols-3 gap-12">
    <div class="reveal border-t border-white/15 pt-6"><p class="font-display font-extrabold text-7xl md:text-8xl text-lime"><span data-count="40" data-suffix="+">0+</span></p><p class="mt-4 text-white/65">Years of multidisciplinary engineering and infrastructure consulting.</p></div>
    <div class="reveal border-t border-white/15 pt-6"><p class="font-display font-extrabold text-7xl md:text-8xl text-lime"><span data-count="700" data-suffix="+">0+</span></p><p class="mt-4 text-white/65">Kilometres of transportation infrastructure delivered.</p></div>
    <div class="reveal border-t border-white/15 pt-6"><p class="font-display font-extrabold text-7xl md:text-8xl text-lime"><span data-count="132">0</span></p><p class="mt-4 text-white/65">Water and community systems implemented across Ghana.</p></div>
  </div>
</section>
<section class="bg-ink text-white pb-28 md:pb-40"><div class="max-w-6xl mx-auto px-6 lg:px-8">
  <div class="text-center py-20"><div class="reveal">{eyebrow("History", "text-lime")}</div><h2 class="reveal font-display font-extrabold text-4xl md:text-6xl leading-[1] mt-6" style="--d:.1s">Timeline &amp; milestones.</h2></div>
  <div class="relative"><div class="tl-line absolute left-5 md:left-1/2 top-0 bottom-0 w-[2px] md:-translate-x-1/2"></div>{tl}</div>
</div></section>
<section class="py-28 md:py-36"><div class="max-w-7xl mx-auto px-6 lg:px-8 grid lg:grid-cols-2 gap-16 items-center">
  <div><div class="reveal">{eyebrow("Legacy")}</div><h2 class="reveal font-display font-extrabold text-4xl md:text-6xl leading-[1] mt-6" style="--d:.1s">Infrastructure beyond generations.</h2><p class="reveal mt-8 text-lg text-mute leading-relaxed">Tabcon's history is built on decades of execution across transportation, water systems, hydroelectric projects, renewable energy and environmental planning.</p></div>
  <div class="grid grid-cols-2 gap-6"><div class="reveal bg-white p-10 lift"><p class="font-display font-extrabold text-6xl text-leaf"><span data-count="15" data-suffix="+">0+</span></p><p class="mt-3 text-mute font-semibold">Major infrastructure programmes</p></div><div class="reveal bg-white p-10 lift" style="--d:.1s"><p class="font-display font-extrabold text-6xl text-brand"><span data-count="4">0</span></p><p class="mt-3 text-mute font-semibold">African regions</p></div></div>
</div></section>
"""
        + cta("Future forward", "Building Africa's next chapter.", "Infrastructure is not simply construction. It is economic momentum, energy security, mobility and long-term transformation.", "workk.jpg")
        + footer()
    )


# ---------------------------------------------------------------- TAIN
def tain():
    return (
        head("Tain Hybrid Hydro-Solar Energy Project | Tabcon Energy", "A 70 MW hybrid hydro-solar and battery storage project in the Tain & Wenchi Districts, Bono Region, Ghana.")
        + header("projects.html")
        + page_hero("plant.jpg", "Project brief · Tabcon Energy Limited", "Tain <span class='text-lime'>Hybrid Hydro-Solar</span> Energy Project", "Tain &amp; Wenchi Districts · Bono Region · Ghana", "<a class='hover:text-lime' href='projects.html'>Projects</a> <span class='mx-2'>/</span> Tain")
        + dark_stats(stat(70, " MW", "Total installed capacity"), stat(55, " MW", "Solar PV"), stat(15, " MW", "Hydro + BESS"), pad="py-20")
        + f"""<section class="py-28 md:py-36"><div class="max-w-7xl mx-auto px-6 lg:px-8 grid lg:grid-cols-12 gap-16 items-center">
  <div class="lg:col-span-6"><div class="reveal">{eyebrow("Overview")}</div><h2 class="reveal font-display font-extrabold text-4xl md:text-6xl leading-[1] mt-6" style="--d:.1s">A flagship renewable energy initiative.</h2><p class="reveal mt-8 text-lg text-mute leading-relaxed" style="--d:.15s">The Tain Hybrid Hydro-Solar Energy Project is a large-scale initiative combining solar PV, hydropower and battery storage to provide reliable clean energy and regional development support.</p></div>
  <div class="lg:col-span-6 reveal-img overflow-hidden"><img class="w-full aspect-[4/3] object-cover" src="{IMG}PANEL.JPG" alt="Floating solar and hydropower reservoir" loading="lazy"></div>
</div></section>
<section class="py-28 bg-stone"><div class="max-w-7xl mx-auto px-6 lg:px-8">
  <div class="reveal">{eyebrow("Roadmap")}</div><h2 class="reveal font-display font-extrabold text-4xl md:text-6xl leading-[1] mt-6 mb-16" style="--d:.1s">Two-phase energy development plan.</h2>
  <div class="grid md:grid-cols-2 gap-6">
    <div class="reveal lift bg-white p-10 md:p-14 border-t-4 border-lime"><span class="font-display font-extrabold text-leaf tracking-widest">PHASE 1</span><h3 class="font-display font-extrabold text-3xl mt-3">Solar power development</h3><ul class="mt-8 space-y-4 text-lg text-mute"><li class="flex gap-3"><span class="material-symbols-outlined text-leaf">check_circle</span>55 MW utility-scale solar PV plant</li><li class="flex gap-3"><span class="material-symbols-outlined text-leaf">check_circle</span>Transmission infrastructure &amp; grid connection</li><li class="flex gap-3"><span class="material-symbols-outlined text-leaf">check_circle</span>Monitoring &amp; control systems</li></ul></div>
    <div class="reveal lift bg-ink text-white p-10 md:p-14 border-t-4 border-lime" style="--d:.12s"><span class="font-display font-extrabold text-lime tracking-widest">PHASE 2</span><h3 class="font-display font-extrabold text-3xl mt-3">Hybrid hydro-solar development</h3><ul class="mt-8 space-y-4 text-lg text-white/75"><li class="flex gap-3"><span class="material-symbols-outlined text-lime">check_circle</span>10 MW battery energy storage system</li><li class="flex gap-3"><span class="material-symbols-outlined text-lime">check_circle</span>5 MW hydroelectric plant on the River Tain</li><li class="flex gap-3"><span class="material-symbols-outlined text-lime">check_circle</span>Integrated solar + hydro dispatchability</li></ul></div>
  </div>
  <p class="reveal mt-10 text-lg text-mute max-w-4xl">70 MW total renewable generation capacity combining solar PV, hydropower and BESS storage, with complementary development in eco-tourism, watershed conservation, agricultural programmes and value-added processing.</p>
</div></section>
"""
        + cta("Partner with us", "Power the next era.", "Talk to Tabcon Energy about partnerships, financing and development on the Tain project.", "picture6.jpg")
        + footer()
    )


# ---------------------------------------------------------------- GALLERY
def gallery():
    items = [
        ("IMG_7634-300x200.jpg", "Solar Array", "Renewable Energy", "energy"),
        ("ghana-body.jpg", "Community Engagement", "Stakeholder Session", "community"),
        ("WhatsApp-Image-2022-04-11-at-10.47.47-PM-637x424.jpeg", "Hydro Collaboration", "Energy Development", "energy"),
        ("plant.jpg", "Plant Overview", "Infrastructure Site", "infrastructure"),
        ("R.jPG", "Road Development", "Infrastructure", "infrastructure"),
        ("SOLARINST.jpg", "Solar Installation", "Clean Energy", "energy"),
        ("WORKERS.jpg", "Engineering Team", "Field Operations", "community"),
        ("ROADCONS.jpg", "Highway Construction", "Road Infrastructure", "infrastructure"),
        ("AREA.jpg", "Development Zone", "Project Area", "infrastructure"),
        ("TOPFLOOR.jpg", "Structural Works", "Engineering Development", "infrastructure"),
        ("PPP.JPG", "Project Planning", "Infrastructure Concept", "infrastructure"),
        ("PANEL.JPG", "Solar Panel Systems", "Renewable Technology", "energy"),
    ]
    figs = "".join(
        f"""<figure data-cat="{c}" data-title="{t}" data-label="{l}"><button type="button" class="zoom group relative block w-full overflow-hidden text-left" aria-label="Open {t}"><img class="w-full object-cover" src="{IMG}{im}" alt="{t}" loading="lazy"><span class="absolute inset-0 bg-gradient-to-t from-ink/85 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></span><span class="absolute inset-x-0 bottom-0 p-5 text-white translate-y-3 opacity-0 group-hover:translate-y-0 group-hover:opacity-100 transition-all"><span class="block text-[11px] uppercase tracking-widest text-lime font-bold">{l}</span><span class="block font-display font-extrabold text-xl">{t}</span></span></button></figure>"""
        for im, t, l, c in items
    )
    chips = "".join(
        '<button type="button" class="chip%s" data-filter="%s">%s</button>' % (" is-active" if v == "all" else "", v, n)
        for v, n in [("all", "All"), ("energy", "Energy"), ("infrastructure", "Infrastructure"), ("community", "People & community")]
    )
    return (
        head("Gallery | Tabcon Ghana", "Photos of Tabcon's engineering projects, renewable energy initiatives and field operations across Ghana.")
        + header("")
        + page_hero("oooo.jpg", "Gallery", "Inside the projects <span class='text-lime'>shaping Ghana.</span>", "A visual journey through our engineering concepts, renewable energy initiatives, infrastructure projects and field operations.", "Gallery", "min-h-[70svh]")
        + f"""<section class="py-20 md:py-28"><div class="max-w-7xl mx-auto px-6 lg:px-8">
  <div class="flex flex-wrap gap-3 mb-12" role="group" aria-label="Filter gallery">{chips}</div>
  <div id="gallery-grid" class="masonry">{figs}</div>
</div></section>
<dialog id="lightbox" class="w-screen h-screen">
  <div class="w-full h-full flex flex-col items-center justify-center p-4 md:p-10 relative">
    <button id="lb-close" class="absolute top-5 right-5 w-12 h-12 grid place-items-center text-white bg-white/10 hover:bg-white/20 rounded-full" aria-label="Close"><span class="material-symbols-outlined">close</span></button>
    <button id="lb-prev" class="absolute left-3 md:left-8 top-1/2 -translate-y-1/2 w-12 h-12 grid place-items-center text-white bg-white/10 hover:bg-white/20 rounded-full" aria-label="Previous"><span class="material-symbols-outlined">chevron_left</span></button>
    <button id="lb-next" class="absolute right-3 md:right-8 top-1/2 -translate-y-1/2 w-12 h-12 grid place-items-center text-white bg-white/10 hover:bg-white/20 rounded-full" aria-label="Next"><span class="material-symbols-outlined">chevron_right</span></button>
    <img id="lightbox-img" class="max-w-full max-h-[78vh] object-contain" alt="">
    <p id="lightbox-cap" class="mt-5 text-white font-display font-bold text-lg"></p>
  </div>
</dialog>
"""
        + cta("Build with Tabcon", "Infrastructure beyond concrete.", "Engineering vision, renewable innovation and development systems shaping Africa's next era of growth.", "JYT.jpg")
        + footer()
    )


# ---------------------------------------------------------------- NEWS
NEWS = [
    {"title": "Tabcon Energy and UENR Sign MoU for 65 MW Hybrid Power Plant", "date": "2022-04-11", "category": "MoU", "tags": ["UENR", "Tain Hybrid", "Partnerships"], "image": IMG + "WhatsApp-Image-2022-04-10-at-1.36.04-PM.jpeg",
     "excerpt": "A memorandum of understanding with the University of Energy and Natural Resources targets an $85 million, 65 MW hybrid hydro-solar facility in the Bono Region.",
     "body": "<p>Tabcon Energy Limited signed an MoU with the University of Energy and Natural Resources (UENR) to build a 65 MW hybrid hydro-solar renewable energy facility valued at $85 million. The project aims to strengthen electricity supply in the Bono Region, support irrigation-led agriculture, and drive industrial growth in the Tain and Wenchi districts.</p><p>UENR will serve as technical lead and academic partner, creating research and hands-on training opportunities for students. Source: UENR and Ghana News Online reports.</p>"},
    {"title": "Strategic MoUs & Government Endorsements", "date": "2025-08-18", "category": "MoU", "tags": ["Partnerships", "Voith", "Tain"], "image": IMG + "WhatsApp-Image-2022-04-11-at-10.47.47-PM-637x424.jpeg",
     "excerpt": "A cooperation track with Voith (Germany) and support highlights from leadership visits, advancing bankable execution for Tain and future assets.",
     "body": "<p>Tabcon Ghana has initiated a cooperation track with Voith in Germany, focusing on hybrid hydro–solar optimisation, long-lead equipment pathways and knowledge transfer supporting the Tain Hybrid Project. Leadership engagements reinforced the national priority for reliable, clean baseload.</p>"},
    {"title": "Tain Project Milestones", "date": "2025-07-12", "category": "Project", "tags": ["Tain Hybrid", "BESS"], "image": IMG + "IMG_7634-300x200.jpg",
     "excerpt": "Stage 1: 55 MW Solar PV + 6 MW BESS progressing through development gates. Stage 2 plans a 10 MW hydro-solar expansion.",
     "body": "<p>Stage 1 delivers PV generation with battery storage to stabilise the grid. Stage 2 explores hydro-solar synergy to expand output and support local industry while minimising curtailment and improving resilience.</p>"},
    {"title": "Community Engagement in Tain & Wenchi", "date": "2025-06-03", "category": "Community", "tags": ["Engagement", "E&S"], "image": IMG + "ghana-body.jpg",
     "excerpt": "Ongoing consultations align environmental safeguards, local jobs and community benefits across deployment phases.",
     "body": "<p>Our team held stakeholder sessions with district leadership and community representatives to align environmental &amp; social measures, skills programmes and local job pathways prior to early works.</p>"},
]


def news():
    chips = "".join(
        '<button type="button" class="chip%s" data-news-cat="%s">%s</button>' % (" is-active" if c == "All" else "", c, c)
        for c in ["All", "MoU", "Project", "Community"]
    )
    data = json.dumps(NEWS, ensure_ascii=False).replace("</", "<\\/")
    return (
        head("News & Updates | Tabcon Ghana", "Milestones, MoUs and community engagement from Tabcon Ghana and Tabcon Energy Limited.")
        + header("news.html")
        + page_hero("newpic2.jpg", "News & updates", "Milestones on the road to <span class='text-lime'>clean energy.</span>", "MoUs, project progress and community engagement from Tabcon Ghana.", "News", "min-h-[70svh]")
        + f"""<section class="py-20 md:py-28"><div class="max-w-7xl mx-auto px-6 lg:px-8">
  <div class="flex flex-col md:flex-row gap-6 md:items-center justify-between mb-12">
    <div class="flex flex-wrap gap-3" role="group" aria-label="Filter news">{chips}</div>
    <label class="relative block md:w-80"><span class="sr-only">Search news</span><span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-mute">search</span><input id="news-search" type="search" placeholder="Search news" class="field !pl-12"></label>
  </div>
  <div id="news-grid" class="grid md:grid-cols-2 lg:grid-cols-3 gap-6"></div>
  <p id="news-empty" class="text-center text-mute py-16 text-lg" hidden>No stories match your search.</p>
  <div class="text-center mt-12"><button id="news-more" class="btn btn-dark" hidden>Load more</button></div>
</div></section>
<dialog id="news-dialog" class="w-[min(46rem,94vw)] m-auto bg-paper max-h-[92vh] overflow-auto">
  <img id="nd-img" class="w-full aspect-[16/9] object-cover" alt="">
  <button id="nd-close" class="absolute top-4 right-4 w-11 h-11 grid place-items-center bg-ink text-white rounded-full" aria-label="Close"><span class="material-symbols-outlined">close</span></button>
  <div class="p-8 md:p-12"><p id="nd-cat" class="text-xs font-bold uppercase tracking-widest text-brand"></p><h2 id="nd-title" class="font-display font-extrabold text-3xl md:text-4xl mt-3 leading-tight"></h2><div id="nd-body" class="mt-6 text-lg text-mute leading-relaxed space-y-4"></div><a href="contact.html" class="btn btn-green mt-8">Talk to our team <span class="material-symbols-outlined">arrow_forward</span></a></div>
</dialog>
<script id="news-data" type="application/json">{data}</script>
"""
        + footer()
    )


# ---------------------------------------------------------------- PARTNERS
def partners():
    tiles = "".join(
        f'<div class="reveal logo-tile h-40 bg-white grid place-items-center p-8 lift"><img class="max-h-full max-w-full object-contain" src="{PARTNERS}{f}" alt="{n}" loading="lazy"></div>'
        for f, n in PARTNER_FILES
    )
    return (
        head("Partners | Tabcon Ghana", "Tabcon collaborates with technology providers, EPCs, lenders and public agencies to deliver bankable infrastructure.")
        + header("partners.html")
        + page_hero("WhatsApp-Image-2022-04-11-at-10.47.47-PM-637x424.jpeg", "Partners", "Better built <span class='text-lime'>together.</span>", "We collaborate with technology providers, EPCs, lenders and public agencies to deliver bankable infrastructure, combining local execution with global standards.", "Partners", "min-h-[70svh]")
        + f"""<section class="py-24 md:py-32"><div class="max-w-7xl mx-auto px-6 lg:px-8"><div class="reveal mb-12">{eyebrow("Our network")}</div><div class="grid grid-cols-2 md:grid-cols-3 gap-5">{tiles}</div></div></section>
"""
        + cta("Collaborate", "Become a Tabcon partner.", "Technology providers, lenders and agencies: let's deliver bankable infrastructure together.", "IMG_7634-300x200.jpg")
        + footer()
    )


# ---------------------------------------------------------------- CONTACT
def contact():
    topics = ["Engineering & infrastructure", "Renewable energy", "Project development", "Advisory & policy", "Partnership", "Other"]
    opts = "".join(f"<option>{t.replace('&', '&amp;')}</option>" for t in topics)

    def row(icon, label, body):
        return f"""<div class="flex gap-5"><span class="w-12 h-12 shrink-0 grid place-items-center bg-lime text-ink rounded-sm"><span class="material-symbols-outlined">{icon}</span></span><div><p class="text-xs uppercase tracking-widest font-bold text-white/50">{label}</p><p class="mt-1 text-lg">{body}</p></div></div>"""

    phones = f'<a class="hover:text-lime" href="tel:{PHONE_MAIN[1]}">{PHONE_MAIN[0]}</a><br><a class="hover:text-lime" href="tel:{PHONE_OFFICE[1]}">{PHONE_OFFICE[0]}</a>'
    emails = f'<a class="hover:text-lime" href="mailto:{EMAIL_MAIN}">{EMAIL_MAIN}</a><br><a class="hover:text-lime" href="mailto:{EMAIL_OFFICE}">{EMAIL_OFFICE}</a>'
    return (
        head("Contact | Tabcon Ghana", "Contact Tabcon Ghana about infrastructure, renewable energy, engineering consultancy and strategic partnerships.")
        + header("contact.html")
        + page_hero("ghana-body.jpg", "Contact Tabcon", "Let's build the <span class='text-lime'>future together.</span>", "Reach out to discuss infrastructure development, renewable energy systems, engineering consultancy and strategic partnerships.", "Contact", "min-h-[70svh]")
        + f"""<section class="py-24 md:py-32"><div class="max-w-7xl mx-auto px-6 lg:px-8 grid lg:grid-cols-12 gap-10">
  <div class="lg:col-span-5 bg-ink text-white p-10 md:p-14 relative overflow-hidden"><div class="blueprint absolute inset-0"></div>
    <div class="relative"><div>{eyebrow("Contact information", "text-lime")}</div><h2 class="font-display font-extrabold text-4xl md:text-5xl leading-[1] mt-6">Start a conversation.</h2><p class="mt-6 text-white/70 leading-relaxed">Our team is ready to discuss engineering, infrastructure, renewable energy and project development opportunities across Africa.</p>
    <div class="mt-12 space-y-8">
      {row("call", "Phone", phones)}
      {row("mail", "Email", emails)}
      {row("location_on", "Head office", "Accra, Greater Accra Region, Ghana")}
    </div></div>
  </div>
  <div class="lg:col-span-7 bg-white p-8 md:p-14 shadow-sm">
    <h2 class="font-display font-extrabold text-3xl md:text-4xl">Send a message</h2>
    <form id="contact-form" class="mt-8 grid gap-5 md:grid-cols-2" data-to="{EMAIL_MAIN}" novalidate>
      <label class="block"><span class="text-sm font-semibold">Full name</span><input class="field mt-2" name="name" type="text" required autocomplete="name"></label>
      <label class="block"><span class="text-sm font-semibold">Email</span><input class="field mt-2" name="email" type="email" required autocomplete="email"></label>
      <label class="block"><span class="text-sm font-semibold">Phone <span class="font-normal text-mute">(optional)</span></span><input class="field mt-2" name="phone" type="tel" autocomplete="tel"></label>
      <label class="block"><span class="text-sm font-semibold">I'm interested in</span><select class="field mt-2" name="topic">{opts}</select></label>
      <label class="block md:col-span-2"><span class="text-sm font-semibold">Message</span><textarea class="field mt-2" name="message" rows="6" required></textarea></label>
      <div class="md:col-span-2"><button class="btn btn-green" type="submit">Send message <span class="material-symbols-outlined">send</span></button><p id="form-status" class="mt-5 text-leaf font-semibold" role="status" hidden></p></div>
    </form>
  </div>
</div></section>
<section class="relative bg-ink text-white overflow-hidden"><img class="absolute inset-0 w-full h-full object-cover opacity-40" src="{IMG}newpic7.jpg" alt="" loading="lazy"><div class="absolute inset-0 bg-gradient-to-r from-ink via-ink/70 to-transparent"></div>
  <div class="relative max-w-7xl mx-auto px-6 lg:px-8 py-28"><div class="reveal">{eyebrow("Headquarters", "text-lime")}</div><h2 class="reveal font-display font-extrabold text-5xl md:text-7xl mt-6 leading-[.95]">Tabcon Ghana</h2><p class="reveal mt-6 max-w-xl text-white/75 text-lg">Engineering development consultants focused on infrastructure, renewable energy and strategic project delivery across Africa.</p></div></section>
"""
        + footer()
    )


if __name__ == "__main__":
    pages = {
        "index.html": home, "about_us.html": about, "services.html": services, "projects.html": projects,
        "track-record.html": track, "tain-project.html": tain, "gallery.html": gallery, "news.html": news,
        "partners.html": partners, "contact.html": contact,
    }
    for name, fn in pages.items():
        write(name, fn())
        print("wrote", name)
