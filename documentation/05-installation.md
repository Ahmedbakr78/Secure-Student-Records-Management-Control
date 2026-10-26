# 05 · Installation

This guide sets up SRMS from a clean checkout on Linux, macOS, or Windows. The primary path uses SQL Server 2022 in Docker. A SQLite fallback is available for development and UI review.

> [!WARNING]
> The commands below use the published classroom password `Srms@2024!` and the `SA` account. Replace them before using the environment for anything other than a local demonstration.

---

## Prerequisites

| Requirement | Recommended | Check |
| :-- | :-- | :-- |
| Python | 3.10+ | `python3 --version` |
| pip | Current | `python3 -m pip --version` |
| Docker | 24+ | `docker --version` |
| SQL Server | 2022 image | Pulled by the command below |
| sqlcmd | Bundled in the image | `/opt/mssql-tools18/bin/sqlcmd` |
| Tkinter | System package | `python3 -c "import tkinter"` |
| Git | Current | `git --version` |

Optional tools:

- DBeaver or Azure Data Studio for SQL inspection.
- A virtual-environment manager such as `venv`.
- A modern browser for the Flask viewer and documentation website.

### Linux Tkinter note

On Debian/Ubuntu:

```bash
sudo apt-get update
sudo apt-get install -y python3-tk python3-venv
```

On Fedora:

```bash
sudo dnf install -y python3-tkinter
```

---

## 1. Clone the repository

```bash
git clone https://github.com/Ahmedbakr78/Secure-Student-Records-Management-Control.git
cd "Secure-Student-Records-Management-Control"
```

If you are working from a local copy, open a terminal in the repository root. Every command below assumes that directory.

---

## 2. Start SQL Server

```bash
docker run \
  -e 'ACCEPT_EULA=Y' \
  -e 'MSSQL_SA_PASSWORD=Srms@2024!' \
  -p 1433:1433 \
  --name sqlserver2022 \
  --hostname sqlserver \
  -d mcr.microsoft.com/mssql/server:2022-latest
```

Check that the container is running:

```bash
docker ps --filter name=sqlserver2022
docker logs --tail 50 sqlserver2022
```

Wait for a message indicating that SQL Server is ready for client connections. The first start can take a minute.

### If the container already exists

```bash
docker start sqlserver2022
```

### If port 1433 is busy

Stop the conflicting service or map a different host port, then update `SQLSERVER_CONFIG['port']` in `src/database/connection.py`. The container still listens on 1433 internally.

---

## 3. Create the database

```bash
docker exec -it sqlserver2022 \
  /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U SA -P 'Srms@2024!' -C \
  -Q "IF DB_ID('SRMS_SecureDB') IS NULL CREATE DATABASE SRMS_SecureDB;"
```

### Run the scripts in order

```bash
docker exec -i sqlserver2022 /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U SA -P 'Srms@2024!' -C -d SRMS_SecureDB \
  < sql/sqlserver_schema.sql
```

```bash
docker exec -i sqlserver2022 /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U SA -P 'Srms@2024!' -C -d SRMS_SecureDB \
  < sql/sqlserver_roles.sql
```

```bash
docker exec -i sqlserver2022 /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U SA -P 'Srms@2024!' -C -d SRMS_SecureDB \
  < sql/sqlserver_views.sql
```

```bash
docker exec -i sqlserver2022 /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U SA -P 'Srms@2024!' -C -d SRMS_SecureDB \
  < sql/sqlserver_procedures.sql
```

```bash
docker exec -i sqlserver2022 /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U SA -P 'Srms@2024!' -C -d SRMS_SecureDB \
  < sql/sqlserver_sample_data.sql
```

Optional security checks:

```bash
docker exec -i sqlserver2022 /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U SA -P 'Srms@2024!' -C -d SRMS_SecureDB \
  < sql/security_checker.sql
```

### Expected output

Each script prints check marks and a summary. If a script stops, read the first error rather than continuing to the next script. A partial schema will cause later procedures and views to fail.

> [!IMPORTANT]
> `sqlserver_schema.sql` drops and recreates SRMS tables. Never run it against a database containing records you need.

---

## 4. Install Python dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The `pymssql` package requires system build tools on some platforms. If installation fails, install your platform's build dependencies or use a wheel available for your Python version.

### Minimal install for the Flask viewer

The viewer still imports the project's database layer. Install the full requirements if you want to avoid import surprises.

---

## 5. Configure the application

The default settings are in `src/database/connection.py`:

```python
DATABASE_TYPE = 'sqlserver'

SQLSERVER_CONFIG = {
    'server': 'localhost',
    'port': 1433,
    'database': 'SRMS_SecureDB',
    'user': 'SA',
    'password': 'Srms@2024!',
}
```

Set a development encryption key:

```bash
export SRMS_MASTER_KEY="replace-with-a-long-random-secret"
```

