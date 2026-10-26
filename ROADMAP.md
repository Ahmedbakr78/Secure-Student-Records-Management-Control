# Roadmap

The roadmap is organised by outcome, not by arbitrary version numbers. Items marked **P0** are prerequisites for any production discussion; **P1** items improve trust and maintainability; **P2** items are exploratory.

---

## Now — v1.0 documentation release

- [x] Publish the complete repository under the new name.
- [x] Replace the legacy README with a long-form technical guide.
- [x] Add architecture, security, database, setup, testing, deployment, and FAQ documentation.
- [x] Publish the GitHub Pages website.
- [x] Publish diagrams and Mermaid sources.
- [x] Create the `v1.0.0` release with assets.
- [x] Configure repository topics, description, and homepage.

---

## Next — security and correctness

- [ ] **P0** Replace all demo credentials and remove `SA` from the application path.
- [ ] **P0** Move database and encryption secrets to environment variables or a vault.
- [ ] **P0** Add automated tests for RBAC, MLS, inference control, and flow control.
- [ ] **P0** Add an end-to-end test that proves a student cannot read another student's grades.
- [ ] **P1** Unify the application encryption path and document the chosen algorithm.
- [ ] **P1** Add parameterised-query checks and SQL-injection regression tests.
- [ ] **P1** Add account-lockout and session-expiry tests.
- [ ] **P1** Improve error handling so stack traces and connection strings never reach the UI.
- [ ] **P1** Add structured audit events and export.

---

## Then — product quality

- [ ] **P1** Add a real TOTP provider with QR provisioning and recovery codes.
- [ ] **P1** Add a configuration wizard for SQL Server and SQLite modes.
- [ ] **P1** Improve accessibility: focus order, contrast, screen-reader labels, and reduced motion.
- [ ] **P1** Add a reproducible Docker Compose stack for SQL Server, the app, and the viewer.
- [ ] **P1** Add database migration scripts and version tracking.
- [ ] **P1** Add Arabic and English UI localisation with RTL support.
- [ ] **P1** Add transcript PDF export with an explicit classification banner.
- [ ] **P1** Add backup and restore verification tests.

---

## Later — research extensions

- [ ] **P2** Add attribute-based access control (ABAC) as a complement to RBAC.
- [ ] **P2** Add purpose-based access control for analytics.
- [ ] **P2** Add differential-privacy noise for statistical exports.
- [ ] **P2** Add a tamper-evident audit chain using hash linking.
- [ ] **P2** Add a policy-as-code layer for security rules.
- [ ] **P2** Add a threat-modeling notebook and attack trees.
- [ ] **P2** Add a benchmarking harness for secure-query overhead.

---

## Non-goals

- Processing real student data without an independent security review.
- Claiming regulatory compliance out of the box.
- Replacing a production student information system.
- Adding cloud dependencies that undermine the local-first educational model.
