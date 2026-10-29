#!/usr/bin/env python3
"""Digital Profit Review static site. Run: python3 build.py
To add a category: add an entry to CATEGORIES and a content/<key>.py with POSTS."""
import os, re, html, importlib, datetime, shutil
BASE = "https://digitalprofitreview.com"
TAG = "hearthhaven0b-20"
SITE = "Digital Profit Review"
DISC = "As an Amazon Associate we earn from qualifying purchases."
REL = 'rel="sponsored nofollow noopener"'

CATEGORIES = [
  dict(key="home", name="Home & Decor", blurb="Cozy, practical picks for every room, plus gift guides for people who love being home."),
  dict(key="beauty", name="Beauty", blurb="Luxury skincare, routines and at-home spa rituals, with only highly rated products."),
]
# Amazon products for the Home & Decor posts (key -> ASIN)
HOME_ASINS = dict(sherpa="B0158EQJSY", yankee="B0F3DPXQP1", lights="B00JR5N0JM", flameless="B0BNBFRFCM",
  diffuser="B00V9JP8EE", reed="B0B24QJ217", lazy="B0BR1RYYFQ", board="B07P5JSMXG")
amz = lambda asin: f"https://www.amazon.com/dp/{asin}?tag={TAG}"
def aff(key, text): return f'<a href="{amz(HOME_ASINS[key])}" target="_blank" {REL}>{text}</a>'
def btn(key, text="Check price on Amazon"):
    return f'<p class="cta"><a class="btn" href="{amz(HOME_ASINS[key])}" target="_blank" {REL}>{text}</a></p>'

def load():
    posts = []
    for c in CATEGORIES:
        for p in importlib.import_module("content." + c["key"]).POSTS:
            p = dict(p); b = p["body"]
            b = b(aff, btn) if callable(b) else b
            b = re.sub(r"\{\{AMZ:([A-Z0-9]+)\}\}", lambda m: amz(m.group(1)), b)
            b = re.sub(r'rel="sponsored[^"]*"', REL, b)
            p.update(body=b, cat=c, url=f"/{c['key']}/{p['slug']}/")
            posts.append(p)
    return posts

LOGO = '<a class="wordmark" href="/" aria-label="Digital Profit Review home"><span class="mono">DPR</span><span class="wm">Digital Profit <em>Review</em></span></a>'
def nav():
    return "".join(f'<a href="/{c["key"]}/">{c["name"]}</a>' for c in CATEGORIES) + '<a href="/about/">About</a>'

def page(title, desc, body, path, image=None, kind="website"):
    url = BASE + path
    og = BASE + "/" + (image or "assets/og.png")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="{kind}"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{og}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css"></head><body>
<div class="discbar">{DISC} <a href="/affiliate-disclosure/">Learn more</a></div>
<header class="site"><div class="wrap">{LOGO}<nav>{nav()}</nav></div></header>
<main>{body}</main>
<footer class="site"><div class="wrap"><div class="fcol">{LOGO}<p>Independent, hands-on buying guides. We recommend only well-reviewed products and say why.</p></div>
<div class="fcol"><h4>Categories</h4>{"".join(f'<a href="/{c["key"]}/">{c["name"]}</a>' for c in CATEGORIES)}</div>
<div class="fcol"><h4>Company</h4><a href="/about/">About</a><a href="/affiliate-disclosure/">Affiliate disclosure</a><a href="/privacy/">Privacy</a></div></div>
<div class="wrap legal">&copy; {datetime.date.today().year} {SITE}. {DISC} Amazon and the Amazon logo are trademarks of Amazon.com, Inc. or its affiliates.</div></footer></body></html>"""

def card(p):
    return f"""<a class="card" href="{p['url']}"><div class="thumb"><img src="/{p['image']}" alt="" loading="lazy"></div>
<span class="label">{p['cat']['name']}</span><h3>{p['title']}</h3><p>{p['desc']}</p><span class="more">Read the guide &rarr;</span></a>"""

def crumbs(*items):
    out = ['<a href="/">Home</a>'] + [f'<a href="{u}">{t}</a>' if u else f'<span>{t}</span>' for t, u in items]
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<i>/</i>'.join(out) + '</nav>'

def write(path, s):
    f = "." + path + ("index.html" if path.endswith("/") else "")
    os.makedirs(os.path.dirname(f), exist_ok=True); open(f, "w").write(s)

def main():
    for c in CATEGORIES:
        shutil.rmtree(c["key"], ignore_errors=True)
    for d in ("about", "affiliate-disclosure", "privacy"): shutil.rmtree(d, ignore_errors=True)
    posts = load(); urls = ["/"]
    # home
    cats = "".join(f'<a class="catcard" href="/{c["key"]}/"><span class="n">{i+1:02d}</span><h3>{c["name"]}</h3><p>{c["blurb"]}</p><span class="more">{sum(p["cat"] is c for p in posts)} guides &rarr;</span></a>' for i, c in enumerate(CATEGORIES))
    feat = posts[-1] if False else posts[0]
    body = f"""<section class="hero"><div class="wrap"><p class="eyebrow">Buying guides &middot; Reviews &middot; Gift edits</p>
