# Repository operations

## Production hosting

- Site: https://vedsoftvera.com/ and https://www.vedsoftvera.com/
- Production server: **178.104.104.20**, hostname **ai-sales**.
- Site directory: **/var/www/vedsoftvera**.
- Runtime: static HTML/CSS/JavaScript/assets served by Nginx; no application database.
- Deployable content: public root files and `assets/`, staged by `.github/scripts/prepare-site.py`.
- Automatic deployment: `.github/workflows/deploy.yml` validates PRs and deploys `main` to the VPS using `deploy-vedsoftvera`. GitHub Pages is a separate preview.
- Before merging, run `python3 .github/scripts/test_prepare_site.py` and stage the site with the packaging script.
- Source repository: https://github.com/jiteshdhamaniya/vedsoftvera-site.
- Hosting migrated from Contabo `109.123.253.23` on 2026-10-02. Do not deploy this site to Contabo.
- Read [deploy/SERVER.md](deploy/SERVER.md) before deployment or server changes. Verify current DNS and repository deployment settings rather than relying solely on this dated record.

## Work boundaries

The server also hosts The Doctors Directory and JD Softvera. Limit changes to this site's files, Nginx virtual host, and certificate. Do not restart or modify unrelated services.

Use existing authorised SSH access; never commit private keys, credentials, customer data, or server backups. Validate Nginx before reloading it. Preserve a rollback copy before changing production.

Create ready-for-review PRs, never drafts. Run relevant checks, review the diff, and verify public HTTPS separately from local validation and deployment success. Server relocation does not authorise marketing/content changes.
