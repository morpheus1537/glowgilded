#!/usr/bin/env python3
"""Builds the Glow & Gilded static site. Run: python3 build.py"""
import os, re, datetime, html
BASE = os.environ.get("SITE_URL", "https://digitalprofitreview.com").rstrip("/")
PIN = "https://www.pinterest.com/glowgilded/"
NAME = "Glow & Gilded"
TAG = "hearthhaven0b-20"
DISC = "As an Amazon Associate we earn from qualifying purchases. Some links on this site are affiliate links, which means we may earn a commission at no extra cost to you."
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Montserrat:wght@400;500;600&display=swap" rel="stylesheet">'
def amz(asin): return f"https://www.amazon.com/dp/{asin}?tag={TAG}"
def page(title, desc, body, path, image="assets/og.jpg", depth=0, kind="website"):
    r = "../" * depth
    url = f"{BASE}/{path}".replace("index.html", "")
    t = html.escape(f"{title} | {NAME}")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title><meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}"><link rel="icon" href="{r}assets/favicon.png">
<meta property="og:type" content="{kind}"><meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/{image}">
<meta name="twitter:card" content="summary_large_image">{FONTS}
<link rel="stylesheet" href="{r}assets/style.css">
<script async defer data-pin-hover="true" data-pin-tall="true" src="https://assets.pinterest.com/js/pinit.js"></script>
</head><body><div class="topbar">Considered luxury beauty · Gift guides · Rituals worth keeping</div>
<header class="site"><a class="brand" href="{r}index.html"><img src="{r}assets/logo.jpg" alt="{NAME} logo" width="48" height="48"><span>GLOW &amp; GILDED</span></a>
<nav><a href="{r}index.html">Journal</a><a href="{r}about.html">About</a><a href="{PIN}" target="_blank" rel="noopener">Pinterest</a></nav></header>
<main>{body}</main>
<footer><p class="fbrand">GLOW &amp; GILDED</p><p class="disc">{DISC}</p>
<p><a href="{PIN}" target="_blank" rel="noopener">Follow on Pinterest</a> · <a href="{r}affiliate-disclosure.html">Affiliate Disclosure</a> · <a href="{r}privacy.html">Privacy Policy</a> · <a href="{r}about.html">About</a></p>
<p>Content is for general information and is not medical advice. Patch-test new products.</p><p>&copy; {datetime.date.today().year} {NAME}</p></footer></body></html>"""

from posts import POSTS
pages, cards = {}, ""
for p in POSTS:
    body = re.sub(r"\{\{AMZ:(\w+)\}\}", lambda m: amz(m.group(1)), p["body"])
    share = f"https://www.pinterest.com/pin/create/button/?url={BASE}/posts/{p['slug']}.html&amp;media={BASE}/{p['image']}&amp;description={html.escape(p['title'])}"
    art = f"""<article class="post"><p class="kicker">{p['kicker']}</p><h1>{p['title']}</h1><p class="meta">Updated {p['date']} · By the Glow &amp; Gilded editors</p>
<p class="disc-top"><strong>Disclosure:</strong> {DISC}</p>
<figure class="pinwrap"><img src="../{p['image']}" alt="{html.escape(p['title'])}" width="1000" height="1500" data-pin-description="{html.escape(p['title'])} | {NAME}" data-pin-url="{BASE}/posts/{p['slug']}.html"></figure>
{body}
<p class="pin-cta"><a class="btn" href="{share}" target="_blank" rel="noopener">Save this guide to Pinterest</a></p></article>"""
    pages[f"posts/{p['slug']}.html"] = page(p["title"], p["desc"], art, f"posts/{p['slug']}.html", p["image"], 1, "article")
    cards += f"""<a class="card" href="posts/{p['slug']}.html"><img src="{p['image']}" alt="" loading="lazy" width="1000" height="1500"><div><p class="kicker">{p['kicker']}</p><h3>{p['title']}</h3><p>{p['desc']}</p></div></a>"""

pages["index.html"] = page("Luxury Beauty Gift Guides & Skincare Rituals", "Considered luxury beauty: curated skincare gift guides, premium routines and at-home spa rituals.",
 f"""<section class="hero"><div><p class="eyebrow">The Glow &amp; Gilded Journal</p><h1>Beauty that feels like a little luxury, every day</h1>
