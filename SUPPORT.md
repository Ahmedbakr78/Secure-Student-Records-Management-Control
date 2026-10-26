# Support

## Getting help

| Need | Where to go |
| :-- | :-- |
| Read the documentation | [Documentation index](documentation/README.md) |
| Browse the website | <https://ahmedbakr78.github.io/Secure-Student-Records-Management-Control/> |
| Ask a usage question | Open a GitHub Discussion or a Question issue |
| Report a reproducible bug | Open a Bug Report issue |
| Request a feature | Open a Feature Request issue |
| Report a vulnerability | Follow [SECURITY.md](SECURITY.md) — privately |
| Review the release | [Releases](https://github.com/Ahmedbakr78/Secure-Student-Records-Management-Control/releases) |

## Before opening an issue

1. Search existing issues and the FAQ.
2. Confirm the problem is reproducible.
3. Collect the operating system, Python version, SQL Server version, and the exact error text.
4. Remove passwords, connection strings, personal data, and student records from logs.
5. State whether you are running SQL Server or the SQLite fallback.

## Common first checks

```bash
python --version
pip install -r requirements.txt
docker ps
```

```sql
SELECT @@VERSION;
SELECT name FROM sys.tables;
```

See [Troubleshooting](documentation/10-troubleshooting.md) for a full diagnostic guide.

## What this project does not provide

- A hosted production service.
- A guarantee of compliance with FERPA, GDPR, or any other regulation.
- Support for real student data.
- Private consulting unless arranged directly with the maintainer.
