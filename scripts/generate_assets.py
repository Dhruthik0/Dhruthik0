"""Generates every animated SVG used by README.md.

Run from the repo root:  python3 scripts/generate_assets.py
Needs network access once per run to fetch the tech icons from skillicons.dev.
"""
import random
import re
import textwrap
import urllib.request
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
TEXT, MUTED, DIM, LINE = "#e2e8f0", "#94a3b8", "#64748b", "#1e3a5f"
GREEN, BLUE, VIOLET, ROSE, AMBER, TEAL = "#34d399", "#38bdf8", "#a78bfa", "#fb7185", "#fbbf24", "#2dd4bf"


# ---------- shared pieces ----------

def frame(w, h, body, title, desc=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">
  <title id="t">{escape(title)}</title>
  <desc id="d">{escape(desc)}</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1220"/><stop offset="1" stop-color="#111a2e"/></linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#1c2840" stroke-width="1"/></pattern>
    <clipPath id="frame"><rect width="{w}" height="{h}" rx="16"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{w}" height="{h}" fill="url(#bg)"/>
    <rect width="{w}" height="{h}" fill="url(#grid)" opacity="0.6"/>
  </g>
{body}
</svg>
'''


def hide_until(t, attr="opacity"):
    # Hidden until t, then back to the base value; without SMIL the element simply shows.
    return f'<animate attributeName="{attr}" from="0" to="0" dur="{t:.2f}s"/>' if t > 0 else ""


def rise(t, dy=14, dur=0.5):
    # Fade in while sliding up into place.
    return (hide_until(t) +
            f'<animateTransform attributeName="transform" type="translate" values="0 {dy};0 0" dur="{dur}s" begin="{t:.2f}s" calcMode="spline" keyTimes="0;1" keySplines="0.2 0.8 0.3 1"/>'
            f'<animate attributeName="opacity" values="0;1" dur="{dur}s" begin="{t:.2f}s"/>')


def typed(text, start, cps=0.06):
    out = []
    for i, ch in enumerate(text):
        t = start + i * cps
        out.append(f'<tspan>{escape(ch)}<animate attributeName="fill-opacity" from="0" to="0" dur="{t:.2f}s"/></tspan>')
    return "".join(out), start + len(text) * cps


def blink(begin=0.0):
    return f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" begin="{begin:.2f}s" repeatCount="indefinite"/>'


def border_sweep(w, h, color, dur=6, begin=0.0):
    # A short bright segment that travels around the card edge forever.
    per = 2 * (w + h - 4)
    return (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="15" fill="none" stroke="{LINE}" stroke-width="1.5"/>'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="15" fill="none" stroke="{color}" stroke-width="2" '
            f'stroke-dasharray="{per*0.12:.0f} {per*0.88:.0f}" stroke-linecap="round">'
            f'<animate attributeName="stroke-dashoffset" values="0;{-per:.0f}" dur="{dur}s" begin="{-begin:.2f}s" repeatCount="indefinite"/></rect>')


def pulse_dot(cx, cy, color, begin=0.0):
    return (f'<circle cx="{cx}" cy="{cy}" r="4" fill="{color}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="4" fill="none" stroke="{color}" stroke-width="1.5">'
            f'<animate attributeName="r" values="4;12" dur="2s" begin="{-begin:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="stroke-opacity" values="0.8;0" dur="2s" begin="{-begin:.2f}s" repeatCount="indefinite"/></circle>')


def chips(items, x0, y, max_w, color, start, cw=6.6):
    # Stack labels as rounded chips that pop in one after another; wraps onto new rows.
    out, x, rows = [], x0, 1
    for i, label in enumerate(items):
        w = len(label) * cw + 18
        if x + w > x0 + max_w:
            x, y, rows = x0, y + 28, rows + 1
        out.append(
            f'<g opacity="1">{rise(start + i * 0.07, dy=6, dur=0.3)}'
            f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="22" rx="11" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-opacity="0.45"/>'
            f'<text x="{x + w/2:.1f}" y="{y + 15}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{TEXT}">{escape(label)}</text></g>')
        x += w + 8
    return "".join(out), rows


def write(name, svg):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg)


# ---------- banner ----------

def banner():
    W, H, X0 = 1200, 290, 64

    def dropped(text, y, start, gap=0.12, fall=0.45):
        out = []
        for i, ch in enumerate(text):
            t = start + i * gap
            out.append(
                f'<tspan y="{y}">{escape(ch)}'
                f'<animate attributeName="fill-opacity" from="0" to="0" dur="{t:.2f}s"/>'
                f'<animate attributeName="y" values="{y-50};{y+6};{y}" keyTimes="0;0.7;1" dur="{fall}s" begin="{t:.2f}s"/>'
                f'</tspan>')
        return "".join(out), start + (len(text) - 1) * gap + fall

    def prompt(y, body):
        return (f'<text x="{X0}" y="{y}"><tspan fill="{GREEN}">~/Dhruthik0</tspan>'
                f'<tspan fill="{DIM}"> $ </tspan><tspan fill="{TEXT}">{body}</tspan></text>')

    cmd1, t = typed("whoami", 0.6)
    name, t = dropped("Dhruthik", 150, t + 0.25)
    cmd2, t = typed("cat focus.txt", t + 0.4)
    loop_t = t + 0.3

    # Rotating tagline: type, hold, delete, next. Explicit x per char keeps the cursor aligned.
    phrases = [
        "turning Android phones into SMS & call gateways",
        "plugging browser tools into apps you already use",
        "serving ML models behind FastAPI endpoints",
        "wiring backends, dashboards and deploys together",
    ]
    TY, TS, TC = 238, 18, 10.8
    TX = X0 + 2 * TC
    TYPE, DEL, HOLD, GAP = 0.055, 0.025, 1.8, 0.4
    events, spans, s = [(0.0, 0)], [], 0.3
    for k, p in enumerate(phrases):
        n = len(p)
        for i, ch in enumerate(p):
            on = s + (i + 1) * TYPE
            off = s + n * TYPE + HOLD + (n - i) * DEL
            events += [(on, i + 1), (off, i)]
            if ch != " ":
                spans.append((k, i, ch, on, off))
        s += n * TYPE + HOLD + n * DEL + GAP
    T = s
    tag = "".join(
        f'<tspan x="{TX + i*TC:.1f}" fill-opacity="{1 if k == 0 else 0}">{escape(ch)}'
        f'<animate attributeName="fill-opacity" values="0;1;0;0" keyTimes="0;{on/T:.4f};{off/T:.4f};1" '
        f'calcMode="discrete" dur="{T:.2f}s" begin="{loop_t:.2f}s" repeatCount="indefinite"/></tspan>'
        for k, i, ch, on, off in spans)
    events.sort()
    cur_x = ";".join(f"{TX + c*TC:.1f}" for _, c in events) + f";{TX:.1f}"
    cur_k = ";".join(f"{e/T:.4f}" for e, _ in events) + ";1"

    # Protocol-character rain behind everything.
    random.seed(7)
    glyphs = "01010101ATSIPWS{}<>/$#+=*"
    rain = []
    for x in range(20, W, 38):
        n = random.randint(8, 15)
        dur = random.uniform(7, 14)
        head = f' fill="#e0f2fe"'
        col = "".join(f'<tspan x="{x}" y="{j*20}"{head if j == n-1 else ""}>{escape(random.choice(glyphs))}</tspan>' for j in range(n))
        rain.append(
            f'<text font-size="14">{col}<animateTransform attributeName="transform" type="translate" '
            f'values="0 {-n*20};0 {H}" dur="{dur:.1f}s" begin="{-random.uniform(0, dur):.1f}s" repeatCount="indefinite"/></text>')

    def packet(path, color, dur, begin, back=False):
        kp = 'keyPoints="1;0" keyTimes="0;1" calcMode="linear" ' if back else ""
        return (f'<circle r="4" fill="{color}"><animateMotion dur="{dur}s" begin="{-begin}s" repeatCount="indefinite" {kp}>'
                f'<mpath xlink:href="#{path}"/></animateMotion></circle>')

    def pulse(cx, cy, color, begin):
        return (f'<circle cx="{cx}" cy="{cy}" r="30" fill="none" stroke="{color}" stroke-width="1.5">'
                f'<animate attributeName="r" values="30;46" dur="2.4s" begin="{begin}s" repeatCount="indefinite"/>'
                f'<animate attributeName="stroke-opacity" values="0.6;0" dur="2.4s" begin="{begin}s" repeatCount="indefinite"/></circle>')

    scene = f'''
  <g font-family="{MONO}" font-size="12" fill="{DIM}">
    <path id="sms" d="M790 120 C 840 100, 880 110, 915 140" fill="none" stroke="{LINE}" stroke-width="2"/>
    <path id="sip" d="M790 180 C 840 215, 885 210, 915 180" fill="none" stroke="{LINE}" stroke-width="2" stroke-dasharray="4 5"/>
    <path id="ws" d="M985 160 C 1020 140, 1045 130, 1072 130" fill="none" stroke="{LINE}" stroke-width="2"/>
    {pulse(765, 150, GREEN, 0)}{pulse(950, 160, BLUE, 0.8)}{pulse(1110, 135, VIOLET, 1.6)}
    <rect x="743" y="110" width="44" height="78" rx="8" fill="#0f172a" stroke="{GREEN}" stroke-width="2"/>
    <rect x="749" y="120" width="32" height="54" rx="2" fill="#064e3b" opacity="0.6"/>
    <circle cx="765" cy="181" r="2.5" fill="{GREEN}"/>
    <g fill="#0f172a" stroke="{BLUE}" stroke-width="2">
      <rect x="915" y="132" width="70" height="16" rx="3"/><rect x="915" y="152" width="70" height="16" rx="3"/><rect x="915" y="172" width="70" height="16" rx="3"/>
    </g>
    <g fill="{BLUE}"><circle cx="925" cy="140" r="2.5"><animate attributeName="opacity" values="1;0.2;1" dur="0.9s" repeatCount="indefinite"/></circle>
      <circle cx="925" cy="160" r="2.5"><animate attributeName="opacity" values="0.2;1;0.2" dur="1.3s" repeatCount="indefinite"/></circle>
      <circle cx="925" cy="180" r="2.5"><animate attributeName="opacity" values="1;0.3;1" dur="1.7s" repeatCount="indefinite"/></circle></g>
    <rect x="1072" y="105" width="80" height="60" rx="6" fill="#0f172a" stroke="{VIOLET}" stroke-width="2"/>
    <path d="M1072 119 H1152" stroke="{VIOLET}" stroke-width="2"/>
    <rect x="1082" y="128" width="40" height="5" rx="2" fill="#4c1d95"/><rect x="1082" y="139" width="58" height="5" rx="2" fill="#4c1d95"/><rect x="1082" y="150" width="30" height="5" rx="2" fill="#4c1d95"/>
    {packet("sms", GREEN, 1.8, 0)}{packet("sms", GREEN, 1.8, 0.9)}
    {packet("sip", VIOLET, 2.2, 0.4, back=True)}
    {packet("ws", BLUE, 1.4, 0.2)}{packet("ws", BLUE, 1.4, 0.9)}
    <text x="765" y="212" text-anchor="middle">android</text>
    <text x="950" y="212" text-anchor="middle">api</text>
    <text x="1112" y="186" text-anchor="middle">browser</text>
    <text x="852" y="100" text-anchor="middle" fill="{GREEN}">SMS</text>
    <text x="852" y="226" text-anchor="middle" fill="{VIOLET}">SIP</text>
    <text x="1030" y="124" text-anchor="middle" fill="{BLUE}">WS</text>
  </g>'''

    body = f'''  <g clip-path="url(#frame)">
    <g font-family="{MONO}" fill="{BLUE}" opacity="0.13">{"".join(rain)}</g>
    <rect width="{W}" height="36" fill="#0f172a"/>
  </g>
  <circle cx="28" cy="18" r="6" fill="#f87171"/><circle cx="48" cy="18" r="6" fill="{AMBER}"/><circle cx="68" cy="18" r="6" fill="{GREEN}"/>
  <text x="600" y="23" fill="{DIM}" font-family="{MONO}" font-size="13" text-anchor="middle">dhruthik@github: ~</text>
  <g font-family="{MONO}" font-size="20">
    {prompt(84, cmd1)}
    <text x="{X0-2}" y="150" fill="url(#accent)" font-family="{SANS}" font-size="56" font-weight="700">{name}</text>
    {prompt(200, cmd2)}
    <g font-size="{TS}">{hide_until(loop_t)}
      <text x="{X0}" y="{TY}" fill="{DIM}">&gt;</text>
      <text y="{TY}" fill="{MUTED}">{tag}</text>
      <rect x="{TX}" y="{TY-15}" width="{TC:.0f}" height="19" fill="{BLUE}">
        <animate attributeName="x" values="{cur_x}" keyTimes="{cur_k}" calcMode="discrete" dur="{T:.2f}s" begin="{loop_t:.2f}s" repeatCount="indefinite"/>
        {blink()}
      </rect>
    </g>
  </g>
  {scene}'''
    write("banner.svg", frame(W, H, body, "Dhruthik", "Self-hosted systems that connect Android phones, browsers and backends."))


# ---------- section headers ----------

HEADERS = {
    "what_i_work_on": "telephony · browsers · applied ML",
    "tech_stack": "what I ship with",
    "featured_builds": "click a card to open the repo",
    "more_experiments": "smaller builds",
    "github_activity": "regenerated daily",
    "get_in_touch": "LinkedIn or email",
}


def header(slug, comment, color):
    W, H, X = 1200, 64, 28
    cw = 13.2  # 22px monospace cell
    cmd = "./" + slug
    chars = "".join(
        f'<tspan x="{X + (14 + i) * cw:.1f}">{escape(ch)}<animate attributeName="fill-opacity" from="0" to="0" dur="{0.3 + i*0.05:.2f}s"/></tspan>'
        for i, ch in enumerate(cmd))
    end = 0.3 + len(cmd) * 0.05
    cur_x = X + (14 + len(cmd)) * cw
    steps = ";".join(f"{X + (14 + i) * cw:.1f}" for i in range(len(cmd) + 1))
    keys = ";".join(f"{(0.3 + (i-1)*0.05)/end:.4f}" if i else "0" for i in range(len(cmd) + 1))
    body = f'''  <g font-family="{MONO}" font-size="22">
    <text x="{X}" y="41"><tspan fill="{GREEN}">~/Dhruthik0</tspan><tspan fill="{DIM}"> $ </tspan></text>
    <text y="41" fill="{TEXT}" font-weight="600">{chars}</text>
    <rect x="{cur_x:.1f}" y="23" width="12" height="24" fill="{color}">
      <animate attributeName="x" values="{steps}" keyTimes="{keys}" calcMode="discrete" dur="{end:.2f}s"/>
      {blink(end)}
    </rect>
    <text x="{W - X}" y="40" text-anchor="end" font-size="14" fill="{DIM}">{rise(end + 0.2, dy=0)}# {escape(comment)}</text>
  </g>
  <rect x="0" y="{H-3}" width="{W}" height="3" fill="{color}" opacity="0.8">
    <animate attributeName="width" values="0;{W}" dur="0.9s" begin="0.2s" calcMode="spline" keyTimes="0;1" keySplines="0.2 0.8 0.3 1"/>
  </rect>
  <rect x="0" y="{H-3}" width="120" height="3" fill="#ffffff" opacity="0.55">
    <animate attributeName="x" values="-120;{W}" dur="3.5s" begin="1.2s" repeatCount="indefinite"/>
  </rect>'''
    write(f"headers/{slug}.svg", frame(W, H, body, cmd, comment))


# ---------- about ----------

def about():
    W, X = 1200, 40
    intro = ("I build the plumbing: Android phones that work as SMS and call gateways, browser tools that plug "
             "into apps people already use, and the backends that hold it all together. Most of my projects are "
             "full systems, with a mobile client, an API, a dashboard and deployment.")
    items = [
        (GREEN, "Telephony and messaging", "Routing real cellular calls and SMS through Android handsets, with Asterisk, SIP and WebSockets in between."),
        (BLUE, "Browser automation and extensions", "Manifest V3 extensions and Playwright/CDP tooling that work with existing web apps."),
        (VIOLET, "Applied ML and AI", "URL-based phishing detection with classical and deep models, and speech-to-text, LLM and text-to-speech pipelines in production-style backends."),
        (AMBER, "Current focus", "Extending Telora and prototyping HistoWay, a travel companion that narrates the history of places as you pass them."),
    ]
    out, y = [], 50
    for i, line in enumerate(textwrap.wrap(intro, 108)):
        out.append(f'<text x="{X}" y="{y}" fill="{TEXT}" font-size="17"><tspan>{escape(line)}</tspan></text>')
        y += 27
    out = [f'<g>{rise(0.2)}{"".join(out)}</g>']
    y += 22
    for i, (color, label, text) in enumerate(items):
        t = 0.7 + i * 0.35
        lines = textwrap.wrap(text, 118)
        block = [f'<rect x="{X}" y="{y-16}" width="4" height="{22 + 22*len(lines)}" rx="2" fill="{color}"/>',
                 f'<text x="{X+20}" y="{y}" fill="{color}" font-size="16" font-weight="700">{escape(label)}</text>']
        for j, line in enumerate(lines):
            block.append(f'<text x="{X+20}" y="{y + 24 + 22*j}" fill="{MUTED}" font-size="15">{escape(line)}</text>')
        block.append(pulse_dot(W - 48, y - 4, color, begin=i * 0.5))
        out.append(f'<g>{rise(t, dy=0)}<g>'
                   f'<animateTransform attributeName="transform" type="translate" values="-24 0;0 0" dur="0.5s" begin="{t:.2f}s" calcMode="spline" keyTimes="0;1" keySplines="0.2 0.8 0.3 1"/>'
                   f'{"".join(block)}</g></g>')
        y += 30 + 22 * len(lines) + 18
    H = y
    body = f'  <g font-family="{MONO}">{"".join(out)}</g>\n  {border_sweep(W, H, GREEN, dur=9)}'
    write("about.svg", frame(W, H, body, "What I work on", intro))


# ---------- tech stack ----------

def fetch_icon(name, idx, x, y, size):
    req = urllib.request.Request(f"https://skillicons.dev/icons?i={name}", headers={"User-Agent": "curl/8"})
    raw = urllib.request.urlopen(req, timeout=20).read().decode()
    ids = set(re.findall(r'id="([^"]+)"', raw))
    for i in ids:  # icons share id names, so namespace them per embed
        raw = raw.replace(f'id="{i}"', f'id="i{idx}_{i}"').replace(f'#{i})', f'#i{idx}_{i})').replace(f'"#{i}"', f'"#i{idx}_{i}"')
    return re.sub(r'<svg width="48" height="48"', f'<svg x="{x}" y="{y}" width="{size}" height="{size}"', raw.strip(), count=1)


STACK = [
    ("Languages", GREEN, [("java", "Java"), ("py", "Python"), ("js", "JavaScript"), ("ts", "TypeScript"), ("kotlin", "Kotlin")], ""),
    ("Mobile", TEAL, [("react", "React Native"), ("androidstudio", "Android")], "native Android in Kotlin and Java"),
    ("Backend", BLUE, [("nodejs", "Node.js"), ("nestjs", "NestJS"), ("express", "Express"), ("fastapi", "FastAPI")], ""),
    ("Frontend", VIOLET, [("react", "React"), ("vite", "Vite"), ("tailwind", "Tailwind")], ""),
    ("Data", AMBER, [("postgres", "Postgres"), ("redis", "Redis"), ("mongodb", "MongoDB"), ("sqlite", "SQLite"), ("prisma", "Prisma")], ""),
    ("Tooling", ROSE, [("docker", "Docker"), ("vitest", "Vitest"), ("jest", "Jest")], "Playwright · Asterisk (ARI/PJSIP) · Turborepo · pnpm"),
    ("AI / ML", GREEN, [("pytorch", "PyTorch"), ("sklearn", "scikit-learn"), ("tensorflow", "TensorFlow")], "Gemini · Deepgram · Google Cloud TTS · sentence-transformers"),
    ("E-commerce", "#95bf47", [], "Shopify"),
]


def stack():
    W, COLW, ROWH, S = 1200, 580, 118, 44
    out, idx = [], 0
    for r, (label, color, icons, extra) in enumerate(STACK):
        col, row = r % 2, r // 2
        x0, y0 = 40 + col * (COLW + 20), 40 + row * ROWH
        t = 0.2 + r * 0.25
        out.append(f'<g>{rise(t, dy=0)}<text x="{x0}" y="{y0 + 16}" fill="{color}" font-size="14" font-weight="700">{escape(label)}</text>'
                   f'<rect x="{x0}" y="{y0 + 24}" width="28" height="2" fill="{color}"/></g>')
        for i, (key, name) in enumerate(icons):
            cx, cy = x0 + 150 + i * 82 + S / 2, y0 + S / 2
            ti = t + 0.1 + i * 0.08
            out.append(
                f'<g transform="translate({cx},{cy})">{hide_until(ti)}<g>'
                f'<animateTransform attributeName="transform" type="scale" values="0;1.15;1" keyTimes="0;0.7;1" dur="0.45s" begin="{ti:.2f}s"/>'
                f'<g>{fetch_icon(key, idx, -S/2, -S/2, S)}'
                f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -3;0 0" dur="3s" begin="{-(idx % 7) * 0.4:.1f}s" repeatCount="indefinite"/></g>'
                f'</g></g>'
                f'<text x="{cx}" y="{y0 + S + 18}" text-anchor="middle" fill="{MUTED}" font-size="11">{hide_until(ti)}{escape(name)}</text>')
            idx += 1
        if extra:
            ex_y = y0 + S + 40 if icons else y0 + 26
            ex_x = x0 + 150
            if not icons:  # Shopify has no skillicon, so draw a chip instead
                w = len(extra) * 8.4 + 30
                out.append(f'<g>{rise(t + 0.1, dy=6, dur=0.35)}<rect x="{ex_x}" y="{y0}" width="{w}" height="{S}" rx="10" fill="{color}" fill-opacity="0.15" stroke="{color}"/>'
                           f'<text x="{ex_x + w/2}" y="{y0 + 28}" text-anchor="middle" fill="{TEXT}" font-size="15" font-weight="700">{escape(extra)}</text></g>')
            else:
                out.append(f'<text x="{ex_x}" y="{ex_y}" fill="{DIM}" font-size="11">{hide_until(t + 0.5)}+ {escape(extra)}</text>')
    H = 40 + 4 * ROWH
    body = f'  <g font-family="{MONO}">{"".join(out)}</g>\n  {border_sweep(W, H, BLUE, dur=10)}'
    names = "; ".join(f"{l}: " + ", ".join(n for _, n in ic) + (f" ({e})" if e else "") for l, _, ic, e in STACK)
    write("stack.svg", frame(W, H, body, "Tech stack", names))


# ---------- project cards ----------

PROJECTS = [
    ("telora", "Telora", GREEN,
     "Cellular calls and SMS through your own Android phones, run from one backend and one dashboard.",
     ["SMS over an authenticated device WebSocket with delivery acks. Inbound messages are buffered and replayed if the link drops.",
      "Voice over SIP through Asterisk ARI, and the handset places the real cellular call.",
      "Speech-to-text → LLM → text-to-speech pipeline for automated calls. API keys are stored only as SHA-256 hashes."],
     ["TypeScript", "NestJS", "React + Vite", "Kotlin", "Asterisk", "PostgreSQL", "Prisma", "Redis", "BullMQ", "Docker", "Turborepo"]),
    ("phishing", "Phishing URL Detector", ROSE,
     "Two models, one verdict on whether a URL is phishing.",
     ["A Random Forest on engineered URL features plus a character-level CNN on the raw URL. The API averages both.",
      "A FastAPI /predict service (phish-detector) serves the models.",
      "A Manifest V3 extension checks the active tab, and a Streamlit UI is included for demos."],
     ["Python", "scikit-learn", "PyTorch", "FastAPI", "Streamlit", "Chrome MV3"]),
    ("varoza", "Varoza", AMBER,
     "A poster marketplace with buyer, seller and admin sides. Live at varoza.vercel.app.",
     ["Buyers browse, add to cart and check out. Sellers upload posters, track earnings and request withdrawals.",
      "Admins approve sellers, posters and payments, and manage margins, coupons and shipping.",
      "JWT auth with role-based route guards. Images are stored in Cloudinary."],
     ["React", "Vite", "Tailwind CSS", "Node.js", "Express", "MongoDB", "Cloudinary", "Vercel"]),
    ("ai-bridge", "AI Bridge", BLUE,
     "Pipe prompts from your scripts and shell to your own ChatGPT web session.",
     ["Attaches to a real Chrome profile over CDP, and each request runs in a fresh temporary chat.",
      "Loopback-only, with a constant-time bearer token check, DNS-rebinding defense, request size caps and no prompt logging by default.",
      "Sync, async, poll and cancel job API, with unit, live and end-to-end tests."],
     ["Python", "FastAPI", "Playwright", "pytest", "systemd"]),
    ("finledger", "FinLedger", TEAL,
     "Borrowers, loans, monthly interest and collections for a small lending business.",
     ["Generates monthly interest due dates and applies each payment to the oldest pending interest first (FIFO), so the user only enters an amount.",
      "Dashboard for due-today, overdue and next-7-days items, plus a due-date calendar, browser notifications and Excel export.",
      "One Docker Compose command runs PostgreSQL, the API and the Nginx-served frontend."],
     ["React", "Vite", "Tailwind CSS", "Node.js", "Express", "Prisma", "PostgreSQL", "Docker"]),
    ("sms-freebie", "sms-freebie", VIOLET,
     "A self-hosted SMS gateway on paired Android phones instead of a paid SMS API. The predecessor of Telora's SMS side.",
     ["An Android foreground service dispatches across multiple SIMs, stores messages in Room during network drops and restarts on boot.",
      "An Express server on SQLite (WAL mode) with JWT and API-key auth, a WebSocket device pool and live SSE dashboard updates.",
      "Ships with Docker and an end-to-end integration test script."],
     ["Kotlin", "Node.js", "Express", "SQLite", "WebSocket", "SSE", "Docker"]),
]


def card_body(title, color, tagline, bullets, tech, W, wrap_tag, wrap_bul, start=0.0):
    X = 28
    out = [f'<g>{rise(start)}',
           pulse_dot(X + 6, 38, color, begin=start),
           f'<text x="{X + 22}" y="46" fill="{TEXT}" font-family="{SANS}" font-size="26" font-weight="700">{escape(title)}</text>',
           f'<text x="{W - X}" y="44" text-anchor="end" fill="{color}" font-size="20">↗</text></g>']
    y = 80
    tag = [f'<text x="{X}" y="{y + 20*i}" fill="{color}" font-size="14" font-weight="600">{escape(l)}</text>'
           for i, l in enumerate(textwrap.wrap(tagline, wrap_tag))]
    out.append(f'<g>{rise(start + 0.25, dy=8)}{"".join(tag)}</g>')
    y += 20 * len(tag) + 16
    for b, text in enumerate(bullets):
        t = start + 0.5 + b * 0.25
        lines = textwrap.wrap(text, wrap_bul)
        g = [f'<text x="{X}" y="{y}" fill="{color}" font-size="13">›</text>']
        g += [f'<text x="{X + 16}" y="{y + 19*i}" fill="{MUTED}" font-size="13">{escape(l)}</text>' for i, l in enumerate(lines)]
        out.append(f'<g>{rise(t, dy=0)}<g><animateTransform attributeName="transform" type="translate" values="-16 0;0 0" dur="0.4s" begin="{t:.2f}s" calcMode="spline" keyTimes="0;1" keySplines="0.2 0.8 0.3 1"/>{"".join(g)}</g></g>')
        y += 19 * len(lines) + 10
    y += 6
    if tech:
        c, rows = chips(tech, X, y, W - 2 * X, color, start + 0.5 + len(bullets) * 0.25)
        out.append(c)
        y += 28 * rows
    return "".join(out), y + 16


def cards(items, prefix, W, wrap_tag, wrap_bul):
    built = [(slug, title, color, card_body(title, color, tag, bul, tech, W, wrap_tag, wrap_bul))
             for slug, title, color, tag, bul, tech in items]
    H = max(h for *_, (_, h) in built)  # same height so side-by-side cards line up
    for n, (slug, title, color, (body, _)) in enumerate(built):
        src = next(p for p in items if p[0] == slug)
        desc = src[3] + " " + " ".join(src[4])
        svg = frame(W, H, f'  <g font-family="{MONO}">{body}</g>\n  {border_sweep(W, H, color, dur=7, begin=n * 1.3)}', title, desc)
        write(f"{prefix}/{slug}.svg", svg)


EXPERIMENTS = [
    ("chat-trace", "Chat-trace", BLUE,
     "A Chrome extension that records which ChatGPT answer prompted each follow-up question, so you can jump back to it.",
     [], ["WXT", "React", "TypeScript"]),
    ("otp-autofill", "OTP AutoFill Assistant", GREEN,
     "A Manifest V3 extension that reads one-time codes from Outlook or Gmail and fills them into login forms.",
     [], ["TypeScript", "Vite", "Chrome MV3"]),
    ("resume-screen-agent", "resume-screen-agent", AMBER,
     "Ranks resumes against a job description with semantic search.",
     [], ["Streamlit", "sentence-transformers", "FAISS"]),
    ("emotion-detection", "emotion-detection", ROSE,
     "Webcam emotion detection served over FastAPI.",
     [], ["FastAPI", "DeepFace", "TensorFlow"]),
]


if __name__ == "__main__":
    banner()
    for i, (slug, comment) in enumerate(HEADERS.items()):
        header(slug, comment, [GREEN, BLUE, VIOLET, AMBER, TEAL, ROSE][i])
    about()
    stack()
    cards(PROJECTS, "cards", 590, 62, 66)
    cards(EXPERIMENTS, "experiments", 590, 62, 66)
    print("assets written to", OUT)
