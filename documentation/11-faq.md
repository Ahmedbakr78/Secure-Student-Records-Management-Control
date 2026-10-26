# 11 · FAQ

## General

### What is SRMS?

Secure Student Records Management Control is a Database Security course project: a Tkinter student information system backed by SQL Server and built around five security models.

### Is it production-ready?

No. It is an educational reference implementation with published demo credentials, hard-coded connection settings, simulated 2FA/email, and incomplete automated testing. See [13 · Threat model](13-threat-model.md).

### Who is it for?

Course instructors, security reviewers, students learning application security, and contributors who want a readable end-to-end example.

### What does SRMS stand for?

**Secure Student Records Management** — the trailing “Control” is part of the project name, not the acronym. Use **SRMS** as the short name.

### Why was the repository renamed?

The original coursework repository used a very long name. This release uses **Secure Student Records Management Control** while preserving the source and the original remote repository.

### What is the license?

GNU Affero General Public License v3.0. See [LICENSE](../LICENSE). Network use of a modified version triggers source-offer obligations.

---

## Security

### Does it really implement five security models?

Yes, at the application and SQL Server layers where applicable:

1. RBAC — permission matrix, own-row checks, database roles.
2. MLS — Bell–LaPadula NRU and NWD.
3. Inference control — minimum set size, MIN/MAX threshold, tracker detection.
4. Flow control — directional flow and action blocking.
5. Encryption — SQL Server AES-256 hierarchy and application Fernet/bcrypt.

The implementation has documented limitations. See [03 · Security models](03-security-models.md).

### Is AES-256 used everywhere?

No. The SQL Server `SRMS_SymmetricKey` uses AES-256. The Python application layer uses Fernet, which is AES-128-CBC plus HMAC-SHA256 in its standard construction, with PBKDF2-HMAC-SHA256 key derivation. The docs state this precisely.

### Why are the demo passwords public?

So a reviewer can test every role without provisioning accounts. They are deliberately insecure and must be removed or rotated before any non-demo use.

### Can a student see another student's grades?

The intended controls prevent it: own-row RBAC, the student view, the student dashboard filter, and the published-grade condition. Any observed bypass is a security defect and should be reported.

### Can a TA see grades?

No. The TA application matrix has no `GRADES` permission, and `db_TA` is denied on the table.

### Does MLS block the TA from recording attendance?

Potentially. TA clearance is Confidential (2), while attendance is Secret (3). The course delegates attendance duties to TAs and uses assignment filters/views, but a pure NRU check would deny the read. This is an explicit policy tension documented in [03 · Security models](03-security-models.md). A production design must define delegated access, not silently bypass MLS.

### Why does the student see their own Confidential profile with Unclassified clearance?

SRMS treats it as a controlled ownership exception. The student does not get a higher global clearance; a dedicated own-profile view/model path exposes only their linked record.

### Is the audit log tamper-proof?

No. It is a normal table and a database administrator can modify it. Tamper-evident logging is a roadmap item.

### Is 2FA real?

No. It is a six-digit dialog simulation with a five-minute expiry and three attempts. It is not TOTP and has no recovery flow.

### Is the Flask viewer safe to expose?

No. It is a read-only inspection tool with no authentication. Bind it to localhost only.

### Where do I report a vulnerability?

Follow [SECURITY](../SECURITY.md). Do not open a public issue with exploit details.

---

## Installation and operation

### Do I need SQL Server?

For the full security demonstration, yes. SQLite is a fallback for UI and application-layer evaluation.

### Why does `sqlcmd` reject `GO`?

`GO` is a batch separator understood by `sqlcmd`/Azure Data Studio, not T-SQL. Use a tool that supports batches.

### Why does the schema drop tables?

It is a repeatable classroom setup script. It guarantees a clean state. Never run it against real data.

### Can I use the backup instead of the scripts?

Yes. Restore `SRMS_SecureDB.bak` in the container. If logical file paths differ, add `MOVE` clauses. The backup is a demo artifact and is not encrypted.

