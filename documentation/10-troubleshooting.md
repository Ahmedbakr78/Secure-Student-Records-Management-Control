# 10 · Troubleshooting

Use this guide to diagnose common setup and runtime problems. Start with the exact error text and the backend in use. Do not paste passwords, keys, or personal data into an issue.

---

## Quick triage

| Symptom | First check |
| :-- | :-- |
| `ModuleNotFoundError` | Virtual environment active and dependencies installed |
| `pymssql` build failure | System build dependencies or a compatible wheel |
| `Tkinter` import failure | OS package `python3-tk` or equivalent |
| SQL Server connection refused | Container running, port mapping, ready state |
| Login always fails | Backend selected, demo data loaded, password path |
| GUI starts but tables are empty | Wrong database or unseeded backend |
| Viewer cannot connect | Same backend config as the client |
| Export fails | Flow control, filesystem permissions, optional dependency |
| Website assets missing | Serve from `docs/`, check case-sensitive paths |

---

## Installation

### `python3: command not found`

Install Python 3.10 or newer from your platform's package manager or python.org. Confirm:

```bash
python3 --version
```

### `No module named tkinter`

Tkinter is an OS package, not a pip package.

```bash
# Debian / Ubuntu
sudo apt-get install -y python3-tk

# Fedora
sudo dnf install -y python3-tkinter
```

Then recreate the virtual environment if necessary.

### `No module named pymssql`

```bash
source .venv/bin/activate
python -m pip install pymssql
```

If it tries to compile and fails, install build tools:

```bash
# Debian / Ubuntu
sudo apt-get install -y build-essential python3-dev freetds-dev
```

Check the Python version. A wheel may not exist for a very new interpreter.

### `No module named flask`

```bash
python -m pip install Flask
```

Or install the full requirements:

```bash
python -m pip install -r requirements.txt
```

### Dependency conflict

Create a clean environment instead of forcing upgrades into a broken one:

```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## SQL Server

### `docker: command not found`

Install Docker Engine or Docker Desktop and confirm the daemon is running:

```bash
docker info
```

### Container exits immediately

```bash
docker logs sqlserver2022
```

Common causes:

- The SA password does not meet complexity requirements.
- The host has insufficient memory.
- The data directory is not writable.
- The `ACCEPT_EULA` variable is missing.

The published demo password `Srms@2024!` meets the SQL Server complexity rules, but replace it for any non-demo use.

### `Cannot connect to SQL Server` or `Connection refused`

```bash
docker ps -a --filter name=sqlserver2022
docker start sqlserver2022
docker logs --tail 100 sqlserver2022
```

Wait until the log reports that SQL Server is ready. Then test:

```bash
docker exec -it sqlserver2022 \
  /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U SA -P 'Srms@2024!' -C \
  -Q "SELECT @@VERSION;"
```

### Port 1433 already in use

```bash
ss -ltnp | grep 1433
```

Stop the conflicting service or map a different host port:

```bash
-p 1434:1433
```

Then update `SQLSERVER_CONFIG['port']` to `1434`.

### `Login failed for user 'SA'`

- Confirm the container password matches `SQLSERVER_CONFIG`.
- If the container was created earlier with a different password, the image will not change it. Recreate the container in a disposable environment.
- Check for a trailing space or shell quoting problem.

### TLS / certificate error with sqlcmd

The `-C` flag trusts the server certificate for this local connection. It is appropriate only for a local demo. In production, configure a trusted certificate and remove blind trust.

### `sqlcmd: command not found` inside the container

Recent SQL Server images place `sqlcmd` under `/opt/mssql-tools18/bin/`. Use the full path. Older images may use `/opt/mssql-tools/bin/`.

### Script stops at `GO`

`GO` is a `sqlcmd` batch separator, not T-SQL. Use `sqlcmd`, Azure Data Studio, or another tool that understands batches. Do not paste the whole file into a driver as a single statement.

### `Database 'SRMS_SecureDB' does not exist`

Create it first:

```bash
docker exec -it sqlserver2022 \
  /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U SA -P 'Srms@2024!' -C \
  -Q "IF DB_ID('SRMS_SecureDB') IS NULL CREATE DATABASE SRMS_SecureDB;"
