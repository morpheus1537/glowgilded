# Digital Profit Review (digitalprofitreview.com)

This is a static site. `build.py` turns Markdown articles into HTML, and the generated HTML is committed to the repo. Vercel serves it and auto-deploys every push to `main`. Vercel does not run the build, so **you must run `python3 build.py` and commit its output.**

## Folder structure
```
content/
  _template.md            copy this to start a new article (not built)
  home/<slug>.md          one Markdown file per article, folder = category key
  beauty/<slug>.md
data/
  products.yaml           every Amazon product: ASIN -> name, rating, count, checked (YYYY-MM-DD)
  categories.yaml         list of categories (key, name, blurb)
assets/<category>/        hero images: <name>-lg.webp (900w), <name>-sm.webp (480w), <name>-og.jpg (1200x630)
build.py                  generator + validation
requirements.txt          pinned: markdown, PyYAML, Pillow
home/ beauty/ about/ ...  GENERATED HTML (never edit by hand)
```

## How to add an article (follow exactly, including automated pin routines)
1. **Pull first:** `git pull --rebase origin main`. Other routines push to this repo too.
2. **Install once:** `pip install -r requirements.txt`. If pip refuses, add `--user --break-system-packages`.
3. **Products:** for each product, open `https://www.amazon.com/dp/<ASIN>` today and confirm it is in stock. Copy its star rating and rating count.
   - Add or update its entry in `data/products.yaml` with `checked` set to today's date.
   - Do not add prices or made-up ratings.
4. **Hero image:** save it under `assets/<category>/`. Generate the three sizes with this snippet:
   ```python
   from PIL import Image; im=Image.open("SRC.jpg").convert("RGB"); b="assets/home/my-post"
   for w,k in ((900,"lg"),(480,"sm")): w=min(w,im.width); im.resize((w,round(im.height*w/im.width))).save(f"{b}-{k}.webp",quality=76)
   W,H=im.size; ch=round(W*630/1200); t=(H-ch)//3; im.crop((0,t,W,t+ch)).resize((1200,630)).save(b+"-og.jpg",quality=82)
   ```
5. **Article:** copy `content/_template.md` to `content/<category>/<slug>.md`. The file name must equal `slug`.
   - Fill in every front matter field.
   - Write the body in Markdown. Aim for 1,200–1,800 words, an intro, and one `## ` section per product.
   - Each product section has `### Why we like it`, `### Who it's for`, `### Pros` and `### Cons`, and ends with `{{ product <ASIN> }}`.
   - Add buying tips sections, then finish with `## The bottom line`.
6. **Build:** `python3 build.py`.
   - It prints each URL with its word count and reading time.
   - If it prints `BUILD FAILED`, fix the listed problems, rebuild, and **do not push** until it passes.
7. **Commit and push:** `git add -A && git commit -m "Add article: <title>" && git push origin main`.
   - If the push is rejected, run `git pull --rebase origin main`, then `python3 build.py`, then push again.
8. **Check:** after about a minute, `https://digitalprofitreview.com/<category>/<slug>/` should return 200.

## What the build does for you
The template adds these to every article automatically:
- the disclosure (top of the post and the footer), byline, dates and reading time
- the table of contents and the comparison table (from `comparison`)
- numbered product H2s linked to Amazon, each with its verified rating line
- the pros and cons boxes and the "Check price on Amazon" button (from `{{ product ASIN }}`)
- the FAQ (from `faq`), related posts and internal links
- the canonical URL, Open Graph and Twitter tags, and JSON-LD (BlogPosting, ItemList, FAQPage, BreadcrumbList)
- the sitemap with lastmod, and robots.txt

Every Amazon link is `https://www.amazon.com/dp/<ASIN>?tag=hearthhaven0b-20` with `rel="sponsored nofollow noopener" target="_blank"`. **Never paste raw Amazon links.** Use `{{ product ASIN }}`; the build fails on any untagged Amazon link.

## Validation (the build fails on)
- missing front matter fields (title, slug, category, description, date, updated, author, hero image and alt, products, faq)
- a slug that does not match the file name, or a category that does not match the folder
- an unknown ASIN (one not in `data/products.yaml`), or a shortcode ASIN missing from `products`
- missing hero image files
- any Amazon link in the output without the tag, rel or target

## Add a category
Add one entry to `data/categories.yaml` and create `content/<key>/`.

## Rules
- No fake ratings or reviews, and no prices.
- Do not hotlink Amazon product images.
- Keep exactly one H1; the build handles that.
