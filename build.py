"""Builds the static portfolio site. Run: python3 build.py
Charts are generated from data/*.csv as inline SVG, so the site has no JS dependencies."""
import csv, html, math
from collections import OrderedDict

SITE = "Luca Luperto"
DOMAIN = "lucaluperto.it"
LINKEDIN = "https://www.linkedin.com/in/lupertoluca"
EMAIL = "lucaluperto99@gmail.com"
CV = "cv-luca-luperto.pdf"

ALL_CASES = [
    ("azzurro-ads.html", "Azzurro Ads"),
    ("comedy-week.html", "Comedy Week"),
    ("italy-food-prn.html", "Italy Food PRN"),
    ("kolms-creative.html", "Kolms Creative"),
]

# Only these are built and linked. Add a file here when its page is complete.
PUBLISHED = {"comedy-week.html", "kolms-creative.html", "italy-food-prn.html", "azzurro-ads.html"}
CASES = [c for c in ALL_CASES if c[0] in PUBLISHED]

def fmt(n):  # 32810205 -> 32,810,205
    return f"{n:,}"

def short(n):
    if n >= 1_000_000:
        s = f"{n/1_000_000:.1f}".rstrip("0").rstrip(".")
        return s + "M"
    if n >= 10000:
        return f"{round(n/1000):,}K"
    if n >= 1000:
        return (f"{n/1000:.1f}".rstrip("0").rstrip(".")) + "K"
    return str(n)

# PostHog — plain string (NOT an f-string): the snippet is full of { } braces
# and inside an f-string they would have to be doubled. Keep it here, insert
# it into the template with {POSTHOG}. Project 281900, EU Cloud.
POSTHOG = """<script>
!function(t,e){var o,n,p,r;e.__SV||(window.posthog && window.posthog.__loaded)||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}p||((p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",p.onerror=function(){p=null},(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r));var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],Object.defineProperty(u,"toString",{configurable:!0,enumerable:!0,writable:!0,value:function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e}}),Object.defineProperty(u.people,"toString",{configurable:!0,enumerable:!0,writable:!0,value:function(){return u.toString(1)+".people (stub)"}}),o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagResult isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
posthog.init('phc_v96eDoyRSB9aAFanDd546SFta744k8Ng2YSQQuPfHL4T', {
  api_host: 'https://eu.i.posthog.com',
  defaults: '2026-05-30'
})
</script>"""


def page(title, desc, body, current=None, canon="", jsonld=""):
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
<meta property="og:image" content="https://lucaluperto.it/og.png">
<meta property="og:type" content="website">
<meta property="og:url" content="https://lucaluperto.it/">
<meta name="twitter:card" content="summary_large_image">
<meta name="author" content="Luca Luperto">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="https://lucaluperto.it/{canon}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Caveat:wght@500&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='0' fill='%23c4341c'/><path d='M16 20h15v44h28v16H16z' fill='white'/><path d='M84 80H69V36H41V20h43z' fill='white' fill-opacity='0.55'/></svg>">
{POSTHOG}
</head>
<body>
<header class="site"><div class="w">
  <a class="name" href="index.html"><svg class="mark" viewBox="0 0 100 100" aria-hidden="true" width="24" height="24"><path d="M8 12h18v58h34v18H8z" fill="currentColor"/><path d="M92 88H74V30H40V12h52z" fill="var(--accent)"/></svg><span>{SITE}</span></a>
  <nav>{nav}<a href="index.html#about">About</a><a href="{CV}">CV</a><a href="index.html#contact">Contact</a></nav>
</div></header>
<main>
{body}
</main>
<footer class="site"><div class="w">
  <span><a href="mailto:{EMAIL}">{EMAIL}</a></span>
  <span>EU citizen · available 1 November 2026</span>
  <span><a href="{LINKEDIN}">LinkedIn</a></span>
  <span>Anonymous analytics, hosted in the EU. No ads, no third-party tracking.</span>
</div></footer>
{jsonld}<script src="tip.js"></script>
</body>
</html>
"""

def next_links(current):
    if len(CASES) < 2:
        return '<div class="next"><a href="index.html">&larr; Back to all work</a></div>'
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
    # nice axis: pick a round step, four ticks
    raw = vmax / 4 if vmax else 1
    mag = 10 ** math.floor(math.log10(raw)) if raw > 0 else 1
    step = next(c * mag for c in (1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10) if c * mag >= raw)
    amax = step * 4
    n = len(items)
    slot = pw / n
    bw = min(bar_max, slot - 2)
    out = [f'<svg class="chart chart-v" viewBox="0 0 {W} {H}" role="img">']
    for k in range(5):
        val = step * k
        y = top + ph - ph * k / 4
        out.append(f'<line class="grid" x1="{left}" x2="{W-right}" y1="{y:.1f}" y2="{y:.1f}"/>')
        lbl = short(int(val)) if val >= 1 else (f"{val:g}" if val else "0")
        out.append(f'<text x="{left-8}" y="{y+4:.1f}" text-anchor="end">{lbl}</text>')
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
    out = [f'<svg class="chart chart-h" viewBox="0 0 {W} {H}" role="img">']
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

def sector_of(f):
    return CASE_ROWS[f][1] if f in CASE_ROWS else ""


def sector_line(f):
    return f'<p class="sector">{html.escape(sector_of(f))}</p>'


def todo(text):
    return f'<div class="todo">{text}</div>'

# ---------- data ----------

rows = list(csv.DictReader(open("comedy-week.csv", encoding="utf-8")))
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
    top5_cards = "".join(
        f'''<a class="reel" href="{r["link"]}"><span class="rank">#{i+1}</span>
      <b>{html.escape(r["creator"])}</b><span class="muted">{r["edition"]}</span>
      <span class="reel-n">{short(num(r["instagram"]))} views</span>
      <span class="go">Watch on Instagram &#8599;</span></a>'''
        for i, r in enumerate(ranked[:5]))
    cpm_items = [(ed_short(e), round(40000 / (sum(v) / 1000), 2),
                  f"{e}: 40000€ for {sum(v):,} views, {40000/(sum(v)/1000):.2f}€ per thousand")
                 for e, v in editions.items()]
    cpm_fig = figure(
        "Cost per thousand views, by edition",
        "Same budget every edition: 40000€. Only the season changes.",
        vbar(cpm_items, bar_max=90, height=280),
        table(["Edition", "Budget €", "Instagram views", "Cost per 1,000 views €"],
              [(e, "40,000", f"{sum(v):,}", f"{40000/(sum(v)/1000):.2f}") for e, v in editions.items()],
              numeric=(1, 2, 3)),
    )
    body = f"""<article class="w col">
<p class="eyebrow">Case study · Azzurro Club Vacanze · 2024–2025</p>
{sector_line("comedy-week.html")}
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
  <li>Built a tracking sheet with one row per collaboration: creator, edition, views per channel, link. <a href="comedy-week.csv">The raw data is in this repo.</a></li>
  <li>Used it to decide who to invite back and where to spend production time.</li>
</ul>

<h2>Results</h2>
{ed_fig}

<h2>What the data said</h2>
<h3>1. It's a long tail, not an average</h3>
<p>The mean video did {fmt(round(mean))} views; the median did {fmt(median)}. A gap of {mean/median:.0f}x means the average describes nothing. The top 10 videos produced {pct(top10/total_ig)} of reach; the other 33 together did {fmt(total_ig-top10)}.</p>
{rank_fig}

