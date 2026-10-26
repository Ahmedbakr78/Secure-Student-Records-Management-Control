# 15 · Project structure

This guide explains every top-level path in the repository and the rules for adding files.

---

## Repository tree

```text
Secure-Student-Records-Management-Control/
├── .github/
│   ├── CODEOWNERS
│   ├── dependabot.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   ├── config.yml
│   │   └── feature_request.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       └── ci.yml
├── config.py
├── database/
│   ├── schema.sql
│   ├── sqlserver_procedures.sql
│   ├── sqlserver_roles.sql
│   ├── sqlserver_roles_views.sql
│   ├── sqlserver_sample_data.sql
│   ├── sqlserver_schema.sql
│   ├── sqlserver_views.sql
│   └── srms.db
├── db_viewer.py
├── docs/
│   ├── .nojekyll
│   ├── 404.html
│   ├── architecture.html
│   ├── database.html
│   ├── docs.html
│   ├── faq.html
│   ├── index.html
│   ├── security.html
│   ├── setup.html
│   ├── testing.html
│   ├── styles.css
│   ├── script.js
│   ├── robots.txt
│   ├── sitemap.xml
│   └── assets/
│       ├── brand/
│       ├── diagrams/
│       └── og-image.png
├── documentation/
│   ├── README.md
│   ├── 01-overview.md … 16-role-workflow.md
│   └── diagrams/
│       └── *.mmd
├── src/
│   ├── database/
│   ├── gui/
│   ├── security/
│   └── utils/
├── sql/
│   ├── schema.sql
│   ├── security_checker.sql
│   ├── sqlserver_procedures_fixed.sql
│   ├── sqlserver_procedures.sql
│   ├── sqlserver_roles.sql
│   ├── sqlserver_roles_views.sql
│   ├── sqlserver_sample_data.sql
│   ├── sqlserver_schema.sql
│   └── sqlserver_views.sql
├── d_ds.pdf
├── launch.py
├── run.py
├── run_all.sh
├── run_with_dbeaver.sh
├── SRMS_SecureDB.bak
├── verify_project.py
├── web_viewer.py
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── SUPPORT.md
├── CITATION.cff
├── ROADMAP.md
├── ACKNOWLEDGMENTS.md
├── LICENSE
├── .editorconfig
├── .gitattributes
└── .gitignore
```

---

## Top-level files

| Path | Purpose | Notes |
| :-- | :-- | :-- |
| `README.md` | Project front page | Long-form overview, quickstart, diagrams, doc map |
| `CHANGELOG.md` | Release history | Keep a Changelog format |
| `CONTRIBUTING.md` | Contribution workflow | Commit style, security rules, checklist |
| `CODE_OF_CONDUCT.md` | Community standards | Contributor Covenant-derived |
| `SECURITY.md` | Disclosure policy | Private reporting, supported scope |
| `SUPPORT.md` | Support routes | Docs, issues, private security |
| `CITATION.cff` | Citation metadata | Academic use |
| `ROADMAP.md` | Public checklist | Mirrors the roadmap guide |
| `ACKNOWLEDGMENTS.md` | Credits | Course context and tools |
| `LICENSE` | AGPL-3.0 text | Do not remove |
| `requirements.txt` | Python dependencies | Install in a venv |
| `config.py` | Security and theme constants | Central policy source |
| `launch.py` | Orchestrated launcher | Docker, DBeaver, Flask, GUI |
| `run.py` | DBeaver + GUI launcher | Optional |
| `run_all.sh` | Shell workflow | Unix shell |
| `run_with_dbeaver.sh` | DBeaver helper | Unix shell |
| `db_viewer.py` | Flask viewer | Documented entry point |
| `web_viewer.py` | Viewer copy | Keep aligned |
| `verify_project.py` | Verification checks | Requires a configured backend |
| `d_ds.pdf` | Architecture report | Original project artifact |
| `SRMS_SecureDB.bak` | SQL Server demo backup | Unencrypted; demo only |

### `.gitignore` and ignored files

The ignore rules cover Python caches, virtual environments, logs, local secrets, editor files, Node tooling for documentation builds, and Jekyll artifacts. Exceptions preserve:

- `database/srms.db`
- `SRMS_SecureDB.bak`
- `d_ds.pdf`
- `.vscode/extensions.json` and `.vscode/settings.json`

Never force-add a secret that is ignored. Rotate it if it was ever committed.

### `.gitattributes`

Normalises text handling and marks binary assets. The SQL backup and PDF are binary; the database file is binary. Do not let a text conversion corrupt them.

---

## `.github/`

| Path | Purpose |
| :-- | :-- |
| `workflows/ci.yml` | Static syntax, YAML, file, link, and diagram checks |
| `ISSUE_TEMPLATE/bug_report.yml` | Structured bug report |
| `ISSUE_TEMPLATE/feature_request.yml` | Structured feature proposal |
| `ISSUE_TEMPLATE/config.yml` | Template chooser and security link |
| `PULL_REQUEST_TEMPLATE.md` | Review checklist |
| `CODEOWNERS` | Default review ownership |
| `dependabot.yml` | GitHub Actions and pip update checks |

CI must not run the desktop application or connect to SQL Server. It is a repository quality gate.

---

## `src/`

### `src/database/`

| File | Role |
| :-- | :-- |
| `connection.py` | Canonical connection factory and backend classes |
| `db_switcher.py` | Runtime backend selection |
| `sqlserver_connection.py` | Alternate SQL Server layer and model helpers |
| `sqlserver_auth.py` | Authentication and login audit |
| `models.py` | Domain models and secure persistence |
| `seed_data.py` | SQLite demo seed |

