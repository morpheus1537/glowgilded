#!/usr/bin/env python3
"""Digital Profit Review static site generator. Run: python3 build.py  (see README.md)"""
import os, re, sys, html, json, glob, shutil, math
import yaml, markdown
PRODUCTS = yaml.safe_load(open("data/products.yaml"))["products"]

BASE = "https://digitalprofitreview.com"
TAG = "hearthhaven0b-20"
SITE = "Digital Profit Review"
AUTHOR = "Digital Profit Review Editors"
DISC = "As an Amazon Associate we earn from qualifying purchases."
REL = 'rel="sponsored nofollow noopener" target="_blank"'
CATEGORIES = yaml.safe_load(open("data/categories.yaml"))
SITECFG = yaml.safe_load(open("data/site.yaml")) or {}
VERIFY = "".join(f'<meta name="{v["name"]}" content="{v["content"]}"/>' for v in SITECFG.get("verification") or [])
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

REQUIRED = ["title", "slug", "category", "description", "date", "updated", "author", "hero", "products", "faq"]
SHORT = re.compile(r"\{\{\s*product\s+([A-Z0-9]{10})\s*\}\}")
ERRORS = []
def err(f, msg): ERRORS.append(f"{f}: {msg}")

def load():
    posts = []
    keys = {c["key"]: c for c in CATEGORIES}
    for c in CATEGORIES:
        for f in sorted(glob.glob(f"content/{c['key']}/*.md")):
            raw = open(f, encoding="utf-8").read()
            m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
            if not m: err(f, "missing YAML front matter"); continue
            fm = yaml.safe_load(m.group(1)) or {}
            miss = [k for k in REQUIRED if not fm.get(k)]
            if miss: err(f, "missing front matter fields: " + ", ".join(miss)); continue
            if not (isinstance(fm["hero"], dict) and fm["hero"].get("image") and fm["hero"].get("alt")): err(f, "hero needs image and alt"); continue
            if fm["category"] != c["key"]: err(f, f"category '{fm['category']}' does not match folder '{c['key']}'")
            if fm["slug"] + ".md" != os.path.basename(f): err(f, "slug must match the file name")
            for k in ("date", "updated"): fm[k] = str(fm[k])
            used = SHORT.findall(m.group(2))
            for asin in set(fm["products"]) | set(used) | {r["asin"] for r in fm.get("comparison") or []}:
                if asin not in PRODUCTS: err(f, f"unknown ASIN {asin} (add it to data/products.yaml)")
            for asin in used:
                if asin not in fm["products"]: err(f, f"shortcode ASIN {asin} not listed in front matter products")
            for x in fm["faq"]:
                if not (x.get("question") and x.get("answer")): err(f, "each faq item needs question and answer")
            base = fm["hero"]["image"].rsplit(".", 1)[0] if fm["hero"]["image"].endswith((".jpg", ".webp", ".png")) else fm["hero"]["image"]
            base = base.lstrip("/").replace("-lg", "")
            for suf in ("-lg.webp", "-sm.webp", "-og.jpg"):
                if not os.path.exists(base + suf): err(f, f"missing image {base + suf}")
            fm.update(cat=c, file=f, body_md=m.group(2), base=base, url=f"/{c['key']}/{fm['slug']}/")
            posts.append(fm)
    return posts

def md(text): return markdown.markdown(text, extensions=["extra"])

def parse_body(text):
    parts = re.split(r"^## +(.+)$", text, flags=re.M)
    intro = parts[0].strip(); secs = []
    for i in range(1, len(parts), 2):
        h, b = parts[i].strip(), parts[i+1].strip()
        found = SHORT.findall(b)
        secs.append(dict(h=h, md=b, asin=found[0] if found else None))
    return intro, secs

def render_product(b, asin):
    out = []; pc = {}
    def take(name):
        nonlocal b
        m = re.search(rf"^### +{name}\s*\n(.*?)(?=^### |^\{{\{{|\Z)", b, re.S | re.M)
        if m: pc[name] = md(m.group(1).strip()); b = b[:m.start()] + b[m.end():]
    take("Pros"); take("Cons")
    b = SHORT.sub("", b).strip()
    out.append(md(b))
    if pc: out.append('<div class="pc"><div><h4>Pros</h4>' + pc.get("Pros", "") + '</div><div><h4>Cons</h4>' + pc.get("Cons", "") + "</div></div>")
    out.append(btn(asin))
    return "".join(out)

