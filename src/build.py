"""Builds every image in ../assets, in a dark and a light version.

GitHub strips CSS from READMEs, so the design lives in SVGs loaded through <img>.
Space Mono is embedded as base64 so the type matches yveskwameh.com, and screenshots
are embedded the same way so each SVG is one self-contained file.
"""
import base64, os
from xml.sax.saxutils import escape as esc

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'assets')
FONTS = os.path.join(HERE, 'fonts')

def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

F400 = b64(f'{FONTS}/space-mono-400.woff2')
F700 = b64(f'{FONTS}/space-mono-700.woff2')

def img(name):
    ext = name.rsplit('.', 1)[1]
    mime = 'image/png' if ext == 'png' else 'image/jpeg'
    return f'data:{mime};base64,{b64(os.path.join(HERE, name))}'

THEMES = {
    'dark': dict(bg='#1b1b20', bg2='#232329', bar='#26262d', ink='#f2f2ef', muted='#8f8f97',
                 line='#34343c', accent='#3cc2b0', onaccent='#0c0c0e', chip='#2a2a31',
                 shadow='0.55'),
    'light': dict(bg='#f6f6f3', bg2='#ecece8', bar='#e6e6e3', ink='#16161a', muted='#64646a',
                  line='#d6d6d1', accent='#077167', onaccent='#ffffff', chip='#ffffff',
                  shadow='0.18'),
}

CW = 0.612  # Space Mono advance width, in em

def style(t):
    return f'''<style>
@font-face{{font-family:'SM';font-weight:400;src:url(data:font/woff2;base64,{F400}) format('woff2')}}
@font-face{{font-family:'SM';font-weight:700;src:url(data:font/woff2;base64,{F700}) format('woff2')}}
text{{font-family:'SM',ui-monospace,'SF Mono',Menlo,Consolas,monospace;fill:{t['ink']}}}
.m{{fill:{t['muted']}}} .a{{fill:{t['accent']}}} .b{{font-weight:700}}
.caret{{animation:blink 1.1s steps(1) infinite}}
.pulse{{animation:pulse 2.2s ease-out infinite;transform-box:fill-box;transform-origin:center}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes pulse{{0%{{opacity:.6;transform:scale(1)}}100%{{opacity:0;transform:scale(2.6)}}}}
@media (prefers-reduced-motion:reduce){{.caret,.pulse{{animation:none}}}}
</style>'''

def svg(w, h, t, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
            f'{style(t)}<defs><filter id="sh" x="-20%" y="-20%" width="140%" height="160%">'
            f'<feDropShadow dx="0" dy="8" stdDeviation="11" flood-color="#000" flood-opacity="{t["shadow"]}"/></filter></defs>'
            f'{body}</svg>')

def wrap(s, size, width):
    n = int(width / (CW * size))
    words, lines, cur = s.split(), [], ''
    for wd in words:
        if len(cur) + len(wd) + (1 if cur else 0) > n:
            lines.append(cur); cur = wd
        else:
            cur = f'{cur} {wd}' if cur else wd
    if cur: lines.append(cur)
    return lines

def para(x, y, s, size, width, lh, cls='', weight=''):
    out = []
    for i, ln in enumerate(wrap(s, size, width)):
        out.append(f'<text x="{x}" y="{y + i*lh}" font-size="{size}" class="{cls}" {weight}>{esc(ln)}</text>')
    return ''.join(out), len(wrap(s, size, width))

def window(x, y, w, h, t, title, r=16):
    """A YvesOS window: frame, title bar, traffic lights."""
    return (f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{t["bg"]}" stroke="{t["line"]}"/></g>'
            f'<path d="M{x} {y+r} a{r} {r} 0 0 1 {r} -{r} h{w-2*r} a{r} {r} 0 0 1 {r} {r} v{44-r} h-{w} z" fill="{t["bar"]}"/>'
            f'<line x1="{x}" y1="{y+44}" x2="{x+w}" y2="{y+44}" stroke="{t["line"]}"/>'
            f'<circle cx="{x+24}" cy="{y+22}" r="6.5" fill="#ff5f57"/><circle cx="{x+46}" cy="{y+22}" r="6.5" fill="#febc2e"/>'
            f'<circle cx="{x+68}" cy="{y+22}" r="6.5" fill="#28c840"/>'
            f'<text x="{x+w/2}" y="{y+27}" font-size="14" class="m" text-anchor="middle">{esc(title)}</text>')

