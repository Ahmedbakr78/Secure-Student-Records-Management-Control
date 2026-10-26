# 07 · Testing

SRMS has a manual security test matrix, a verification script, and static documentation checks. It does **not** yet have automated unit or integration tests for every control. This guide defines what to test, the expected result, and how to report evidence.

> [!IMPORTANT]
> Do not run the application or its test scripts as part of a documentation-only build. Installation and verification require a configured database.

---

## Test layers

| Layer | What it checks | How |
| :-- | :-- | :-- |
| Static repository | Required files, links, YAML, HTML, diagrams | Shell and Python checks |
| Documentation build | Pages load, navigation works, no broken local links | Local server + browser |
| Import smoke test | Python modules import in the configured environment | `verify_project.py` |
| Database schema | Tables, views, procedures, roles, sample data | `sqlcmd` inspection |
| Security policy | RBAC, MLS, inference, flow, encryption decisions | Manual matrix and security dashboard |
| Authentication | Valid, invalid, locked, inactive accounts | Manual login tests |
| Role workflow | Submit, approve, deny, audit | Manual Part B workflow |
| Regression | Known behaviours remain stable | Manual checklist until automated tests exist |

---

## Preconditions

1. SQL Server is running and `SRMS_SecureDB` is loaded, or SQLite is selected.
2. The Python environment has the requirements installed.
3. `SRMS_MASTER_KEY` is set for application encryption.
4. Demo users exist for each role.
5. The tester records the backend, commit, date, and environment.

```bash
docker ps --filter name=sqlserver2022
python --version
git rev-parse HEAD
```

Store evidence in a test report, not in the repository, if it contains personal data or secrets.

---

## Automated checks that do not run the app

### Documentation link check

```bash
python - <<'PY'
import pathlib, re
root = pathlib.Path('.')
broken = []
for path in root.rglob('*.md'):
    if '.git' in path.parts or 'node_modules' in path.parts:
        continue
    text = path.read_text(encoding='utf-8')
    for target in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', text):
        if target.startswith(('http://', 'https://', 'mailto:', '#')):
            continue
        candidate = (path.parent / target).resolve()
        if not candidate.exists():
            broken.append(f'{path}: {target}')
print('\n'.join(broken) if broken else 'No broken local Markdown links')
PY
```

### YAML parse check

```bash
python - <<'PY'
import pathlib
try:
    import yaml
except ImportError:
    raise SystemExit('PyYAML not installed; use ruby -e or another parser')
for path in pathlib.Path('.github').rglob('*.yml'):
    yaml.safe_load(path.read_text())
    print('OK', path)
PY
```

### HTML sanity check

```bash
python - <<'PY'
import pathlib
from html.parser import HTMLParser

class Check(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
    def handle_starttag(self, tag, attrs):
        if tag not in {'meta', 'link', 'img', 'br', 'hr', 'input', 'source', 'path'}:
            self.stack.append(tag)
    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()

for path in pathlib.Path('docs').glob('*.html'):
    parser = Check()
    parser.feed(path.read_text(encoding='utf-8'))
    print(path, 'OK' if not parser.stack else f'unclosed: {parser.stack[-5:]}')
PY
```

These checks are convenience commands. They do not replace a browser review of the published Pages site.

---

## Verification script

```bash
python verify_project.py
```

The script checks:

- Imports for configuration, database, models, and security modules.
- Database connectivity and required table presence.
- RBAC role definitions and a sample permission.
- MLS manager availability.
- Inference minimum set size.
- Flow controller availability.
- Encryption round trip.
- Authentication for representative roles.
- Role-request model and SQL asset files.

Record the output and environment. If an import fails because a GUI dependency is missing, install the full requirements before concluding that the security code is broken.

---

## Security test matrix

Use the demo accounts for each row. Record pass/fail and the relevant audit event.

### RBAC

| ID | Actor | Action | Expected |
| :-- | :-- | :-- | :-- |
| `TC-RBAC-01` | Guest | Select grades | Denied |
| `TC-RBAC-02` | Student | Update a grade | Denied |
| `TC-RBAC-03` | TA | Select grades | Denied |
| `TC-RBAC-04` | Instructor | Update a grade for an assigned course | Allowed |
| `TC-RBAC-05` | Instructor | Update a grade for an unassigned course | Denied |
| `TC-RBAC-06` | Admin | Manage users | Allowed |
| `TC-RBAC-07` | Student | Read another student's profile | Denied |
| `TC-RBAC-08` | TA | Delete attendance | Denied |