LOGO = '<a class="wordmark" href="/"><span class="mono">DPR</span><span class="wm">Digital Profit <em>Review</em></span></a>'
NAV_TOP = 6  # categories shown directly in the desktop nav; the rest go under "More" (all show in the mobile swipe nav)
def nav():
    lk = lambda c, cls="": f'<a{cls} href="/{c["key"]}/">{E(c.get("short", c["name"]))}</a>'
    top, rest = CATEGORIES[:NAV_TOP], CATEGORIES[NAV_TOP:]
    more = (f'<div class="more"><span tabindex="0" aria-haspopup="true">More &#9662;</span><div class="dd">{"".join(lk(c) for c in rest)}</div></div>' if rest else "")
    return "".join(lk(c) for c in top) + "".join(lk(c, ' class="x"') for c in rest) + more + '<a href="/gift-finder/">Gift finder</a><a href="/search/">Search</a><a href="/about/">About</a>'
def ld(obj): return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"
ORG = {"@type": "Organization", "@id": BASE + "/#org", "name": SITE, "url": BASE + "/", "logo": {"@type": "ImageObject", "url": BASE + "/assets/logo.png", "width": 512, "height": 512}, "description": "Independent product research site publishing buying guides and gift guides for home, beauty, kitchen, tech, fitness, pets, baby, outdoor, office, car and travel.", "sameAs": ["https://www.pinterest.com/hearthhavenhome99/", "https://www.pinterest.com/glowgilded/"]}
def cnt(asin): return int(str(PRODUCTS[asin]["count"]).replace(",", ""))
def author_ld(p):  # set author_person: {name, url, bio} in front matter to switch to a named Person
    ap = p.get("author_person")
    if isinstance(ap, dict) and ap.get("name"):
        return {"@type": "Person", "name": ap["name"], "url": ap.get("url") or BASE + "/about/", **({"description": ap["bio"]} if ap.get("bio") else {}), "worksFor": {"@id": BASE + "/#org"}}
    return {"@type": "Organization", "name": p["author"], "url": BASE + "/about/", "@id": BASE + "/#org"}

def crumbs(items):  # items: [(name, path or None)], Home prepended
    full = [("Home", "/")] + items
    vis = '<nav class="crumbs" aria-label="Breadcrumb">' + "<i>/</i>".join(f'<a href="{u}">{E(t)}</a>' if u and i < len(full)-1 else f"<span>{E(t)}</span>" for i, (t, u) in enumerate(full)) + "</nav>"
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        dict({"@type": "ListItem", "position": i+1, "name": t}, **({"item": BASE + u} if u else {})) for i, (t, u) in enumerate(full)]}
    return vis, data

def page(title, desc, body, path, schema, image="/assets/og.png", kind="website", extra_head=""):
    url = BASE + path
    og = BASE + image
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{VERIFY}
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{url}"><meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:site_name" content="{SITE}"><meta property="og:type" content="{kind}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{og}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{og}">
<meta name="theme-color" content="#14261f"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="alternate" type="application/rss+xml" title="{SITE}" href="{BASE}/feed.xml">
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
    return f"""<a class="card" href="{p['url']}"><div class="thumb"><img src="{src}" alt="{E(p['hero']['alt'])}" width="{w}" height="{h}" {'fetchpriority="high"' if eager else 'loading="lazy"'} decoding="async"></div>
<span class="label">{E(p['cat']['name'])}</span><h3>{E(p['title'])}</h3><p>{E(p['description'])}</p><span class="more">Read the guide &rarr;</span></a>"""

def words(s): return len(re.sub(r"<[^>]+>", " ", s).split())

