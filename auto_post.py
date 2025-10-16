#!/usr/bin/env python3
import os, json, datetime, requests, re

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
POSTS_DIR = os.path.join(SITE_ROOT, "posts")
ASSETS_DIR = os.path.join(SITE_ROOT, "assets")
TEMPLATES_DIR = os.path.join(SITE_ROOT, "templates")
SHOP_URL = "http://www.redbubble.com/people/minimalistix"

BASE_HTML = "<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n  <title>{title} \u00b7 Quiet Feed</title>\n  <meta name=\"description\" content=\"Quiet, minimalist daily notes for calm focus.\" />\n  <link rel=\"stylesheet\" href=\"/assets/style.css\" />\n  <!-- Google AdSense (paste your code below and remove the comments)\n  <script async src=\"https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=YOUR-ADSENSE-CLIENT-ID\"\n     crossorigin=\"anonymous\"></script>\n  -->\n</head>\n<body>\n<div class=\"container\">\n  <div class=\"header\">\n    <div>\n      <div class=\"brand\">Quiet Feed</div>\n      <div class=\"tagline\">Simple notes for calm focus</div>\n    </div>\n    <div class=\"nav\">\n      <a href=\"/\">Home</a>\n      <a href=\"/about.html\">About</a>\n      <a href=\"{shop_url}\" target=\"_blank\" rel=\"noopener\">Shop Minimalistix</a>\n    </div>\n  </div>\n  {content}\n  <div class=\"footer\">\n    \u00a9 {year} Quiet Feed \u00b7 Built by Minimalistix \u00b7 <a href=\"{shop_url}\" target=\"_blank\" rel=\"noopener\">Shop the calm</a>\n  </div>\n</div>\n</body>\n</html>\n"
INDEX_CONTENT_TPL = "\n<div class=\"hero\">\n  <h2 style=\"margin:0 0 8px 0;\">Quiet Feed</h2>\n  <p style=\"margin:0;\">This site updates itself with small daily notes for focus and calm.</p>\n  <div class=\"ad\">Ad block placeholder \u2014 add AdSense code to monetize impressions/clicks.</div>\n</div>\n\n<h3 style=\"margin:20px 0 8px 0;\">Latest posts</h3>\n<div class=\"grid\">\n  {cards}\n</div>\n"
CARD_TPL = "\n<a href=\"/posts/{slug}.html\" class=\"card\">\n  <h3>{title}</h3>\n  <p>{excerpt}</p>\n  <p style=\"margin-top:8px;font-size:12px;\">{date}</p>\n</a>\n"

def sanitize_slug(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\-\s]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text[:60] or "daily-note"

def fetch_quote():
    try:
        r = requests.get("https://zenquotes.io/api/random", timeout=10)
        data = r.json()
        q = data[0].get("q", "").strip()
        a = data[0].get("a", "Unknown").strip()
        if q:
            return q, a
    except Exception as e:
        print("ZenQuotes failed:", e)
    try:
        r = requests.get("https://api.quotable.io/quotes/random?limit=1", timeout=10)
        data = r.json()
        q = data[0].get("content","").strip()
        a = data[0].get("author","Unknown").strip()
        if q:
            return q, a
    except Exception as e:
        print("Quotable failed:", e)
    return "Small calm moments build quiet strength.", "Minimalistix"

def build_post(title: str, quote: str, author: str, date_str: str, slug: str):
    with open(os.path.join(TEMPLATES_DIR, "post_template.html"), "r") as f:
        post_tpl = f.read()
    content = post_tpl.format(title=title, quote=quote, author=author, date=date_str, shop_url=SHOP_URL)
    html = BASE_HTML.format(title=title, year=datetime.date.today().year, shop_url=SHOP_URL, content=content)
    out_path = os.path.join(POSTS_DIR, f"{slug}.html".format(slug=slug))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path

def rebuild_index():
    cards = []
    entries = []
    for name in os.listdir(POSTS_DIR):
        if name.endswith(".html"):
            path = os.path.join(POSTS_DIR, name)
            ts = os.path.getmtime(path)
            entries.append((ts, name))
    for _, name in sorted(entries, reverse=True):
        slug = name.replace(".html","")
        # Human-readable title for card
        title = slug.replace("-", " ").title()
        date = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(POSTS_DIR, name))).strftime("%b %d, %Y")
        excerpt = "A small daily note for calm focus."
        cards.append(CARD_TPL.format(slug=slug, title=title, excerpt=excerpt, date=date))

    index_html = BASE_HTML.format(
        title="Home",
        year=datetime.date.today().year,
        shop_url=SHOP_URL,
        content=INDEX_CONTENT_TPL.format(cards="\n".join(cards))
    )
    with open(os.path.join(SITE_ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

def main():
    os.makedirs(POSTS_DIR, exist_ok=True)
    quote, author = fetch_quote()
    today = datetime.date.today()
    date_str = today.strftime("%B %d, %Y")
    first_words = "-".join(quote.lower().split()[:4])
    slug = sanitize_slug(f"daily-note-{}-{}".format(today.isoformat(), first_words))
    title = f"Daily Quiet Note — {}".format(date_str)
    post_path = build_post(title, quote, author, date_str, slug)
    print("Generated post:", post_path)
    rebuild_index()
    print("Rebuilt index. Done.")

if __name__ == "__main__":
    main()
