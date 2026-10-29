#!/usr/bin/env python3
"""Digital Profit Review static site generator. Run: python3 build.py  (see README.md)"""
import os, re, html, json, glob, runpy, shutil, math
from content.products import PRODUCTS, CHECKED

BASE = "https://digitalprofitreview.com"
TAG = "hearthhaven0b-20"
SITE = "Digital Profit Review"
AUTHOR = "Digital Profit Review Editors"
DISC = "As an Amazon Associate we earn from qualifying purchases."
REL = 'rel="sponsored nofollow noopener" target="_blank"'
CATEGORIES = [
  dict(key="home", name="Home & Decor", blurb="Cozy, practical picks for every room, plus gift guides for people who love being home."),
  dict(key="beauty", name="Beauty", blurb="Luxury skincare, routines and at-home spa rituals, with only highly rated products."),
]
E = html.escape
CSS = open("assets/fonts.css").read() + open("assets/style.css").read()
CSS = re.sub(r"\s*\n\s*", "", CSS)
amz = lambda asin: f"https://www.amazon.com/dp/{asin}?tag={TAG}"
def alink(asin, text=None, cls=""):
    return f'<a{" class=%s" % cls if cls else ""} href="{amz(asin)}" {REL}>{E(text or PRODUCTS[asin]["name"])}</a>'
def btn(asin): return f'<p class="cta">{alink(asin, "Check price on Amazon", "btn")}</p>'
def slugify(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def fmt(d):  # 2026-10-29 -> October 29, 2026
    y, m, dd = map(int, d.split("-"))
    return ["January","February","March","April","May","June","July","August","September","October","November","December"][m-1] + f" {dd}, {y}"
def img(base, kind):  # base like assets/home/1-x ; kind lg|sm
    from PIL import Image
    w, h = Image.open(f"{base}-{kind}.webp").size
    return f"/{base}-{kind}.webp", w, h

def load():
    posts = []
    for c in CATEGORIES:
        for f in sorted(glob.glob(f"content/{c['key']}/*.py")):
            p = dict(runpy.run_path(f)["POST"]); p["cat"] = c
            p["url"] = f"/{c['key']}/{p['slug']}/"; p["base"] = p["image"].rsplit(".", 1)[0]
            for pr in p["products"]:
                assert pr["asin"] in PRODUCTS, f"{f}: unknown ASIN {pr['asin']} (add it to content/products.py)"
            posts.append(p)
    return posts

LOGO = '<a class="wordmark" href="/"><span class="mono">DPR</span><span class="wm">Digital Profit <em>Review</em></span></a>'
def nav(): return "".join(f'<a href="/{c["key"]}/">{E(c["name"])}</a>' for c in CATEGORIES) + '<a href="/about/">About</a>'
def ld(obj): return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"
ORG = {"@type": "Organization", "@id": BASE + "/#org", "name": SITE, "url": BASE + "/", "logo": {"@type": "ImageObject", "url": BASE + "/assets/logo.png", "width": 512, "height": 512}}

def crumbs(items):  # items: [(name, path or None)], Home prepended
    full = [("Home", "/")] + items
    vis = '<nav class="crumbs" aria-label="Breadcrumb">' + "<i>/</i>".join(f'<a href="{u}">{E(t)}</a>' if u and i < len(full)-1 else f"<span>{E(t)}</span>" for i, (t, u) in enumerate(full)) + "</nav>"
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        dict({"@type": "ListItem", "position": i+1, "name": t}, **({"item": BASE + u} if u else {})) for i, (t, u) in enumerate(full)]}
    return vis, data

def page(title, desc, body, path, schema, image="/assets/og.png", kind="website", extra_head=""):
    url = BASE + path
    og = BASE + image
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{url}"><meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:site_name" content="{SITE}"><meta property="og:type" content="{kind}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{og}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{og}">
<meta name="theme-color" content="#14261f"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/fraunces.woff2" as="font" type="font/woff2" crossorigin>{extra_head}
<style>{CSS}</style>{"".join(ld(s) for s in schema)}</head><body>
<div class="discbar">{DISC} <a href="/affiliate-disclosure/">Read our affiliate disclosure</a></div>
<header class="site"><div class="wrap">{LOGO}<nav aria-label="Main">{nav()}</nav></div></header>
<main>{body}</main>
<footer class="site"><div class="wrap"><div class="fcol">{LOGO}<p>Independent buying guides. We recommend only well-reviewed products and say why.</p></div>
<div class="fcol"><h2 class="fh">Categories</h2>{"".join(f'<a href="/{c["key"]}/">{E(c["name"])}</a>' for c in CATEGORIES)}</div>
<div class="fcol"><h2 class="fh">Company</h2><a href="/about/">About</a><a href="/affiliate-disclosure/">Affiliate disclosure</a><a href="/privacy/">Privacy</a></div></div>
<div class="wrap legal"><p>&copy; 2026 {SITE}. {DISC} Amazon and the Amazon logo are trademarks of Amazon.com, Inc. or its affiliates.</p></div></footer></body></html>"""

def card(p, eager=False):
    src, w, h = img(p["base"], "sm")
    return f"""<a class="card" href="{p['url']}"><div class="thumb"><img src="{src}" alt="{E(p['image_alt'])}" width="{w}" height="{h}" {'fetchpriority="high"' if eager else 'loading="lazy"'} decoding="async"></div>
