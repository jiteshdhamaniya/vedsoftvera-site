# Production server

Verified migration date: 2026-10-02. Recheck live configuration before future changes.

| Item | Value |
| --- | --- |
| Domains | `vedsoftvera.com`, `www.vedsoftvera.com` |
| Server | `178.104.104.20` (`ai-sales`) |
| Web root | `/var/www/vedsoftvera` |
| Web server | Nginx on Ubuntu |
| Nginx configuration | `/etc/nginx/sites-available/vedsoftvera.com` |
| Enabled vhost | `/etc/nginx/sites-enabled/vedsoftvera.com` |
| TLS certificate | `/etc/letsencrypt/live/vedsoftvera.com/fullchain.pem` |
| ACME webroot | `/var/www/letsencrypt` |
| Access/error logs | `/var/log/nginx/vedsoftvera.access.log`, `/var/log/nginx/vedsoftvera.error.log` |

## Deployment

Manual static deployment from this repository. There is no GitHub Actions workflow deploying this site to the VPS; the existing GitHub Pages job is a separate preview.

The active source is `jiteshdhamaniya/vedsoftvera-site`, not the legacy WordPress repository `jiteshdhamaniya/vedsoftvera.com` or the separate `vedsoftvera-new` implementation.

For a reviewed and authorised release, stage the public files only (HTML/CSS and `assets/`) into a clean temporary directory. Compare that staged manifest with the intended release, then use the existing administrative SSH connection to synchronise that directory to `/var/www/vedsoftvera/`, preserving readable 755 directory and 644 file permissions. Confirm the exact destination before using rsync deletion. Never publish `.git`, credentials, server backups, or internal operational documentation. No PHP or database migration is required.

## DNS and HTTPS

Cloudflare hosts DNS. A record for the apex is DNS-only; `www` is a DNS-only CNAME to the apex. Preserve proxy settings and unrelated DNS records (mail and subdomains) when modifying the origin. The origin A record targets `178.104.104.20`.

Fresh Let's Encrypt certificates were issued on the new server; no private TLS keys were copied from Contabo. HTTP redirects to HTTPS except for `/.well-known/acme-challenge/`, served from the ACME webroot. `certbot.timer` schedules renewal and `/etc/letsencrypt/renewal-hooks/deploy/reload-nginx` reloads Nginx after renewal.

## Verification

```sh
curl --fail --resolve vedsoftvera.com:443:178.104.104.20 https://vedsoftvera.com/ -o /tmp/vedsoftvera-origin.html
curl --fail --head https://vedsoftvera.com/
curl --fail --head https://www.vedsoftvera.com/
```

Also verify a contact page, a stylesheet/image, an extensionless route, and the real public DNS path. Check the existing Doctors Directory remains reachable after shared Nginx changes. Successful HTTP responses do not certify contact-form delivery.

## Rollback and old hosting

A root-only migration backup of both sites and their original Nginx configurations is on the destination at `/root/softvera-migration-20261002/site-backup.tar.gz`. It contains no TLS private keys. Restore individual site files/configuration only after inspecting the archive and taking a backup of the current state. Do not overwrite the sibling sites.

The former origin `109.123.253.23` is retired for these two websites only. It continues hosting unrelated applications and previews, including `qc.jdsoftvera.com`; it is not a server-cancellation target. Do not restore old DNS or deployment targets without explicitly planning a rollback.
