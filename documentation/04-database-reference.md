# 04 · Database reference

This is the reference for the SQL Server schema and the SQLite development fallback. The canonical scripts live in `sql/`; the copies in `database/` are convenience copies used by the application and the verification script.

> [!IMPORTANT]
> `sql/sqlserver_schema.sql` starts with `USE SRMS_SecureDB;` and drops existing SRMS tables. Create the database first and never run the script against a database that contains real records.

---

## Object inventory

| Object class | SQL Server | SQLite |
| :-- | :--: | :--: |
| Core tables | 11 | 14 |
| Secure views | 11 | — |
| Canonical stored procedures | 14 | — (stubs) |
| Database roles | 5 | — |
| Encryption hierarchy | Master key, certificate, AES-256 symmetric key | Application-level Fernet |
| Demo database | `SRMS_SecureDB.bak` | `database/srms.db` |

The SQLite schema adds application-support tables such as announcements, notifications, sessions, enrollments, assignments, and system settings. The SQL Server schema uses the canonical coursework table names shown below.

---

## SQL Server tables

### 1. `SECURITY_CLASSIFICATION`

Defines the classification scale.

| Column | Type | Notes |
| :-- | :-- | :-- |
| `ClassificationID` | `INT` | Primary key |
| `ClassificationName` | `NVARCHAR(50)` | Public, Unclassified, Confidential, Secret, Top Secret |
| `NumericLevel` | `INT` | 0–4 |
| `Description` | `NVARCHAR(200)` | Human-readable purpose |

Seeded values:

| ID | Name | Level |
| :--: | :-- | :--: |
| 0 | Public | 0 |
| 1 | Unclassified | 1 |
| 2 | Confidential | 2 |
| 3 | Secret | 3 |
| 4 | Top Secret | 4 |

### 2. `USERS` — Top Secret

Authentication and authorization identity.

| Column | Type | Notes |
| :-- | :-- | :-- |
| `UserID` | `INT IDENTITY` | Primary key |
| `Username` | `NVARCHAR(50)` | Unique login name |
| `Username_Encrypted` | `VARBINARY(256)` | Optional encrypted copy |
| `PasswordHash` | `VARBINARY(256)` | SHA-256 hash in SQL Server path |
| `PasswordSalt` | `VARBINARY(128)` | Per-user salt |
| `Role` | `NVARCHAR(20)` | CHECK: Admin, Instructor, TA, Student, Guest |
| `ClearanceLevel` | `INT` | CHECK 0–4 |
| `LinkedID` | `INT` | Student or instructor record |
| `LinkedType` | `NVARCHAR(20)` | CHECK: Student, Instructor, TA, NULL |
| `IsActive` | `BIT` | Inactive accounts cannot authenticate |
| `IsLocked` | `BIT` | Lockout state |
| `FailedLoginAttempts` | `INT` | Locked at five failures |
| `LastLoginDate` | `DATETIME` | Updated on successful login |
| `CreatedDate`, `ModifiedDate`, `ModifiedBy` | | Audit metadata |

Indexes: `Username`, `Role`, `ClearanceLevel`.

### 3. `INSTRUCTOR` — Confidential

| Column | Type | Notes |
| :-- | :-- | :-- |
| `InstructorID` | `INT IDENTITY` | Primary key |
| `FullName` | `NVARCHAR(100)` | |
| `Email` | `NVARCHAR(100)` | Unique |
| `Phone` | `VARBINARY(256)` | AES encrypted |
| `Phone_Display` | `NVARCHAR(20)` | Masked display |
| `Department` | `NVARCHAR(50)` | |
| `Title` | `NVARCHAR(50)` | |
| `ClearanceLevel` | `INT` | Default 3 |
| `ClassificationLevel` | `INT` | Default 2 |
| `IsActive` | `BIT` | Default 1 |
| `CreatedDate` | `DATETIME` | |

### 4. `STUDENT` — Confidential

| Column | Type | Notes |
| :-- | :-- | :-- |
| `StudentID` | `INT IDENTITY` | Primary key |
| `StudentID_Encrypted` | `VARBINARY(256)` | AES encrypted identifier copy |
| `FullName` | `NVARCHAR(100)` | |
| `Email` | `NVARCHAR(100)` | Unique |
| `Phone` | `VARBINARY(256)` | AES encrypted |
| `Phone_Display` | `NVARCHAR(20)` | Masked display |
| `DOB` | `DATE` | |
| `Department` | `NVARCHAR(50)` | |
| `EnrollmentDate` | `DATE` | Default today |
| `Status` | `NVARCHAR(20)` | Active, Inactive, Graduated, Suspended |
| `ClearanceLevel` | `INT` | Default 1 |
| `ClassificationLevel` | `INT` | Default 2 |
| `CreatedDate` | `DATETIME` | |