### MLS

| ID | Actor | Action | Expected |
| :-- | :-- | :-- | :-- |
| `TC-MLS-01` | Student | Read Secret grades without own-record projection | NRU denial |
| `TC-MLS-02` | Instructor | Read Confidential student profile | Allowed |
| `TC-MLS-03` | Instructor | Read Top Secret users | NRU denial |
| `TC-MLS-04` | Guest | Write Confidential data | NWD denial |
| `TC-MLS-05` | Admin | Write to Public | Allowed as trusted principal |
| `TC-MLS-06` | Student | Read own Confidential profile through the own-record path | Allowed by explicit ownership policy |

### Inference control

| ID | Actor | Action | Expected |
| :-- | :-- | :-- | :-- |
| `TC-INF-01` | TA | Aggregate over 2 records | Blocked |
| `TC-INF-02` | TA | Aggregate over 5 records | Allowed |
| `TC-INF-03` | Instructor | MIN/MAX over 5 records | Blocked |
| `TC-INF-04` | Instructor | MIN/MAX over 6 records | Allowed |
| `TC-INF-05` | Analyst | Complementary query differing by one record | High-risk tracker block |
| `TC-INF-06` | Guest | Restricted column projection | Sensitive columns removed |
| `TC-INF-07` | Admin | Zero-row aggregate | Allowed with no disclosure |

### Flow control

| ID | Actor | Action | Expected |
| :-- | :-- | :-- | :-- |
| `TC-FLOW-01` | Any | Secret → Public | Blocked |
| `TC-FLOW-02` | Any | Public → Secret | Allowed |
| `TC-FLOW-03` | Instructor | Export grades | Blocked |
| `TC-FLOW-04` | Student | Print transcript containing Secret context | Blocked |
| `TC-FLOW-05` | Admin | Copy Top Secret data | Blocked |
| `TC-FLOW-06` | Any | Copy Confidential data | Allowed by default action policy |
| `TC-FLOW-07` | Any | View Secret data | Allowed |
| `TC-FLOW-08` | Any | Clipboard lock after Secret context | Locked |

### Encryption

| ID | Action | Expected |
| :-- | :-- | :-- |
| `TC-ENC-01` | Encrypt/decrypt a value | Round trip succeeds |
| `TC-ENC-02` | Raw select of an encrypted grade | Ciphertext |
| `TC-ENC-03` | Password storage | Hash + salt, no plaintext |
| `TC-ENC-04` | Wrong password verification | `False` |
| `TC-ENC-05` | Tampered ciphertext | `DecryptionError` |
| `TC-ENC-06` | Authorised display | Plaintext only in the authorised path |

### Authentication and audit

| ID | Action | Expected |
| :-- | :-- | :-- |
| `TC-AUTH-01` | Valid login | Dashboard opens, `LOGIN_SUCCESS` |
| `TC-AUTH-02` | Invalid password | Generic failure, `LOGIN_FAILED` |
| `TC-AUTH-03` | Unknown username | Generic failure, no account enumeration |
| `TC-AUTH-04` | Five failures | Account locked |
| `TC-AUTH-05` | Inactive account | Denied |
| `TC-AUDIT-01` | Denied access | Denial event recorded |
| `TC-AUDIT-02` | Admin role approval | Workflow event recorded |
| `TC-AUDIT-03` | Audit view | Event visible to admin |

### Role workflow

| ID | Actor | Action | Expected |
| :-- | :-- | :-- | :-- |
| `TC-PB-01` | Student | Submit a TA request | Status Pending |
| `TC-PB-02` | Student | Submit with empty reason | Rejected |
| `TC-PB-03` | Admin | Approve | Role and clearance updated |
| `TC-PB-04` | Admin | Deny | Role unchanged, comments stored |
| `TC-PB-05` | Student | View own request | Visible with status |
| `TC-PB-06` | Student | View another user's request | Denied |
| `TC-PB-07` | Admin | Duplicate/invalid request | Rejected by validation |

### Guest and public data

| ID | Action | Expected |
| :-- | :-- | :-- |
| `TC-GUEST-01` | Open catalog | Public course fields only |
| `TC-GUEST-02` | Request student list | Denied |
| `TC-GUEST-03` | Request grades | Denied |
| `TC-GUEST-04` | Submit role request | Denied |

---

## Manual acceptance checklist