<p class="lead">We curate the creams, cleansers and spa-night rituals worth the splurge, and we skip the ones that aren't. Highly rated picks only, explained in plain language.</p>
<p><a class="btn" href="#latest">Read the journal</a> &nbsp; <a class="btn ghost" href="{PIN}" target="_blank" rel="noopener">Follow on Pinterest</a></p></div>
<div class="art"><img src="assets/hero-gift-guide.jpg" alt="Luxury skincare gift guide" width="1000" height="1500"></div></section>
<h2 class="sec" id="latest">Latest from the journal</h2><hr class="divider"><div class="grid">{cards}</div>
<section class="band"><p class="eyebrow">Our promise</p><h2>Only well-loved, in-stock picks</h2><p>Every product we feature is rated 4.3 stars or higher by real buyers and was in stock when we checked. When something sells out, we update the guide.</p></section>""", "index.html")
pages["about.html"] = page("About", f"About {NAME}.", f"""<article class="post"><p class="kicker">About</p><h1>About {NAME}</h1>
<p>{NAME} is a small beauty journal for people who love a good ritual: the cleanser that melts away the day, the cream that makes skin feel cared for, the quiet ten minutes that feel like a spa visit at home.</p>
<p>We focus on premium, well-reviewed skincare and beauty tools, and we try to explain <em>why</em> something earns a place in a routine instead of just telling you to buy it. We favor products with large numbers of real buyer reviews, and we re-check availability when we update a guide.</p>
<p>We are not dermatologists, and nothing here is medical advice. If you have a skin condition, are pregnant, or use prescription skincare, check with a qualified professional before adding new actives or devices.</p>
<p>Find daily inspiration on <a href="{PIN}" target="_blank" rel="noopener">our Pinterest</a>.</p></article>""", "about.html")
pages["affiliate-disclosure.html"] = page("Affiliate Disclosure", f"How {NAME} earns money.", f"""<article class="post"><p class="kicker">Transparency</p><h1>Affiliate Disclosure</h1>
<p>{NAME} is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com.</p>
<p><strong>As an Amazon Associate we earn from qualifying purchases.</strong> If you click a product link on this site or on our Pinterest pins and then buy something, we may earn a small commission. It costs you nothing extra.</p>
<p>Commissions never decide what we feature. We choose products based on ingredients, design, buyer ratings and review volume. Prices and availability change often, so always check the current details on Amazon before you buy.</p>
<p>Questions? Message us through <a href="{PIN}" target="_blank" rel="noopener">Pinterest</a>.</p></article>""", "affiliate-disclosure.html")
pages["privacy.html"] = page("Privacy Policy", f"Privacy policy for {NAME}.", f"""<article class="post"><p class="kicker">Legal</p><h1>Privacy Policy</h1><p class="meta">Last updated {datetime.date.today():%B %d, %Y}</p>
<p>This site does not ask you to create an account and does not collect your name, email or payment details.</p>
<h2>Third parties</h2><ul><li><strong>Hosting:</strong> our host (Vercel) may keep standard server logs (IP address, browser, pages requested) for security and reliability.</li>
<li><strong>Google Fonts:</strong> fonts load from Google, which receives your IP address under <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google's privacy policy</a>.</li>
<li><strong>Pinterest:</strong> the Pinterest Save button loads a script from Pinterest, which may set cookies under <a href="https://policy.pinterest.com/privacy-policy" target="_blank" rel="noopener">Pinterest's privacy policy</a>.</li>
<li><strong>Amazon:</strong> if you click an Amazon link, Amazon may use cookies to credit the referral to us, under <a href="https://www.amazon.com/privacy" target="_blank" rel="noopener">Amazon's privacy notice</a>.</li></ul>
<h2>Your choices</h2><p>You can block or delete cookies in your browser settings. We don't sell personal information because we don't collect it. You can contact us through Pinterest with any privacy request.</p>
<h2>Children</h2><p>This site is not directed at children under 13.</p></article>""", "privacy.html")
for path, h in pages.items():
    open(path, "w").write(h)
today = datetime.date.today().isoformat()
open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
 "".join(f"  <url><loc>{BASE}/{p.replace('index.html','')}</loc><lastmod>{today}</lastmod></url>\n" for p in pages) + "</urlset>\n")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
for p in POSTS: print(p["slug"], len(re.sub("<[^>]+>", " ", p["body"]).split()), "words")