<h4>The five videos that carried it</h4>
<div class="reels">{top5_cards}</div>

<h3>2. Two creators carried 70%</h3>
<p>Giovanni d'Angella alone produced {pct(top_creator_share)} of all views, Chiara "Cammela" Anicito {pct(cammela_share)}. The other {len(creators)-2} acts shared the remaining {pct(1-top_creator_share-cammela_share)}.</p>
{d_fig}
<div class="insight"><p><b>The finding I'd defend in any meeting:</b> d'Angella's first video did 27,400 views, among the weakest of the first edition. His fourth did 8 million. Judged on the first collaboration, he would have been dropped. With creators, the value is in the second and third collaboration, so the first one should be treated as a test, not a verdict.</p></div>

<h3>3. Two of four channels weren't worth the work</h3>
<p>Instagram produced {fmt(total_ig)} views, YouTube {fmt(ch['youtube'])}, TikTok {fmt(ch['tiktok'])}, Facebook {fmt(ch['facebook'])}. Adapting every video for four channels cost production time; two of them returned almost nothing. YouTube was the exception worth watching: sporadic, but Marco Passiglia's Summer 2024 video did 1.4M there, more than on Instagram.</p>
{ch_fig}

<h2>What it cost</h2>
<p>Each edition ran on a dedicated budget of <b>40000€</b>, so the four editions cost about <b>160000€</b>. Charge all of it to reach and the programme delivered 32.8 million organic Instagram views at <b>4.88€ per thousand</b>, or 4.49€ counting the other channels.</p>
<p>That number is deliberately the worst case, because the fee was not buying a video. It was buying <b>a live show</b>: the comedians performed for guests, in the resort's arena in summer and in the group's theatres in winter, with a peak of about <b>800 people in the audience</b> for Chiara "Cammela" Anicito at the Lido di Savio village. The entertainment was already part of the guest experience the group sells. The videos were the by-product, which means the true marginal cost of those 32.8 million views was a fraction of 4.88€ per thousand.</p>
<figure class="photo two">
  <div>
    <img src="live-summer.jpg" width="1500" height="1000" alt="Full audience at a summer show in the resort arena" loading="lazy">
    <img src="live-winter.jpg" width="1500" height="999" alt="Scintilla Fubelli on stage during a winter edition" loading="lazy">
  </div>
  <figcaption>Summer: Chiara "Cammela" Anicito closing a show at the Lido di Savio village, about 800 people in the audience. Winter: Scintilla Fubelli on a theatre stage. The same fee paid for both the evening and the video.</figcaption>
</figure>

{cpm_fig}
<div class="insight"><p>The average hides the decision. The two summer editions delivered views at 3.13€ and 2.87€ per thousand; the two winter ones at 13.84€ and 12.47€, on exactly the same budget and the same format. Winter cost four times more per view, every time. That does not make winter wrong, because in winter the show filled the group's theatres and the audience in the room was the point. It does mean a winter edition had to be justified by attendance and by the guest experience, not by reach, and budgeting it as a marketing line was the mistake to avoid.</p></div>

<h2>One thing most people get wrong</h2>
<p>Creator programmes are usually evaluated per post and per creator, on the first result. That kills exactly the relationships that compound. Budget a first collaboration as a test, set the bar for a second one low, and decide on the second or third.</p>

<h2>What didn't work, and what's missing</h2>
<ul class="clean">
  <li><b>No cost per individual creator.</b> The budget is known per edition, not per act, so I can state a cost per thousand views for the programme but not which comedian delivered reach most cheaply. With per-creator fees, the two names carrying 70% of the reach could be priced against the other 26.</li>
  <li><b>Cross-channel tracking started late.</b> YouTube, TikTok and Facebook were tracked systematically only from Winter 2025, so channel totals understate the first two editions.</li>
  <li><b>No link to bookings.</b> Views were never tied to direct bookings, which was the business goal.</li>
</ul>
{next_links("comedy-week.html")}
</article>"""
    return page("Comedy Week case study · Luca Luperto",
                "How a comedy programme produced 32.8 million organic Instagram views, and what per-video tracking revealed.",
                body, "comedy-week.html", canon="comedy-week.html")


def kolms():
    clients = [
        ("Roseo Hotel Euroterme Wellness Resort", "Bagno di Romagna"),
        ("Grand Hotel da Vinci", "Cesenatico"),
        ("Grand Hotel Rimini", "Rimini"),
        ("Palace Hotel", "Milano Marittima"),
        ("Hotel Atlantic", "Rimini"),
        ("Hotel Litoraneo", "Riccione"),
        ("Hotel Cesa Tyrol", "Canazei"),
        ("Hotel Waldorf", "Milano Marittima"),
        ("Hotel Derby", "Milano Marittima"),
        ("Hotel Posillipo", "Gabicce Monte"),
        ("Hotel Nautico", "Canazei"),
        ("Hotel Conturina", "Canazei"),
        ("Hotel Lupo Bianco", "Canazei"),
        ("Hotel Astoria", "Riccione"),
        ("Das Post Hotel", "Zell am Ziller, Austria"),
    ]
    client_list = "".join(f'<li><b>{c}</b> <span class="muted">{loc}</span></li>' for c, loc in clients)
    works_data = [
        ("XB32aeEuvFM", "Hotel Waldorf", "Milano Marittima · 5-star luxury",
         "Property film: rooms, wellness and restaurant in one piece, cut for the hotel's own channels."),
        ("Z34dHeLaLwA", "Litoraneo Suite Hotel", "Rimini seafront",
         "Full video service for a seafront property, from the shoot plan to the formats published on social."),
        ("fjkOmv7LNKc", "La Settima Restaurant", "Hotel Waldorf, Milano Marittima",
         "The hotel restaurant sold as an experience in its own right, not as a hotel amenity."),
    ]
    works = "".join(
        f'''<a class="work" href="https://www.youtube.com/watch?v={vid}">
      <img loading="lazy" src="https://i.ytimg.com/vi/{vid}/maxresdefault.jpg" onerror="this.onerror=null;this.src='https://i.ytimg.com/vi/{vid}/mqdefault.jpg'" alt="{html.escape(name)}">
      <div class="work-t"><b>{html.escape(name)}</b><span class="muted">{html.escape(loc)}</span><span>{html.escape(note)}</span>
      <span class="go">Watch the film &#8599;</span></div></a>'''
        for vid, name, loc, note in works_data)
    funnel = [("Contacted", 143, "143 properties received a first DM"),
              ("Any answer", 49, "49 answered something: 23 people, 26 autoresponders"),
              ("Real reply", 23, "23 real replies, 16% of those contacted"),
              ("Call booked", 10, "10 turned into a call"),
              ("Signed", 2, "2 became paying clients")]
    funnel_fig = figure(
        "Outbound on Instagram, 2026",
        "One row per property: first DM, follow-up, and what came back.",
        hbar(funnel),
        table(["Stage", "Properties"], [(a, b) for a, b, _ in funnel], numeric=(1,)),
    )
    body = f"""<article class="w col">
