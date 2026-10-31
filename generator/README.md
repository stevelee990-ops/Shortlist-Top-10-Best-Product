# The Shortlist — how this site is built and updated

Live site: https://the-shortlist-top10best.netlify.app/
Netlify publishes the `public/` folder automatically whenever `main` is pushed (see `netlify.toml`).
**Never edit files in `public/` by hand** — they are regenerated. Edit `generator/build.py` and `generator/style.css`, then run:

```
python3 generator/build.py
```

## Where things live in `build.py`
- `CATS` — every guide. Product lists have no `kind`; gift guides have `"kind": "gift"`.
  Each guide: `slug`, `icon`, `tint`, `short`, `title`, `card`, `lead`, `filters`, `products` (exactly 10), `tips`, `faq`, `sources`.
  Each product: `name`, `badge`, `price` (`$`–`$$$$`), `f` (filter keys), `tags`, `summary`, `pros` (2–3), `cons` (1–2).
- `ASIN` — product name → Amazon ASIN for exact product links. `QUERY` — product name → Amazon search phrase when no exact single listing exists.
  Every product needs one or the other. The Amazon tag (`shortlisttop1-20`) is added by `public/assets/config.js`; never hard-code it.
- Design: navy + white with yellow round "stickers" for ranks; display font Adventor Bold (self-hosted from `generator/fonts/`, GUST font license), body Inter. Keep new pages consistent with this look.
- `PHOTOS` — Unsplash photos (free Unsplash License only, never Unsplash+). `ICONS` — SVG icons. New category tints go in `style.css`.
- `NOUN`, `QOVERRIDE` — wording for the "Quick answer" box and the "by need" questions. Add a `NOUN` entry for every new product list, and override any question that reads awkwardly.
- `RELATED` — 3 related pages for each guide (add one for every new guide, and link it from 1–2 existing guides).
- `UPDATED`, `UPDATED_ISO`, `UPDATED_LONG` — set to the day you publish.

## Content rules (non-negotiable)
1. **Research before writing.** Base picks on recent (current-year) buying guides from reputable, hands-on testers (e.g. RTINGS, Wirecutter-style outlets, Tom's Guide, TechRadar, Forbes Vetted, America's Test Kitchen, Food Network, Reviewed, What Hi-Fi?). Use at least 2 sources per guide and list them in `sources`.
2. **Never invent facts.** No made-up specs, prices, star ratings, review counts, test results or quotes. Only state what sources say. Price tiers are rough ranges.
3. **No fake experience.** Never claim we tested a product. Never write first-person testimonials or create fake reviewers/people (FTC rule on fake reviews).
4. **Write in our own words.** Paraphrase; never copy sentences from sources.
5. **Amazon links:** only use an ASIN when an amazon.com search result clearly shows that exact product (right model, new, not a bundle/renewed). Otherwise use a `QUERY` search link. Never use Amazon or brand product images anywhere.
6. **Audience:** adults. Do not create content directed at children under 13 (Amazon Associates rule). Teen/kid gift pages only if clearly written for adult buyers.
7. **Don't touch:** Amazon tag, AdSense code, `ads.txt`, Google verification tag, disclosure text, or existing page URLs (never rename or delete a published page).

## Before every publish — checks
- `python3 generator/build.py` runs without errors and every guide has exactly 10 products.
- Every product has an `ASIN` or `QUERY` entry; every `Check price` link carries `tag=shortlisttop1-20` (config.js adds it).
- All `application/ld+json` blocks parse as JSON; `<title>` ≤ 65 characters.
- Quick answer and "by need" questions read naturally (fix with `NOUN`/`QOVERRIDE`).
- If Playwright is available: no page is wider than 390px on a phone-sized viewport, and filters never show an empty list.
- Add a line to `generator/CHANGELOG.md`.

## Publishing
One commit and one push to `main` per day (each push costs Netlify credits). Commit message ends with the attribution lines the session asks for.
