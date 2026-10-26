# 01 · Overview

## The problem

Student information systems concentrate identity data, contact details, grades, attendance, and administrative decisions in one place. A conventional CRUD application can authenticate users and hide menu items, but those measures do not answer the questions a database-security review will ask:

- Is access controlled by role **and** by row ownership?
- Is classified data protected in both read and write directions?
- Can a user recover an individual's grade from aggregate queries?
- Can classified data be exported, printed, copied, or saved to a lower-classification context?
- Are sensitive columns protected at rest?
- Can an administrator reconstruct who did what?

SRMS was built as a working answer to those questions for a Database Security course project. It is deliberately small enough to inspect, but complete enough to demonstrate the controls through a real desktop client and a SQL Server database.

---

## Goals

| Goal | How the project meets it |
| :-- | :-- |
| Demonstrate RBAC | Five roles, an explicit permission matrix, own-row checks, SQL Server roles, and GUI enforcement |
| Demonstrate MLS | Five classification levels with Bell–LaPadula No Read Up and No Write Down |
| Demonstrate inference control | Minimum query-set size, stricter MIN/MAX threshold, tracker-attack detection, and column redaction |
| Demonstrate flow control | Directional flow checks plus action blocking for export, print, copy, paste, save, and screenshot |
| Demonstrate encryption | SQL Server certificate/key hierarchy, Fernet application encryption, bcrypt and SHA-256 password paths |
| Demonstrate auditability | An `AUDIT_LOG` table written by authentication, models, and administrative workflows |
| Demonstrate a governed privilege change | A submitted, reviewed, approved/denied role-request workflow |
| Remain reproducible | Docker-based SQL Server setup, SQL scripts, sample data, SQLite fallback, and a verification script |

---

## Scope

### In scope

- A Tkinter desktop client with dashboards for Admin, Instructor, TA, Student, and Guest.
- Authentication, account lockout, login auditing, session tracking, and a simulated second factor.
- Student, instructor, course, grade, attendance, enrollment, assignment, notification, request, and audit data.
- Application-level security managers and matching SQL Server objects.
- A read-only Flask database inspector for demonstration and review.
- Documentation, diagrams, a static website, and release assets.

### Out of scope

- Production identity federation (LDAP, OAuth, SAML).
- Real email delivery or SMS.
- Real TOTP provisioning.
- Regulatory certification or a claim of production readiness.
- Cloud infrastructure, multi-tenancy, or horizontal scaling.
- Processing real student records.

---

## Design principles

### 1. Security decisions are explicit

Permissions are not inferred from which window happens to be open. The application asks security managers for a decision:

```python
rbac.has_permission(role, "GRADES", "SELECT", user_id, target_id)
mls.check_access(role, "GRADES", "read")
inference.validate_aggregate_query("AVG", result_count, role)
flow.can_export(classification)
```

### 2. Defence in depth

Each control is represented at more than one layer where practical:

| Control | Application | Database | Interface |
| :-- | :-- | :-- | :-- |
| RBAC | `RBACManager` and `PERMISSION_MATRIX` | `db_*` roles, grants and denials | Role-specific dashboards |
| MLS | `MLSManager` | `sp_MLSReadCheck`, `sp_MLSWriteCheck` | Clearance messages and restricted navigation |
| Inference | `InferenceController` | `sp_GetCourseStatistics` | Query-size warnings |
| Flow | `FlowController` | `sp_CheckDataFlow`, `sp_CheckExportAllowed` | Disabled export, print, and copy actions |
| Encryption | `EncryptionManager` | Certificate + AES-256 symmetric key | Masked fields and authorised reveal paths |
| Audit | Model and authentication writes | `AUDIT_LOG` table | Admin audit view and Flask `/audit` |

### 3. Least privilege by default

The permission matrix starts from denial. A role receives only the operations listed for it, and database roles mirror the same intent. The TA role, for example, has no `GRADES` permission in either layer.

### 4. Teachable failure