- [ ] All five roles can sign in with valid credentials.
- [ ] Every role lands on the correct dashboard.
- [ ] Guest can see course public information and nothing confidential.
- [ ] Student can see own profile, published grades, and own attendance.
- [ ] Student cannot see another student's data through any visible control.
- [ ] TA can record attendance for an assigned course.
- [ ] TA cannot see grades.
- [ ] Instructor can enter a grade for an assigned course.
- [ ] Instructor cannot enter a grade for an unassigned course.
- [ ] Admin can manage users and approve a role request.
- [ ] A small aggregate is rejected with a clear reason.
- [ ] A MIN/MAX aggregate below six records is rejected.
- [ ] A complementary query is flagged.
- [ ] Secret export is blocked.
- [ ] Print/copy/save controls follow the flow matrix.
- [ ] Encrypted values do not appear in raw table output.
- [ ] Audit shows both success and denial events.
- [ ] Account locks after five failed attempts.
- [ ] Flask viewer loads all allow-listed routes on localhost.
- [ ] No real student data is present in the repository.

---

## Database-level checks

Run these as a DBA against a disposable demo database.

### Object presence

```sql
SELECT name, type_desc
FROM sys.objects
WHERE schema_id = SCHEMA_ID('dbo')
  AND type IN ('U', 'V', 'P')
ORDER BY type_desc, name;
```

Expected: 11 tables, 11 views, 14 canonical procedures.

### Role presence

```sql
SELECT name
FROM sys.database_principals
WHERE type = 'R'
  AND name LIKE 'db[_]%'
ORDER BY name;
```

Expected: `db_Admin`, `db_Instructor`, `db_TA`, `db_Student`, `db_Guest`.

### Encryption keys

```sql
SELECT name, algorithm_desc
FROM sys.symmetric_keys
WHERE name = 'SRMS_SymmetricKey';
```

Expected: `AES_256`.

### Ciphertext check

```sql
SELECT TOP 5 GradeID, GradeValue, GradeValue_Display
FROM GRADES;
```

`GradeValue` should be binary ciphertext; `GradeValue_Display` is the reporting helper and is not a substitute for encryption of the primary value.

### Audit query

```sql
SELECT TOP 20 ActionType, TableName, Username, UserRole, AccessGranted, ActionDate
FROM AUDIT_LOG
ORDER BY ActionDate DESC;
```

---

## Negative testing

The security value is in the denials. Test at least one of each:

| Denial class | Example | Evidence |
| :-- | :-- | :-- |
| Unauthorized operation | TA selects grades | UI denial and/or audit event |
| Insufficient clearance | Student reads users | NRU message |
| No Write Down | Guest writes confidential | NWD message |
| Inference risk | Aggregate of 2 | Blocked query message |
| Flow violation | Secret → Public | Flow denial |
| Blocked action | Export grades | Disabled action or error |
| Authentication failure | Wrong password | Generic error and audit |
| Workflow rejection | Empty reason | Validation message |

A test that only exercises the happy path does not prove the control.

---

## Environment matrix

| Environment | Why test it |
| :-- | :-- |
| SQL Server 2022 | Primary security path |
| SQLite fallback | UI and application managers without SQL Server |
| Fresh install | Missing dependency and setup errors |
| Existing database | Upgrade and idempotency risks |
| Headless documentation build | Link and HTML checks only |
| Published Pages site | Navigation and static asset integrity |

Do not run a real-data environment for this project. Use disposable demo data only.

---

## Test report template

```text
Project: Secure Student Records Management Control
Version: v1.0.0
Commit:
Date:
Tester:
OS:
Python:
Backend: SQL Server 2022 / SQLite
Database seeded from: scripts / backup / SQLite file

Test ID:
Role:
Action:
Expected:
Observed:
Pass / Fail:
Audit event:
Notes:
```

Store evidence without credentials, personal data, or secrets. Screenshots of the UI are acceptable only for demo data.

---

## Known gaps

- No automated unit tests for `RBACManager`, `MLSManager`, `InferenceController`, `FlowController`, or `EncryptionManager`.
- No integration test that proves an instructor cannot write to an unassigned course through every code path.
- No automated UI test.
- No test for session expiry.
- No test for SQL injection beyond parameterised-query review.
- No test for every database grant and denial.
- No continuous security scanning.

These gaps are tracked in [12 · Roadmap](12-roadmap.md).

---

## Related reading

- [03 · Security models](03-security-models.md)
- [04 · Database reference](04-database-reference.md)
- [10 · Troubleshooting](10-troubleshooting.md)
- [13 · Threat model](13-threat-model.md)