def write(name, w, h, fn, label):
    for mode, t in THEMES.items():
        with open(os.path.join(OUT, f'{name}-{mode}.svg'), 'w') as f:
            f.write(svg(w, h, t, fn(t), label))

# ---------------------------------------------------------------- hero
def hero(t):
    W, H = 1200, 660
    g = window(12, 2, W-24, H-44, t, 'about-yves.txt')
    g += f'<text x="600" y="120" font-size="17" class="a b" text-anchor="middle" letter-spacing="3">YVES KWAMEH  //  DESIGN ENGINEER</text>'
    g += f'<text x="600" y="282" font-size="150" class="b" text-anchor="middle" letter-spacing="-6">YVES</text>'
    g += f'<text x="600" y="420" font-size="150" text-anchor="middle" letter-spacing="-8">Kwameh</text>'
    g += f'<text x="600" y="484" font-size="26" class="m" text-anchor="middle">I design interfaces and build them, so the thing</text>'
    g += f'<text x="600" y="522" font-size="26" class="m" text-anchor="middle">that ships is the thing that was designed.</text>'
    g += f'<rect class="caret" x="942" y="500" width="14" height="28" fill="{t["accent"]}"/>'
    # status pill
    pw = 446
    px = 600 - pw/2
    g += f'<rect x="{px}" y="552" width="{pw}" height="40" rx="20" fill="{t["chip"]}" stroke="{t["line"]}"/>'
    g += f'<circle class="pulse" cx="{px+24}" cy="572" r="6" fill="{t["accent"]}"/><circle cx="{px+24}" cy="572" r="6" fill="{t["accent"]}"/>'
    g += f'<text x="{px+44}" y="578" font-size="16" letter-spacing="1">OPEN TO DESIGN ENGINEER ROLES</text>'
    return g

# ---------------------------------------------------------------- statement
STMT = "Clients hire me to design and build Webflow and Framer sites. My own products pushed me further: a multiplayer game on Cloudflare's edge, a budgeting app built for web, iOS and Android, and a portfolio that runs like an operating system."
COLS = [
    ('DESIGN TO CODE', "I design in Figma, then build what was approved. One person on both ends, so nothing gets lost in the handoff."),
    ('STACK BY RESEARCH', "Before any code, I compare the options and write down why, costs included. Every stack here was picked for how the product is actually used."),
    ('AI AGENTS, MY SPECS', "I write the specs, the design system and the rules. AI agents build against them, and I review every change before it ships."),
]
def statement(t):
    g, n = para(0, 46, STMT, 33, 1190, 48)
    y = 46 + n*48 + 40
    g += f'<line x1="0" y1="{y}" x2="1200" y2="{y}" stroke="{t["line"]}"/>'
    for i, (lab, body) in enumerate(COLS):
        x = i * 410
        g += f'<text x="{x}" y="{y+44}" font-size="15" class="a b" letter-spacing="2">{esc(lab)}</text>'
        p, _ = para(x, y+84, body, 19, 380, 30, 'm')
        g += p
    return g

# ---------------------------------------------------------------- section header
def header(kicker, title, count, right):
    def fn(t):
        g = f'<text x="0" y="22" font-size="16" class="m">{esc(kicker)}</text>'
        g += f'<text x="0" y="82" font-size="46" class="b" letter-spacing="-2">{esc(title)}</text>'
        tw = len(title) * CW * 46 - 2*len(title)
        g += f'<text x="{tw+8}" y="52" font-size="18" class="a b">{esc(count)}</text>'
        g += f'<text x="1200" y="82" font-size="17" class="m" text-anchor="end">{esc(right)}</text>'
        g += f'<line x1="0" y1="112" x2="1200" y2="112" stroke="{t["line"]}"/>'
        return g
    return fn