### Why do SQL Server and SQLite show different record counts?

They use different sample datasets. The SQL Server script creates a smaller coursework dataset; the SQLite file includes additional support tables and data. Use the matching demo credentials and treat counts as backend-specific.

### Why does the app connect as `SA`?

It is a classroom convenience and a known hardening gap. Production must use a least-privilege application login.

### Why does login fail after five attempts?

The account is locked after five failed passwords. An admin can unlock it. The counter is part of the authentication path.

### How do I switch to SQLite?

Set `DATABASE_TYPE = 'sqlite'` in `src/database/connection.py`, or use the switcher, then relaunch. Data is not migrated automatically.

### The GUI does not start on a server. Why?

Tkinter requires a display. Use a desktop session or X forwarding. Headless CI should run static checks only.

### How do I start the Flask viewer?

```bash
python db_viewer.py
```

Then open <http://127.0.0.1:5000>. Keep it local.

### Where is the website deployed?

From `docs/` on GitHub Pages. The intended URL is `https://ahmedbakr78.github.io/Secure-Student-Records-Management-Control/`.

---

## Data and privacy

### Does the repository contain real student data?

No. The names, emails, phone numbers, and grades are synthetic classroom demo data. Do not add real records.

### Can I delete the demo database?

Yes, in a disposable local environment. Recreate it from the schema and seed scripts. Keep a backup if you need the original demo state.

### What data is encrypted?

SQL Server: student ID copy, student phone, instructor phone, grade value, and password material. Application layer: values passed through `EncryptionManager`, plus bcrypt password hashes on the SQLite path.

### What is `GradeValue_Display`?

A reporting/display helper column separate from the encrypted `GradeValue`. It is not a substitute for encrypting the primary value, and it must be treated as sensitive.

### Why are phone numbers masked?

Masked display values reduce casual exposure while the full value remains encrypted. A production design should define who may reveal the full value and audit the reveal.

---

## Contribution and project direction

### How can I contribute?

Read [CONTRIBUTING](../CONTRIBUTING.md), follow the [Code of Conduct](../CODE_OF_CONDUCT.md), and use the issue templates. Security reports go through [SECURITY](../SECURITY.md).

### Are automated tests included?

Not yet for the security controls. There is a manual matrix and a verification script. Automated tests are the top engineering priority in the [roadmap](12-roadmap.md).

### Why is there no Docker Compose file?

It is a roadmap item. The current setup uses a single `docker run` command and native Python processes.

### Will there be an Arabic interface?

Arabic/English localisation with RTL support is on the roadmap. It is not implemented.

### Can I use this for my own course project?

Yes, under AGPL-3.0, with attribution and an honest description of the security limitations. Do not present it as a certified production system.

### Why are there two Flask viewer files?

`db_viewer.py` and `web_viewer.py` are copies kept for compatibility. Use `db_viewer.py` as the documented entry point and keep them aligned.

### Why are there two password-hashing paths?

The project supports SQL Server and SQLite. SQL Server sample data uses SHA-256 + salt to match T-SQL; the SQLite/model path uses bcrypt. This is a documented limitation, not ideal design.

---

## Troubleshooting

### Where do I start when something fails?

See [10 · Troubleshooting](10-troubleshooting.md). Identify the layer from the exact error and confirm the backend before changing code.

### Why is an export blocked?

Flow control blocks export for Confidential and above. The block is intentional. Check the classification and the action policy.

### Why is a small aggregate blocked?

The inference controller requires at least three records; MIN/MAX requires six. Zero rows is allowed because no individual is disclosed.

### Why can’t I open a dashboard as another role?

The application routes the authenticated account to its role dashboard. Use the matching demo account. The dashboard is a usability boundary; the policy layer is the actual control.

---

## Still stuck?

- Read [05 · Installation](05-installation.md) and [10 · Troubleshooting](10-troubleshooting.md).
- Search existing issues.
- Open a new issue with a minimal, secret-free reproduction.
- Report security problems privately.
