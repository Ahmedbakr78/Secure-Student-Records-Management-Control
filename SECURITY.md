# Security Policy

## Supported versions

| Version | Supported | Notes |
| :-- | :--: | :-- |
| `1.x` | ✅ | Current documentation and reference release |
| `0.x` | ⚠️ | Historical course phases; no security updates |

SRMS is an educational reference implementation. It is **not** certified for production use with real student records without the hardening work described below.

---

## Reporting a vulnerability

**Do not open a public issue for a security vulnerability.**

Please report privately using one of these routes:

1. GitHub's private vulnerability reporting: **Security → Advisories → New draft security advisory** on the repository.
2. Contact the maintainer through the [GitHub profile](https://github.com/Ahmedbakr78) and request a private channel.

Include:

- A clear description of the issue.
- The affected file, component, or SQL object.
- Reproduction steps or a proof of concept.
- The potential impact (confidentiality, integrity, availability).
- Any suggested remediation.

You can expect an acknowledgement within **7 days** and a resolution plan within **30 days** for valid reports. Please allow time for a fix before public disclosure.

---

## Scope

In scope:

- Authentication and session handling.
- RBAC, MLS, inference-control, flow-control, and encryption logic.
- SQL scripts, stored procedures, views, and database roles.
- The Flask database viewer.
- Documentation claims that materially misrepresent security behaviour.

Out of scope:

- Vulnerabilities in third-party dependencies that are already publicly known and fixed upstream.
- Social engineering of project maintainers.
- Denial-of-service against a local demo instance.
- Reports that only state “the demo password is weak” without demonstrating a production impact.

---

## Demo credentials and intentional limitations

This repository contains classroom demo accounts such as `admin / admin123`. They are public by design so that instructors and reviewers can reproduce the project. **They are not a vulnerability in themselves.**

Known limitations that must be addressed before production use:

| Area | Current state | Production requirement |
| :-- | :-- | :-- |
| Demo accounts | Published in documentation and sample data | Remove or rotate before deployment |
| SQL Server `SA` login | Demo password in launch scripts | Use a least-privilege login and a secret manager |
| Hard-coded connection settings | Present in `src/database/connection.py` | Move to environment variables or a vault |
| 2FA | Simulated six-digit dialog | Integrate a real TOTP provider |
| Email notifications | Local simulation/log | Integrate a transactional email provider |
| Application-layer encryption | Fernet + PBKDF2 fallback | Define key custody and rotation policy |
| Audit retention | Local table | Centralised, tamper-evident log storage |
| Database backup | Shipped for reproducibility | Encrypt backups and restrict access |
| Transport | Local connections | Enforce TLS and network segmentation |

---

## Security design summary

- **RBAC:** Five roles mapped to explicit operations and table permissions.
- **MLS:** Bell–LaPadula no-read-up and no-write-down properties.
- **Inference control:** Minimum query-set size of three; MIN/MAX require six.
- **Flow control:** Downward data flow and export/print/copy of classified data blocked.
- **Encryption:** SQL Server AES-256 symmetric key protected by a certificate; Python field encryption via Fernet; password hashing via bcrypt (Python path) or SHA-256 + per-user salt (SQL Server path).
- **Audit:** Authentication events, access decisions, and administrative actions recorded in `AUDIT_LOG`.
- **Account protection:** Failed-login counter and account lockout after five failures.

---

## Hardening checklist

- [ ] Replace every demo credential.
- [ ] Move all secrets out of source code.
- [ ] Enforce TLS for SQL Server and the web viewer.
- [ ] Run the database behind a private network.
- [ ] Remove the `SA` account from the application path.
- [ ] Enable database backup encryption.
- [ ] Add rate limiting to authentication endpoints.
- [ ] Add a real 2FA provider.
- [ ] Centralise audit logs and define retention.
- [ ] Add automated security regression tests.
- [ ] Perform an independent code and database review.
- [ ] Complete a privacy impact assessment for the target jurisdiction.

---

## Safe harbour

Good-faith security research that follows this policy will not be pursued or reported. Please avoid privacy violations, data destruction, and disruption of services.