# ---------------------------------------------------------------- product cards
def card(shot, sw, sh, well, title, sub, tags, w=590, h=740, shot_h=500, desk=False):
    def fn(t):
        g = f'<g filter="url(#sh)"><rect x="2" y="2" width="{w-4}" height="{h-42}" rx="16" fill="{t["bg"]}" stroke="{t["line"]}"/></g>'
        g += f'<clipPath id="well"><path d="M2 18 a16 16 0 0 1 16 -16 h{w-36} a16 16 0 0 1 16 16 v{shot_h+20} h-{w-4} z"/></clipPath>'
        g += f'<rect x="2" y="2" width="{w-4}" height="{shot_h+36}" fill="{well}" clip-path="url(#well)"/>'
        # dot grid on the well
        g += f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="#ffffff" opacity=".10"/></pattern>'
        g += f'<rect x="2" y="2" width="{w-4}" height="{shot_h+36}" fill="url(#dots)" clip-path="url(#well)"/>'
        if desk:
            iw = 900; ih = iw*sh/sw
            ix = (w-iw)/2; iy = 34
        else:
            iw = 340; ih = iw*sh/sw
            ix = (w-iw)/2; iy = 2 + (shot_h+36-ih)/2
        r = 10 if desk else 26
        g += f'<clipPath id="shot"><rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="{r}"/></clipPath>'
        g += f'<g filter="url(#sh)"><rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="{r}" fill="#000"/></g>'
        g += f'<image x="{ix}" y="{iy}" width="{iw}" height="{ih}" href="{img(shot)}" clip-path="url(#shot)" preserveAspectRatio="xMidYMin slice"/>'
        g += f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="{r}" fill="none" stroke="#ffffff" stroke-opacity=".18"/>'
        g += f'<line x1="2" y1="{shot_h+38}" x2="{w-2}" y2="{shot_h+38}" stroke="{t["line"]}"/>'
        ty = shot_h + 86
        g += f'<text x="32" y="{ty}" font-size="34" class="b" letter-spacing="-1">{esc(title)}</text>'
        g += f'<text x="{w-32}" y="{ty}" font-size="28" class="a b" text-anchor="end">↗</text>'
        g += f'<text x="32" y="{ty+34}" font-size="19" class="m">{esc(sub)}</text>'
        x = 32
        for i, tg in enumerate(tags):
            tw = len(tg)*(CW*14 + 1) + (42 if i == 0 else 28)
            g += f'<rect x="{x}" y="{ty+56}" width="{tw}" height="32" rx="16" fill="{t["chip"]}" stroke="{t["line"]}"/>'
            if i == 0:
                g += f'<circle cx="{x+16}" cy="{ty+72}" r="4.5" fill="{t["accent"]}"/>'
                g += f'<text x="{x+30}" y="{ty+77}" font-size="14" letter-spacing="1">{esc(tg)}</text>'
            else:
                g += f'<text x="{x+14}" y="{ty+77}" font-size="14" class="m" letter-spacing="1">{esc(tg)}</text>'
            x += tw + 8
        return g
    return fn

# ---------------------------------------------------------------- spec panels (story + stack.txt)
def spec(kicker, title, body, rows):
    def fn(t):
        g = f'<text x="0" y="40" font-size="15" class="a b" letter-spacing="2">{esc(kicker)}</text>'
        p, n = para(0, 88, title, 30, 470, 40, 'b')
        g += p
        y = 88 + (n-1)*40 + 48
        p, n2 = para(0, y, body, 19, 470, 31, 'm')
        g += p
        # terminal, dark in both themes
        x0, y0, w, h = 512, 2, 674, 80 + len(rows)*40 + 24
        g += f'<g filter="url(#sh)"><rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="14" fill="#0f0f13" stroke="#2c2c34"/></g>'
        g += f'<path d="M{x0} {y0+14} a14 14 0 0 1 14 -14 h{w-28} a14 14 0 0 1 14 14 v26 h-{w} z" fill="#18181e"/>'
        g += f'<line x1="{x0}" y1="{y0+40}" x2="{x0+w}" y2="{y0+40}" stroke="#2c2c34"/>'
        for i, c in enumerate(['#ff5f57', '#febc2e', '#28c840']):
            g += f'<circle cx="{x0+22+i*20}" cy="{y0+20}" r="6" fill="{c}"/>'
        g += f'<text x="{x0+w/2}" y="{y0+26}" font-size="15" text-anchor="middle" style="fill:#8f8f97">stack.txt</text>'
        g += f'<text x="{x0+26}" y="{y0+80}" font-size="18" style="fill:#6c6c74">$ cat stack.txt</text>'
        for i, (k, v) in enumerate(rows):
            yy = y0 + 80 + (i+1)*40
            g += f'<text x="{x0+26}" y="{yy}" font-size="18" style="fill:#3cc2b0">{esc(k)}</text>'
            g += f'<text x="{x0+196}" y="{yy}" font-size="18" style="fill:#e9e9e6">{esc(v)}</text>'
        return g
    return fn