### 5. `COURSE` — Unclassified

| Column | Type | Notes |
| :-- | :-- | :-- |
| `CourseID` | `INT IDENTITY` | Primary key |
| `CourseCode` | `NVARCHAR(20)` | Unique |
| `CourseName` | `NVARCHAR(100)` | |
| `Description` | `NVARCHAR(MAX)` | |
| `PublicInfo` | `NVARCHAR(MAX)` | Guest-safe projection |
| `Credits` | `INT` | Default 3 |
| `Department` | `NVARCHAR(50)` | |
| `Semester` | `NVARCHAR(20)` | |
| `Year` | `INT` | |
| `MaxCapacity` | `INT` | Default 30 |
| `InstructorID` | `INT` | FK → `INSTRUCTOR` |
| `ClassificationLevel` | `INT` | Default 1 |
| `IsActive` | `BIT` | Default 1 |
| `CreatedDate` | `DATETIME` | |

### 6. `GRADES` — Secret

| Column | Type | Notes |
| :-- | :-- | :-- |
| `GradeID` | `INT IDENTITY` | Primary key |
| `StudentID` | `INT` | FK → `STUDENT` |
| `StudentID_Encrypted` | `VARBINARY(256)` | AES encrypted copy |
| `CourseID` | `INT` | FK → `COURSE` |
| `GradeValue` | `VARBINARY(256)` | AES encrypted numeric value |
| `GradeValue_Display` | `DECIMAL(5,2)` | Display/aggregate helper |
| `GradeLetter` | `NVARCHAR(2)` | A+, A, A−, B+, … |
| `Semester` | `NVARCHAR(20)` | |
| `DateEntered` | `DATETIME` | |
| `EnteredBy` | `INT` | FK → `INSTRUCTOR` |
| `IsPublished` | `BIT` | Students see published grades only |
| `IsFinal` | `BIT` | |
| `ClassificationLevel` | `INT` | Default 3 |
| `CreatedDate` | `DATETIME` | |

### 7. `ATTENDANCE` — Secret

| Column | Type | Notes |
| :-- | :-- | :-- |
| `AttendanceID` | `INT IDENTITY` | Primary key |
| `StudentID` | `INT` | FK → `STUDENT` |
| `CourseID` | `INT` | FK → `COURSE` |
| `AttendanceDate` | `DATE` | |
| `Status` | `BIT` | 1 present, 0 absent |
| `StatusText` | computed | Present/Absent |
| `Remarks` | `NVARCHAR(200)` | |
| `RecordedBy` | `INT` | User who recorded |
| `ClassificationLevel` | `INT` | Default 3 |
| `CreatedDate` | `DATETIME` | |

### 8. `COURSE_ENROLLMENT`

| Column | Type | Notes |
| :-- | :-- | :-- |
| `EnrollmentID` | `INT IDENTITY` | Primary key |
| `StudentID` | `INT` | FK → `STUDENT` |
| `CourseID` | `INT` | FK → `COURSE` |
| `EnrollmentDate` | `DATE` | |
| `Status` | `NVARCHAR(20)` | Enrolled, Dropped, Completed |
| `Semester` | `NVARCHAR(20)` | |
| `Year` | `INT` | |

Unique: `(StudentID, CourseID, Semester, Year)`.

### 9. `COURSE_ASSIGNMENT`

| Column | Type | Notes |
| :-- | :-- | :-- |
| `AssignmentID` | `INT IDENTITY` | Primary key |
| `CourseID` | `INT` | FK → `COURSE` |
| `UserID` | `INT` | FK → `USERS` |
| `AssignmentType` | `NVARCHAR(20)` | Instructor or TA |
| `Semester` | `NVARCHAR(20)` | |
| `Year` | `INT` | |
| `IsActive` | `BIT` | |
| `AssignedDate` | `DATETIME` | |

Unique: `(CourseID, UserID, Semester, Year)`.

### 10. `ROLE_REQUESTS` — Secret