<h1>Smart picks, honestly reviewed.</h1><p class="lede">Digital Profit Review researches the products worth your money across home, beauty and more, so you can buy once and buy well.</p>
<p><a class="btn" href="#latest">Read the latest</a> <a class="btn ghost" href="#categories">Browse categories</a></p></div></section>
<section class="sec" id="categories"><div class="wrap"><div class="sechead"><h2>Categories</h2></div><div class="catgrid">{cats}</div></div></section>
<section class="sec" id="latest"><div class="wrap"><div class="sechead"><h2>Latest guides</h2></div><div class="grid">{"".join(card(p) for p in posts)}</div></div></section>
<section class="band"><div class="wrap"><h2>How we choose</h2><p>We favour products with a long track record of strong buyer ratings, explain who each pick suits, and never invent prices. If a product slips in quality or goes out of stock, we replace it.</p></div></section>"""
    write("/", page(f"{SITE}: Honest Buying Guides for Home, Beauty & More", "Independent buying guides and gift edits across home & decor, beauty and more.", body, "/"))
    for c in CATEGORIES:
        cp = [p for p in posts if p["cat"] is c]
        b = f"""<section class="cathero"><div class="wrap">{crumbs((c['name'], None))}<h1>{c['name']}</h1><p class="lede">{c['blurb']}</p></div></section>
<section class="sec"><div class="wrap"><div class="grid">{"".join(card(p) for p in cp)}</div></div></section>"""
        write(f"/{c['key']}/", page(f"{c['name']} Guides | {SITE}", c["blurb"], b, f"/{c['key']}/")); urls.append(f"/{c['key']}/")
        for p in cp:
            others = [q for q in cp if q is not p][:2]
            b = f"""<article class="post"><div class="wrap narrow">{crumbs((c['name'], f"/{c['key']}/"), (p['title'], None))}
<span class="label">{c['name']}</span><h1>{p['title']}</h1><p class="meta">Updated {p['date']} &middot; By the {SITE} editors</p>
<p class="disc-top"><strong>Disclosure:</strong> {DISC} Some links on this page are affiliate links, which means we may earn a commission at no extra cost to you.</p>
<figure class="heroimg"><img src="/{p['image']}" alt="{html.escape(p['title'])}"></figure>
<div class="body">{p['body']}</div>
<p class="disc-bottom">{DISC} Prices and availability change; check Amazon for current details.</p></div></article>
<section class="sec related"><div class="wrap"><div class="sechead"><h2>More in {c['name']}</h2><a href="/{c['key']}/">View all &rarr;</a></div><div class="grid two">{"".join(card(q) for q in others)}</div></div></section>"""
            write(p["url"], page(f"{p['title']} | {SITE}", p["desc"], b, p["url"], p["image"], "article")); urls.append(p["url"])
    static = {
     "about": ("About", f"<p>{SITE} publishes practical buying guides across categories, starting with Home &amp; Decor and Beauty. We focus on products with a strong track record of buyer reviews, explain who each pick is for, and keep guides updated when products change.</p><p>We are reader-supported. When you buy through links on our site we may earn an affiliate commission, which never changes the price you pay.</p>"),
     "affiliate-disclosure": ("Affiliate Disclosure", f"<p>{SITE} is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. <strong>{DISC}</strong></p><p>Links to Amazon are marked as sponsored. Commissions come at no extra cost to you and do not affect which products we recommend. Prices and availability are accurate as of the date shown and are subject to change.</p>"),
     "privacy": ("Privacy Policy", f"<p>This site is hosted on Vercel, which may log standard request data (such as IP address and browser type) for security and performance. We do not run our own analytics, ads or newsletter signup, and we do not sell personal information.</p><p>When you click an Amazon link, Amazon may set cookies to attribute purchases to us; see Amazon's privacy notice. Questions: contact the site owner via the details on our About page.</p><p>Last updated October 29, 2026.</p>"),
    }
    for slug, (t, txt) in static.items():
        b = f'<article class="post"><div class="wrap narrow">{crumbs((t, None))}<h1>{t}</h1><div class="body">{txt}</div></div></article>'
        write(f"/{slug}/", page(f"{t} | {SITE}", f"{t} for {SITE}.", b, f"/{slug}/")); urls.append(f"/{slug}/")
    open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{BASE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    open("404.html", "w").write(page(f"Page not found | {SITE}", "Page not found", '<section class="cathero"><div class="wrap"><h1>Page not found</h1><p class="lede"><a href="/">Back to the home page</a></p></div></section>', "/404"))
    for p in posts: print(p["url"], len(re.sub("<[^>]+>", " ", p["body"]).split()), "words")
main()