def spec_h(title, body, rows):
    n = len(wrap(title, 30, 470)); n2 = len(wrap(body, 19, 470))
    left = 88 + (n-1)*40 + 48 + (n2-1)*31 + 24
    right = 2 + 80 + len(rows)*40 + 24 + 46
    return int(max(left, right))

# ---------------------------------------------------------------- chapters (stack timeline)
CHAPTERS = [
    ('01', 'Figma', 'Where every project starts'),
    ('02', 'Webflow · Framer', 'Client sites'),
    ('03', 'Astro · TypeScript · Cloudflare', 'YvesOS'),
    ('04', 'Expo · React Native · Next.js', 'pennivault'),
    ('05', 'Workers · Durable Objects · D1', 'Dara X&O'),
    ('06', 'AI agents on my specs', 'How all of it ships'),
]
def chapters(t):
    g = f'<text x="0" y="22" font-size="16" class="m">stack.history</text>'
    g += f'<text x="0" y="86" font-size="46" class="b" letter-spacing="-2">Each product needed something</text>'
    g += f'<text x="0" y="142" font-size="46" letter-spacing="-2">the last tool couldn’t do.</text>'
    # Büro-style line with a dot
    g += f'<line x1="0" y1="196" x2="1200" y2="196" stroke="{t["ink"]}" stroke-opacity=".5"/>'
    g += f'<circle cx="1196" cy="196" r="5" fill="{t["ink"]}"/>'
    g += f'<text x="0" y="248" font-size="17" class="m">(06) Chapters</text>'
    y = 236
    for num, stack, what in CHAPTERS:
        g += f'<line x1="360" y1="{y-22}" x2="1200" y2="{y-22}" stroke="{t["line"]}"/>' if num != '01' else ''
        g += f'<text x="360" y="{y+12}" font-size="17" class="a b">{num}</text>'
        g += f'<text x="414" y="{y+12}" font-size="22">{esc(stack)}</text>'
        g += f'<text x="1200" y="{y+12}" font-size="18" class="m" text-anchor="end">{esc(what)}</text>'
        y += 56
    g += f'<line x1="360" y1="{y-22}" x2="1200" y2="{y-22}" stroke="{t["line"]}"/>'
    return g

# ---------------------------------------------------------------- client index
CLIENTS = [
    ('The Car Guys', '43 form fields cut to 22', 'Figma, Webflow'),
    ('BOH Financial', 'A page for each audience', 'Figma, Webflow'),
    ('Scroll House Studio', 'The films play first', 'Figma, Webflow'),
    ('Altabrio', 'Shipped on its launch date', 'Figma'),
    ("Tem's", 'Booking in 3 short screens', 'Figma'),
]
def clients(t):
    g = f'<text x="0" y="22" font-size="16" class="m">clients.index</text>'
    g += f'<text x="0" y="82" font-size="46" class="b" letter-spacing="-2">Client work</text>'
    g += f'<text x="{11*CW*46-22+8}" y="52" font-size="18" class="a b">{len(CLIENTS):02d}</text>'
    p, _ = para(560, 54, "Sites and products I designed and built for clients, through Minerva Creative Co. and Upwork. Full case studies are on yveskwameh.com.", 18, 640, 28, 'm')
    g += p
    y = 160
    g += f'<text x="0" y="{y}" font-size="15" class="m" letter-spacing="2">CLIENT</text>'
    g += f'<text x="560" y="{y}" font-size="15" class="m" letter-spacing="2">RESULT</text>'
    g += f'<text x="900" y="{y}" font-size="15" class="m" letter-spacing="2">BUILT WITH</text>'
    y += 22
    for name, ind, built in CLIENTS:
        g += f'<line x1="0" y1="{y}" x2="1200" y2="{y}" stroke="{t["line"]}"/>'
        g += f'<text x="0" y="{y+37}" font-size="23">{esc(name)}</text>'
        g += f'<text x="560" y="{y+37}" font-size="19" class="m">{esc(ind)}</text>'
        g += f'<text x="900" y="{y+37}" font-size="19" class="m">{esc(built)}</text>'
        y += 56
    g += f'<line x1="0" y1="{y}" x2="1200" y2="{y}" stroke="{t["line"]}"/>'
    g += f'<text x="0" y="{y+46}" font-size="16" class="a b" letter-spacing="1">TOP RATED ON UPWORK  ·  100% JOB SUCCESS  ·  30+ JOBS DELIVERED</text>'
    return g

