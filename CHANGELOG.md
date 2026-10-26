# Changelog

All notable changes to **Secure Student Records Management Control (SRMS)** are documented in this file.

The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned

- Automated unit and integration test suite for every security model.
- Native TOTP 2FA with QR provisioning and recovery codes.
- Environment-first configuration loader with secret-manager adapters.
- Structured JSON audit export and SIEM-friendly event schema.
- Accessibility audit and keyboard-navigation pass for all dashboards.
- Reproducible SQL Server container bootstrap script.

---

## [1.0.0] — 2026-10-27

### Added

- Complete public repository for the **Secure Student Records Management Control** project.
- Production-quality documentation suite covering architecture, security, database, installation, testing, deployment, threat model, and FAQs.
- Ten-page GitHub Pages documentation website with interactive role explorer, security diagrams, responsive mobile layout, light and dark themes, and long-form technical guides.
- Dedicated 14-diagram gallery with full-size SVGs, editable Mermaid sources, captions, and implementation limits.
- Mermaid source files and rendered SVG diagrams for architecture, request lifecycle, authentication, audit, RBAC, MLS, inference control, flow control, encryption, ERD, role workflow, threat model, deployment, and backup/restore.
- Repository metadata: bug and feature issue forms, pull request template, CI workflow, release workflow, Dependabot configuration, code owners, citation metadata, support and security policies.
- Static validation suite covering 632 repository, link, HTML, YAML, SVG, manifest, sitemap, and asset checks.
- Release assets including the SQL Server backup, SQLite database, SQL scripts, and project report.
- GitHub topics, repository description, homepage, discussions, security alerts, and structured release notes.

### Changed

- Project folder and repository name changed from `Data-Security-Secure-Student-Records-Management-System-SRMS-` to **Secure Student Records Management Control**.
- README rebuilt as a long-form technical overview with diagrams, tables, quickstart, security model matrix, and documentation map.
- Documentation consolidated and de-duplicated while preserving the original Phase 2 project details.

### Security

- Documented the intended production-hardening path for demo credentials, hard-coded connection settings, application-layer encryption, and simulated 2FA/email flows.
- Added an explicit responsible-disclosure policy and threat model.
- Documented the dual password-hashing implementations: bcrypt for the Python model path and SHA-256 + per-user salt for the SQL Server path.

### Known limitations

- Demo accounts and the SQL Server `SA` password are intentionally retained for classroom reproducibility. They must never be used in production.
- Two-factor authentication, email delivery, and some analytics are local simulations.
- The Flask database viewer is a read-only inspection tool, not a production API.

---

## [0.2.0] — Phase 2 course release

### Added

- Five security models: RBAC, MLS (Bell–LaPadula), inference control, flow control, and encryption.
- SQL Server schema, secure views, database roles, stored procedures, sample data, and backup.
- Tkinter role dashboards for Admin, Instructor, TA, Student, and Guest.
- Role upgrade request workflow with admin approval and denial.
- Audit logging, account lockout, session management, and 2FA simulation.
- DBeaver launcher, Flask database viewer, analytics, GPA calculator, transcript generator, notifications, import/export, search, and backup tools.

---

## [0.1.0] — Phase 1 course release

### Added

- Initial secure student records concept and database design.
- Preliminary RBAC and MLS rules.
- First Tkinter prototype and SQL schema.

---

### Version legend

| Marker | Meaning |
| :-- | :-- |
| **Added** | New capabilities |
| **Changed** | Changes to existing behaviour |
| **Deprecated** | Features scheduled for removal |
| **Removed** | Features removed |
| **Fixed** | Defects corrected |
| **Security** | Security-relevant changes |
