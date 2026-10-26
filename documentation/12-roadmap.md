# 12 · Roadmap

The roadmap is organised by outcome. **P0** items block any production discussion. **P1** items improve trust and maintainability. **P2** items are exploratory.

The canonical checklist is [ROADMAP.md](../ROADMAP.md). This guide adds the reasoning behind it.

---

## Current release — v1.0.0

| Outcome | Status |
| :-- | :--: |
| Repository renamed and rebuilt around the new project name | Done |
| Long-form README and 17-guide documentation suite | Done |
| Mermaid sources and rendered diagrams | Done |
| Static GitHub Pages website | Done |
| Issue templates, PR template, CI, Dependabot, CODEOWNERS | Done |
| Repository description, homepage, topics | Done |
| GitHub Pages enabled from `/docs` | Done |
| `v1.0.0` release with database backup and report | Done |
| Honest security limitations and production checklist | Done |

---

## Next — security and correctness (P0/P1)

### P0 — remove demo trust

- [ ] Remove all published credentials from seed data and documentation examples.
- [ ] Stop using `SA` as the application login.
- [ ] Create least-privilege SQL Server logins for each role.
- [ ] Move connection settings to environment variables or a vault.
- [ ] Remove the published fallback `SRMS_MASTER_KEY`.
- [ ] Add a first-run secret-generation path that never writes secrets to git.

### P0 — make the controls testable

- [ ] Unit-test `RBACManager`: allow, deny, own-row, grant, revoke, explicit deny.
- [ ] Unit-test `MLSManager`: NRU, NWD, trusted admin, boundary levels.
- [ ] Unit-test `InferenceController`: size, MIN/MAX, tracker, history cap.
- [ ] Unit-test `FlowController`: every direction and action.
- [ ] Unit-test `EncryptionManager`: round trip, wrong password, tampered ciphertext.
- [ ] Add an integration test proving a student cannot read another student's grades through any exposed path.
- [ ] Add a test proving a TA cannot read grades through the database or application.

### P0 — close policy gaps

- [ ] Resolve the TA attendance/MLS conflict with an explicit delegated-access policy.
- [ ] Ensure every model read path calls the same RBAC and MLS checks.
- [ ] Add a regression test for unassigned-course writes.
- [ ] Make the Flask viewer authenticated or absent from any shared deployment.
- [ ] Enforce localhost binding in configuration.

### P1 — credential and crypto hygiene

- [ ] Choose one password-hashing scheme and migrate all accounts.
- [ ] Add a migration plan for existing hashes.
- [ ] Unify application encryption and key management.
- [ ] Add key rotation and re-encryption tooling.
- [ ] Add tamper-evident audit chaining.
- [ ] Export audit events in a structured, SIEM-friendly format.

### P1 — query and error safety

- [ ] Audit every SQL call for parameterisation and allow-listing.
- [ ] Add SQL-injection regression tests.
- [ ] Ensure stack traces and connection strings never reach the UI.
- [ ] Add structured application logging with sensitive-field redaction.
- [ ] Add input validation for all user-supplied identifiers and dates.

---

## Then — product quality (P1)

- [ ] Real TOTP with QR provisioning and recovery codes.
- [ ] Session expiry and re-authentication tests.
- [ ] Configuration wizard for SQL Server and SQLite.
- [ ] Reproducible Docker Compose stack for SQL Server, client, and viewer.
- [ ] Database migrations and schema version tracking.
- [ ] Accessibility review: focus order, labels, contrast, reduced motion.
- [ ] Arabic/English localisation with RTL support.
- [ ] Transcript PDF export with a classification banner.
- [ ] Backup and restore verification.
- [ ] Screenshot set generated from demo data and kept current.
- [ ] Automated documentation link and diagram checks in CI.

---

## Later — research extensions (P2)

- [ ] Attribute-based access control (ABAC) as a complement to RBAC.
- [ ] Purpose-based access control for analytics.
- [ ] Differential privacy for statistical exports.
- [ ] Policy-as-code with testable rules.
- [ ] Attack-tree notebook and tabletop exercises.
- [ ] Benchmark secure-query overhead.
- [ ] Browser-based client with a separate API boundary.
- [ ] Multi-tenant data isolation study.

---

## Non-goals

- Processing real student data without an independent security review.
- Claiming regulatory compliance out of the box.
- Replacing a commercial student information system.
- Adding cloud dependencies that undermine the local-first teaching model.
- Hiding limitations behind marketing language.

---

## Release criteria for v1.1

A v1.1 security-focused release should not ship unless:

- [ ] Demo credentials are removed from the default deployment.
- [ ] Automated tests cover every control.
- [ ] The TA/attendance policy is explicit.
- [ ] The viewer is localhost-only by enforced configuration.
- [ ] CI runs the tests and fails on regressions.
- [ ] The threat model is updated with the new controls.
- [ ] A migration note explains how to upgrade demo databases.

---

## How to propose a roadmap change

1. Open a feature request with the problem, not only the solution.
2. State the security impact.
3. Identify the affected modules and tests.
4. Update [ROADMAP.md](../ROADMAP.md) and this guide when accepted.
5. Keep the public roadmap honest: do not mark an item complete until it is verified.

---

## Related reading

- [CHANGELOG](../CHANGELOG.md)
- [13 · Threat model](13-threat-model.md)
- [CONTRIBUTING](../CONTRIBUTING.md)