<p class="eyebrow">Case study · Kolms Creative · 2023–present</p>
{sector_line("kolms-creative.html")}
<h1>Kolms Creative: selling content to hotels that had never bought it</h1>
<div class="meta"><span><b>Role</b> strategist &amp; account manager</span><span><b>Clients</b> 30+ properties</span><span><b>Alongside</b> a full-time marketing job</span></div>
<p class="lede">A four-person content studio for hotels, where I own the commercial side: finding the properties, pitching, scoping the work and keeping the accounts. This is the case study about selling, not about making.</p>

<div class="stats">
  <div class="stat"><b>30+</b><span>hotel clients</span></div>
  <div class="stat"><b>€110,000</b><span>in contracts closed</span></div>
  <div class="stat"><b>4</b><span>people in the studio</span></div>
  <div class="stat"><b>3</b><span>regions: Romagna, Dolomites, Austria</span></div>
</div>

<h2>Context</h2>
<p>A hotel lives on how it looks, but most independent properties have no one to produce that: the owner films a room tour on a phone, or an agency quotes a yearly retainer they can't justify. Kolms sits in between, a small studio with a video, photo and post-production team, selling defined content projects to four and five star hotels.</p>
<p>I am not behind the camera. I find the properties, run the meetings, scope and price the project, direct what the content has to say, and keep the client afterwards.</p>

<h2>What I do</h2>
<ul class="clean">
  <li><b>Prospecting:</b> cold email and Instagram DMs to properties whose positioning is better than their content, plus referrals from clients already served. Referrals close faster; cold outreach is what stops the pipeline from depending on them.</li>
  <li><b>Pitching and pricing:</b> turning a hotel's situation into a scoped project with a number attached, and negotiating it to signature.</li>
  <li><b>Creative direction:</b> deciding what the content has to say before anyone shoots. Seasonality, the territory and the experience, not a list of rooms.</li>
  <li><b>Account management:</b> the relationship after delivery, which is where the second and third project comes from.</li>
</ul>

<h2>Selected work</h2>
<p>Full video services, social content and photography for hotels in Romagna, the Dolomites and Austria.</p>
<div class="works">{works}</div>
<p class="muted">More work: <a href="https://www.kolmshotels.com">kolmshotels.com</a> · <a href="https://www.instagram.com/kolmscreative">@kolmscreative</a> on Instagram.</p>

<h2>Clients</h2>
<p>Properties the studio has worked with:</p>
<ul class="clean cols">{client_list}</ul>

<h2>One thing most people get wrong</h2>
<p>Hotels buy content as a list of assets: a pool video, a room tour, a drone shot. What sells a stay is the experience around those things, and the guest can only picture it if the content is built around a season, a place and a reason to come. Scoping the project by what the hotel needs to sell, rather than by how many clips it gets, is also what makes the price defensible.</p>

<h2>The funnel, once I started measuring it</h2>
<p>In 2026 I built the thing I should have had from the first month: a tracker with one row per property, its handle, the date of the first DM, the follow-up, and what came back. It covers a list of 243 properties, 143 of them contacted so far.</p>
{funnel_fig}
<p>Of 143 properties contacted, <b>23 replied for real</b>: 16%. Another 26 sent an automatic reply, which reads like a response and is worth nothing. Of those 23 conversations, <b>10 became a call and 2 became clients</b>.</p>
<div class="insight"><p>Read as rates, the funnel says something I had wrong: 1.4% of contacted properties end up signing, but <b>one call in five closes</b>. The problem was never the pitch or the price. It was that 94 properties out of 143 never answered a message at all, so the pitch rarely got to happen.</p></div>
<p>That changes what to fix. Not the proposal, not the deck: the first message, the sender's credibility, and the number of conversations started per week. A studio with recognisable work and a referral gets to have the call; a cold DM from an unknown account mostly does not.</p>

<h2>What didn't work</h2>
<p>The close rate was low, and for a reason I underestimated: luxury hospitality is a closed market that buys on reputation. Arriving by cold email or DM, with a studio nobody had heard of and few followers to point at, meant every conversation started from zero credibility. A 2500€ proposal would often get no answer at all, which is worse than a no because it tells you nothing.</p>
<p>What I would do differently, in order:</p>
<ul class="clean">
  <li><b>Build proof before selling.</b> Named work, a reference from a comparable property, numbers from a previous shoot. In this market one credible referrer is worth more than a hundred cold emails.</li>
  <li><b>Make the first commitment smaller.</b> A single shoot with one deliverable and a fixed price is a decision a hotel manager can take alone; a 2500€ project usually is not, and silence is often an internal approval that never happened.</li>
  <li><b>Treat the quote as the middle of the conversation, not the end.</b> A proposal sent and awaited has no follow-up built in. A proposal presented, with a date already set to review it, does.</li>
  <li><b>Measure the funnel.</b> I never tracked contacts, replies, meetings, quotes and signatures as a sequence, so I could see that closing was hard but not <em>where</em> it broke. That is the first thing I would instrument now.</li>
</ul>
{next_links("kolms-creative.html")}
</article>"""
    return page("Kolms Creative case study · Luca Luperto",
                "Selling content projects to 30+ luxury hotels: prospecting, pricing and account management.",
                body, "kolms-creative.html", canon="kolms-creative.html")


IFP_MONTHS = [
    ("2024-01", 2), ("2024-02", 3), ("2024-03", 5), ("2024-04", 13), ("2024-05", 17), ("2024-06", 21),
    ("2024-07", 21), ("2024-08", 15), ("2024-09", 14), ("2024-10", 16), ("2024-11", 18), ("2024-12", 17),
    ("2025-01", 10), ("2025-02", 12), ("2025-03", 14), ("2025-04", 16), ("2025-05", 18), ("2025-06", 21),
    ("2025-07", 20), ("2025-08", 14), ("2025-09", 11), ("2025-10", 17), ("2025-11", 18), ("2025-12", 22),
]
IFP_TOP = [
    ("2024-07-12", 1600000, "https://www.instagram.com/ifpemilia/reel/C9UY7i1Igey/"),
    ("2024-07-29", 1300000, "https://www.instagram.com/ifpemilia/reel/C-A4I8ToLxA/"),
    ("2025-02-28", 1100000, "https://www.instagram.com/ifpemilia/reel/DGnPu3UoCPc/"),
    ("2025-06-05", 1000000, "https://www.instagram.com/ifpemilia/reel/DKg9XMzIXXV/"),
    ("2024-07-09", 1000000, "https://www.instagram.com/ifpemilia/reel/C9Mq0b7oD5-/"),
    ("2025-09-04", 642000, "https://www.instagram.com/ifpemilia/reel/DOLSIcdgdFd/"),
]
IFP_TOTAL_REELS = 332
IFP_TOTAL_VIEWS = 31693506


def ifp():
    def lab(m):
        y, mo = m.split("-")
        names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        return names[int(mo) - 1] + (" '" + y[2:] if mo in ("01",) else "")
    items = [(lab(m), n, f"{m}: {n} reels published") for m, n in IFP_MONTHS]
    prod_fig = figure(
        "Reels published per month",
        "January to March 2024 is the three months before the new workflow: 2 to 5 reels a month. From April on, never fewer than 10.",
        vbar(items, bar_max=26, height=300, label_every=3, value_idx=set(), show_values=False),
        table(["Month", "Reels"], [(m, n) for m, n in IFP_MONTHS], numeric=(1,)),
    )
    top_cards = "".join(
        f'''<a class="reel" href="{u}"><span class="rank">#{i+1}</span>
      <b>{short(v)} views</b><span class="muted">{d}</span>
      <span class="go">Watch on Instagram &#8599;</span></a>'''
        for i, (d, v, u) in enumerate(IFP_TOP))
    before = sum(n for m, n in IFP_MONTHS[:3]) / 3
    after = sum(n for m, n in IFP_MONTHS[3:]) / 21
    channels = [("Instagram", 92400, "Instagram: 92,400 followers"),
                ("TikTok", 76100, "TikTok: 76,100 followers, 1.8M likes"),
                ("Facebook", 23343, "Facebook: 23,343 followers"),
                ("YouTube", 2830, "YouTube: 2,830 subscribers across 369 videos")]
    chan_fig = figure(
        "Followers by channel, September 2026",
        "Same videos, same upload, four channels.",
        hbar(channels),
        table(["Channel", "Followers"], [(a, f"{b:,}") for a, b, _ in channels], numeric=(1,)),
    )
    body = f"""<article class="w col">