```

### `There is already an object named ...`

The schema script is designed to drop and recreate SRMS objects. If it stops partway, fix the first error and rerun from a clean disposable database. Do not run it against real data.

### Restore fails with file paths

Inspect logical names:

```sql
RESTORE FILELISTONLY FROM DISK='/var/opt/mssql/backup/SRMS_SecureDB.bak';
```

Add `MOVE` clauses for the data and log files to a writable path inside the container.

### Out of disk or memory

SQL Server needs memory and disk for the database, logs, and backup. Free space and, for local review, consider a smaller SQL Server memory setting via the container environment. Do not tune production based on a classroom container.

---

## Application

### Application starts but cannot connect

Check the active backend:

```bash
python - <<'PY'
from src.database.connection import get_database_type
print(get_database_type())
PY
```

If it reports `sqlserver`, verify the container. If it reports `sqlite`, verify `database/srms.db`.

### GUI opens with an empty dashboard

- The wrong backend is selected.
- The database schema was created but sample data was not loaded.
- The SQLite seed was not run.
- The user is linked to a record that does not exist.

Load the sample data for the selected backend. The SQL Server and SQLite datasets differ.

### `Invalid credentials` for a known demo account

1. Confirm the backend dataset.
2. Confirm the account exists:

```sql
SELECT Username, Role, IsActive, IsLocked, FailedLoginAttempts
FROM USERS
WHERE Username IN ('admin', 'student1', 'guest');
```

3. Check `IsLocked`. Five failures lock the account.
4. Confirm the password path. SQL Server sample data uses SHA-256 + salt; SQLite uses bcrypt.
5. If the user was created with a different hash path, authentication will fail.

### Account is locked

An admin can unlock it through user management, or in a demo database:

```sql
UPDATE USERS
SET IsLocked = 0, FailedLoginAttempts = 0
WHERE Username = 'student1';
```

This is a demo repair, not a production unlock procedure. Production should require an audited administrative action.

### Login succeeds but the dashboard is blank or wrong

- The role value may not match a dashboard route.
- The linked student or instructor record may be missing.
- The account's `LinkedType` may be inconsistent with `LinkedID`.

Inspect:

```sql
SELECT UserID, Username, Role, ClearanceLevel, LinkedID, LinkedType
FROM USERS;
```

### `TclError: no display name` on a headless machine

The Tkinter client needs a graphical display. Use a desktop session or X forwarding. Do not try to run the GUI in a headless CI job.

### Fonts or theme look broken

- Install the fonts used by the theme, or use the default ttk fallback.
- Check display scaling.
- Try the light theme if the dark theme has low contrast on your display.

### 2FA code rejected

The demo code is generated per dialog and expires after five minutes with three attempts. If it expired, close and reopen the flow. This is a simulation, not a real authenticator.

---

## Security controls

### `Access denied` for an action that should work

Check the role, table, operation, and ownership. The denial reason often identifies the layer:

- `No permissions defined` → RBAC matrix.
- `NRU Violation` → MLS read.
- `NWD Violation` → MLS write.
- `BLOCKED: Query set size` → inference control.
- `BLOCKED: 'export'` → flow control.

If the role is correct but the decision is wrong, inspect `config.py` and the relevant manager. Do not weaken the check by editing only the UI.

### Student cannot see a grade

Possible causes:

- The grade is not published.
- The user is linked to a different student.
- The course is not active.
- The grade was not entered for that student.
- The student dashboard is using a filtered projection.

Verify the grade and `IsPublished` state.

### TA can see grades

This is a security defect. Record the exact path, role, and data. Check:

- Application matrix: `PERMISSION_MATRIX['TA']['GRADES']` should be empty.
- Dashboard query: it must not select from `GRADES` and ignore the matrix.
- Database grants: `db_TA` should be denied on `GRADES`.
- The user's role value must be exactly `TA`, not a display label that maps elsewhere.

Do not treat a hidden menu item as proof of control. Confirm the operation is denied at the data path.

### Secret data exports successfully

Check whether the export function invokes `FlowController.can_export()` before writing. A new export path can bypass the policy. Record the route and fix the caller, not just the button state.

### Small aggregate is allowed

Confirm the query path calls `validate_aggregate_query()` or the stored procedure. Aggregate logic implemented ad hoc in a dashboard may bypass the controller.

### MLS denial prevents an intended own-record view

The design uses a controlled ownership projection for a student's own Confidential profile. Use the dedicated student view or model path, not a global clearance elevation. Do not simply raise the Student role to Confidential.

### TA attendance versus MLS

The current policy has a known tension: TA clearance is Confidential, attendance is Secret, yet TAs are delegated attendance duties. If the pure MLS check blocks attendance, record the policy conflict. The intended demo path relies on assignment filtering and the attendance projection. A production fix must define delegated access explicitly, not silently bypass MLS. See [03 · Security models](03-security-models.md).

### Encryption round trip fails

- Confirm `SRMS_MASTER_KEY` has not changed between writes and reads.
- Confirm the ciphertext was produced by the same key derivation.
- Check for truncated or re-encoded values in a database column.
- Do not attempt to decrypt SQL Server ciphertext with the Python Fernet key; they are different layers.

### Password verification always fails

Check which hashing path created the account. `bcrypt` hashes are not SHA-256 hashes, and vice versa. Recreate demo data with the matching script instead of mixing paths.

---

## Flask viewer

### Viewer loads but tables are missing

The viewer uses the application connection. Confirm the same backend and database are selected. If SQL Server is configured but unavailable, the viewer will fail or show an error page.

### `Address already in use` on port 5000

Find the process:

```bash
ss -ltnp | grep 5000
```

Stop it, or run the viewer on another port and update the documented URL.

### Viewer is accessible on the network

It should not be. Bind to `127.0.0.1`, not `0.0.0.0`. Check firewall rules. The viewer has no authentication and must not be public.

### Ad-hoc query form does not allow a statement

The viewer is read-only by design. Write statements should be rejected. This is expected.

---

## Documentation website

### CSS or images are missing

Serve the site over HTTP from the `docs/` directory:

```bash
python -m http.server 8080 --directory docs
```

Directly opening `index.html` can break absolute paths. GitHub Pages also needs the `docs/` root, not the repository root.

### A diagram does not render

- Check the asset path and case.
- Confirm the SVG exists.
- If the site uses an external Mermaid runtime, confirm the CDN script is allowed.
- Rebuild source diagrams from `documentation/diagrams/*.mmd`.

### Pages shows a 404

- Confirm the Pages source is `main` and `/docs`.
- Confirm `docs/index.html` exists.
- Wait for the Pages deployment to finish.
- Check the repository name in the URL.
- For a project site, the path is `/<repository>/`.

### Link works locally but not on GitHub

Case sensitivity is the usual cause. Linux and GitHub Pages distinguish `Docs` from `docs`. Use lowercase paths consistently.

---

## Git and release

### `gh: not authenticated`

```bash
gh auth login
gh auth status
```

Use the intended account and the minimum scopes needed. Do not paste a token into a document.

### Push rejected

- The remote may already have commits.
- The branch may be protected.
- The authentication token may lack `repo` scope.

Fetch and inspect before forcing anything. Never force-push a shared branch without explicit approval.

### Release asset upload fails

Check the file size and path. Use the exact filename. Do not upload generated secrets or temporary environment files.

---

## When to open an issue

Open a public issue for:

- Reproducible setup failures.
- Documentation errors.
- Non-sensitive UI defects.
- Feature proposals.

Do **not** open a public issue for a security vulnerability. Follow [SECURITY](../SECURITY.md) and report privately.

Include:

- Version or commit.
- OS and Python version.
- Backend.
- Exact error text with secrets removed.
- Steps to reproduce using demo data.
- Expected and observed result.

---

## Related reading

- [05 · Installation](05-installation.md)
- [07 · Testing](07-testing.md)
- [09 · Deployment](09-deployment.md)
- [11 · FAQ](11-faq.md)