| Column | Type | Notes |
| :-- | :-- | :-- |
| `RequestID` | `INT IDENTITY` | Primary key |
| `UserID` | `INT` | FK → `USERS` |
| `Username` | `NVARCHAR(50)` | Snapshot at submission |
| `CurrentRole` | `NVARCHAR(20)` | |
| `RequestedRole` | `NVARCHAR(20)` | CHECK: TA, Instructor |
| `CurrentClearance` | `INT` | |
| `RequestedClearance` | `INT` | |
| `Reason` | `NVARCHAR(MAX)` | Required |
| `Comments` | `NVARCHAR(MAX)` | Requester comment |
| `Status` | `NVARCHAR(20)` | Pending, Approved, Denied |
| `DateSubmitted` | `DATETIME` | |
| `DateProcessed` | `DATETIME` | |
| `ProcessedBy` | `INT` | FK → `USERS` |
| `ProcessedByUsername` | `NVARCHAR(50)` | |
| `AdminComments` | `NVARCHAR(MAX)` | |

### 11. `AUDIT_LOG` — Top Secret

| Column | Type | Notes |
| :-- | :-- | :-- |
| `LogID` | `INT IDENTITY` | Primary key |
| `ActionType` | `NVARCHAR(50)` | Login, access, write, workflow, system |
| `TableName` | `NVARCHAR(50)` | Affected object |
| `RecordID` | `INT` | Affected row |
| `UserID` | `INT` | Actor identifier |
| `Username` | `NVARCHAR(50)` | Actor snapshot |
| `UserRole` | `NVARCHAR(20)` | Role at event time |
| `UserClearance` | `INT` | Clearance at event time |
| `DataClassification` | `INT` | Classification of target data |
| `AccessGranted` | `BIT` | Outcome |
| `Description` | `NVARCHAR(MAX)` | Human-readable event |
| `OldValues`, `NewValues` | `NVARCHAR(MAX)` | Change evidence |
| `IPAddress` | `NVARCHAR(50)` | Optional source address |
| `ActionDate` | `DATETIME` | Default today |

Indexes: `ActionType`, `UserID`, `ActionDate`.

---

## Views

| View | Consumer | Key restriction |
| :-- | :-- | :-- |
| `vw_PublicCourseInfo` | Guest | Active courses, public columns only |
| `vw_StudentOwnProfile` | Student | Linked student, masked phone |
| `vw_StudentOwnGrades` | Student | Own published grades; no encrypted value |
| `vw_StudentOwnAttendance` | Student | Own attendance only |
| `vw_TAAssignedStudents` | TA | Assigned courses and active assignments |
| `vw_TAAttendance` | TA | Attendance in assigned courses |
| `vw_InstructorStudents` | Instructor | Students in assigned courses |
| `vw_InstructorGrades` | Instructor | Grades in assigned courses |
| `vw_InstructorAttendance` | Instructor | Attendance in assigned courses |
| `vw_AdminAllData` | Admin | Full grade projection |
| `vw_PendingRoleRequests` | Admin | Pending requests only |

### View caveats

- Several views use `SYSTEM_USER` to identify the current database principal. This is meaningful only when each application user connects with a distinct SQL Server login mapped to a database role. The default demo connects as `SA`, so `SYSTEM_USER` is the same for every user and the application-level identity checks remain essential.
- `vw_StudentOwnGrades` exposes the letter grade, not the encrypted numeric value.
- `vw_TAAttendance` is a row/assignment filter, not an MLS elevation. See the policy note in [03 · Security models](03-security-models.md).

---

## Stored procedures

| Procedure | Inputs (summary) | Security purpose |
| :-- | :-- | :-- |
| `sp_UserLogin` | username, password hash/salt | Verify credentials, lock after failures |
| `sp_MLSReadCheck` | role clearance, classification | Return No Read Up decision |
| `sp_MLSWriteCheck` | role clearance, classification | Return No Write Down decision |
| `sp_MLSAccessCheck` | clearance, classification, operation | Combined MLS decision |
| `sp_GetCourseStatistics` | course, aggregate type | Reject undersized aggregates |
| `sp_CheckDataFlow` | source/target level | Reject downflow |
| `sp_CheckExportAllowed` | classification, role | Reject classified export |
| `sp_EncryptData` | plaintext | Encrypt with AES-256 key |
| `sp_DecryptData` | ciphertext | Decrypt authorised value |
| `sp_InsertGrade` | student, course, value, actor | MLS check + encryption + insert |
| `sp_SubmitRoleRequest` | user, role, reason | Create pending request |
| `sp_GetPendingRoleRequests` | — | List pending requests |
| `sp_ProcessRoleRequest` | request, decision, admin, comments | Approve/deny and update role |
| `sp_CreateUser` | username, password, role | Create user with hash and audit |

Legacy compatibility procedures live in `sql/sqlserver_procedures_fixed.sql`:

- `usp_SubmitRoleRequest`
- `usp_ProcessRoleRequest`
- `usp_UpdateGrade`
- `usp_UpdateAttendance`
- `usp_FlowControlCheck`
- `usp_GetSecureStatistics`
- `usp_AddUser`

