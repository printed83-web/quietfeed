
Quiet Feed — Auto-Updating Minimalist Site
=========================================

This folder contains a self-updating static website that posts a small daily note for calm focus.

What's inside
-------------
- index.html — home page (auto-rebuilt)
- about.html — about page
- assets/style.css — minimalist styling
- posts/ — generated posts live here (one HTML file per run)
- templates/post_template.html — HTML for each post
- auto_post.py — the script that fetches a quote and builds a new post

Quick start
-----------
1) Install Python 3 and then:
   pip install requests

2) Run:
   python auto_post.py

3) Open index.html in your browser to see the site update.

Monetize
--------
- Paste your Google AdSense snippet into index.html and templates/post_template.html
  (search for 'Ad block placeholder').
- Add affiliate links if you want.
- Header already links to your shop: http://www.redbubble.com/people/minimalistix

Deploy free
-----------
- Netlify: drag the entire 'auto_site' folder into Netlify to deploy.
- GitHub + Netlify (recommended): connect repo so every commit auto-redeploys.

Automate daily
--------------
- Use Windows Task Scheduler or macOS launchd to run 'python auto_post.py' once per day.
- Or use a cloud cron (Render.com / GitHub Actions) to rebuild automatically.

— Built for Minimalistix · "Quiet strength. Simple truth. Art that breathes."
