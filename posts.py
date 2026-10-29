def P(n, name, asin, rating, text, cta="View on Amazon"):
    return f"""<div class="product"><div class="num">{n:02d}</div><div><h3>{name}</h3><p class="rating">{rating} · checked October 2026</p><p>{text}</p>
<a class="btn" href="{{{{AMZ:{asin}}}}}" target="_blank" rel="sponsored noopener">{cta}</a></div></div>"""

MC = ("ELEMIS Pro-Collagen Marine Cream", "B00BEEK5II", "4.6 stars on Amazon from 2,900+ ratings")
CB = ("ELEMIS Pro-Collagen Cleansing Balm", "B08MJZYW8P", "4.5 stars on Amazon from 16,000+ ratings")
NC = ("ELEMIS Pro-Collagen Night Cream", "B00175YVOS", "4.7 stars on Amazon from 1,700+ ratings")
LM = ("LANEIGE Lip Sleeping Mask (Berry)", "B07XXPHQZK", "4.6 stars on Amazon from 37,000+ ratings")
SP = ("Slip Pure Silk Queen Pillowcase (Black)", "B0FJYZH32G", "4.6 stars on Amazon from 1,700+ ratings")
PC = ("Paula's Choice Skin Perfecting 2% BHA Liquid Exfoliant", "B00949CTQQ", "4.5 stars on Amazon from 117,000+ ratings")
SM = ("Shark CryoGlow LED Face Mask", "B0DSGJCS47", "4.4 stars on Amazon")

