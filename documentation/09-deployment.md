# 09 · Deployment

SRMS has three deployable pieces:

1. The Tkinter desktop client.
2. The SQL Server database (or the SQLite fallback).
3. The static GitHub Pages documentation website.

There is also a local Flask database inspector. None of these pieces is production-hardened as shipped.

> [!CAUTION]
> The demo uses `SA`, a published password, and an unencrypted backup. Do not expose SQL Server or the Flask viewer to the internet, and do not use this deployment model for real student records.

---

## Deployment options

| Target | What runs | Intended use |
| :-- | :-- | :-- |
| Local workstation | SQL Server container + desktop client | Course demonstration |
| Local workstation, SQLite | Desktop client + SQLite file | UI review without SQL Server |
| Local Flask viewer | Read-only browser inspector | Schema and audit inspection |
| GitHub Pages | Static website from `docs/` | Public documentation |
| CI | Syntax, YAML, link, and documentation checks | Repository quality gate |

There is no supported production server deployment.

---

## Local desktop deployment

### 1. Prepare the host

- Install Python 3.10+ and Tkinter.
- Install Docker.
- Create a working directory with at least a few hundred MB free.
- Ensure port 1433 and, if used, port 5000 are available.

### 2. Start SQL Server

```bash
docker run \
  -e 'ACCEPT_EULA=Y' \
  -e 'MSSQL_SA_PASSWORD=Srms@2024!' \
  -p 127.0.0.1:1433:1433 \
  --name sqlserver2022 \
  --hostname sqlserver \
  -d mcr.microsoft.com/mssql/server:2022-latest
```

Binding to `127.0.0.1` is safer than exposing the port on every interface. If the client runs in another container, use a Docker network instead of publishing the port publicly.

### 3. Load the database

Follow [05 · Installation](05-installation.md). The short version:

```text
create SRMS_SecureDB
→ sqlserver_schema.sql
→ sqlserver_roles.sql
→ sqlserver_views.sql
→ sqlserver_procedures.sql
→ sqlserver_sample_data.sql
```