Windows PowerShell:

```powershell
$env:SRMS_MASTER_KEY = "replace-with-a-long-random-secret"
```

> [!WARNING]
> `SRMS_MASTER_KEY` protects application-layer encryption. The fallback value is published. Use a unique secret for any data you care about, and never commit it.

### Environment variable pattern

The current source reads `SRMS_MASTER_KEY` from the environment, but the SQL Server connection settings are still source constants. If you modify the project, load host, user, and password from the environment and keep the source free of secrets.

---

## 6. Launch the desktop client

```bash
python src/gui/main.py
```

Or use a launcher:

```bash
python launch.py       # Docker + DBeaver + Flask + GUI orchestration
python run.py          # DBeaver + GUI
bash run_all.sh        # Shell workflow
```

The login screen offers shortcuts for demo accounts and guest entry. Start with `admin` / `admin123` and then test each role.

---

## Alternative: restore the backup

The repository includes `SRMS_SecureDB.bak`.

```bash
docker cp SRMS_SecureDB.bak sqlserver2022:/var/opt/mssql/backup/
```

```bash
docker exec -it sqlserver2022 \
  /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U SA -P 'Srms@2024!' -C \
  -Q "RESTORE DATABASE SRMS_SecureDB FROM DISK='/var/opt/mssql/backup/SRMS_SecureDB.bak' WITH REPLACE;"
```

If the restore reports a file-path conflict:

```bash
docker exec -it sqlserver2022 \
  /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U SA -P 'Srms@2024!' -C \
  -Q "RESTORE FILELISTONLY FROM DISK='/var/opt/mssql/backup/SRMS_SecureDB.bak';"
```

Then add `MOVE 'logical_name' TO '/var/opt/mssql/data/target.mdf'` clauses to the restore command.

The backup is a demo artifact. It is not encrypted and must not contain real data.

---

## Alternative: SQLite mode

SQLite mode is useful when SQL Server is unavailable.

1. Confirm that `database/srms.db` exists.
2. Set `DATABASE_TYPE = 'sqlite'` in `src/database/connection.py`.
3. Ensure `SRMS_MASTER_KEY` is set if you will exercise encryption.
4. Launch the same GUI:

```bash
python src/gui/main.py
```

Or use the switcher:

```python
from src.database.db_switcher import set_database_type, test_connection

set_database_type("sqlite")
print(test_connection())
```

SQLite limitations:

- No stored procedures.
- No database roles or T-SQL grants.
- No SQL Server encryption hierarchy.
- Different password-hashing path.
- Views and assignment filters are not available in the same form.

See [10 · Troubleshooting](10-troubleshooting.md) if the application connects to the wrong backend.

---

## Verification

The project includes `verify_project.py`. It checks imports, schema presence, security managers, authentication, role requests, and SQL asset files.

```bash
python verify_project.py
```

> [!NOTE]
> The documentation release did not execute this script during the website build. Run it only after configuring a backend. It is not a substitute for the manual security test matrix.

A smaller smoke test after installation:

```bash
python - <<'PY'
import tkinter
print("Tkinter OK")
import pymssql
print("pymssql OK")
import flask
print("Flask OK")
PY
```

---

## Web database viewer

```bash
python db_viewer.py
```

Open <http://127.0.0.1:5000>.

The viewer is read-only but has no application authentication. Keep it bound to localhost. Do not expose port 5000 through a public interface.

---

## Uninstall or reset

### Stop the container

```bash
docker stop sqlserver2022
```

### Remove the container and its data

```bash
docker rm -f sqlserver2022
```

The named container does not use a named volume in the command above. Removing it discards the database. If you created a volume, remove it deliberately.

### Recreate a clean database

```bash
docker run \
  -e 'ACCEPT_EULA=Y' \
  -e 'MSSQL_SA_PASSWORD=Srms@2024!' \
  -p 1433:1433 \
  --name sqlserver2022 \
  --hostname sqlserver \
  -d mcr.microsoft.com/mssql/server:2022-latest
```

Then repeat the database creation and script order.

---

## Installation checklist

- [ ] Python 3.10+ and Tkinter available.
- [ ] Virtual environment active.
- [ ] Dependencies installed.
- [ ] SQL Server container healthy, or SQLite selected.
- [ ] `SRMS_SecureDB` exists.
- [ ] Schema, roles, views, procedures, and sample data loaded in order.
- [ ] `SRMS_MASTER_KEY` set for development.
- [ ] Login works for at least Admin, Student, and Guest.
- [ ] Flask viewer loads on localhost.
- [ ] Demo credentials understood to be public.

---

## Related reading

- [04 · Database reference](04-database-reference.md)
- [09 · Deployment](09-deployment.md)
- [10 · Troubleshooting](10-troubleshooting.md)
