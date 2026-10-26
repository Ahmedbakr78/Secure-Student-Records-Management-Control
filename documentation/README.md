# SRMS documentation

This directory is the long-form reference for **Secure Student Records Management Control (SRMS)**. The root [README](../README.md) is the project front page; these guides go deeper into architecture, controls, database objects, setup, operation, testing, and risk.

> [!IMPORTANT]
> SRMS is an educational database-security project. It contains published demo credentials and an unencrypted classroom backup. Never place real student records in this repository or use the demo configuration in production.

---

## Start here

| If you want to… | Read |
| :-- | :-- |
| Understand the problem and scope | [01 · Overview](01-overview.md) |
| Understand how the application is put together | [02 · Architecture](02-architecture.md) |
| Understand or review the five security models | [03 · Security models](03-security-models.md) |
| Look up a table, view, procedure, or role | [04 · Database reference](04-database-reference.md) |
| Install and run the project | [05 · Installation](05-installation.md) |
| Use a dashboard | [06 · User guide](06-user-guide.md) |
| Run the acceptance tests | [07 · Testing](07-testing.md) |
| Find the module that owns a behaviour | [08 · Modules](08-modules.md) |
| Deploy the app, viewer, or website | [09 · Deployment](09-deployment.md) |
| Diagnose a failure | [10 · Troubleshooting](10-troubleshooting.md) |
| Get a short answer | [11 · FAQ](11-faq.md) |
| See what comes next | [12 · Roadmap](12-roadmap.md) |
| Review assets, threats, and residual risk | [13 · Threat model](13-threat-model.md) |
| Define a security or database term | [14 · Glossary](14-glossary.md) |
| Understand every path in the repository | [15 · Project structure](15-project-structure.md) |
| Follow the Part B role-upgrade workflow | [16 · Role workflow](16-role-workflow.md) |

---

## Reading paths

### Reviewer or instructor

1. [01 · Overview](01-overview.md) — what was built and why.
2. [03 · Security models](03-security-models.md) — the five required controls.
3. [04 · Database reference](04-database-reference.md) — evidence in the schema, views, and procedures.
4. [07 · Testing](07-testing.md) — test matrix and expected outcomes.
5. [16 · Role workflow](16-role-workflow.md) — the Part B workflow.

### Student or new contributor

1. [05 · Installation](05-installation.md)
2. [06 · User guide](06-user-guide.md)
3. [08 · Modules](08-modules.md)
4. [15 · Project structure](15-project-structure.md)
5. [CONTRIBUTING](../CONTRIBUTING.md)

### Security reviewer

1. [13 · Threat model](13-threat-model.md)
2. [03 · Security models](03-security-models.md)
3. [04 · Database reference](04-database-reference.md)
4. [SECURITY](../SECURITY.md)
5. [07 · Testing](07-testing.md)

### Operator

1. [05 · Installation](05-installation.md)
2. [09 · Deployment](09-deployment.md)
3. [10 · Troubleshooting](10-troubleshooting.md)
4. [SECURITY](../SECURITY.md)

---

## Documentation conventions

- **Canonical name:** Secure Student Records Management Control.
- **Short name:** SRMS.
- **Database layer:** Microsoft SQL Server 2022, T-SQL, `sqlcmd`, database roles and stored procedures.
- **Application layer:** Python 3.10+, Tkinter, `pymssql`, with a SQLite development fallback.
- **Classification notation:** `0 Public`, `1 Unclassified`, `2 Confidential`, `3 Secret`, `4 Top Secret`.
- **Role notation:** `Admin`, `Instructor`, `TA`, `Student`, `Guest`.
- **Code references:** paths are relative to the repository root, for example `src/security/mls.py`.
- **Commands:** assume Linux/macOS unless a Windows variant is shown.
- **Simulations:** two-factor authentication, email delivery, and some analytics are explicitly labelled as simulations.

---

## Status of the documentation

| Area | Status | Notes |
| :-- | :-- | :-- |
| Architecture and security | Complete | Matches the released source tree |
| Database reference | Complete | Mirrors the canonical `sql/` scripts |
| Installation and operation | Complete | SQL Server and SQLite paths documented |
| Testing | Complete | Manual and static checks; automated security tests are roadmap work |
| Threat model | Complete | Includes residual risk and production gaps |
| Website | Complete | Static GitHub Pages site under `docs/` |
| Diagrams | Complete | 14 editable Mermaid sources and rendered SVGs, with a dedicated website gallery |
| Screenshots | Not provided | The release avoids stale UI captures; diagrams carry the visual explanation |

---

## Related policies

- [Contributing guide](../CONTRIBUTING.md)
- [Code of conduct](../CODE_OF_CONDUCT.md)
- [Security policy](../SECURITY.md)
- [Support](../SUPPORT.md)
- [Changelog](../CHANGELOG.md)
- [Roadmap](../ROADMAP.md)
- [License](../LICENSE) — AGPL-3.0

---

<sub>SRMS documentation · v1.0.0 · 2026-10-27</sub>
