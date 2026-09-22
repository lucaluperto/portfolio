"""Legacy generator from the portfolio's previous directory structure.

The production HTML files in the repository root are now the source of truth.
Do not run this script on the production branch until its templates and paths
have been refactored to match the current site.
"""
import csv, html
from collections import OrderedDict

SITE = "Luca Luperto"
DOMAIN = "lucaluperto.it"
LINKEDIN = "https://www.linkedin.com/in/lupertoluca"
EMAIL = "lucaluperto99@gmail.com"

CASES = [
    ("comedy-week.html", "Comedy Week"),
    ("kolms-creative.html", "Kolms Creative"),
    ("italy-food-prn.html", "Italy Food PRN"),
    ("azzurro-ads.html", "Azzurro Ads"),
]

def fmt(n):  # 32810205 -> 32,810,205
    return f"{n:,}"

def short(n):
    if n >= 1_000_000:
        s = f"{n/1_000_000:.1f}".rstrip("0").rstrip(".")
        return s + "M"
    if n >= 1000:
        return f"{round(n/1000):,}K"
    return str(n)

def page(title, desc, body, current=None):
    cur = ' aria-current="page"'
    nav = "".join(
        f'<a href="{f}" class="hide-sm"{cur if f == current else ""}>{n}</a>' for f, n in CASES
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='7' fill='%232a78d6'/><text x='16' y='22' font-family='Georgia' font-size='17' font-weight='700' fill='white' text-anchor='middle'>LL</text></svg>">
</head>
<body>
<header class="site"><div class="wrap wide">
  <a class="name" href="index.html">{SITE}</a>
  <nav>{nav}<a href="{LINKEDIN}">LinkedIn</a></nav>
</div></header>
<main>
{body}
</main>
<footer class="site"><div class="wrap wide">
  {SITE} · Growth &amp; Digital Marketing · <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{LINKEDIN}">LinkedIn</a><br>
  EU citizen · available from 1 November 2026
</div></footer>
<script src="assets/tip.js"></script>
</body>
</html>
"""

def next_links(current):
    files = [f for f, _ in CASES]
    i = files.index(current)
    prev_f, prev_n = CASES[i - 1]
    next_f, next_n = CASES[(i + 1) % len(CASES)]
    return f'<div class="next"><a href="{prev_f}">&larr; {prev_n}</a><a href="index.html">All work</a><a href="{next_f}">{next_n} &rarr;</a></div>'

# ---------- charts ----------

def vbar(items, highlight=None, height=240, label_every=1, show_values=True, x_labels=True, bar_max=56, value_idx=None):
    """items: list of (label, value, tip). Vertical bars on a single axis."""
    highlight = highlight or set()
    W, H = 680, height
    left, right, top, bottom = 60, 8, 30, 36 if x_labels else 12
    pw, ph = W - left - right, H - top - bottom
    vmax = max(v for _, v, _ in items)
    # nice axis max
    steps = [1, 2, 2.5, 5, 10]
    mag = 10 ** (len(str(int(vmax))) - 1)
    amax = next(s * mag for s in steps if s * mag >= vmax)
    n = len(items)
    slot = pw / n
    bw = min(bar_max, slot - 2)
    out = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img">']
    for k in range(5):
        val = amax * k / 4
        y = top + ph - ph * k / 4
        out.append(f'<line class="grid" x1="{left}" x2="{W-right}" y1="{y:.1f}" y2="{y:.1f}"/>')
        out.append(f'<text x="{left-8}" y="{y+4:.1f}" text-anchor="end">{short(int(val)) if val else 0}</text>')
    for i, (lab, v, tip) in enumerate(items):
        h = max(ph * v / amax, 1.5)
        x = left + i * slot + (slot - bw) / 2
        y = top + ph - h
        r = min(4, bw / 2)
        cls = "bar" if (not highlight or i in highlight) else "bar mute"
        # rounded top only, anchored to baseline
        path = (f"M{x:.1f},{top+ph:.1f} V{y+r:.1f} Q{x:.1f},{y:.1f} {x+r:.1f},{y:.1f} "
                f"H{x+bw-r:.1f} Q{x+bw:.1f},{y:.1f} {x+bw:.1f},{y+r:.1f} V{top+ph:.1f} Z")
        out.append(f'<path class="{cls}" d="{path}" tabindex="0" data-tip="{html.escape(tip)}"/>')
        if show_values and (value_idx is None or i in value_idx) and (not highlight or i in highlight):
            out.append(f'<text class="val" x="{x+bw/2:.1f}" y="{y-6:.1f}" text-anchor="middle">{short(v)}</text>')
        if x_labels and i % label_every == 0:
            out.append(f'<text x="{x+bw/2:.1f}" y="{H-12}" text-anchor="middle">{html.escape(lab)}</text>')
    out.append("</svg>")
    return "".join(out)

def hbar(items, label_w=130):
    """items: list of (label, value, tip). Horizontal bars, values labelled."""
    W = 680
    row = 34
    H = row * len(items) + 8
    pw = W - label_w - 160
    vmax = max(v for _, v, _ in items)
    out = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img">']
    for i, (lab, v, tip) in enumerate(items):
        y = 4 + i * row
        w = max(pw * v / vmax, 2)
        r = min(4, w / 2)
        x0 = label_w
        path = (f"M{x0},{y+4} H{x0+w-r:.1f} Q{x0+w:.1f},{y+4} {x0+w:.1f},{y+4+r} "
                f"V{y+row-8-r} Q{x0+w:.1f},{y+row-8} {x0+w-r:.1f},{y+row-8} H{x0} Z")
        out.append(f'<text x="{label_w-10}" y="{y+row/2+1:.1f}" text-anchor="end">{html.escape(lab)}</text>')
        out.append(f'<path class="bar" d="{path}" tabindex="0" data-tip="{html.escape(tip)}"/>')
        out.append(f'<text class="val" x="{x0+w+8:.1f}" y="{y+row/2+1:.1f}">{fmt(v)}</text>')
    out.append("</svg>")
    return "".join(out)

def table(headers, rows, numeric=()):
    th = "".join(f'<th class="{"n" if i in numeric else ""}">{h}</th>' for i, h in enumerate(headers))
    trs = "".join(
        "<tr>" + "".join(f'<td class="{"n" if i in numeric else ""}">{c}</td>' for i, c in enumerate(r)) + "</tr>"
        for r in rows
    )
    return f'<div class="table-scroll"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'

def figure(title, sub, svg, tbl):
    return f"""<figure><figcaption>{title}</figcaption><div class="sub">{sub}</div>{svg}
<details><summary>Show data table</summary>{tbl}</details></figure>"""

def todo(text):
    return f'<div class="todo">{text}</div>'

# ---------- data ----------

rows = list(csv.DictReader(open("data/comedy-week.csv", encoding="utf-8")))
def num(s):
    return int(s) if s else 0
videos = [r for r in rows if r["instagram"]]
total_ig = sum(num(r["instagram"]) for r in videos)
editions = OrderedDict()
for r in videos:
    editions.setdefault(r["edition"], []).append(num(r["instagram"]))
creators = OrderedDict()
for r in videos:
    creators[r["creator"]] = creators.get(r["creator"], 0) + num(r["instagram"])
ranked = sorted(videos, key=lambda r: -num(r["instagram"]))
top5 = sum(num(r["instagram"]) for r in ranked[:5])
top10 = sum(num(r["instagram"]) for r in ranked[:10])
vals = sorted(num(r["instagram"]) for r in videos)
median = vals[len(vals) // 2]
mean = total_ig / len(videos)
ch = {c: sum(num(r[c]) for r in rows) for c in ("facebook", "youtube", "tiktok")}
n_collabs = len(rows)
n_creators = len({r["creator"].lower() for r in rows})
dang = [r for r in videos if "d'angella" in r["creator"].lower()]
top_creator_share = creators["Giovanni d'Angella"] / total_ig
cammela_share = creators['Chiara Anicito "Cammela"'] / total_ig
summer_share = (sum(editions["Summer 2024"]) + sum(editions["Summer 2025"])) / total_ig

def ed_short(e):
    return ("Win " if e.startswith("Winter") else "Sum ") + "'" + e[-2:]

def pct(x):
    return f"{x*100:.1f}%"

# ---------- pages ----------

def comedy_week():
    ed_items = [(ed_short(e), sum(v), f"{e}: {fmt(sum(v))} views from {len(v)} videos") for e, v in editions.items()]
    ed_fig = figure(
        "Instagram views by edition",
        f"Summer editions delivered {pct(summer_share)} of all views.",
        vbar(ed_items, bar_max=90, height=300),
        table(["Edition", "Videos", "Instagram views"], [(e, len(v), fmt(sum(v))) for e, v in editions.items()], numeric=(1, 2)),
    )
    rank_items = [(str(i + 1), num(r["instagram"]), f'#{i+1} {r["creator"]} ({r["edition"]}): {fmt(num(r["instagram"]))}')
                  for i, r in enumerate(ranked)]
    rank_fig = figure(
        "All 43 videos, ranked by Instagram views",
        f"The top 5 (highlighted) produced {pct(top5/total_ig)} of total reach. The median video did {fmt(median)}.",
        vbar(rank_items, highlight=set(range(5)), x_labels=False, height=280, value_idx={0, 1}),
        table(["#", "Creator", "Edition", "Instagram views"],
              [(i + 1, f'<a href="{r["link"]}">{html.escape(r["creator"])}</a>', r["edition"], fmt(num(r["instagram"])))
               for i, r in enumerate(ranked)], numeric=(0, 3)),
    )
    d_items = [(ed_short(r["edition"]), num(r["instagram"]), f'{r["edition"]}: {fmt(num(r["instagram"]))}') for r in dang]
    d_fig = figure(
        "One creator, five collaborations",
        "Giovanni d'Angella's Instagram views per video, in order of publication.",
        vbar(d_items, bar_max=70, height=300),
        table(["Edition", "Instagram views", "Video"],
              [(r["edition"], fmt(num(r["instagram"])), f'<a href="{r["link"]}">Reel</a>') for r in dang], numeric=(1,)),
    )
    ch_items = [("Instagram", total_ig, "Instagram, all editions"),
                ("YouTube", ch["youtube"], "YouTube, tracked mainly from Winter 2025"),
                ("TikTok", ch["tiktok"], "TikTok, tracked mainly from Winter 2025"),
                ("Facebook", ch["facebook"], "Facebook, tracked from Winter 2025")]
    ch_fig = figure(
        "Views by channel",
        "Same videos, four channels. TikTok and Facebook together: " + pct((ch['tiktok'] + ch['facebook']) / (total_ig + sum(ch.values()))) + " of reach.",
        hbar(ch_items),
        table(["Channel", "Views"], [(a, fmt(b)) for a, b, _ in ch_items], numeric=(1,)),
    )
    body = f"""<article class="wrap">
<p class="eyebrow">Case study · Azzurro Club Vacanze · 2024–2025</p>
<h1>Comedy Week: 32.8 million organic views, and what the data said about them</h1>
<div class="meta"><span><b>Role</b> programme lead</span><span><b>Scope</b> 4 editions, 13 hotels</span><span><b>Channels</b> Instagram, YouTube, TikTok, Facebook</span></div>
<p class="lede">A national stand-up comedy programme run inside a hotel group's resorts, turned into an organic content engine. The reach was big. The more useful part was what tracking it video by video revealed.</p>

<div class="stats">
  <div class="stat"><b>32.8M</b><span>organic Instagram views</span></div>
  <div class="stat"><b>{n_collabs}</b><span>collaborations</span></div>
  <div class="stat"><b>{n_creators}</b><span>comedians and groups</span></div>
  <div class="stat"><b>0€</b><span>paid amplification</span></div>
</div>

<h2>Context</h2>
<p>Azzurro Club Vacanze runs 13 four and five star resorts. After COVID the group needed to rely less on OTAs and build direct demand. The comedy programme brought comedians from the Zelig circuit into the resorts; each performance was also a short video published on the brand's Instagram, cross-posted from Winter 2025 to YouTube, TikTok and Facebook.</p>

<h2>What I did</h2>
<ul class="clean">
  <li>Ran the programme across four editions (Winter 2024 to Summer 2025): creator selection, booking, briefs, approvals and publishing.</li>
  <li>Built a tracking sheet with one row per collaboration: creator, edition, views per channel, link. <a href="data/comedy-week.csv">The raw data is in this repo.</a></li>
  <li>Used it to decide who to invite back and where to spend production time.</li>
</ul>

<h2>Results</h2>
{ed_fig}

<h2>What the data said</h2>
<h3>1. It's a long tail, not an average</h3>
<p>The mean video did {fmt(round(mean))} views; the median did {fmt(median)}. A gap of {mean/median:.0f}x means the average describes nothing. The top 10 videos produced {pct(top10/total_ig)} of reach; the other 33 together did {fmt(total_ig-top10)}.</p>
{rank_fig}

<h3>2. Two creators carried 70%</h3>
<p>Giovanni d'Angella alone produced {pct(top_creator_share)} of all views, Chiara "Cammela" Anicito {pct(cammela_share)}. The other {len(creators)-2} acts shared the remaining {pct(1-top_creator_share-cammela_share)}.</p>
{d_fig}
<div class="insight"><p><b>The finding I'd defend in any meeting:</b> d'Angella's first video did 27,400 views, among the weakest of the first edition. His fourth did 8 million. Judged on the first collaboration, he would have been dropped. With creators, the value is in the second and third collaboration, so the first one should be treated as a test, not a verdict.</p></div>

<h3>3. Two of four channels weren't worth the work</h3>
<p>Instagram produced {fmt(total_ig)} views, YouTube {fmt(ch['youtube'])}, TikTok {fmt(ch['tiktok'])}, Facebook {fmt(ch['facebook'])}. Adapting every video for four channels cost production time; two of them returned almost nothing. YouTube was the exception worth watching: sporadic, but Marco Passiglia's Summer 2024 video did 1.4M there, more than on Instagram.</p>
{ch_fig}

<h2>One thing most people get wrong</h2>
<p>Creator programmes are usually evaluated per post and per creator, on the first result. That kills exactly the relationships that compound. Budget a first collaboration as a test, set the bar for a second one low, and decide on the second or third.</p>

<h2>What didn't work, and what's missing</h2>
<ul class="clean">
  <li><b>No cost per creator in the dataset.</b> The programme sat inside a roughly 200000€ annual budget but its share was never isolated, so I can't state a cost per thousand views or a cost per booking. This is a reach story, not yet an efficiency story.</li>
  <li><b>Cross-channel tracking started late.</b> YouTube, TikTok and Facebook were tracked systematically only from Winter 2025, so channel totals understate the first two editions.</li>
  <li><b>No link to bookings.</b> Views were never tied to direct bookings, which was the business goal.</li>
</ul>
{todo("Cosa è stato cambiato dopo questa analisi (es. inviti ripetuti ai creator migliori, stop a TikTok/Facebook)? E, se recuperabili, i compensi dei creator anche aggregati per edizione: servono per calcolare il costo per mille views.")}
{next_links("comedy-week.html")}
</article>"""
    return page("Comedy Week case study · Luca Luperto",
                "How a comedy programme produced 32.8 million organic Instagram views, and what per-video tracking revealed.",
                body, "comedy-week.html")


def kolms():
    body = f"""<article class="wrap">
<p class="eyebrow">Case study · Founder · 2023–present</p>
<h1>Kolms Creative: a content service for luxury hotels, built and sold from zero</h1>
<div class="meta"><span><b>Role</b> founder</span><span><b>Clients</b> 30+ hotels</span><span><b>Model</b> B2B service, alongside a full-time job</span></div>
<p class="lede">A content marketing service for luxury hotels, from the first cold message to more than 30 client properties. This is the case study about selling, not just making.</p>

<div class="stats">
  <div class="stat"><b>30+</b><span>hotel clients</span></div>
  <div class="stat"><b>110000€+</b><span>contracts <span class="todo">venduti o gestiti?</span></span></div>
  <div class="stat"><b><span class="todo">?</span></b><span>close rate</span></div>
  <div class="stat"><b><span class="todo">?</span></b><span>repeat clients</span></div>
</div>

<h2>Context</h2>
<p>Luxury hotels need a steady flow of photo and video content, but most can't justify an in-house team and find agencies slow and expensive. I started Kolms in 2023 to fill that gap, running it in parallel with a full-time marketing role.</p>
{todo("Cosa vendi esattamente (pacchetti, shooting, gestione social, video)? Prezzo medio per cliente o fascia di prezzo. Anno di avvio preciso e se esiste un sito Kolms da linkare.")}

<h2>The metric</h2>
<p>For a service business the numbers that matter are close rate (how many conversations become contracts), value per client and how many clients come back.</p>

<h2>What I did</h2>
<ul class="clean">
  <li><b>Business development:</b> prospecting and qualifying hotels, first contact, proposals.</li>
  <li><b>Pricing and negotiation:</b> building offers and closing contracts.</li>
  <li><b>Creative direction:</b> content strategy and direction of shoots for each property.</li>
  <li><b>Client management:</b> relationships and renewals across 30+ properties.</li>
</ul>
{todo("Come trovavi i clienti (outbound email, LinkedIn, passaparola, visite)? Quanti contatti per chiudere un cliente? Un esempio concreto di trattativa.")}

<h2>Selected work</h2>
{todo("3–6 lavori migliori: link a reel/foto o immagini da mettere in assets/kolms/. Nomi dei clienti solo se condivisibili, altrimenti 'hotel 5 stelle, Lago di Garda' ecc. Un numero per lavoro se c'è (views, follower, prenotazioni).")}

<h2>What didn't work</h2>
{todo("Una cosa che non ha funzionato: un canale di vendita che non ha reso, un prezzo sbagliato, un cliente perso e perché. È la sezione che rende credibile il resto.")}
{next_links("kolms-creative.html")}
</article>"""
    return page("Kolms Creative case study · Luca Luperto",
                "A content service for luxury hotels, built and sold from zero to 30+ clients.", body, "kolms-creative.html")


def ifp():
    body = f"""<article class="wrap">
<p class="eyebrow">Case study · Italy Food PRN · May 2024 – Dec 2025</p>
<h1>Italy Food PRN: from zero to 80,000 followers by industrialising production</h1>
<div class="meta"><span><b>Role</b> project manager</span><span><b>Region</b> Emilia-Romagna</span><span><b>Channels</b> Instagram, TikTok, Facebook, YouTube</span></div>
<p class="lede">An editorial food project for Emilia-Romagna, run end to end. The growth came from two things: finding the formats that brought in new people, and building a production process that could publish more of them.</p>

<div class="stats">
  <div class="stat"><b>80,000+</b><span>organic followers in 18 months</span></div>
  <div class="stat"><b>4</b><span>platforms</span></div>
  <div class="stat"><b>15+</b><span>stakeholders and local partners</span></div>
  <div class="stat"><b><span class="todo">?→?</span></b><span>videos per week, before and after</span></div>
</div>

<h2>Context</h2>
<p>A regional food publisher needed an audience from zero, on four platforms, with content that also served more than 15 local partners and stakeholders.</p>

<h2>What I did</h2>
<ul class="clean">
  <li>Owned the editorial strategy and distribution across Instagram, TikTok, Facebook and YouTube.</li>
  <li>Monitored performance continuously and moved the editorial plan towards the formats that reached new audiences.</li>
  <li>Redesigned the production workflow: shooting, editing in Premiere and CapCut, scheduled publishing.</li>
  <li>Coordinated creators, talent and production agencies around partners' needs.</li>
</ul>

<h2>The production process</h2>
<p>The constraint was output: more good videos per week without more people. The workflow was rebuilt step by step and tracked.</p>
{todo("Il tracking dell'incremento: quanti video a settimana/mese all'inizio e alla fine? Tempo medio per video prima e dopo? Quali passaggi hai cambiato (template di montaggio, shooting in batch, calendario, riuso cross-piattaforma)? Se hai un foglio mensile lo trasformo in un grafico come quelli della Comedy Week.")}

<h2>Best videos</h2>
{todo("5–8 video migliori con link, piattaforma, views/like e perché hanno funzionato (formato, gancio iniziale, luogo). Serve anche l'account del progetto da linkare.")}

<h2>Growth</h2>
{todo("Follower per mese o per trimestre (anche 5–6 punti bastano) e per piattaforma: diventa il grafico di crescita da 0 a 80.000.")}

<h2>What didn't work</h2>
{todo("Un formato o una piattaforma che non ha reso, e cosa hai smesso di fare di conseguenza.")}
{next_links("italy-food-prn.html")}
</article>"""
    return page("Italy Food PRN case study · Luca Luperto",
                "Growing a regional food publisher from zero to 80,000 followers by rebuilding content production.", body, "italy-food-prn.html")


def azzurro():
    body = f"""<article class="wrap">
<p class="eyebrow">Case study · Azzurro Club Vacanze · Dec 2022 – Feb 2026</p>
<h1>Azzurro ads: moving a hotel group from OTAs to direct bookings</h1>
<div class="meta"><span><b>Role</b> digital marketing specialist</span><span><b>Portfolio</b> 13 hotels, 4 and 5 star</span><span><b>Budget</b> ~200000€ per year</span></div>
<p class="lede">After COVID, a hotel group paying OTA commissions on most online sales needed its own channel. Over two years, direct online bookings went from 20% to 70% of revenue.</p>

<div class="stats">
  <div class="stat"><b>20% → 70%</b><span>direct online bookings on revenue</span></div>
  <div class="stat"><b>~200000€</b><span>annual budget: paid, talent, agencies</span></div>
  <div class="stat"><b>13</b><span>properties</span></div>
  <div class="stat"><b><span class="todo">?</span></b><span>ROAS or cost per booking</span></div>
</div>

<h2>Context</h2>
<p>Every booking through an OTA costs a commission. The goal was to make the direct channel the default, including for past guests who would otherwise come back through an intermediary.</p>

<h2>What I did</h2>
<ul class="clean">
  <li><b>Paid social (Meta):</b> campaigns across 13 properties. <span class="todo">obiettivi, pubblici, creatività</span></li>
  <li><b>Google Ads:</b> mostly brand campaigns, to capture people already searching for the hotels instead of letting OTAs buy that traffic.</li>
  <li><b>Email reactivation:</b> the existing guest database re-engaged to bring past guests back direct.</li>
  <li><b>Weekly reallocation</b> of budget between paid social, email and content based on Google Analytics and Excel reporting.</li>
</ul>

<h2>The analysis</h2>
{todo("Qui va il cuore del case study. Serve un export anche parziale da Meta Ads e/o Google Ads (spesa, click, conversioni, valore) per campagna o per mese. Anche screenshot va bene. Con quelli costruisco: spesa per canale, costo per prenotazione, ROAS, e il confronto con la commissione OTA.")}

<h3>Direct vs OTA: the unit economics</h3>
{todo("Commissione media OTA (es. 15–20%) e valore medio prenotazione: permettono di stimare quanto ha risparmiato il gruppo passando dal 20% al 70%. Le stime vanno bene se dichiarate come stime.")}

<h3>Email reactivation</h3>
{todo("Dimensione del database, open rate, click rate, prenotazioni o fatturato recuperati.")}

<h2>What didn't work</h2>
{todo("Una campagna o un canale che non ha reso e cosa hai spostato di conseguenza.")}
{next_links("azzurro-ads.html")}
</article>"""
    return page("Azzurro ads case study · Luca Luperto",
                "How a 13-hotel group moved direct online bookings from 20% to 70% of revenue.", body, "azzurro-ads.html")


def index():
    body = f"""<section class="wrap wide">
<h1>Luca Luperto</h1>
<p class="lede">Growth &amp; digital marketing. I build channels that bring in customers directly, and I track them closely enough to know which parts are working.</p>
<p class="muted">Milan · EU citizen · available from 1 November 2026 · <a href="mailto:{EMAIL}">{EMAIL}</a></p>

<div class="cards">
  <a class="card" href="comedy-week.html"><span class="tag">Creator programme · data</span><h3>Comedy Week</h3>
    <p>A comedy programme across 13 hotels, and what per-video tracking revealed about where reach really came from.</p>
    <div class="big">32.8M<small>organic Instagram views, 0€ paid</small></div></a>
  <a class="card" href="azzurro-ads.html"><span class="tag">Paid · CRM · direct channel</span><h3>Azzurro ads</h3>
    <p>Moving a hotel group from OTA dependence to its own channel with Meta, Google Ads and email reactivation.</p>
    <div class="big">20% → 70%<small>direct online bookings on revenue</small></div></a>
  <a class="card" href="italy-food-prn.html"><span class="tag">Content · operations</span><h3>Italy Food PRN</h3>
    <p>A regional food publisher grown from zero by finding the right formats and rebuilding how they were produced.</p>
    <div class="big">80,000+<small>organic followers in 18 months</small></div></a>
  <a class="card" href="kolms-creative.html"><span class="tag">Founder · sales</span><h3>Kolms Creative</h3>
    <p>A content service for luxury hotels, built and sold from the first cold message to 30+ clients.</p>
    <div class="big">30+<small>hotel clients</small></div></a>
</div>
</section>"""
    return page("Luca Luperto · Growth & Digital Marketing",
                "Portfolio of Luca Luperto: case studies in growth, paid, creator and content marketing.", body)


if __name__ == "__main__":
    for name, fn in [("index.html", index), ("comedy-week.html", comedy_week), ("kolms-creative.html", kolms),
                     ("italy-food-prn.html", ifp), ("azzurro-ads.html", azzurro)]:
        open(name, "w", encoding="utf-8").write(fn())
        print("wrote", name)