A blocked action returns a reason, not a silent no-op. The UI explains whether a decision came from RBAC, MLS, inference control, or flow control. This makes the security model visible during a demonstration.

### 5. Local-first reproducibility

The default stack runs on one workstation. SQL Server runs in Docker, the client runs as a Python process, and the Flask viewer binds to localhost. This avoids cloud dependencies and keeps the review path short.

---

## The five security models at a glance

| Model | Core question | Primary implementation |
| :-- | :-- | :-- |
| RBAC | *May this role perform this operation on this table?* | `config.py`, `src/security/rbac.py`, `sql/sqlserver_roles.sql` |
| MLS | *Does clearance permit this read or write?* | `src/security/mls.py`, `sp_MLS*` procedures |
| Inference control | *Does the result set reveal an individual?* | `src/security/inference_control.py`, `sp_GetCourseStatistics` |
| Flow control | *Is this movement or action allowed for this classification?* | `src/security/flow_control.py`, `sp_Check*` procedures |
| Encryption | *Is sensitive data protected at rest and in transit?* | `src/security/encryption.py`, `sp_EncryptData`, `sp_DecryptData` |

A full treatment, including limitations, is in [03 · Security models](03-security-models.md).

---

## Project history and naming

The project began as a two-part Database Security coursework submission. The original repository used the long name `Data-Security-Secure-Student-Records-Management-System-SRMS-`.

For this release:

- The application and repository name became **Secure Student Records Management Control**.
- The short name remains **SRMS**.
- The source application was preserved rather than rewritten.
- The original remote repository was left untouched.
- Documentation, metadata, diagrams, and a static website were rebuilt around the existing implementation.

The historical phases are recorded in the [changelog](../CHANGELOG.md):

| Phase | Focus |
| :-- | :-- |
| 0.1 | Initial database design and prototype |
| 0.2 | Five security models, dashboards, SQL Server objects, Part B workflow |
| 1.0 | Rename, documentation, website, release engineering, hardening notes |

---

## Success criteria

The release is considered complete when:

- [x] All five security models have a named implementation and a documented expected outcome.
- [x] The database schema, views, procedures, and roles are present and documented.
- [x] Every role has a working dashboard and a defined permission boundary.
- [x] The role-upgrade workflow supports submission, approval, denial, and audit.
- [x] Demo credentials and demo-only risks are clearly labelled.
- [x] A reviewer can boot the database, load the schema, and launch the client from written instructions.
- [x] A static documentation website is published from `docs/`.
- [x] The repository has a license, contribution policy, security policy, issue templates, and CI.
- [ ] Automated regression tests cover every security control (roadmap).

---

## Intended audience

| Audience | What they need from SRMS |
| :-- | :-- |
| Course instructor | Evidence that the specified controls exist and can be demonstrated |
| Security reviewer | A clear policy-to-code mapping and an honest residual-risk statement |
| Student developer | A readable example of layered application security in Python |
| DBA | SQL Server schema, roles, views, procedures, and backup |
| Future contributor | Stable structure, documented conventions, and a realistic roadmap |

---

## Known limitations

SRMS is not production-ready. The most important limitations are:

- Public demo credentials and a demo `SA` password.
- Hard-coded connection settings in `src/database/connection.py`.
- Two password-hashing paths: bcrypt for the model/SQLite path and SHA-256 + salt for the SQL Server authentication path.
- Application-layer Fernet encryption plus database-layer AES-256, with separate key-management designs.
- Simulated two-factor authentication and email.
- No automated test suite for the security controls.
- The Flask viewer has no authentication of its own and must remain bound to localhost.
- Audit records are stored in a normal table, not an append-only or tamper-evident store.

See [13 · Threat model](13-threat-model.md) and the root [security policy](../SECURITY.md) for mitigations.

---

## Next reading

- [02 · Architecture](02-architecture.md)
- [03 · Security models](03-security-models.md)
- [05 · Installation](05-installation.md)
- [16 · Role workflow](16-role-workflow.md)