POSTS = [
dict(slug="luxury-skincare-gift-guide", kicker="The Gift Edit", image="assets/hero-gift-guide.jpg", date="October 29, 2026",
title="The Luxury Skincare Gift Guide: 5 Splurges She'll Actually Use",
desc="Five highly rated luxury skincare and beauty gifts, from a cult cleansing balm to a pure silk pillowcase, and how to choose the right one for her.",
body=f"""
<p>The best beauty gifts are not the ones that look pretty under the tree and then sit in a drawer. They are the ones that quietly become part of someone's day: the cleanser she reaches for every night, the cream she rations because she loves it. This guide is built around that idea. Every pick below is a genuine luxury, has thousands of real buyer ratings behind it, and was in stock on Amazon when we checked.</p>
<h2>How to choose a skincare gift</h2>
<ul><li><strong>Pick a texture, not a promise.</strong> Most people know whether they like rich balms or light gels. If you're unsure, a cleanser or lip treatment is the safest choice, because almost everyone uses one.</li>
<li><strong>Avoid strong actives for surprise gifts.</strong> Retinoids and acids are personal; save them for someone who has asked for them.</li>
<li><strong>Think about fragrance.</strong> Several premium lines are lightly scented. If she has sensitive skin, look for fragrance-free versions.</li></ul>
<h2>The edit</h2>
{P(1, *CB, "The gift that converts people to cleansing balms. It starts as a solid balm, melts into an oil as you massage, then turns milky when you add water, taking long-wear makeup and sunscreen with it. The aromatherapy-style scent makes the nightly cleanse feel like a facial. A beautiful 'first luxury' for someone who has never splurged on skincare.")}
{P(2, *MC, "ELEMIS's best-known moisturizer: a lightweight gel-cream with marine algae that sits nicely under makeup. It is the kind of product people buy for themselves once and then keep repurchasing, which is exactly what makes it a good gift. Pair it with the cleansing balm for a complete morning-and-night set.")}
{P(3, *SP, "A silk pillowcase is the gift people love but rarely buy for themselves. Slip uses heavy 22-momme mulberry silk, which glides rather than tugs, so hair stays smoother and night creams stay on the face instead of the pillow. Queen size with a hidden zipper; black hides makeup marks.")}
{P(4, *LM, "The best stocking stuffer in beauty. A rich overnight lip mask with shea and murumuru butters that leaves lips soft by morning. It's an easy add-on to any bigger gift, and at its price it's a nice way to try a premium brand.")}
{P(5, *NC, "For the person who loves a rich cream. This is the heavier, nighttime partner to the Marine Cream, with a thick balm-like texture that suits dry or mature skin, especially in colder months.")}
<div class="tip"><strong>Build a set:</strong> Cleansing Balm + Marine Cream + Lip Sleeping Mask covers a full routine for someone who enjoys skincare. Add the silk pillowcase for a true splurge.</div>
<h2>Wrapping it like a luxury gift</h2>
<p>Skincare gifts look most considered when presented as a ritual. Tuck the products into a soft towel or a small basket, add a handwritten card with the order to use them (cleanse, moisturize, lip mask last), and finish with a ribbon. It turns a few jars into an experience.</p>
<p>Prices and stock change quickly in gifting season, so check the current listing before you buy. If an item has sold out, we'll swap in an alternative when we update this guide.</p>
"""),
dict(slug="premium-skincare-routine", kicker="The Routine", image="assets/hero-routine.jpg", date="October 29, 2026",
title="A Premium Skincare Routine, Step by Step (Morning & Night)",
desc="A simple, luxurious morning and evening skincare routine built on five well-reviewed products, with the right order and how often to use each one.",
body=f"""
<p>A luxury routine does not need twelve steps. It needs a handful of products that each do one job well, used in the right order. Below is a simple morning and evening routine built on five widely loved products, plus the reasoning behind each step, so you can swap in what you already own.</p>
<h2>The golden rule: thinnest to thickest</h2>
<p>Apply products from the most watery to the richest. Light liquids absorb first; creams and balms seal everything in. In the morning, sunscreen is always the final skincare step.</p>
<h2>Evening routine</h2>
{P(1, *CB, "Step one at night: massage a pea-sized amount over dry skin for a minute to dissolve makeup and sunscreen, then add warm water and remove with a damp cloth. If you wear heavy makeup, this single step does the work of a makeup remover and first cleanse.")}
{P(2, *PC, "Two or three evenings a week (not every night at first), sweep this leave-on salicylic acid exfoliant over the face with a cotton pad after cleansing. It helps with visible pores and rough texture. Start slowly, skip it if your skin feels tight or stings, and always wear sunscreen the next day.")}
{P(3, *NC, "Finish with a rich cream. This one has a thick, cushiony texture that feels lovely on dry or mature skin overnight. Warm it between your fingertips and press it in rather than rubbing.")}
{P(4, *LM, "Last step: a generous layer on the lips. You'll wake up to noticeably softer lips, which also makes lipstick go on better the next day.")}
<h2>Morning routine</h2>
<ol><li><strong>Rinse or gentle cleanse.</strong> If you cleansed well the night before, lukewarm water is often enough in the morning.</li>
<li><strong>Moisturize.</strong> Use something lighter than your night cream so makeup sits well.</li></ol>
{P(5, *MC, "A lightweight gel-cream that absorbs quickly and gives a smooth base for makeup. It's the daytime partner to the night cream above.")}
<ol start="3"><li><strong>Sunscreen, every day.</strong> Broad-spectrum SPF 30 or higher is the single most effective anti-aging step there is. Apply it after moisturizer and before makeup.</li></ol>
<div class="tip"><strong>New to exfoliating acids?</strong> Introduce one new product at a time, two weeks apart, and patch-test on your jawline first. If you use prescription retinoids, ask your dermatologist before adding a BHA.</div>
<h2>How long until you see a difference?</h2>
<p>Hydration you can feel immediately. Texture and glow usually take four to six weeks of consistent use, because that's roughly how long skin takes to renew its surface. Consistency matters more than any single product, so pick a routine you'll genuinely enjoy doing.</p>
"""),
dict(slug="at-home-spa-night-beauty-tech", kicker="At-Home Spa", image="assets/hero-spa.jpg", date="October 29, 2026",
title="The At-Home Spa Night: Beauty Tech & Rituals Worth the Splurge",
desc="Recreate a spa facial at home with an LED mask, a melting cleansing balm and a silk pillowcase, plus a simple 45-minute spa-night ritual.",
body=f"""
<p>A good facial is part technique, part atmosphere. You can recreate a surprising amount of both at home: dim lights, a warm cloth, a slow cleanse, and a little beauty tech. Here is our favorite 45-minute spa-night ritual and the well-reviewed tools that make it feel indulgent.</p>
<h2>Set the scene (5 minutes)</h2>
<p>Run a warm shower to steam the bathroom, light a candle, and put your phone on Do Not Disturb. Soak a small face cloth in warm water. The point is to signal to yourself that this is a pause, not another chore.</p>
<h2>The ritual</h2>
{P(1, *CB, "Step one is a slow, massaging cleanse. Take two full minutes, working the balm in small circles along the jaw, cheekbones and brow, then press the warm cloth over your face for a few breaths before wiping. This is the moment that feels most like a professional facial.")}
{P(2, *SM, "LED masks are the headline piece of at-home beauty tech. Shark's CryoGlow combines red, blue and infrared light with a cooling under-eye panel that feels wonderful after a long day. Use it on clean, dry skin and follow the manufacturer's session times and safety guidance. Results from LED build gradually with regular use over weeks, not in a single night.")}
{P(3, *NC, "After your light session, seal everything in with a rich cream. Press it in with flat palms, then use your knuckles to sweep gently from the center of the face outward, like a facialist's lymphatic massage.")}
{P(4, *LM, "Lips get a thick layer of mask while the rest of the ritual sinks in.")}
{P(5, *SP, "End the night on silk. A silk pillowcase reduces friction on skin and hair while you sleep and keeps your night cream on your face, so it's the perfect final step of any spa night.")}
<div class="tip"><strong>Safety first with devices:</strong> LED masks aren't for everyone. Check the instructions before use if you have light sensitivity, epilepsy, eye conditions, are pregnant, or take medication that increases photosensitivity, and ask a doctor if unsure.</div>
<h2>Make it a weekly habit</h2>
<p>Choose one evening a week, like Sunday, and protect it. Over a month, the combination of thorough cleansing, regular LED sessions and better sleep on silk adds up to skin that looks rested, and you'll get four genuinely restful evenings out of it too.</p>
"""),
]
