# Ved Softvera — Static Site

A **multi-page** static replacement for the WordPress site at vedsoftvera.com.
No PHP, no database, no plugins, no build step — just HTML + one CSS file.

## Structure

- `index.html` — home
- `about.html`, `about-us.html`, `contact.html`, `work.html`, `blog.html`, `products.html`, `thank-you.html`
- Legal: `privacy-policy.html`, `terms-and-conditions.html`, `refund-and-cancellation.html`
- ~26 service pages (e.g. `laravel-development.html`, `android-app-development.html`, `it-consulting.html`, …)
- 47 portfolio pages `portfolio-<slug>.html` + `case-study-road-haul-services.html`
- `styles.css` — the single shared stylesheet (design lives here)

All links are relative, so it works both on a project GitHub Pages subpath
and at a root domain.

## Content

Page copy is reproduced **verbatim** from the live site. The original
WordPress install had been hacked and injected with ~14,000 pages of
multilingual casino/gambling SEO spam — **all of that was excluded**. Only
genuine Ved Softvera business content was kept. A few source pages were
entirely spam (`about-us`, `thank-you` was partly spam) and are noted in the
build; several portfolio items were image-only on the source and were
rebuilt as clean titled placeholders (no invented copy).

Note: some source pages carry legacy "JD Softvera" / partner boilerplate in
their own text (privacy, terms, a few service pages). That is what the live
site actually says, so it was preserved as-is rather than rewritten.

## Preview locally

```bash
python3 -m http.server 8000   # visit http://localhost:8000
```

## Deploy (all free)

- **GitHub Pages** — already configured for this repo.
- **Netlify** — drag the folder onto https://app.netlify.com/drop
- **Cloudflare Pages / Vercel** — connect the repo.

Point `vedsoftvera.com` DNS at the new host and cancel the WordPress hosting
once it's live. (Doing this also kills the injected spam farm.)

## Editing

Design: edit `styles.css` (colors are the `:root { --brand: … }` variables at
the top). Content: each page is its own `.html` file — edit the text directly.
The header/footer are duplicated per page; if you change the nav, update it
across files (or ask and I'll add a small include).

The contact form currently opens the visitor's email client (`mailto:`). For
inbox-delivered submissions with no backend, swap the `<form action>` to
Formspree or Web3Forms — a one-line change.
