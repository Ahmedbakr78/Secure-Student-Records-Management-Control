# 14 · Glossary

Definitions are written for this project. Where a term has a broader industry meaning, the SRMS usage is noted.

---

## A

**ABAC (Attribute-Based Access Control)**  
An access model that evaluates attributes of the subject, object, action, and environment. SRMS uses RBAC; ABAC is a roadmap extension.

**Access control**  
The process of deciding whether a subject may perform an operation on an object. SRMS combines RBAC, ownership, MLS, and flow policies.

**AES (Advanced Encryption Standard)**  
A symmetric block cipher. SQL Server's `SRMS_SymmetricKey` uses `AES_256`.

**AGPL-3.0 (GNU Affero General Public License v3.0)**  
The project license. It extends GPL obligations to network use of modified versions.

**Aggregate query**  
A query that returns a summary such as `COUNT`, `SUM`, `AVG`, `MIN`, or `MAX`. SRMS applies inference control to aggregates.

**Audit log**  
A record of security-relevant actions. In SRMS, the `AUDIT_LOG` table with an admin view and a Flask `/audit` route.

**Authentication**  
Proving an identity. SRMS verifies a username, password hash, account state, and lockout state.

**Authorization**  
Deciding what an authenticated identity may do. SRMS uses RBAC, MLS, ownership, and flow policies.

---

## B

**Bell–LaPadula (BLP)**  
A multilevel security model with a simple security property (No Read Up) and a star property (No Write Down). SRMS implements both, with Admin as a trusted principal for writes.

**bcrypt**  
A password-hashing function with a configurable cost. Used on the SQLite/model path with cost 12.

**Blocked action**  
An operation denied by flow policy, such as exporting Secret data or copying Top Secret data.

---

## C

**Classification**  
The sensitivity label of an object. SRMS uses 0 Public through 4 Top Secret.

**Clearance**  
The maximum classification a subject may read. Derived from role in SRMS.

**Clipboard lock**  
A UI state that blocks copy/paste when sensitive data is displayed. Cooperative, not an OS-level control.

**Confidential**  
Classification level 2. Student and instructor profiles.

**Course assignment**  
A mapping between a course and an instructor or TA. Used to scope delegated duties.

**Ciphertext**  
Encrypted data that should be unreadable without the key.

**Credential stuffing**  
Trying known username/password pairs from other breaches. SRMS has lockout but no IP throttling.

---

## D

**Database role**  
A SQL Server principal grouping permissions. SRMS defines `db_Admin`, `db_Instructor`, `db_TA`, `db_Student`, and `db_Guest`.

**Defence in depth**  
Layering independent controls so one failure does not expose everything. SRMS mirrors several policies in Python and T-SQL.

**Denial (explicit)**  
A policy decision that overrides a grant. In SQL, `DENY`; in SRMS, `RBACManager.deny()` for the process lifetime.

**Downflow**  
Movement of data from a higher classification to a lower one. Blocked by flow control.

**DBeaver**  
An optional database tool used to inspect the SQL Server schema.

---

## E

**Encryption**  
Reversible transformation of plaintext into ciphertext. SRMS uses SQL Server AES-256 and application Fernet.

**Enrollment**  
A student's registration in a course, stored in `COURSE_ENROLLMENT`.

**Explicit denial**  
See **Denial (explicit)**.

**Export**  
Writing data to a file. Controlled by classification; Confidential and above are blocked in the current action policy.

---

## F

**Fernet**  
An authenticated-encryption construction from the Python `cryptography` library. It uses AES-128-CBC and HMAC-SHA256 in its standard form.

**Flow control**  
Preventing data from moving to a context that is not permitted for its classification. Includes direction checks and action blocks.

**Foreign key (FK)**  
A database constraint linking rows across tables.

---

## G

**GradeValue**  
The encrypted numeric grade column in `GRADES`.

**GradeValue_Display**  
A separate display/reporting column for numeric grades. Sensitive and not a substitute for encryption.

**Guest**  
Clearance 0. Public course information only.

---

## H

**Hash**  
A one-way transformation used for password storage. SHA-256 + salt and bcrypt are both used in SRMS.

**Honeypot**  
A decoy asset. Not implemented.

---

## I

**Inference control**  
Preventing deduction of individual data from aggregates or query patterns.

**Instructor**  
Clearance 3. Grades for assigned courses, student roster, attendance view.

**Integrity**  
Protection against unauthorized or accidental modification. Audit and write checks support it.

---

## K

**Key derivation function (KDF)**  
A function that derives a key from a secret. SRMS uses PBKDF2-HMAC-SHA256 with 100,000 iterations for Fernet key derivation.

**Key management**  
Generation, storage, rotation, and destruction of keys. SRMS does not implement a complete lifecycle.

---

## L

**Least privilege**  
Granting only the access needed for a task. The TA grade denial is an example.