def article(p, related):
    c = p["cat"]
    intro, secs = parse_body(p["body_md"])
    prods = [x for x in secs if x["asin"]]
    bottom = [x for x in secs if x["h"].lower() == "the bottom line"]
    others = [x for x in secs if not x["asin"] and x not in bottom]
    sid = lambda x: "bottom-line" if x in bottom else slugify(x["h"].split(":")[-1] if x["asin"] else x["h"])
    comp = p.get("comparison") or []
    toc = ([("At a glance: our picks compared", "at-a-glance")] if comp else []) + [(x["h"], sid(x)) for x in prods + others] + [("Frequently asked questions", "faq")] + [(x["h"], sid(x)) for x in bottom]
    checked = fmt(max(PRODUCTS[a]["checked"] for a in p["products"]))
    disc = f'<p class="disc-top"><strong>Disclosure:</strong> {DISC} Product links on this page go to Amazon and are affiliate links, so we may earn a commission at no extra cost to you. We do not list prices because they change often; use the buttons to check the current price.</p>'
    best = {r["asin"]: r["best_for"] for r in comp}
    qa = "".join(f'<li><strong>{E(x["h"].partition(":")[0])}:</strong> {alink(x["asin"])} &mdash; rated {PRODUCTS[x["asin"]]["rating"]}/5 by {PRODUCTS[x["asin"]]["count"]} Amazon shoppers' + (f'. Best for: {E(best[x["asin"]])}' if x["asin"] in best else "") + "</li>" for x in prods)
    quick = (f'<aside class="quick" aria-label="Quick answer"><h2 id="quick-answer">Quick answer: our top picks at a glance</h2><p>{E(p["description"])}</p><ul>{qa}</ul><p class="verified">Last updated <time datetime="{p["updated"]}">{fmt(p["updated"])}</time>. Ratings checked on Amazon on {checked}.</p></aside>') if prods else ""
    sticky = (f'<div class="sticky" role="complementary" aria-label="Top pick"><span>Top pick: {E(PRODUCTS[prods[0]["asin"]]["name"])}</span>{alink(prods[0]["asin"], "Check price on Amazon", "btn")}</div>') if prods else ""
    out = [quick, md(intro)]
    out.append('<nav class="toc" aria-label="Table of contents"><h2>In this guide</h2><ol>' + "".join(f'<li><a href="#{a}">{E(t)}</a></li>' for t, a in toc) + "</ol></nav>")
    if comp:
        rows = "".join(f'<tr><td>{alink(r["asin"])}</td><td>{E(r["best_for"])}</td><td>{PRODUCTS[r["asin"]]["rating"]}/5 ({PRODUCTS[r["asin"]]["count"]} ratings)</td><td>{alink(r["asin"], "Check price")}</td></tr>' for r in comp)
        out.append(f'<h2 id="at-a-glance">At a glance: our picks compared</h2><div class="tablewrap"><table class="cmp"><caption class="verified">Amazon ratings as checked on {checked}. Ratings change over time.</caption><thead><tr><th scope="col">Product</th><th scope="col">Best for</th><th scope="col">Amazon rating</th><th scope="col">Price</th></tr></thead><tbody>{rows}</tbody></table></div>')
    for i, x in enumerate(prods, 1):
        info = PRODUCTS[x["asin"]]; lead = x["h"].partition(":")[0]
        out.append(f'<section class="pick"><h2 id="{sid(x)}">{i}. {E(lead)}: {alink(x["asin"])}</h2>')
        out.append(f'<p class="verified">Rated {info["rating"]} out of 5 by {info["count"]} Amazon shoppers (checked {fmt(info["checked"])}). Price: check current price on Amazon.</p>')
        out.append(render_product(x["md"], x["asin"]) + "</section>")
    for x in others: out.append(f'<h2 id="{sid(x)}">{E(x["h"])}</h2>' + md(SHORT.sub(lambda m: btn(m.group(1)), x["md"])))
    out.append('<section class="faq"><h2 id="faq">Frequently asked questions</h2>' + "".join(f"<h3 id=\"faq-{i}\">{E(q['question'])}</h3><p>{E(q['answer'])}</p>" for i, q in enumerate(p["faq"], 1)) + "</section>")
    for x in bottom: out.append(f'<h2 id="bottom-line">{E(x["h"])}</h2>' + md(x["md"]))
    out.append(f'<p class="disc-bottom">{DISC} Ratings were checked on {checked}; prices and availability change, so check Amazon for current details.</p>')
    body = "".join(out)
    mins = max(1, math.ceil(words(body) / 230))
    vis, bc = crumbs([(c["name"], f"/{c['key']}/"), (p["title"], None)])
    src, w, h = img(p["base"], "lg")
    html_ = f"""<article class="post"><div class="wrap narrow">{vis}
<span class="label">{E(c['name'])}</span><h1>{E(p['title'])}</h1>
<p class="byline">By <a href="/about/">{E(p["author"])}</a> &middot; Published <time datetime="{p['date']}">{fmt(p['date'])}</time> &middot; Updated <time datetime="{p['updated']}">{fmt(p['updated'])}</time> &middot; {mins} min read</p>
{disc}<figure class="heroimg"><img src="{src}" alt="{E(p['hero']['alt'])}" width="{w}" height="{h}" fetchpriority="high" decoding="async"></figure>
<div class="body">{body}</div></div></article>{sticky}
<section class="sec related"><div class="wrap"><div class="sechead"><h2>Related guides</h2><a href="/{c['key']}/">View all &rarr;</a></div><div class="grid two">{"".join(card(q) for q in related)}</div></div></section>"""
    og = "/" + p["base"] + "-og.jpg"
    schema = [
      {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["description"], "image": [BASE + og, BASE + src],
       "datePublished": p["date"] + "T08:00:00+08:00", "dateModified": p["updated"] + "T08:00:00+08:00",
       "author": author_ld(p), "publisher": ORG, "abstract": p["description"],
       "mainEntityOfPage": {"@type": "WebPage", "@id": BASE + p["url"]}, "articleSection": c["name"], "wordCount": words(body), "inLanguage": "en-US"},
      {"@context": "https://schema.org", "@type": "ItemList", "name": p["title"], "numberOfItems": len(p["products"]), "itemListElement": [
        {"@type": "ListItem", "position": i, "name": PRODUCTS[a]["name"], "url": amz(a)} for i, a in enumerate(p["products"], 1)]},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["question"], "acceptedAnswer": {"@type": "Answer", "text": q["answer"]}} for q in p["faq"]]},
      bc]
    head = f'<link rel="preload" as="image" href="{src}" fetchpriority="high"><meta property="article:published_time" content="{p["date"]}"><meta property="article:modified_time" content="{p["updated"]}"><meta property="article:section" content="{E(c["name"])}"><meta property="article:author" content="{BASE}/about/">'
    return page(p.get("seo_title", p["title"]) + f" | {SITE}" if len(p.get("seo_title", p["title"])) < 45 else p.get("seo_title", p["title"]),
                p["description"], html_, p["url"], schema, og, "article", head), words(body), mins