<p class="eyebrow">Case study · Italy Food PRN · May 2024 – Dec 2025</p>
{sector_line("italy-food-prn.html")}
<h1>Italy Food PRN: publishing five times more, with the same two hands</h1>
<div class="meta"><span><b>Role</b> project manager</span><span><b>Region</b> Emilia-Romagna</span><span><b>Channels</b> Instagram, TikTok, YouTube, Facebook</span></div>
<p class="lede">A regional food publisher with an audience to build from zero. The constraint was never ideas, it was throughput: how many good videos could leave the door each week. So the job became rebuilding the production line.</p>

<div class="stats">
  <div class="stat"><b>{IFP_TOTAL_REELS}</b><span>reels published in 20 months</span></div>
  <div class="stat"><b>{short(IFP_TOTAL_VIEWS)}</b><span>Instagram views on those reels</span></div>
  <div class="stat"><b>{before:.0f} &rarr; {after:.0f}</b><span>reels per month, before and after</span></div>
  <div class="stat"><b>80,000+</b><span>followers gained in 18 months</span></div>
</div>

<h2>Context</h2>
<p>Italy Food PRN covers food experiences across Emilia-Romagna for more than 15 local partners, on four platforms at once. Every restaurant visit produces raw footage; the value only appears when that footage is published, in the right format, on every channel, quickly enough to stay current.</p>
<p>When I took the project over, the account was publishing two to five reels a month. The editorial plan was not the bottleneck. Everything between a finished shoot and a scheduled post was: subtitles, cover, caption, hashtags, then repeating it by hand for each platform.</p>

<h2>What I did</h2>
<p>I rebuilt the publishing step into a fixed sequence and timed it until one reel took <b>seven minutes</b> end to end, which is what makes 20 to 25 pieces a week possible without a team.</p>
<ol class="clean">
  <li><b>Set the rails once.</b> A Canva project for covers, a fixed subtitle style, a ChatGPT project holding the tone of voice, the recurring hashtags and the hook rules, and every channel connected in the scheduler.</li>
  <li><b>Subtitles first, on mobile.</b> The raw file goes from Drive into an AI subtitle tool; this single step carries most of the speed.</li>
  <li><b>Export and keep the transcript.</b> The transcript is the input for the next step, so it never has to be typed.</li>
  <li><b>Caption from the transcript.</b> The transcript goes into the ChatGPT project, which returns a caption already in the right voice. It always gets reread and humanised, and every correction is fed back as an example.</li>
  <li><b>Cover and schedule.</b> Five title options from the same transcript, one cover in Canva, then a single upload that schedules Instagram, TikTok, YouTube and Facebook together.</li>
</ol>
<p class="muted">Tools: Google Drive, Captions, ChatGPT, Canva, Publer. Write-up of the full workflow: <a href="https://www.linkedin.com/pulse/pubblicare-20-reel-settimana-senza-impazzire-ecco-il-sistema-luperto-og7uf/">Publishing 20 reels a week without losing your mind</a>.</p>

<h2>What happened to output</h2>
{prod_fig}
<div class="insight"><p>The three months before the new workflow averaged {before:.1f} reels a month. The twenty-one months after averaged {after:.1f}, and never dropped below ten, including August, Christmas and every other month that usually kills a publishing calendar. Same person, same shooting days.</p></div>

<h2>The reels that travelled</h2>
<p>Across those 20 months the {IFP_TOTAL_REELS} reels collected {IFP_TOTAL_VIEWS:,} views on Instagram alone. The five biggest account for about 19% of that, which is a much flatter distribution than a creator programme: here the reach comes from volume and consistency rather than from a handful of hits.</p>
<div class="reels">{top_cards}</div>

<h2>Four channels, three audiences</h2>
<p>Everything published went out on Instagram, TikTok, Facebook and YouTube from the same upload. Three years in, the audiences look like this.</p>
{chan_fig}
<p>Instagram and TikTok carry the project: about 168,000 followers between them, with 1.8 million likes on TikTok alone. Facebook holds a real but smaller audience that skews older and local, which is exactly the one regional partners care about. YouTube received the same 369 videos and never took off: single shorts land in the thousands of views, against tens or hundreds of thousands on Instagram.</p>
<div class="insight"><p>Cross-posting from one upload costs almost nothing, so keeping a channel that underperforms is defensible — as long as it stays a by-product. It stops being defensible the moment someone starts cutting, titling and thumbnailing for it. That was the rule: same export everywhere, effort only where the audience already is.</p></div>

<h2>What the audience was for</h2>
<p>An audience of this kind pays for itself in two ways: the local partners the project was built to serve, and brand campaigns that rent the format. The clearest example is a <b>Deliveroo</b> shoot in Parma in October 2024, produced end to end: a travel-and-food piece where the talent orders from a local restaurant, receives the delivery in front of the Pilotta, tastes the dish, then goes into the kitchen to watch the tortelli being made and packs them for the next order.</p>
<p>Two things made it work as a piece of client work rather than an ad dropped into an editorial feed. The product appears as part of the story, not as a banner: the order, the rider, the bag, all inside a sequence a viewer would watch anyway. And the format is the same one the account publishes every week, so the sponsored piece does not feel like a foreign object on the profile.</p>

<h2>One thing most people get wrong</h2>
<p>Teams treat publishing as the boring end of the process and protect the creative start instead. But the publishing step is where the calendar actually dies: when a post takes forty minutes, the third video of the day never goes out. Time that step, take it apart, and the editorial plan you already had starts working.</p>

<h2>What didn't work</h2>
<ul class="clean">
  <li><b>Volume does not buy reach on its own.</b> August 2024 published 15 reels and collected fewer views than months with the same output. Monthly totals swung by four times regardless of how much went out, because reach depends on the subject and the hook, not on the count.</li>
  <li><b>The AI-written caption is a draft, never the final text.</b> Left unedited it reads generic and flattens the account's voice; the rule became that every caption gets rewritten by hand before scheduling.</li>
  <li><b>No link between views and partner value.</b> Reach was measured, but what those views did for the 15+ local partners, or for a brand campaign like the Deliveroo one, was never tracked beyond the view count. That is the number I would instrument first if I did it again.</li>
