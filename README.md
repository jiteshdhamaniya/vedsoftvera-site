# Ved Softvera — Static Site

A single-file, static replacement for the WordPress site at vedsoftvera.com.
No PHP, no database, no plugins, no build step — just `index.html`.

## Preview locally

Open `index.html` in any browser, or serve the folder:

```bash
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Deploy (all free)

Pick one — each hosts a static folder:

- **Netlify** — drag the folder onto https://app.netlify.com/drop
- **Cloudflare Pages** — connect a repo or upload the folder
- **GitHub Pages** — push to a repo, enable Pages on the `main` branch
- **Vercel** — `vercel` in this folder, or import the repo
- **Any shared host** — upload `index.html` to the web root via FTP

Then point the `vedsoftvera.com` DNS at the new host and cancel the
WordPress hosting once it's live.

## Editing

Everything is in `index.html` — content, styles, and one small script are
all inline. Search for the text you want to change and edit it directly.

- Company info / services / portfolio: the `<section>` blocks in `<main>`.
- Colors: the `:root { --brand: ... }` variables near the top of `<style>`.
- Contact form: currently opens the visitor's email client (`mailto:`).
  For a real inbox-delivered form with no backend, swap the `<form action>`
  to a service like Formspree or Web3Forms (one-line change).

## Notes

- Content mirrors the current site: web, mobile, and design services;
  White Label, IT Consulting, and Prebuilt Designs; selected work
  (Brandamos, Chipotle, 22 Pushups, Davy Select); and the Jaipur contact
  details.
- The blog was WordPress-dynamic and is omitted. If you want a blog on the
  static site, the simplest path is a Markdown-based static generator
  (Astro / Eleventy) or an external service — say the word and I'll wire it.