# ---------------------------------------------------------------- process
STEPS = [
    ('Understand the business', 'What has to happen for this to be worth building.'),
    ('Structure the UX', 'Flows and wireframes in grey, before any colour.'),
    ('Design in Figma', 'Every state drawn: empty, loading, error, too long.'),
    ('Choose the stack', 'Options researched and written down, costs included.'),
    ('Build and ship', 'What was approved is what goes live.'),
]
def process(t):
    g = f'<rect x="0" y="0" width="150" height="34" rx="9" fill="{t["chip"]}" stroke="{t["line"]}"/>'
    g += f'<text x="75" y="23" font-size="16" text-anchor="middle">process.md</text>'
    g += f'<text x="0" y="96" font-size="46" class="b" letter-spacing="-2">How I work</text>'
    p, _ = para(0, 140, "The same five steps for a landing page, a client site or a product of my own.", 19, 380, 31, 'm')
    g += p
    y = 2
    for i, (title, line) in enumerate(STEPS):
        g += f'<line x1="480" y1="{y}" x2="1200" y2="{y}" stroke="{t["line"]}"/>' if i else ''
        g += f'<text x="480" y="{y+42}" font-size="25">{esc(title)}</text>'
        g += f'<text x="1200" y="{y+42}" font-size="17" class="a b" text-anchor="end">{i+1:02d}</text>'
        g += f'<text x="480" y="{y+76}" font-size="18" class="m">{esc(line)}</text>'
        y += 104
    return g

# ---------------------------------------------------------------- footer
def footer(t):
    g = f'<text x="600" y="40" font-size="20" class="m" text-anchor="middle">Hiring a design engineer, or need one for a project?</text>'
    w = 560; x = 600 - w/2
    g += f'<rect x="{x}" y="72" width="{w}" height="76" rx="38" fill="{t["accent"]}"/>'
    g += f'<text x="600" y="120" font-size="26" class="b" text-anchor="middle" style="fill:{t["onaccent"]}">hello@yveskwameh.com ↘</text>'
    return g

def _stmt_h():
    n = len(wrap(STMT, 33, 1190)); y = 46 + n*48 + 40
    cols = max(len(wrap(b, 19, 380)) for b in [c[1] for c in COLS])
    return int(y + 84 + (cols-1)*30 + 24)