</ul>
<p class="muted">Figures read from the public @ifpemilia profile in September 2026: every reel published in the period, with its view count and its publication date.</p>
{next_links("italy-food-prn.html")}
</article>"""
    return page("Italy Food PRN case study · Luca Luperto",
                "Rebuilding content production so a regional food publisher could publish five times more, and what that did for reach.",
                body, "italy-food-prn.html", canon="italy-food-prn.html")


AZ_CREATIVE = [
    ("Alexander", "pool from above + flag", [2.10, 2.96, 3.87]),
    ("Classic", "pool from above / ball", [1.21, 13.70, 4.90]),
    ("Tokio", "4k video / ball", [2.27, 9.65, 8.46]),
    ("Mediterraneo", "ball", [1.56, None, None]),
    ("Marina Beach", "hotel + pool", [8.30, None, None]),
    ("King", "hotel front + pool", [9.70, None, None]),
]


def azzurro():
    rows = list(csv.DictReader(open("azzurro-ads.csv", encoding="utf-8")))
    weeks = [r["week"] for r in rows]
    leads = [int(r["leads"]) for r in rows]
    cpl = [float(r["cpl_eur"]) for r in rows]
    lpv = [int(r["landing_views"]) for r in rows]
    spend = sum(float(r["spend_eur"]) for r in rows)
    tot_leads = sum(leads)
    clicks = sum(int(r["clicks"]) for r in rows)
    impr = sum(int(r["impressions"]) for r in rows)
    peak_i = leads.index(max(leads))
    lead_fig = figure(
        "Leads per week",
        "Twelve weeks of the same lead campaign, at a nearly flat weekly budget.",
        vbar([(w.split("-")[0], v, f"{w}: {v:,} leads, €{float(rows[i]['spend_eur']):,.0f} spent")
              for i, (w, v) in enumerate(zip(weeks, leads))],
             bar_max=34, height=300, label_every=2, value_idx={peak_i}),
        table(["Week", "Spend €", "Leads", "Cost per lead €"],
              [(r["week"], r["spend_eur"], r["leads"], r["cpl_eur"]) for r in rows], numeric=(1, 2, 3)),
    )
    conv = [round(l / v * 100, 1) for l, v in zip(leads, lpv)]
    conv_fig = figure(
        "Landing page views that became a lead (%)",
        "Traffic held up in January. What stopped was the conversion on the page.",
        vbar([(w.split("-")[0], c, f"{w}: {c}% of {lpv[i]:,} landing page views became leads")
              for i, (w, c) in enumerate(zip(weeks, conv))],
             bar_max=34, height=280, label_every=2, value_idx={0, len(conv) - 1}),
        table(["Week", "Landing page views", "Leads", "Conversion %"],
              [(r["week"], r["landing_views"], r["leads"], f"{c}%") for r, c in zip(rows, conv)], numeric=(1, 2, 3)),
    )
    cre_rows = []
    for name, hook, vals in AZ_CREATIVE:
        cre_rows.append((name, hook, *[f"€{v:.2f}" if v else "—" for v in vals]))
    dec_leads, dec_spend = sum(leads[:8]), sum(float(r["spend_eur"]) for r in rows[:8])
    jan_leads, jan_spend = sum(leads[8:]), sum(float(r["spend_eur"]) for r in rows[8:])
    social_rows = [
        ("Instagram", "+8,300 &rarr; 10,300", "496", "32,810,205"),
        ("YouTube", "+6,109", "—", "2,759,817"),
        ("Facebook", "+5,000", "—", "19,807"),
        ("TikTok", "2,404 (from zero)", "—", "51,248"),
    ]
    social_fig = figure(
        "Owned audience vs borrowed reach",
        "Followers on the group account, against the views the comedy programme produced on each channel.",
        hbar([("Instagram", 32810205, "Instagram: 32,810,205 programme views, ~10,300 followers"),
              ("YouTube", 2759817, "YouTube: 2,759,817 programme views"),
              ("TikTok", 51248, "TikTok: 51,248 programme views, 2,404 followers"),
              ("Facebook", 19807, "Facebook: 19,807 programme views")]),
        table(["Channel", "Followers gained", "Posts published", "Views from the programme"], social_rows, numeric=(1, 2, 3)),
    )
    az_top_data = [
        ("Resort content", "August 2025", 868000, "https://www.instagram.com/azzurroclubvacanze/reel/DNz7z-o2OI8/"),
        ("Resort content", "November 2025", 693000, "https://www.instagram.com/azzurroclubvacanze/reel/DQvpLzcD0UA/"),
        ("Resort content", "December 2025", 311000, "https://www.instagram.com/azzurroclubvacanze/reel/DSITLCJjylN/"),
        ("Resort content", "December 2025", 231000, "https://www.instagram.com/azzurroclubvacanze/reel/DSkDTFCDZki/"),
        ("Resort content", "November 2025", 224000, "https://www.instagram.com/azzurroclubvacanze/reel/DRfHBqDk4SO/"),
        ("Resort content", "December 2025", 200000, "https://www.instagram.com/azzurroclubvacanze/reel/DSC7saIjANA/"),
    ]
    az_top = "".join(
        f'''<a class="reel" href="{u}"><span class="rank">#{i+1}</span>
      <b>{html.escape(n)}</b><span class="muted">{e}</span>
      <span class="reel-n">{short(v)} views</span>
      <span class="go">Watch on Instagram &#8599;</span></a>'''
        for i, (n, e, v, u) in enumerate(az_top_data))
    email_fig = ('<figure><figcaption>Two email systems, one guest</figcaption>'
                 '<div class="sub">The group ran promotional and transactional email on separate stacks, '
                 'with separate senders and separate data.</div>'
                 + table(["", "Promotional (MailUp)", "Transactional (booking system &amp; app)"],
                         [("Sender", "one group address", "one address per property"),
                          ("Register", "informal, emoji, imperatives", "formal, no emoji, no urgency"),
                          ("Personalisation", "none", "name, property, dates, party size, loyalty credit"),
                          ("Job", "generate a lead for the call centre", "run the stay and the loyalty loop")])
                 + '</figure>')
    body = f"""<article class="w col">
<p class="eyebrow">Case study · Azzurro Club Vacanze · Dec 2022 – Feb 2026</p>
{sector_line("azzurro-ads.html")}
<h1>Azzurro Club Vacanze: owning the direct channel of 13 hotels</h1>
<div class="meta"><span><b>Role</b> digital marketing specialist</span><span><b>Portfolio</b> 13 hotels</span><span><b>Budget</b> ~200000€ per year</span></div>
<p class="lede">After COVID the group needed its own booking channel instead of paying commission on most online sales. Direct online bookings went from 20% to 70% of revenue in two years. Five things did that work: advertising, email, content, influencer marketing and a national comedy programme. Here is each one, including the four weeks when the best campaign stopped working.</p>

<div class="stats">
  <div class="stat"><b>{tot_leads:,}</b><span>leads in 12 weeks</span></div>
  <div class="stat"><b>€{spend:,.0f}</b><span>media spend on this campaign</span></div>
  <div class="stat"><b>€{spend/tot_leads:.2f}</b><span>average cost per lead</span></div>
  <div class="stat"><b>{clicks/impr*100:.2f}%</b><span>click-through rate, {impr/1e6:.1f}M impressions</span></div>
</div>

<h2>Context</h2>
<p>Every booking made through an online travel agency costs the hotel a commission of roughly 15 to 20 percent. The direct channel has no commission, but it has to be built and fed: paid social to create demand, brand search so the intent already there is not bought by someone else, and email to bring back guests who had already stayed.</p>
<p>This campaign ran on Meta over twelve winter weeks, collecting leads for the summer season across the group's seaside properties at a roughly constant weekly budget.</p>