<span class="label">{E(p['cat']['name'])}</span><h3>{E(p['title'])}</h3><p>{E(p['desc'])}</p><span class="more">Read the guide &rarr;</span></a>"""

def words(s): return len(re.sub(r"<[^>]+>", " ", s).split())

def article(p, related):
    c = p["cat"]; prods = p["products"]
    toc = [("At a glance: our picks compared", "at-a-glance")] + [(pr["h2"], slugify(pr["h2"].split(":")[-1])) for pr in prods] + [(h, slugify(h)) for h, _ in p["sections"]] + [("Frequently asked questions", "faq"), ("The bottom line", "bottom-line")]
    rows = "".join(f'<tr><td>{alink(pr["asin"])}</td><td>{E(pr["best"])}</td><td>{PRODUCTS[pr["asin"]]["rating"]}/5 ({PRODUCTS[pr["asin"]]["count"]} ratings)</td><td>{alink(pr["asin"], "Check price")}</td></tr>' for pr in prods)
    disc = f'<p class="disc-top"><strong>Disclosure:</strong> {DISC} Product links on this page go to Amazon and are affiliate links, so we may earn a commission at no extra cost to you. We do not list prices because they change often; use the buttons to check the current price.</p>'
    out = [f"<p>{x}</p>" for x in p["intro"]]
    out.append('<nav class="toc" aria-label="Table of contents"><h2>In this guide</h2><ol>' + "".join(f'<li><a href="#{a}">{E(t)}</a></li>' for t, a in toc) + "</ol></nav>")
    out.append(f'<h2 id="at-a-glance">At a glance: our picks compared</h2><div class="tablewrap"><table class="cmp"><caption class="verified">Amazon ratings as checked on {CHECKED}. Ratings change over time.</caption><thead><tr><th scope="col">Product</th><th scope="col">Best for</th><th scope="col">Amazon rating</th><th scope="col">Price</th></tr></thead><tbody>{rows}</tbody></table></div>')
    for i, pr in enumerate(prods, 1):
        info = PRODUCTS[pr["asin"]]; lead, _, _ = pr["h2"].partition(":")
        out.append(f'<section class="pick"><h2 id="{slugify(pr["h2"].split(":")[-1])}">{i}. {E(lead)}: {alink(pr["asin"])}</h2>')
        out.append(f'<p class="verified">Rated {info["rating"]} out of 5 by {info["count"]} Amazon shoppers (checked {CHECKED}). Price: check current price on Amazon.</p>')
        out.append("<h3>Why we like it</h3>" + "".join(f"<p>{x}</p>" for x in pr["why"]))
        out.append(f"<h3>Who it's for</h3><p>{pr['who']}</p>")
        out.append('<div class="pc"><div><h4>Pros</h4><ul>' + "".join(f"<li>{E(x)}</li>" for x in pr["pros"]) + '</ul></div><div><h4>Cons</h4><ul>' + "".join(f"<li>{E(x)}</li>" for x in pr["cons"]) + "</ul></div></div>")
        out.append(btn(pr["asin"]) + "</section>")
    for h, b in p["sections"]: out.append(f'<h2 id="{slugify(h)}">{E(h)}</h2>{b}')
    out.append('<section class="faq"><h2 id="faq">Frequently asked questions</h2>' + "".join(f"<h3>{E(q)}</h3><p>{E(a)}</p>" for q, a in p["faqs"]) + "</section>")
    out.append('<h2 id="bottom-line">The bottom line</h2>' + "".join(f"<p>{x}</p>" for x in p["conclusion"]) + f'<p>{p["related_text"]}</p>')
    out.append(f'<p class="disc-bottom">{DISC} Ratings were checked on {CHECKED}; prices and availability change, so check Amazon for current details.</p>')
    body = "".join(out)
    mins = max(1, math.ceil(words(body) / 230))
    vis, bc = crumbs([(c["name"], f"/{c['key']}/"), (p["title"], None)])
    src, w, h = img(p["base"], "lg")
    html_ = f"""<article class="post"><div class="wrap narrow">{vis}