**Lockout**  
Disabling login after repeated failures. SRMS locks after five failed attempts.

---

## M

**MFA (Multi-Factor Authentication)**  
Authentication using more than one factor. SRMS provides only a simulation.

**MLS (Multilevel Security)**  
Access control using classification and clearance. Implemented with Bell–LaPadula rules.

**Mermaid**  
A text-to-diagram syntax used for architecture, ERD, and flow diagrams.

---

## N

**No Read Up (NRU)**  
A subject may read only objects at or below its clearance.

**No Write Down (NWD)**  
A subject may write only to objects at or above its clearance. SRMS treats Admin as trusted.

**Non-repudiation**  
Assurance that an actor cannot credibly deny an action. Audit supports it weakly; the log is mutable.

---

## O

**Object**  
A protected resource, such as a table, row, field, or file.

**Own-row access**  
A permission restricted to the record linked to the authenticated user (`SELECT_OWN`, `UPDATE_OWN`).

---

## P

**PBKDF2**  
Password-Based Key Derivation Function 2. Used with HMAC-SHA256 for Fernet key derivation.

**Permission matrix**  
The mapping of roles to tables and operations in `config.py`.

**Plaintext**  
Unencrypted data.

**Principal**  
An identity that can be authenticated and authorized.

**Public**  
Classification level 0. Guest-safe course information.

**pymssql**  
The Python driver used for SQL Server connections.

---

## R

**RBAC (Role-Based Access Control)**  
Access based on role membership. SRMS has five roles and a permission matrix mirrored in SQL Server.

**Residual risk**  
Risk that remains after controls. Documented in the threat model.

**Role request**  
A governed request to change from Student/TA to a higher role. See `ROLE_REQUESTS`.

**Row-level security**  
Restricting access to specific rows. SRMS uses own-row checks, assignment filters, and views.

---

## S

**Salt**  
Random data combined with a password before hashing to prevent precomputation and identical hashes.

**Secret**  
Classification level 3. Grades and attendance.

**Session**  
A period of authenticated activity. SRMS has a session manager with a default 30-minute timeout.

**SHA-256**  
A cryptographic hash function. The SQL Server password path uses SHA-256 with a per-user salt.

**SQL injection**  
Injecting SQL through unsanitized input. Mitigated by parameterised queries and allow-lists.

**SQL Server**  
The primary relational database for the full security demonstration.

**SQLite**  
A file-based development fallback without roles, stored procedures, or the SQL encryption hierarchy.

**Stored procedure**  
A precompiled T-SQL routine. SRMS uses 14 canonical procedures for security and workflow operations.

**Subject**  
An active entity requesting access, usually a user or role.

**Symmetric key**  
A single key used for both encryption and decryption. `SRMS_SymmetricKey` is AES-256.

---

## T

**TA (Teaching Assistant)**  
Clearance 2. Assigned attendance and roster; no grade access.

**Threat model**  
A structured description of assets, actors, threats, controls, and residual risk.

**Top Secret**  
Classification level 4. Users, audit log, and other administrative data.

**Tracker attack**  
Using complementary queries to isolate an individual. Detected heuristically by symmetric set difference.

**Trust boundary**  
A point where data or control passes between differently trusted components.

**TOTP (Time-Based One-Time Password)**  
A real second factor. SRMS simulates a code but does not implement TOTP.

---

## U

**Unclassified**  
Classification level 1. Course information.

**Upflow**  
Movement of data to an equal or higher classification. Allowed by flow control.

---

## V

**View**  
A stored query. SRMS uses 11 secure views to project only authorized rows and columns.

**Vulnerability**  
A weakness that could be exploited. Report privately per [SECURITY](../SECURITY.md).

---

## W

**Web viewer**  
The Flask read-only database inspector. Localhost only, no authentication.

**Write down**  
Writing to a lower classification. Blocked by MLS.

---

## X

**XSS (Cross-Site Scripting)**  
Injection of scripts into a web page. The static site has no user-generated content; the Flask viewer must escape output.

---

## Z

**Zero trust**  
A model that does not grant implicit trust based on network location. SRMS is not a zero-trust system; it relies on local trust boundaries.

---

## Project-specific names

| Name | Meaning |
| :-- | :-- |
| SRMS | Secure Student Records Management (short name) |
| `SRMS_SecureDB` | SQL Server database name |
| `SRMS_SecureDB.bak` | Demo database backup |
| `SRMS_SymmetricKey` | AES-256 database key |
| `SRMS_Certificate` | Certificate protecting the symmetric key |
| `db_Admin` … `db_Guest` | Database roles |
| `vw_*` | Secure view prefix |
| `sp_*` | Canonical stored procedure prefix |
| `usp_*` | Legacy compatibility procedure prefix |
| `TC-*` | Test case identifier |