<h2>What I owned</h2>
<p>A budget of roughly 200000€ a year across paid media, talent, agency fees and production, reallocated weekly between channels on the basis of what the reporting said. Five areas, one goal: make the hotel's own channel cheaper than the commission.</p>
<ul class="clean">
  <li><b>Advertising</b> — Meta and Google Ads, lead campaigns for the season, brand search so intent already in the market was not bought by an intermediary.</li>
  <li><b>Email marketing and CRM</b> — reactivating a database of past guests before they booked again through a platform.</li>
  <li><b>Content strategy</b> — the editorial product for 13 properties, built to sell stays rather than to fill a calendar.</li>
  <li><b>Influencer marketing</b> — talent partnerships across properties and seasons.</li>
  <li><b>The comedy programme</b> — four national editions, the cheapest reach the group ever bought.</li>
</ul>

<h2>Advertising</h2>
{lead_fig}
<p>The first eight weeks produced <b>{dec_leads:,} leads for €{dec_spend:,.0f}</b>, an average of €{dec_spend/dec_leads:.2f} each, with the best week over the holidays at €0.49. The last four weeks produced <b>{jan_leads} leads for €{jan_spend:,.0f}</b>: €{jan_spend/jan_leads:.2f} each, roughly fifteen times more expensive for the same money.</p>

<h2>Where it broke</h2>
<p>The obvious reading is that the audience got tired. The data says otherwise: impressions and clicks stayed in the same range in January, and the landing page kept receiving thousands of visits. What changed is what happened on the page.</p>
{conv_fig}
<div class="insight"><p>In the last week of December, 28% of landing page views became a lead. Two weeks later it was under 4%, with the same ads bringing the same volume of people to the same page. The media was still working; something on the page was not. Watching only the cost per lead would have sent me to rebuild creatives, which is the expensive way to fix the wrong thing.</p></div>
<p><b>I still cannot say what changed that week</b>, and that is the actual finding. A holiday offer expiring, a form field breaking, a page edit made elsewhere in the company: any of them fits the shape of the data, and nothing in the setup could tell them apart, because only the ad account was instrumented. The first thing I would build now is the boring one: page-level conversion tracking with an alert, so a drop this size shows up on day two instead of week four.</p>

<h2>Creative, hotel by hotel</h2>
<p>The same offer, the same weeks, six properties: the cost per lead moved by a factor of eight depending on which opening image was used. A pool shot from above and the flag ran cheap and stayed cheap; a ball as the opening frame worked once and then stopped.</p>
{table(["Property", "Opening frame", "Round 1", "Round 2", "Round 3"], cre_rows)}
<p>The decision this produced was simple: port the winning opening frame across properties instead of writing new scripts, and keep two variants per hotel in rotation so a fatigued hook never takes a whole property down with it.</p>

<h2>Email marketing and CRM</h2>
<p>The most valuable audience a hotel group has is the guests it already served, and the most expensive mistake is letting them come back through a platform that charges commission on a relationship the hotel had already earned. Email was the channel meant to stop that. Read as a system, it was two systems.</p>

{email_fig}

<p><b>The promotional side</b> went out from one group address through MailUp: seasonal offers, one property or the whole group, written in the second person singular with emoji in the subject line, built on four levers that never changed — a time hook ("September is the new August"), an experiential promise, a stack of imperatives, and scarcity. <b>The transactional side</b> lived in the booking system and the app, with a different sender per property, a formal register, and something the promotional side never had: the guest's name, their property, their dates, the size of the party, their loyalty credit.</p>

<h3>The lifecycle, as it actually ran</h3>
<ul class="clean">
  <li><b>Cold opt-in list</b> &rarr; seasonal offer emails, no personalisation at all.</li>
  <li><b>Quote not converted</b> &rarr; two dedicated flows: a "price freeze" that re-confirmed the old quote's conditions in full, and a re-activation that quoted back the exact period and party size the guest had asked for the year before. This was the sharpest piece of the whole programme.</li>
  <li><b>Booked</b> &rarr; pre-check-in data collection and menu pre-ordering through the app.</li>
  <li><b>Checked out</b> &rarr; loyalty credit plus a stay questionnaire.</li>
  <li><b>Loyal guest</b> &rarr; a "customer week" with earned access ("you are receiving this because you qualified"), a 25% welcome-back discount on a second stay, and a 10€ referral for bringing a friend.</li>
</ul>

<div class="insight"><p>The best sequence in the group was the cross-sell cascade. The thank-you email at the end of the summer season closed the sea cycle and, in the same message, sold autumn weekends with theme parks and reminded the guest that the ski price freeze expired on 30 September. Three offers stacked on a contact who had just walked out of the hotel, at the one moment their goodwill was highest.</p></div>

<h3>How the database was segmented</h3>
<p>Five axes, of very different maturity: <b>season and product</b> (Riviera in summer, mountains in winter, with spring bridges and an autumn tail deliberately covered), <b>property</b> — each single-hotel email carried that property's own phone number so the call landed where the availability was, <b>party composition</b>, mostly families with children but explicitly broadened in the mountains to couples and groups of friends, <b>lifecycle stage</b> as above, and <b>price tier</b>, with the same database worked at 1,599–2,399€ a room in August, 999€ a week in September, and 139–299€ tickets for bridges and snow.</p>

<h3>What was wrong with it, and what I would change</h3>
<ul class="clean">
  <li><b>The data was in the wrong system.</b> Everything needed to personalise a promotional email — which property, which dates, how many people, how much credit — existed in the transactional side and was never used by the promotional side. That is the single biggest miss, and it is an integration problem before it is a marketing one.</li>
  <li><b>No email could close a sale.</b> Even the fixed-price offer ended in "request a quote": every campaign fed the call centre. It fits a family audience that wants to speak to a person, but it makes revenue dependent on phone capacity and hides where the funnel actually leaks.</li>
  <li><b>Pressure instead of testing.</b> The same spring creative went out four times in six weeks. There was no subject line test, no holdout, no frequency cap by segment: volume was doing the work that segmentation should have done.</li>
  <li><b>Two voices, sometimes in one email.</b> The promotional register switched between informal and formal mid-message, with recurring typos in the templates. Small, but it is the kind of detail that tells a guest which emails are automated.</li>
</ul>
<p class="muted">What I cannot show here: database size, open and click rates and the revenue attributed to email are in the group's systems and I did not keep a copy. The structure above is reconstructed from the campaigns themselves.</p>

<h2>Content strategy: the product and the results</h2>
<p>Thirteen properties, one group, and a decision to make every week: what does each hotel publish, and what is it supposed to sell. The content was treated as a product with a job, not as a calendar to fill.</p>
<ul class="clean">
  <li><b>One positioning per property.</b> A four star family village on the Adriatic and a five star hotel in the Dolomites share an owner and nothing else. Each had its own formats, its own promise and its own season to defend.</li>
  <li><b>Formats chosen by what they had to do:</b> the room and the pool to answer "where will I sleep", food and experiences to answer "what will we do", staff and events to answer "will I feel welcome".</li>
  <li><b>Production planned around the season</b>, so the summer offer was shot in spring and the winter campaign had images that were not two years old.</li>
  <li><b>The result the content was measured on</b> was not engagement: it was whether the direct channel kept growing. Over two years it went from 20% to 70% of online revenue.</li>