<span class="label">{E(c['name'])}</span><h1>{E(p['title'])}</h1>
<p class="byline">By <a href="/about/">{AUTHOR}</a> &middot; Published <time datetime="{p['published']}">{fmt(p['published'])}</time> &middot; Updated <time datetime="{p['updated']}">{fmt(p['updated'])}</time> &middot; {mins} min read</p>
{disc}<figure class="heroimg"><img src="{src}" alt="{E(p['image_alt'])}" width="{w}" height="{h}" fetchpriority="high" decoding="async"></figure>
<div class="body">{body}</div></div></article>
<section class="sec related"><div class="wrap"><div class="sechead"><h2>More in {E(c['name'])}</h2><a href="/{c['key']}/">View all &rarr;</a></div><div class="grid two">{"".join(card(q) for q in related)}</div></div></section>"""
    og = "/" + p["base"] + "-og.jpg"
    schema = [
      {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "image": [BASE + og, BASE + src],
       "datePublished": p["published"] + "T08:00:00+08:00", "dateModified": p["updated"] + "T08:00:00+08:00",
       "author": {"@type": "Organization", "name": AUTHOR, "url": BASE + "/about/"}, "publisher": ORG,
       "mainEntityOfPage": {"@type": "WebPage", "@id": BASE + p["url"]}, "articleSection": c["name"], "wordCount": words(body), "inLanguage": "en-US"},
      {"@context": "https://schema.org", "@type": "ItemList", "name": p["title"], "numberOfItems": len(prods), "itemListElement": [
        {"@type": "ListItem", "position": i, "name": PRODUCTS[pr["asin"]]["name"], "url": amz(pr["asin"])} for i, pr in enumerate(prods, 1)]},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faqs"]]},
      bc]
    head = f'<link rel="preload" as="image" href="{src}" fetchpriority="high"><meta property="article:published_time" content="{p["published"]}"><meta property="article:modified_time" content="{p["updated"]}">'
    return page(p.get("seo_title", p["title"]) + f" | {SITE}" if len(p.get("seo_title", p["title"])) < 45 else p.get("seo_title", p["title"]),
                p["desc"], html_, p["url"], schema, og, "article", head), words(body), mins

def write(path, s):
    f = "." + path + ("index.html" if path.endswith("/") else "")
    os.makedirs(os.path.dirname(f), exist_ok=True); open(f, "w").write(s)

def main():
    for c in CATEGORIES: shutil.rmtree(c["key"], ignore_errors=True)
    for d in ("about", "affiliate-disclosure", "privacy"): shutil.rmtree(d, ignore_errors=True)
    posts = load(); latest = max(p["updated"] for p in posts)
    sm = [("/", latest)]
    posts_sorted = sorted(posts, key=lambda p: (p["published"], p["slug"]), reverse=True)
    cats = "".join(f'<a class="catcard" href="/{c["key"]}/"><span class="n">{i+1:02d}</span><h3>{E(c["name"])}</h3><p>{E(c["blurb"])}</p><span class="more">{sum(p["cat"] is c for p in posts)} guides &rarr;</span></a>' for i, c in enumerate(CATEGORIES))
    body = f"""<section class="hero"><div class="wrap"><p class="eyebrow">Buying guides &middot; Reviews &middot; Gift edits</p>
<h1>Smart picks, honestly reviewed.</h1><p class="lede">Digital Profit Review researches the products worth your money across home, beauty and more, so you can buy once and buy well.</p>
<p><a class="btn" href="#latest">Read the latest guides</a> <a class="btn ghost" href="#categories">Browse categories</a></p></div></section>
<section class="sec" id="categories"><div class="wrap"><div class="sechead"><h2>Categories</h2></div><div class="catgrid">{cats}</div></div></section>
<section class="sec" id="latest"><div class="wrap"><div class="sechead"><h2>Latest guides</h2></div><div class="grid">{"".join(card(p) for p in posts_sorted)}</div></div></section>
<section class="band"><div class="wrap"><h2>How we choose</h2><p>We favour products with a long track record of strong buyer ratings, explain who each pick suits, and never invent prices. If a product slips in quality or goes out of stock, we replace it. <a href="/about/">More about us</a>.</p></div></section>"""
    _, bc = crumbs([])
    home_schema = [{"@context": "https://schema.org", **ORG}, {"@context": "https://schema.org", "@type": "WebSite", "@id": BASE + "/#website", "name": SITE, "url": BASE + "/", "publisher": {"@id": BASE + "/#org"}, "inLanguage": "en-US"}, bc]
    write("/", page(f"{SITE}: Honest Buying Guides for Home & Beauty", "Independent buying guides and gift edits for home & decor and beauty, featuring only well-reviewed products, with honest pros and cons.", body, "/", home_schema))
    report = []
    for c in CATEGORIES:
        cp = sorted([p for p in posts if p["cat"] is c], key=lambda p: (p["published"], p["slug"]), reverse=True)
        vis, bc = crumbs([(c["name"], None)])
        b = f"""<section class="cathero"><div class="wrap">{vis}<h1>{E(c['name'])} Buying Guides</h1><p class="lede">{E(c['blurb'])}</p></div></section>