### 4. Install the client

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SRMS_MASTER_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
```

Record the generated key somewhere safe for the session. Losing it makes existing application-encrypted values unreadable. Do not commit it.

### 5. Launch

```bash
python src/gui/main.py
```

For the orchestrated path:

```bash
python launch.py
```

The launcher may start Docker, DBeaver, Flask, and the GUI. Treat it as a convenience script, not a supervisor or production process manager.

---

## SQLite deployment

SQLite mode is a development fallback.

```python
# src/database/connection.py
DATABASE_TYPE = 'sqlite'
```

Then:

```bash
python src/gui/main.py
```

Operational notes:

- The database file is `database/srms.db`.
- Back up the file before experiments.
- SQLite has no stored procedures or database roles.
- The application-level managers still enforce their rules where called.
- Do not serve the SQLite file from a web server.

---

## Flask viewer deployment

```bash
python db_viewer.py
```

The viewer is intended for localhost. If you must run it manually, bind to localhost:

```python
app.run(host="127.0.0.1", port=5000, debug=False)
```

Do not enable debug mode on a shared host. The debugger can expose an interactive console.

The viewer has no authentication of its own. It should not be reverse-proxied to the internet, even behind a password, without a full security review.

---

## Static website deployment

The website lives in `docs/` and is designed for GitHub Pages.

### Repository settings

1. Open **Settings → Pages**.
2. Set **Source** to **Deploy from a branch**.
3. Select branch `main` and folder `/docs`.
4. Save.
5. Wait for the Pages build to complete.

The expected URL is:

```text
https://ahmedbakr78.github.io/Secure-Student-Records-Management-Control/
```

### Why `.nojekyll`

The `docs/.nojekyll` file disables Jekyll processing. The site is plain HTML/CSS/JS and does not need a Ruby build. It also ensures assets whose names begin with an underscore are served.

### Custom domain

If you add a custom domain:

1. Add a `CNAME` file in `docs/`.
2. Configure DNS.
3. Enable HTTPS in Pages settings.
4. Update `sitemap.xml`, Open Graph URLs, and repository homepage.

### Local preview

```bash
python -m http.server 8080 --directory docs
```

Open <http://127.0.0.1:8080>. Do not open `docs/index.html` directly from the filesystem if you want to test absolute asset paths; a local HTTP server is closer to Pages.

---

## CI deployment

The workflow in `.github/workflows/ci.yml` performs static checks:

- Python syntax compilation.
- YAML parsing for GitHub configuration.
- Required file presence.
- Local Markdown link validation.
- Optional Mermaid source validation.

It intentionally does not run the desktop application or connect to SQL Server. A future workflow can add unit tests once a test harness exists.

### CI design rules

- Never embed database passwords or encryption keys in the workflow.
- Do not start SQL Server for a documentation-only change.
- Fail on broken local links.
- Keep the workflow fast and deterministic.

---

## Release deployment

A release should include:

| Asset | Why |
| :-- | :-- |
| `SRMS_SecureDB.bak` | Restore path for reviewers |
| SQL script bundle | Reproducible schema without cloning |
| `d_ds.pdf` | Original architecture report |
| Source archive | GitHub-generated automatically |
| Checksums | Integrity verification |

Build checksums after packaging:

```bash
sha256sum SRMS_SecureDB.bak d_ds.pdf > SHA256SUMS.txt
```

Attach assets with `gh release create` or the GitHub UI. Do not attach `.env` files, keys, or real data.

---

## Production hardening checklist

This checklist is deliberately strict. The current project does not satisfy it.

### Identity and access

- [ ] Remove demo accounts and the `SA` application path.
- [ ] Create per-user database logins mapped to database roles.
- [ ] Rotate all credentials.
- [ ] Enforce strong password policy and MFA.
- [ ] Replace the 2FA simulation with a real TOTP or WebAuthn flow.
- [ ] Add rate limiting and alerting for failed logins.

### Secrets

- [ ] Move connection settings to environment variables or a vault.
- [ ] Use a unique, random `SRMS_MASTER_KEY` per environment.
- [ ] Define key rotation and re-encryption procedures.
- [ ] Use encrypted, access-controlled backups.
- [ ] Remove secrets from logs and screenshots.

### Network

- [ ] Require TLS for database and viewer connections.
- [ ] Bind the viewer to localhost or place it behind authenticated TLS.
- [ ] Restrict SQL Server to a private network.
- [ ] Add firewall rules and egress controls.

### Data

- [ ] Replace demo data with synthetic test data only.
- [ ] Define retention and deletion policy.
- [ ] Classify every new column and table.
- [ ] Add database migrations and rollback.
- [ ] Test backup restore regularly.

### Application

- [ ] Unify password hashing on one modern algorithm.
- [ ] Unify encryption and key management.
- [ ] Add automated negative tests for every control.
- [ ] Ensure all SQL is parameterised.
- [ ] Prevent stack traces and connection strings from reaching users.
- [ ] Add structured audit export and tamper evidence.
- [ ] Complete an accessibility review.

### Operations

- [ ] Add health checks, metrics, and alerting.
- [ ] Add centralised logging with retention.
- [ ] Document incident response and rollback.
- [ ] Run a dependency and container vulnerability scan.
- [ ] Complete an independent security review.

---

## Rollback

### Database

- Restore the previous `.bak` to a new database name.
- Point the configuration at the restored database.
- Verify users, roles, views, procedures, and audit.
- Do not overwrite the only copy of the current database during a failed upgrade.

### Application

- Check out the previous release tag.
- Reinstall dependencies from that tag's `requirements.txt`.
- Verify the database schema is compatible.
- Keep encrypted data and its key together; restoring code without the key can make values unreadable.

### Website

- Revert the `docs/` change.
- Let Pages rebuild.
- Verify the home page, CSS, JS, and diagrams.
- Check the live URL after the deployment status reports success.

---

## Deployment evidence

For a course or review handoff, capture:

- Commit SHA and release tag.
- Database restore/load output.
- SQL object inventory.
- Role and grant inventory.
- Login and denial audit samples.
- Screenshot or recording of each role dashboard.
- Test matrix results.
- Known limitations and residual risks.

Do not include passwords, keys, or real data in the evidence pack.

---

## Related reading

- [05 · Installation](05-installation.md)
- [07 · Testing](07-testing.md)
- [10 · Troubleshooting](10-troubleshooting.md)
- [13 · Threat model](13-threat-model.md)
