"""Writes ../README.md. Every image is a <picture> with a dark and a light source."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))

def pic(name, alt, width='100%'):
    return (f'<picture>'
            f'<source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">'
            f'<source media="(prefers-color-scheme: light)" srcset="assets/{name}-light.svg">'
            f'<img alt="{alt}" src="assets/{name}-light.svg" width="{width}">'
            f'</picture>')

def link(url, inner):
    return f'<a href="{url}">{inner}</a>'

GAP = '<br><br>'

parts = [
    '<!-- Profile README for github.com/yveskwameh. Images are built by src/build.py, in a dark and a light version each. -->',
    '',
    link('https://yveskwameh.com', pic('hero', 'Yves Kwameh, design engineer. I design interfaces and build them, so the thing that ships is the thing that was designed.')),
    '',
    '<p align="center">',
    '  <a href="https://yveskwameh.com">yveskwameh.com</a>&nbsp;&nbsp;·&nbsp;&nbsp;',
    '  <a href="https://www.linkedin.com/in/yveskwameh/">LinkedIn</a>&nbsp;&nbsp;·&nbsp;&nbsp;',
    '  <a href="https://x.com/yveskwameh">X</a>&nbsp;&nbsp;·&nbsp;&nbsp;',
    '  <a href="mailto:hello@yveskwameh.com">hello@yveskwameh.com</a>',
    '</p>',
    '',
    '<p align="center">Design engineer. I design interfaces in Figma and build them in Webflow, Framer, Astro, React and React Native.<br>Open to full-time design engineer roles.</p>',
    '',
    GAP,
    '',
    pic('statement', 'Clients hire me to design and build Webflow and Framer sites. My own products pushed me further: a multiplayer game on Cloudflare\'s edge, a budgeting app built for web, iOS and Android, and a portfolio that runs like an operating system.'),
    '',
    GAP,
    '',
    pic('h-products', 'Selected products'),
    '',
    '<p>',
    '  ' + link('https://daraxando.yveskwameh.com', pic('card-daraxando', 'Dara X&amp;O, online tic tac toe for Nigerian players. Live.', '49%')),
    '  ' + link('https://pennivault.xyz', pic('card-pennivault', 'pennivault, monthly budgeting with no bank login. Live on the web.', '49%')),
    '</p>',
    '',
    link('https://github.com/yveskwameh/daraxando', pic('spec-daraxando', 'Dara X&amp;O stack: React 19, Vite 8 and TypeScript on Cloudflare Workers, one Durable Object per match, D1 for players and ranks. Runs at zero cost up to about 300,000 games a month.')),
    '',
    GAP,
    '',
    link('https://pennivault.xyz', pic('spec-pennivault', 'pennivault stack: Expo and React Native for web, iOS and Android, an Express API on MongoDB Atlas and AWS, and an AI agent that turns bank alert emails into entries.')),
    '',
    GAP,
    '',
    link('https://yveskwameh.com', pic('card-yvesos', 'YvesOS, my portfolio built as an operating system. Live at yveskwameh.com.')),
    '',
    link('https://github.com/yveskwameh/yveskwameh-2026', pic('spec-yvesos', 'YvesOS stack: Astro 7, plain TypeScript and CSS, Cloudflare Workers and Durable Objects for live cursors, 10,192 of 10,240 bytes of JavaScript.')),
    '',
    GAP,
    '',
    pic('chapters', 'How my stack grew, in six chapters: Figma; Webflow and Framer for client sites; Astro, TypeScript and Cloudflare for YvesOS; Expo, React Native and Next.js for pennivault; Workers, Durable Objects and D1 for Dara X&amp;O; and AI agents working from my specs.'),
    '',
    GAP,
    '',
    link('https://yveskwameh.com', pic('clients', 'Client work and results: The Car Guys, 43 form fields cut to 22; BOH Financial, a page for each audience; Scroll House Studio, the films play first; Altabrio, shipped on its launch date; Tem\'s, booking in 3 short screens. Top Rated on Upwork, 100% Job Success, 30+ jobs delivered.')),
    '',
    GAP,
    '',
    pic('process', 'How I work: understand the business, structure the UX, design in Figma, choose the stack, build and ship.'),
    '',
    GAP,
    '',
    link('mailto:hello@yveskwameh.com', pic('footer', 'Email hello@yveskwameh.com')),
    '',
    '<p align="center">',
    '  <a href="https://yveskwameh.com">yveskwameh.com</a>&nbsp;&nbsp;·&nbsp;&nbsp;',
    '  <a href="https://www.linkedin.com/in/yveskwameh/">LinkedIn</a>&nbsp;&nbsp;·&nbsp;&nbsp;',
    '  <a href="https://x.com/yveskwameh">X</a>&nbsp;&nbsp;·&nbsp;&nbsp;',
    '  <a href="https://www.instagram.com/yveskwameh/">Instagram</a>',
    '</p>',
    '',
]

with open(os.path.join(HERE, '..', 'README.md'), 'w') as f:
    f.write('\n'.join(parts))
print('ok')