### `src/security/`

| File | Role |
| :-- | :-- |
| `rbac.py` | Permission matrix logic |
| `mls.py` | Bell–LaPadula |
| `inference_control.py` | Aggregate and tracker controls |
| `flow_control.py` | Direction and action policy |
| `encryption.py` | Fernet, PBKDF2, bcrypt |
| `advanced_security.py` | 2FA simulation, sessions, GPA, transcript, bulk operations |

### `src/gui/`

| File group | Role |
| :-- | :-- |
| `main.py`, `login.py` | Shell and authentication UI |
| `admin_dashboard.py` … `guest_dashboard.py` | Role dashboards |
| `security_dashboard.py`, `analytics.py` | Security and analytics views |
| `profile_manager.py`, `student_features.py` | Profile and student tools |
| `components.py`, `components/search_bar.py` | Reusable widgets |
| `dashboard_components.py`, `widgets.py` | Layout and dashboard widgets |
| `modern_theme.py` | Visual system |

### `src/utils/`

| File | Role |
| :-- | :-- |
| `export.py` | CSV, Excel, PDF export with classification checks |
| `data_tools.py` | Import, export, email simulation, search, backup |
| `shortcuts.py` | Keyboard shortcuts |

---

## `sql/` versus `database/`

`sql/` is the canonical script directory. `database/` contains copies and the SQLite database. When changing a schema or procedure:

1. Edit the canonical file in `sql/`.
2. Copy the change to `database/` if the application or verification path reads that copy.
3. Update [04 · Database reference](04-database-reference.md).
4. Update the ERD and any affected diagram.
5. Run the SQL test matrix.

Do not let the two directories drift. The duplication exists for application convenience and coursework compatibility.

---

## `documentation/`

| Path | Purpose |
| :-- | :-- |
| `README.md` | Index, reading paths, conventions |
| `01-overview.md` | Problem, goals, scope |
| `02-architecture.md` | Layers and lifecycle |
| `03-security-models.md` | Five models in depth |
| `04-database-reference.md` | Tables, views, procedures, roles |
| `05-installation.md` | Setup |
| `06-user-guide.md` | Role walkthrough |
| `07-testing.md` | Test matrix |
| `08-modules.md` | Code map |
| `09-deployment.md` | Local, CI, Pages |
| `10-troubleshooting.md` | Diagnostics |
| `11-faq.md` | Short answers |
| `12-roadmap.md` | Plan |
| `13-threat-model.md` | Risk analysis |
| `14-glossary.md` | Terms |
| `15-project-structure.md` | This file |
| `16-role-workflow.md` | Part B workflow |
| `diagrams/*.mmd` | Mermaid sources |

The guide count is **17** including this directory's `README.md`.

---

## `docs/`

Static website for GitHub Pages.

| Path | Purpose |
| :-- | :-- |
| `index.html` | Landing page |
| `architecture.html` | System architecture |
| `security.html` | Five security models |
| `database.html` | Schema and objects |
| `setup.html` | Installation |
| `testing.html` | Verification |
| `docs.html` | Guide index |
| `faq.html` | FAQ |
| `404.html` | Not-found page |
| `styles.css` | Shared design system |
| `script.js` | Navigation, role explorer, copy buttons |
| `.nojekyll` | Disable Jekyll |
| `robots.txt` | Crawler policy |
| `sitemap.xml` | Page index |
| `assets/brand/` | Logo, favicon |
| `assets/diagrams/` | Rendered SVG diagrams |
| `assets/screenshots/` | Reserved; no stale screenshots shipped |
| `assets/og-image.png` | Social preview |

The website is independent of the desktop runtime. It must not load database data or expose secrets.

---

## `docs/assets/`

| Directory | Contents | Rules |
| :-- | :-- | :-- |
| `brand/` | `logo.svg`, `favicon.svg`, social mark | Vector, no external fonts required |
| `diagrams/` | Architecture, RBAC, MLS, inference, flow, encryption, ERD, workflow | Generated from Mermaid sources or hand-authored SVG |
| `screenshots/` | Reserved | Do not add stale UI captures with demo secrets |

Keep filenames lowercase and URL-safe. GitHub Pages is case-sensitive.

---

## Naming rules

| Kind | Convention |
| :-- | :-- |
| Markdown guides | `NN-kebab-case.md` |
| Mermaid sources | `kebab-case.mmd` |
| Website pages | `kebab-case.html` |
| Python modules | `snake_case.py` |
| Classes | `PascalCase` |
| Functions and variables | `snake_case` |
| SQL tables | `UPPER_SNAKE_CASE` |
| SQL views | `vw_` prefix |
| SQL procedures | `sp_` prefix; `usp_` for legacy |
| Assets | lowercase, hyphenated |

---

## Adding a file

1. Place it in the correct layer.
2. Update the tree in this guide.
3. Add a link from the appropriate index or README.
4. Update `.gitattributes` if it is binary.
5. Add a test or verification step.
6. Run the static checks.
7. Do not add generated caches, virtual environments, or secrets.

---

## Files that should not be committed

- `.env` or any file with real credentials.
- Private keys, certificates, and tokens.
- Real student data.
- `__pycache__`, `.pyc`, virtual environments.
- Logs, exports, reports, backups with real data.
- Local editor state other than the allow-listed VS Code settings.
- `node_modules`.

The demo database, backup, and report are deliberate exceptions, clearly labelled as demo artifacts.

---

## Related reading

- [02 · Architecture](02-architecture.md)
- [08 · Modules](08-modules.md)
- [CONTRIBUTING](../CONTRIBUTING.md)