</ul>

<h2>Influencer marketing</h2>
<p>Talent was used for two different jobs, and keeping them separate is what made the budget work. Creators with a local audience to make a specific property credible in a specific season, and national comedians to give the group reach it could not buy at that price anywhere else.</p>
<p>The brief was always the same: the property is the set, not the sponsor. A piece that could have been filmed anywhere sells nothing, so every collaboration had to use something only that hotel had.</p>
<p>And the fee bought two things at once. The comedian performed live for guests, on the resort stage in summer and in the group's theatres in winter, so the same money paid for entertainment the guests had come for and for the content that travelled far beyond them. That double duty, not the view count, is what made the programme defensible in a budget meeting.</p>

<h2>Comedy Week</h2>
<p>The programme that came out of this: four editions, 28 comedians, 47 collaborations, <b>32.8 million organic Instagram views with no paid amplification</b>, on a dedicated budget of 40000€ per edition. That is 4.88€ per thousand views across the programme, and the seasonal split matters more than the average: summer editions delivered views at around 3€ per thousand, winter editions at over 12€.</p>
<p>Tracking it video by video is what turned it from a nice number into a decision: five videos out of 43 carried 63% of the reach, two creators produced 70% of it, and the act with the worst debut became the best performer of the programme. <a href="comedy-week.html">The full analysis is here &rarr;</a></p>

<h2>The social channels, and what they returned</h2>
<p>Between December 2022 and January 2026 the group's Instagram account published <b>496 pieces</b>: 258 reels and 238 photo posts, roughly one every two days for three years, across 13 properties and two seasons a year. Over the same period the audience grew by about <b>8,300 followers on Instagram, 6,109 subscribers on YouTube and 5,000 on Facebook</b>, while TikTok was started from zero and reached 2,404.</p>
<p>And here is the uncomfortable comparison: the audience the group owns, against the reach the comedy programme produced on the same channels.</p>
{social_fig}
<div class="insight"><p>32.8 million views on Instagram sit next to an account with about 10,000 followers. Reach borrowed from creators and from the algorithm does not turn itself into an owned audience: people watch the comedian, laugh, and scroll on. Treating those views as audience growth would have been the easy mistake; the honest reading is that they were paid media at organic prices, to be judged on bookings, not on followers.</p></div>
<p>It also explains where effort stopped going. TikTok and Facebook received the same videos and returned roughly 0.2% of the programme's reach, so they stayed a by-product of one upload rather than a channel with its own production. YouTube behaved differently: sporadic, but when a video landed it landed hard, with one piece doing 1.4 million views there against 1.3 million on Instagram.</p>

<h2>The videos that travelled</h2>
<p>The comedy programme is a case study of its own, so these are the best performing pieces <b>without a comedian in them</b>: ordinary resort content, published in the normal editorial rhythm, between 200,000 and 868,000 views each. They are the proof that the account could travel on its own material, at a fraction of the reach but at a fraction of the cost.</p>
<div class="reels">{az_top}</div>

<h2>One thing most people get wrong</h2>
<p>Lead campaigns get judged on cost per lead, which mixes together three different things: how cheaply you buy attention, how well the page converts, and how good the offer is. Split them and the diagnosis takes minutes instead of a week. Cost per click tells you about the auction, conversion rate tells you about the page, and only the two together tell you what to change.</p>

<h2>What didn't work, and what's missing</h2>
<ul class="clean">
  <li><b>Nobody was watching the page.</b> The ad account had alerts, the landing page did not, so four weeks and about €4,500 went by before the drop was obvious.</li>
  <li><b>Leads are not bookings.</b> This dataset stops at the form. What those 9,134 leads produced in confirmed stays was tracked elsewhere and never tied back to media spend, so I cannot state a cost per booking for this campaign.</li>
  <li><b>No holdout.</b> With a small share of the audience kept out of the campaign, the share of bookings that would have happened anyway would be a number instead of an argument.</li>
</ul>
<p class="muted">Figures from the campaign reporting sheet: twelve weeks, spend, impressions, clicks, landing page views and leads per week. <a href="azzurro-ads.csv">The weekly data is in this repo.</a></p>
{next_links("azzurro-ads.html")}
</article>"""
    return page("Azzurro ads case study · Luca Luperto",
                "9,134 leads in twelve weeks, and how weekly data showed the funnel broke on the page, not in the ads.",
                body, "azzurro-ads.html", canon="azzurro-ads.html")



CASE_ROWS = {
  "comedy-week.html": ("Comedy Week", "Hospitality · Creator marketing · Organic",
    "A comedy programme across 13 hotels. Tracking it video by video showed that 5 of 43 videos carried 63% of the reach, that two creators produced 70% of it, and that the act with the worst debut became the best performer.",
    "32.8M", "organic views · 0€ paid"),
  "kolms-creative.html": ("Kolms Creative", "B2B services · Sales · Content",
    "Selling content projects to luxury hotels: cold outreach, pricing and account management, with an honest account of why the close rate stayed low in a market that buys on reputation.",
    "30+", "hotel clients · 110000€ closed"),
  "azzurro-ads.html": ("Azzurro ads", "Hospitality · Paid media · CRM",
    "Moving a 13-hotel group off OTA dependence with paid social, brand search and email reactivation.",
    "20% → 70%", "direct bookings on revenue"),
  "italy-food-prn.html": ("Italy Food PRN", "Food media · Content operations",
    "A regional food publisher grown from zero by finding the formats that reached new people and rebuilding how they were produced.",
    "80,000+", "followers in 18 months"),
}

TILES = [
  ("big", "https://www.instagram.com/azzurroclubvacanze/reel/DL9HqK9iDV3/", None, "t-a",
   "8M", "Comedy Week · Giovanni d'Angella", "single reel, organic"),
  ("small", "https://www.youtube.com/watch?v=XB32aeEuvFM", "XB32aeEuvFM", "",
   None, "Hotel Waldorf", "property film"),
  ("third", "https://www.instagram.com/azzurroclubvacanze/reel/C9FhJ9oobw7/", None, "t-b",
   "5.6M", "Cammela", "Comedy Week"),
  ("third", "https://www.youtube.com/watch?v=Z34dHeLaLwA", "Z34dHeLaLwA", "",
   None, "Litoraneo Suite", "full video service"),
  ("third", "https://www.youtube.com/watch?v=fjkOmv7LNKc", "fjkOmv7LNKc", "",
   None, "La Settima", "hotel restaurant"),
]

BRANDS = ["Azzurro Club Vacanze", "Italy Food PRN", "Kolms Creative", "Roseo Euroterme",
          "Grand Hotel da Vinci", "Hotel Waldorf", "Das Post Hotel"]


def index():
    tiles = ""
    for size, href, vid, grad, big, name, note in TILES:
        inner = (f'<img loading="lazy" src="https://i.ytimg.com/vi/{vid}/maxresdefault.jpg" '
                 f'onerror="this.onerror=null;this.src=\'https://i.ytimg.com/vi/{vid}/mqdefault.jpg\'" '
                 f'alt="{html.escape(name)}">'
                 if vid else f'<span class="num-tile">{big}</span>')
        tiles += (f'<a class="tile {size} {grad}" href="{href}">{inner}'
                  f'<span class="lab"><b>{html.escape(name)}</b><span>{html.escape(note)}</span></span>'
                  f'<span class="play">Watch &#8599;</span></a>')
    rows = ""
    for f, _ in CASES:
        t, sector, d, k, ks = CASE_ROWS[f]
        rows += (f'<a class="case" href="{f}"><div><h3>{html.escape(t)}</h3>'
                 f'<p class="sector">{html.escape(sector)}</p><p>{html.escape(d)}</p></div>'
                 f'<div class="kpi"><b>{k}</b><span>{ks}</span></div></a>')
    coming = [CASE_ROWS[f][0] for f, _ in ALL_CASES if f not in PUBLISHED]
    coming_line = (f'<p class="muted" style="margin-top:18px">In preparation: {", ".join(coming)}. '
                   f'<a href="mailto:{EMAIL}">Ask me about them.</a></p>' if coming else "")
    brands = "".join(f"<b>{b}</b>" for b in BRANDS)
    body = f"""<section class="w">