The canonical script is `sql/sqlserver_procedures.sql`. Use the fixed compatibility script only when following an older coursework instruction.

---

## Roles and grants

| Role | Grants | Denials |
| :-- | :-- | :-- |
| `db_Admin` | CRUD on business tables; execute on schema; view definition; read/insert audit | Audit update/delete |
| `db_Instructor` | Read students/courses; read/insert/update grades; read attendance; own role requests | User access; student writes; attendance writes; grade delete |
| `db_TA` | Read students/courses; read/insert/update attendance; own role requests | All grade access; user access; student writes |
| `db_Student` | Read students/courses/grades/attendance through role views; own role requests | Own-row enforcement via views; user access |
| `db_Guest` | `SELECT` on `vw_PublicCourseInfo` only | Every base table |

`db_Student` is granted base-table `SELECT` in the current script while the views are intended to enforce row filtering. Because the demo application connects as `SA`, these grants do not provide a complete isolation boundary by themselves. Production use requires per-user database principals and view-only access.

---

## Script execution order

```text
sqlserver_schema.sql
        ↓
sqlserver_roles.sql
        ↓
sqlserver_views.sql
        ↓
sqlserver_procedures.sql
        ↓
sqlserver_sample_data.sql
        ↓
security_checker.sql   (optional)
```

Each script assumes the `SRMS_SecureDB` database exists. Do not run them as one batch through a driver that cannot handle `GO` separators.

### Restore alternative

```bash
docker cp SRMS_SecureDB.bak sqlserver2022:/var/opt/mssql/backup/
docker exec -it sqlserver2022 /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U SA -P 'Srms@2024!' -C \
  -Q "RESTORE DATABASE SRMS_SecureDB FROM DISK='/var/opt/mssql/backup/SRMS_SecureDB.bak' WITH REPLACE;"
```

If the backup uses different logical file paths, inspect it with `RESTORE FILELISTONLY` and add `MOVE` clauses.

---

## Demo data inventory

The published SQL Server script and the SQLite seed are not identical.

| Dataset | Users | Instructors | Students | Courses | Grades | Attendance |
| :-- | :--: | :--: | :--: | :--: | :--: | :--: |
| `sqlserver_sample_data.sql` | 8 | 4 | 8 | 5 | 10 | 15 |
| SQLite `database/srms.db` | 11 | 2 | 5 | 3 | 12 | 50 |

The SQLite database includes support tables used by the GUI (notifications, announcements, sessions, enrollments, assignments, settings). The root README lists the published demo accounts; treat the counts as backend-specific.

### Demo credentials — SQL Server sample

| Username | Password | Role | Clearance |
| :-- | :-- | :-- | :--: |
| `admin` | `admin123` | Admin | 4 |
| `prof_smith` | `prof123` | Instructor | 3 |
| `prof_johnson` | `prof123` | Instructor | 3 |
| `ta_williams` | `ta123` | TA | 2 |
| `student1` | `student123` | Student | 1 |
| `student2` | `student123` | Student | 1 |
| `student3` | `student123` | Student | 1 |
| `guest` | `guest123` | Guest | 0 |

Additional accounts may exist in the SQLite database or the source seed path. Never use any of these credentials outside the classroom.

---

## SQLite fallback

The SQLite database is opened by `SQLiteConnection` from `src/database/connection.py`. If the database or `USERS` table is missing and `database/schema.sql` exists, the schema is created automatically.

Key differences:

| Capability | SQL Server | SQLite |
| :-- | :-- | :-- |
| Stored procedures | Yes | No (`NotImplementedError`) |
| Database roles | Yes | No |
| Secure views | Yes | No |
| AES key hierarchy | Yes | No |
| Password path | SHA-256 + salt | bcrypt |
| Application encryption | Fernet | Fernet |
| Best use | Security demonstration | Development/UI evaluation |

The SQLite `database/srms.db` is included for convenience and contains demo records. Do not add real records to it.

---

## Query conventions

- Use parameters (`%s` for `pymssql`, `?` for SQLite) instead of string interpolation.
- Prefer allow-listed table names in the Flask viewer.
- Keep every allow-listed table query read-only.
- Log access decisions, not just exceptions.
- Do not log plaintext passwords, salts, keys, or full connection strings.
- When adding an encrypted column, update the write path, read path, views, and test matrix.

---

## Related reading

- [03 · Security models](03-security-models.md)
- [05 · Installation](05-installation.md)
- [07 · Testing](07-testing.md)
- [15 · Project structure](15-project-structure.md)