if __name__ == '__main__':
    STATEMENT_H = _stmt_h()
    os.makedirs(OUT, exist_ok=True)
    write('hero', 1200, 660, hero, 'Yves Kwameh, design engineer. I design interfaces and build them, so the thing that ships is the thing that was designed. Open to design engineer roles.')
    write('statement', 1200, STATEMENT_H, statement, 'Clients hire me to design and build Webflow and Framer sites. My own products pushed me further: a multiplayer game, a budgeting app and a portfolio that runs like an operating system.')
    write('h-products', 1200, 120, header('work.folder', 'Selected products', '03', 'Built, shipped and live'), 'Selected products')
    write("card-daraxando", 590, 740, card('dara.jpg', 406, 540, '#120c33', 'Dara X&O', 'Online tic tac toe for Nigerian players', ['LIVE', 'GAME', 'REALTIME']), 'Dara X&O, online tic tac toe for Nigerian players. Live.')
    write("card-pennivault", 590, 740, card('penni.jpg', 406, 540, '#dfeee4', 'pennivault', 'Monthly budgeting, no bank login', ['LIVE ON WEB', 'FINANCE', 'iOS · ANDROID']), 'pennivault, monthly budgeting. Live on the web.')
    write("card-yvesos", 1200, 860, card('yves-desktop-4.jpg', 1440, 900, '#2b3b48', 'YvesOS', 'My portfolio, built as an operating system', ['LIVE', 'PORTFOLIO', 'UNDER 10 KB OF JS'], w=1200, h=860, shot_h=600, desk=True), 'YvesOS, a portfolio built as an operating system. Live at yveskwameh.com.')

    D_ROWS = [('frontend', 'React 19, Vite 8, TypeScript'), ('realtime', 'one Durable Object per match'),
              ('matching', 'your state, your zone, then Nigeria'), ('data', 'Cloudflare D1'),
              ('sign-in', 'Google, or a code by email'), ('ships as', 'installable web app, push alerts'),
              ('first load', '~89 KB of JavaScript'), ('cost', '$0 up to ~300k games a month')]
    D_T = 'One tiny server for every match'
    D_B = "Before writing code I compared a VPS, Colyseus, Firebase, Ably, Vercel and Next.js. Tic tac toe is turn based, so each match runs on its own Durable Object that sleeps between moves. The bill counts the milliseconds a move takes, not the time players spend thinking, so the game runs on Cloudflare's free plan."
    write('spec-daraxando', 1200, spec_h(D_T, D_B, D_ROWS), spec('DARA X&O  ·  WHY THIS STACK', D_T, D_B, D_ROWS), 'Dara X&O stack: React, Vite, TypeScript, Cloudflare Workers, Durable Objects, D1. Runs at zero cost up to about 300,000 games a month.')

    P_ROWS = [('app', 'Expo SDK 57, React Native'), ('platforms', 'web, iOS and Android, one codebase'),
              ('styling', 'NativeWind, tokens from Figma'), ('api', 'Express, TypeScript, JWT auth'),
              ('data', 'MongoDB Atlas'), ('hosting', 'AWS, CI/CD on GitHub Actions'),
              ('ai', 'agent turns bank alerts into entries'), ('design', '~100 screens, light and dark')]
    P_T = 'Rebuilt twice, for the right reasons'
    P_B = "It started on Next.js with Supabase. We rebuilt it in Expo so one codebase ships to web, iOS and Android, then moved to our own API on MongoDB Atlas and AWS to own auth, data and running costs. An AI agent reads bank alert emails and turns them into entries, so nobody types a transaction twice. The web app is live, and the store apps are next."
    write('spec-pennivault', 1200, spec_h(P_T, P_B, P_ROWS), spec('PENNIVAULT  ·  WHY THIS STACK', P_T, P_B, P_ROWS), 'pennivault stack: Expo and React Native, Express API, MongoDB Atlas, AWS, and an AI agent that reads bank alert emails.')

    Y_ROWS = [('framework', 'Astro 7, static, no UI framework'), ('code', 'plain TypeScript and CSS tokens'),
              ('hosting', 'Cloudflare Workers'), ('realtime', 'Durable Objects for live cursors'),
              ('js budget', '10,192 of 10,240 bytes'), ('deploy', 'a push to main')]
    Y_T = 'A portfolio with a weight limit'
    Y_B = "Instead of writing about how I think about interfaces, I built one. It opens on a lock screen, work opens in windows, and you can see everyone else's cursor. A script measures the JavaScript on every build against a 10 KB budget."
    write('spec-yvesos', 1200, spec_h(Y_T, Y_B, Y_ROWS), spec('YVESOS  ·  WHY THIS STACK', Y_T, Y_B, Y_ROWS), 'YvesOS stack: Astro, plain TypeScript, Cloudflare Workers and Durable Objects, under 10 KB of JavaScript.')

    write('chapters', 1200, 236 + 56*len(CHAPTERS) - 10, chapters, 'How my stack grew: Figma, then Webflow and Framer, then Astro and Cloudflare, then Expo and React Native, then Workers and Durable Objects, then AI agents working from my specs.')
    write('clients', 1200, 182 + 56*len(CLIENTS) + 60, clients, 'Client work: The Car Guys, BOH Financial, Scroll House Studio, Altabrio and Tem\'s. Top Rated on Upwork with 100% Job Success.')
    write('process', 1200, 104*len(STEPS) - 10, process, 'How I work: understand the business, structure the UX, design in Figma, choose the stack, build and ship.')
    write('footer', 1200, 160, footer, 'Email hello@yveskwameh.com')
    print('ok')