<div class="hero">
  <p class="hero-name">Luca Luperto — Growth &amp; Lifecycle Marketing</p>
  <h1>Direct bookings went from 20% to 70% of revenue.</h1>
  <p class="lede">Three years owning the marketing of a 13-hotel group: paid acquisition, the CRM and email programme, content, influencer marketing, and a live format that ran four times.</p>
  <p class="belief">I believe in marketing where data and analysis come together: to read what people actually want, and to build the services and offers that improve the quality of their days.</p>
  <span class="avail">Milan · EU citizen · Travel &amp; hospitality</span>
</div>

<div class="gal">{tiles}</div>

<div class="num-row">
  <div class="num"><b>20% &rarr; 70%</b><span>direct online bookings on revenue, 13 hotels, two years</span></div>
  <div class="num"><b>32.8M</b><span>organic Instagram views, zero paid amplification</span></div>
  <div class="num"><b>€110,000</b><span>in content contracts closed alongside a full-time job</span></div>
</div>

<div class="sec-h"><h2>Case studies</h2><span>{len(CASES)} of {len(ALL_CASES)} published</span></div>
{rows}
{coming_line}
<div class="brands">{brands}</div>

<div class="sec-h" id="about" style="margin-top:44px"><h2>About</h2><span>Milan &rarr; Dublin</span></div>
<div class="about">
  <div>
    <p>I did not arrive at marketing through a business degree. I spent my first years at art school in Cuneo, learning composition, light, and why one image holds a person for three seconds while the one next to it does not. Then a master's in Milan, where the question changed: what happens to that attention once a company needs it to become a decision.</p>
    <p>Hospitality is where the two halves met. A hotel is a chain you can see end to end: someone watches a video on a Tuesday night in February and sleeps in a room in July, and between those two moments there are a hundred small decisions you can either guess at or measure. I spent three years measuring them, and the surprise was that the interesting answers were almost never the ones I expected.</p>
    <p>Alongside that I built a content service with three other people and sold it myself, which taught me the part of marketing you cannot learn from a dashboard: pricing your own work, sending a proposal, and living with the silence that follows.</p>
    <p><b>What I believe:</b> marketing works when data and analysis come together with the craft, not against it. Numbers are not the opposite of creativity, they are what tells you which creative act was worth repeating. And the point of the whole exercise is not the click: it is finding what people actually want, and building the service or the offer that makes their days a little better.</p>
    <p>Next chapter: a company with its own users and its own data, where lifecycle and growth are somebody's job rather than an afterthought. I am moving north for it, and I am bringing the habit of writing down what did not work.</p>
  </div>
  <div class="about-side">
    <img class="portrait" src="portrait.png" width="680" height="610" alt="Luca Luperto" loading="lazy">
    <h4>How I work</h4>
    <ul class="clean">
      <li>Start from the metric that is actually broken, with its starting value.</li>
      <li>Write the hypothesis down before acting: changing X to Y will move Z, because…</li>
      <li>Keep a holdout, even a small one, so the result means something.</li>
      <li>Report what did not work with the same detail as what did.</li>
    </ul>
    <h4>Background</h4>
    <p class="muted">MSc Digital Content Management, Università Cattolica, Milan · BA Fine Arts, Accademia di Belle Arti, Cuneo · Italian (native), English (professional) · Meta Ads, Google Ads, GA4, MailUp, Excel</p>
  </div>
</div>

<div class="cta">
  <p>If any of this sounds like the person you need, the fastest way to find out is a conversation.</p>
  <div class="cta-links">
    <a class="btn primary" href="mailto:{EMAIL}">Write to me</a>
    <a class="btn" href="{CV}">Download CV (PDF)</a>
  </div>
</div>


<div class="sec-h" id="contact" style="margin-top:44px"><h2>Contact</h2><span>Open to offers</span></div>
<div class="contact">
  <div>
    <p>I am looking for a <b>growth, lifecycle or CRM role</b> in Dublin, or remote within CET, in a company with its own users and its own data. Available from 1 November 2026, EU citizen, no sponsorship needed.</p>
    <p class="muted">Happy to walk through any of these case studies in a call, including the parts that did not work.</p>
  </div>
  <div class="contact-links">
    <a class="btn" href="mailto:{EMAIL}">{EMAIL}</a>
    <a class="btn" href="{CV}">Download CV (PDF)</a>
    <a class="btn" href="{LINKEDIN}">LinkedIn</a>
  </div>
</div>
</section>"""
    person = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Person","name":"Luca Luperto",
"jobTitle":"Growth & Lifecycle Marketing","url":"https://lucaluperto.it/",
"image":"https://lucaluperto.it/portrait.png","email":"mailto:lucaluperto99@gmail.com",
"address":{"@type":"PostalAddress","addressLocality":"Milan","addressCountry":"IT"},
"sameAs":["https://www.linkedin.com/in/lupertoluca"],
"knowsAbout":["Growth marketing","Lifecycle marketing","CRM","Paid social","Google Ads","Email marketing","Hospitality marketing"],
"alumniOf":[{"@type":"CollegeOrUniversity","name":"Universit\u00e0 Cattolica del Sacro Cuore"},
{"@type":"CollegeOrUniversity","name":"Accademia di Belle Arti di Cuneo"}]}
</script>
"""
    return page("Luca Luperto · Growth & Lifecycle Marketing",
                "Case studies in growth, lifecycle and paid marketing for travel and hospitality: paid media, CRM, creator programmes and content operations.",
                body, jsonld=person)



if __name__ == "__main__":
    builders = {"comedy-week.html": comedy_week, "kolms-creative.html": kolms,
                "italy-food-prn.html": ifp, "azzurro-ads.html": azzurro}
    for name, fn in [("index.html", index)] + [(f, builders[f]) for f, _ in CASES]:
        open(name, "w", encoding="utf-8").write(fn())
        print("wrote", name)
    today = __import__("datetime").date.today().isoformat()
    urls = ["", ] + [f for f, _ in CASES]
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "".join(f"  <url><loc>https://lucaluperto.it/{u}</loc><lastmod>{today}</lastmod>"
                         f"<priority>{'1.0' if u == '' else '0.8'}</priority></url>\n" for u in urls)
               + "</urlset>\n")
    open("sitemap.xml", "w").write(sitemap)
    open("robots.txt", "w").write("User-agent: *\nAllow: /\n\nSitemap: https://lucaluperto.it/sitemap.xml\n")
    print("wrote sitemap.xml, robots.txt")