def write(path, s):
    f = "." + path + ("index.html" if path.endswith("/") else "")
    os.makedirs(os.path.dirname(f), exist_ok=True); open(f, "w").write(s)

def main():
    for c in CATEGORIES: shutil.rmtree(c["key"], ignore_errors=True)
    for d in ("about", "affiliate-disclosure", "privacy", "gift-finder", "search"): shutil.rmtree(d, ignore_errors=True)
    posts = load()
    if ERRORS: print("BUILD FAILED:\n  " + "\n  ".join(ERRORS), file=sys.stderr); sys.exit(1)
    latest = max(p["updated"] for p in posts)
    sm = [("/", latest)]
    posts_sorted = sorted(posts, key=lambda p: (p["date"], p["slug"]), reverse=True)
    cats = "".join(f'<a class="catcard" href="/{c["key"]}/"><span class="n">{i+1:02d}</span><h3>{E(c["name"])}</h3><p>{E(c["blurb"])}</p><span class="more">{(lambda n: f"{n} guide" + ("" if n == 1 else "s"))(sum(p["cat"] is c for p in posts))} &rarr;</span></a>' for i, c in enumerate(CATEGORIES))
    body = f"""<section class="hero"><div class="wrap"><p class="eyebrow">Buying guides &middot; Reviews &middot; Gift edits</p>
<h1>Smart picks, honestly reviewed.</h1><p class="lede">Digital Profit Review researches the products worth your money across home, beauty and more, so you can buy once and buy well.</p>
<p><a class="btn" href="#latest">Read the latest guides</a> <a class="btn ghost" href="#categories">Browse categories</a></p></div></section>
<section class="sec" id="categories"><div class="wrap"><div class="sechead"><h2>Categories</h2></div><div class="catgrid">{cats}</div></div></section>
{{TRENDING}}<section class="sec" id="latest"><div class="wrap"><div class="sechead"><h2>Latest guides</h2></div><div class="grid">{"".join(card(p) for p in posts_sorted)}</div></div></section>
<section class="band"><div class="wrap"><h2>How we choose</h2><p>We favour products with a long track record of strong buyer ratings, explain who each pick suits, and never invent prices. If a product slips in quality or goes out of stock, we replace it. <a href="/about/">More about us</a>.</p></div></section>"""
    where = {}
    for p in posts_sorted:
        for a in p["products"]: where.setdefault(a, p)
    top = sorted(where, key=cnt, reverse=True)[:8]
    tr = "".join(f'<div class="tp"><span class="label">{E(where[a]["cat"]["name"])}</span><h3>{alink(a)}</h3><p class="verified">{PRODUCTS[a]["rating"]}/5 from {PRODUCTS[a]["count"]} Amazon ratings</p><p><a href="{where[a]["url"]}">Read our take</a></p>{alink(a, "Check price on Amazon", "btn")}</div>' for a in top)
    body = body.replace("{TRENDING}", f'<section class="sec" id="popular"><div class="wrap"><div class="sechead"><h2>Most popular picks</h2><a href="/gift-finder/">Open the gift finder &rarr;</a></div><p>The most-reviewed products across our guides, by number of Amazon ratings.</p><div class="tpgrid">{tr}</div></div></section>')
    _, bc = crumbs([])
    home_schema = [{"@context": "https://schema.org", **ORG}, {"@context": "https://schema.org", "@type": "WebSite", "@id": BASE + "/#website", "name": SITE, "url": BASE + "/", "publisher": {"@id": BASE + "/#org"}, "inLanguage": "en-US", "potentialAction": {"@type": "SearchAction", "target": {"@type": "EntryPoint", "urlTemplate": BASE + "/search/?q={search_term_string}"}, "query-input": "required name=search_term_string"}}, bc]
    write("/", page(f"{SITE}: Honest Buying Guides for Home, Beauty, Tech & More", "Independent buying guides and gift edits for home, beauty, kitchen, tech, fitness, pets and gifts, featuring only well-reviewed products, with honest pros and cons.", body, "/", home_schema))
    report = []
    for c in CATEGORIES:
        cp = sorted([p for p in posts if p["cat"] is c], key=lambda p: (p["date"], p["slug"]), reverse=True)
        vis, bc = crumbs([(c["name"], None)])
        b = f"""<section class="cathero"><div class="wrap">{vis}<h1>{E(c['name'])} Buying Guides</h1><p class="lede">{E(c['blurb'])}</p></div></section>
<section class="sec"><div class="wrap"><h2 class="sr">All {E(c['name'])} guides</h2><div class="grid">{"".join(card(p, i == 0) for i, p in enumerate(cp))}</div></div></section>"""
        write(f"/{c['key']}/", page(c.get("seo_title", f"{c['name']} Buying Guides & Gift Ideas | {SITE}"), c.get("seo_description", c["blurb"] + " Honest pros and cons for every pick."), b, f"/{c['key']}/", [bc]))
        sm.append((f"/{c['key']}/", max(p["updated"] for p in cp)))
        for p in cp:
            rel = ([q for q in posts_sorted if q is not p and q["cat"] is c] + [q for q in posts_sorted if q["cat"] is not c])[:2]
            s, wc, mins = article(p, rel); write(p["url"], s); sm.append((p["url"], p["updated"])); report.append((p["url"], wc, mins))
    static = {
     "about": ("About Digital Profit Review", "Who we are and how Digital Profit Review researches and selects the products in our buying guides.", f"<p>{SITE} publishes practical buying guides across categories, including home &amp; decor, beauty, kitchen, tech, fitness, pets and gifts. Our guides are written by the {AUTHOR}. We focus on products with a strong track record of buyer reviews, explain who each pick is for, list honest drawbacks, and update guides when products change or sell out.</p><h2>How we choose products</h2><p>We read product listings, specifications and buyer reviews, and we check each product's Amazon rating and availability on the date shown in every guide. We never invent prices or ratings, and we do not publish star ratings of our own.</p><h2>How we make money</h2><p>We are reader-supported. When you buy through links on our site we may earn an affiliate commission, which never changes the price you pay. See our <a href=\"/affiliate-disclosure/\">affiliate disclosure</a>.</p><h2>At a glance</h2><ul><li><strong>Name:</strong> {SITE}</li><li><strong>Website:</strong> {BASE}</li><li><strong>What we publish:</strong> buying guides and gift guides across {len(CATEGORIES)} categories: {", ".join(E(c["name"]) for c in CATEGORIES)}</li><li><strong>Written by:</strong> the {AUTHOR}</li><li><strong>Affiliation:</strong> Amazon Associates participant; links to Amazon are affiliate links</li><li><strong>Find us on Pinterest:</strong> <a href=\"https://www.pinterest.com/hearthhavenhome99/\">Hearth &amp; Haven Home</a> and <a href=\"https://www.pinterest.com/glowgilded/\">Glow &amp; Gilded</a></li></ul>"),
     "affiliate-disclosure": ("Affiliate Disclosure", "How Digital Profit Review earns money through the Amazon Associates program.", f"<p>{SITE} is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. <strong>{DISC}</strong></p><p>Links to Amazon are marked as sponsored. Commissions come at no extra cost to you and do not affect which products we recommend. Ratings and availability are accurate as of the date shown and are subject to change.</p>"),
     "privacy": ("Privacy Policy", "Privacy policy for Digital Profit Review: what data is collected and how Amazon affiliate links work.", "<p>This site is hosted on Vercel, which may log standard request data (such as IP address and browser type) for security and performance. We do not run our own analytics, ads or newsletter signup, and we do not sell personal information.</p><p>When you click an Amazon link, Amazon may set cookies to attribute purchases to us; see Amazon's privacy notice.</p><p>Last updated October 29, 2026.</p>"),
    }
    for slug, (t, d, txt) in static.items():
        vis, bc = crumbs([(t, None)])
        b = f'<article class="post"><div class="wrap narrow">{vis}<h1>{t}</h1><div class="body">{txt}</div></div></article>'
        write(f"/{slug}/", page(f"{t} | {SITE}", d, b, f"/{slug}/", [bc] + ([{"@context": "https://schema.org", **ORG}, {"@context": "https://schema.org", "@type": "AboutPage", "url": BASE + "/about/", "name": t, "mainEntity": {"@id": BASE + "/#org"}}] if slug == "about" else []))); sm.append((f"/{slug}/", "2026-10-29"))
    # --- gift finder + search (static JSON, no cookies) ---
    GIFTY = ("gift", "stocking", "registry")
    def gifty(a): return any(any(g in (q["slug"] + q["cat"]["key"]) for g in GIFTY) for q in posts if a in q["products"])
    prodj = [{"a": a, "n": PRODUCTS[a]["name"], "r": float(PRODUCTS[a]["rating"]), "c": cnt(a), "k": where[a]["cat"]["key"], "cn": where[a]["cat"]["name"], "g": gifty(a), "u": where[a]["url"], "t": where[a]["title"], "l": amz(a)} for a in sorted(where, key=cnt, reverse=True)]
    os.makedirs("gift-finder", exist_ok=True); json.dump(prodj, open("gift-finder/products.json", "w"), ensure_ascii=False, separators=(",", ":"))
    srch = [{"t": p["title"], "d": p["description"], "u": p["url"], "c": p["cat"]["name"], "p": " ".join(PRODUCTS[a]["name"] for a in p["products"])} for p in posts_sorted]
    os.makedirs("search", exist_ok=True); json.dump(srch, open("search/index.json", "w"), ensure_ascii=False, separators=(",", ":"))
    LINKREL = REL.replace('"', "'")
    opts = "".join(f'<option value="{c["key"]}">{E(c["name"])}</option>' for c in CATEGORIES)
    gf = f"""<section class="cathero"><div class="wrap">{crumbs([("Gift finder", None)])[0]}<h1>Gift Finder</h1><p class="lede">Filter every product from our guides by category, gift-guide picks and Amazon rating. We do not list prices because they change; each button shows the current price on Amazon.</p></div></section>
<section class="sec"><div class="wrap"><form class="gf" onsubmit="return false"><label>Category <select id="gc"><option value="">All categories</option>{opts}</select></label><label>Minimum rating <select id="gr"><option value="0">Any</option><option value="4.5">4.5+</option><option value="4.7">4.7+</option></select></label><label class="ck"><input type="checkbox" id="gg"> Gift-guide picks only</label></form>
<p id="gn" class="verified" aria-live="polite"></p><div class="tpgrid" id="gl"></div><noscript><p>Turn on JavaScript to use the filters, or <a href="/gifts/">browse our gift guides</a>.</p></noscript></div></section>
<script>(function(){{var D=[],e=function(s){{return String(s).replace(/[&<>"]/g,function(c){{return{{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[c]}})}};function R(){{var c=gc.value,r=+gr.value,g=gg.checked,o=D.filter(function(p){{return(!c||p.k==c)&&p.r>=r&&(!g||p.g)}});gn.textContent=o.length+" products";gl.innerHTML=o.map(function(p){{return'<div class="tp"><span class="label">'+e(p.cn)+'</span><h3><a href="'+p.l+'" {LINKREL}>'+e(p.n)+'</a></h3><p class="verified">'+p.r+'/5 from '+p.c.toLocaleString()+' Amazon ratings</p><p><a href="'+p.u+'">Read: '+e(p.t)+'</a></p><a class="btn" href="'+p.l+'" {LINKREL}>Check price on Amazon</a></div>'}}).join("")}}var gc=document.getElementById("gc"),gr=document.getElementById("gr"),gg=document.getElementById("gg"),gn=document.getElementById("gn"),gl=document.getElementById("gl");[gc,gr,gg].forEach(function(x){{x.onchange=R}});var q=new URLSearchParams(location.search).get("c");if(q)gc.value=q;fetch("/gift-finder/products.json").then(function(r){{return r.json()}}).then(function(d){{D=d;R()}})}})();</script>"""
    write("/gift-finder/", page(f"Gift Finder: Highly Rated Gift Ideas by Category | {SITE}", "Find a gift fast: filter well-reviewed Amazon products from our buying guides by category, rating and gift-guide picks.", gf, "/gift-finder/", [crumbs([("Gift finder", None)])[1]])); sm.append(("/gift-finder/", latest))
    se = f"""<section class="cathero"><div class="wrap">{crumbs([("Search", None)])[0]}<h1>Search our guides</h1><form class="gf" role="search" action="/search/" onsubmit="return false"><label>Search <input type="search" id="sq" name="q" placeholder="e.g. candle, dog, skincare" autocomplete="off"></label></form></div></section>
<section class="sec"><div class="wrap"><p id="sn" class="verified" aria-live="polite"></p><div id="sl"></div></div></section>
<script>(function(){{var D=[],q=document.getElementById("sq"),n=document.getElementById("sn"),l=document.getElementById("sl"),e=function(s){{return String(s).replace(/[&<>"]/g,function(c){{return{{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[c]}})}};function R(){{var t=q.value.toLowerCase().split(/\\s+/).filter(Boolean),o=t.length?D.filter(function(d){{var h=(d.t+" "+d.d+" "+d.c+" "+d.p).toLowerCase();return t.every(function(w){{return h.indexOf(w)>-1}})}}):[];n.textContent=t.length?o.length+" guides found":"";l.innerHTML=o.map(function(d){{return'<p><a href="'+d.u+'"><strong>'+e(d.t)+'</strong></a><br><span class="label">'+e(d.c)+'</span> '+e(d.d)+'</p>'}}).join("")}}q.oninput=R;q.value=new URLSearchParams(location.search).get("q")||"";fetch("/search/index.json").then(function(r){{return r.json()}}).then(function(d){{D=d;R()}})}})();</script>"""
    write("/search/", page(f"Search | {SITE}", "Search Digital Profit Review buying guides and products.", se, "/search/", [crumbs([("Search", None)])[1]]).replace('content="index,follow,max-image-preview:large"', 'content="noindex,follow"'))
    # --- llms.txt for AI answer engines ---
    L = [f"# {SITE}", "", f"> Independent buying guides and gift guides ({BASE}). Each guide recommends a few well-reviewed Amazon products, with who each is for, honest pros and cons, Amazon ratings checked on a stated date, and an FAQ. We never invent prices. {DISC}", "", "## Key pages", f"- [About]({BASE}/about/): who we are and how we choose products", f"- [Gift finder]({BASE}/gift-finder/): filter all recommended products by category and rating", f"- [Affiliate disclosure]({BASE}/affiliate-disclosure/)", f"- [Sitemap]({BASE}/sitemap.xml)", ""]
    for c in CATEGORIES:
        L += [f"## {c['name']}", f"[{c['name']} guides]({BASE}/{c['key']}/): {c['blurb']}"] + [f"- [{p['title']}]({BASE}{p['url']}): {p['description'].strip()} (updated {p['updated']})" for p in posts_sorted if p["cat"] is c] + [""]
    open("llms.txt", "w").write("\n".join(L))
    open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in sm) + "</urlset>\n")
    open("robots.txt", "w").write(f"".join(f"User-agent: {b}\nAllow: /\n\n" for b in ("GPTBot", "OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "Perplexity-User", "ClaudeBot", "Claude-SearchBot", "Google-Extended", "Googlebot", "Bingbot", "Applebot", "Applebot-Extended")) + f"User-agent: *\nAllow: /\nDisallow: /404.html\nDisallow: /search/\n\nSitemap: {BASE}/sitemap.xml\n")
    vis, bc = crumbs([("Page not found", None)])
    nf = f'<section class="cathero"><div class="wrap"><h1>Page not found</h1><p class="lede">Sorry, that page does not exist. Try one of our categories or the <a href="/">home page</a>.</p><p>{"".join(f"<a class=btn href=/{c["key"]}/>{E(c["name"])}</a>" for c in CATEGORIES)}</p></div></section>'
    write("/404.html", page(f"Page Not Found | {SITE}", "The page you were looking for could not be found.", nf, "/404.html", [bc]).replace('content="index,follow,max-image-preview:large"', 'content="noindex"'))
    from email.utils import format_datetime
    from datetime import datetime, timezone, timedelta
    rfc = lambda d: format_datetime(datetime.strptime(d, "%Y-%m-%d").replace(hour=8, tzinfo=timezone(timedelta(hours=8))))
    items = "".join(f"<item><title>{E(p['title'])}</title><link>{BASE}{p['url']}</link><guid>{BASE}{p['url']}</guid><pubDate>{rfc(p['date'])}</pubDate><category>{E(p['cat']['name'])}</category><description>{E(p['description'])}</description></item>\n" for p in posts_sorted[:50])
    open("feed.xml", "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>{SITE}</title><link>{BASE}/</link><description>Honest buying guides</description><language>en-us</language><atom:link href="{BASE}/feed.xml" rel="self" type="application/rss+xml"/>\n{items}</channel></rss>\n')
    open("urls.txt", "w").write("".join(f"{BASE}{u}\n" for u, _ in sm))
    validate_output()
    for r in report: print(*r)

def validate_output():
    for f in glob.glob("**/*.html", recursive=True):
        s = open(f, encoding="utf-8").read()
        for a in re.findall(r"<a\b[^>]*>", s):
            if re.search(r"amazon\.|amzn\.", a) and not (f"tag={TAG}" in a and 'rel="sponsored nofollow noopener"' in a and 'target="_blank"' in a):
                err(f, "untagged or unmarked Amazon link: " + a)
    if ERRORS:
        print("BUILD FAILED:\n  " + "\n  ".join(ERRORS), file=sys.stderr); sys.exit(1)

posts_ok = main()