<section class="sec"><div class="wrap"><h2 class="sr">All {E(c['name'])} guides</h2><div class="grid">{"".join(card(p, i == 0) for i, p in enumerate(cp))}</div></div></section>"""
        write(f"/{c['key']}/", page(f"{c['name']} Buying Guides & Gift Ideas | {SITE}", c["blurb"] + " Honest pros and cons for every pick.", b, f"/{c['key']}/", [bc]))
        sm.append((f"/{c['key']}/", max(p["updated"] for p in cp)))
        for p in cp:
            rel = [q for q in posts_sorted if q is not p and q["cat"] is c][:2]
            s, wc, mins = article(p, rel); write(p["url"], s); sm.append((p["url"], p["updated"])); report.append((p["url"], wc, mins))
    static = {
     "about": ("About Digital Profit Review", "Who we are and how Digital Profit Review researches and selects the products in our buying guides.", f"<p>{SITE} publishes practical buying guides across categories, starting with Home &amp; Decor and Beauty. Our guides are written by the {AUTHOR}. We focus on products with a strong track record of buyer reviews, explain who each pick is for, list honest drawbacks, and update guides when products change or sell out.</p><h2>How we choose products</h2><p>We read product listings, specifications and buyer reviews, and we check each product's Amazon rating and availability on the date shown in every guide. We never invent prices or ratings, and we do not publish star ratings of our own.</p><h2>How we make money</h2><p>We are reader-supported. When you buy through links on our site we may earn an affiliate commission, which never changes the price you pay. See our <a href=\"/affiliate-disclosure/\">affiliate disclosure</a>.</p>"),
     "affiliate-disclosure": ("Affiliate Disclosure", "How Digital Profit Review earns money through the Amazon Associates program.", f"<p>{SITE} is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. <strong>{DISC}</strong></p><p>Links to Amazon are marked as sponsored. Commissions come at no extra cost to you and do not affect which products we recommend. Ratings and availability are accurate as of the date shown and are subject to change.</p>"),
     "privacy": ("Privacy Policy", "Privacy policy for Digital Profit Review: what data is collected and how Amazon affiliate links work.", "<p>This site is hosted on Vercel, which may log standard request data (such as IP address and browser type) for security and performance. We do not run our own analytics, ads or newsletter signup, and we do not sell personal information.</p><p>When you click an Amazon link, Amazon may set cookies to attribute purchases to us; see Amazon's privacy notice.</p><p>Last updated October 29, 2026.</p>"),
    }
    for slug, (t, d, txt) in static.items():
        vis, bc = crumbs([(t, None)])
        b = f'<article class="post"><div class="wrap narrow">{vis}<h1>{t}</h1><div class="body">{txt}</div></div></article>'
        write(f"/{slug}/", page(f"{t} | {SITE}", d, b, f"/{slug}/", [bc])); sm.append((f"/{slug}/", "2026-10-29"))
    open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in sm) + "</urlset>\n")
    open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nDisallow: /404.html\n\nSitemap: {BASE}/sitemap.xml\n")
    vis, bc = crumbs([("Page not found", None)])
    nf = f'<section class="cathero"><div class="wrap"><h1>Page not found</h1><p class="lede">Sorry, that page does not exist. Try one of our categories or the <a href="/">home page</a>.</p><p>{"".join(f"<a class=btn href=/{c["key"]}/>{E(c["name"])}</a>" for c in CATEGORIES)}</p></div></section>'
    write("/404.html", page(f"Page Not Found | {SITE}", "The page you were looking for could not be found.", nf, "/404.html", [bc]).replace('content="index,follow,max-image-preview:large"', 'content="noindex"'))
    for r in report: print(*r)
main()
