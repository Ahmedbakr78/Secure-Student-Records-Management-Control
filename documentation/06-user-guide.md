# 06 · User guide

This guide walks through the SRMS desktop client by role. It assumes the database has been installed and the application starts. Commands and setup are in [05 · Installation](05-installation.md).

> [!CAUTION]
> The accounts below are published classroom credentials. They are not suitable for any real deployment.

---

## Signing in

1. Start the application with `python src/gui/main.py`.
2. Enter a username and password, or use a demo shortcut if present.
3. Choose **Sign in**.
4. The application opens the dashboard for the account's role.

### Demo accounts

| Username | Password | Role | Typical use |
| :-- | :-- | :-- | :-- |
| `admin` | `admin123` | Admin | Full console, role approval, audit |
| `prof_smith` | `prof123` | Instructor | Assigned courses and grade entry |
| `prof_johnson` | `prof123` | Instructor | Second instructor context |
| `prof_jones` | `prof123` | Instructor | Seed-path alias for an instructor record |
| `ta_williams` | `ta123` | TA | Attendance workflow |
| `ta_brown` | `ta123` | TA | Second TA context |
| `student1` | `student123` | Student | Own profile, grades, attendance |
| `student2` | `student123` | Student | Second student context |
| `student3`–`student5` | `student123` | Student | Seed-path student records |
| `guest` | `guest123` | Guest | Public course catalog |

Availability depends on the backend and seed path. The SQL Server sample script creates a smaller set than the SQLite database.

### Guest entry

The login screen also offers a guest path. Guest access is intended to demonstrate public-only access. It is not an anonymous bypass of the database: the application still applies the Guest role.

### Lockout

A wrong password increments the failure counter. After five failures, the account is locked. An administrator must unlock it in the user-management area or through SQL. This prevents unlimited password guessing but is not a complete rate-limiting solution.

### Session timeout

The session manager defaults to a 30-minute timeout. Activity refreshes the session. When it expires, the application returns to the login screen. The timeout is configured in `src/security/advanced_security.py`.

### Two-factor simulation

Some flows offer a six-digit code with a five-minute expiry and three attempts. This is a classroom simulation, not real TOTP. Do not treat it as production MFA.

---

## Admin

The admin dashboard is the operations centre.

### Overview

The landing view summarises:

- Users, students, instructors, and courses.
- Grade and attendance counts.
- Pending role requests.
- Recent login and audit activity.

### Users

Use this area to:

- Search and filter accounts.
- Inspect role, clearance, status, and last login.
- Create or modify users where the UI supports it.
- Unlock accounts and review failed attempts.

### Role requests

The workflow is described in [16 · Role workflow](16-role-workflow.md). The admin can:

1. Open the pending list.
2. Read the requester's reason and current role.
3. Approve or deny.
4. Add admin comments.
5. Confirm the role and clearance change.
6. Review the audit event.

### Students and instructors

The rosters show identity, department, status, and masked contact data. Editing is an administrative operation and should be audited.

### Courses

The course view shows code, title, instructor, credits, semester, capacity, and classification. Guest-visible public information is stored separately from the internal description.

### Grades

The grade view shows records, publication state, and the values available to the admin. Grade values are encrypted at rest in SQL Server; the display column supports reporting. Publishing a grade changes what a student can see.

### Attendance

Attendance is displayed by course and date. Attendance is Secret data and is subject to classification and flow rules.

### Audit log

The audit view exposes action type, table, record, user, role, clearance, access result, description, and timestamp. Use it to reconstruct:

- Successful and failed logins.
- Access grants and denials.
- Administrative changes.
- Role-request decisions.

Audit is not tamper-evident. A database administrator can alter the table.

### Security dashboard

The security dashboard presents status cards for the five models and offers self-tests. Use it during a demonstration to show:

- RBAC allow/deny decisions.
- MLS No Read Up / No Write Down results.
- Inference minimum set size and tracker detection.
- Flow direction and blocked actions.
- Encryption round trips.

### SQL viewer

The in-app SQL viewer and the Flask inspector are read-only review tools. They show schema objects, not a general-purpose query console for production.

### Settings

Settings may include theme selection, security preferences, audit maintenance, and database export. Treat exported files as sensitive even when they contain only demo records.

---

## Instructor

The instructor dashboard is limited to assigned courses.

### Overview

The overview shows assigned courses, student counts, grade activity, and attendance context. The header states the instructor's allowed actions, typically **Read Students** and **Create/Update Grades**.

### My courses

Only courses assigned to the instructor should appear. Each card or row includes the course code, title, semester, classification, and roster size.

### Grade entry

1. Select an assigned course.
2. Select a student from the assigned roster.
3. Enter the numeric score and letter grade.
4. Mark the grade final or publish it when appropriate.
5. Save.

Expected controls:

- The course must be assigned to the instructor.
- The grade write is checked by RBAC and MLS.
- A grade value is encrypted in the SQL Server path.
- The action is audited.
- Deleting a grade is denied by policy.

### Students

The roster is filtered to students enrolled in assigned courses. Contact data is masked where appropriate. The instructor does not get a global student directory.

### Attendance

Instructors can view attendance for assigned courses. Attendance writes are reserved for the TA/admin path in the current permission design.

---

## Teaching Assistant

The TA dashboard demonstrates a deliberately narrow delegation.

### Overview

The overview includes a plain-language permission panel. A TA can:

- View assigned courses.
- Read assigned students.
- Record and update attendance for assigned courses.
- Submit a role request.

A TA cannot view grades.

### Attendance

1. Select an assigned course.
2. Select a student.
3. Choose present or absent.
4. Optionally add remarks.
5. Save.

The application should check the course assignment. The database role grants attendance read/insert/update and denies delete.

### Students

The roster is filtered to assigned courses. Contact details are restricted.

### Role request

A TA may request a higher role, typically Instructor. The request is reviewed by an admin.

---

## Student

The student dashboard is scoped to the linked student record.

### My profile

The profile shows the student's own name, email, masked phone, department, enrollment date, and status. It should not expose another student's record.

### My grades

Only the student's published grades should be visible. The student view exposes the course, letter grade, semester, and date entered. Numeric encrypted values are not exposed through the student view.

If a grade is expected but missing:

- It may not be published.
- It may belong to a different student link.
- The course may not be active or assigned in the current data.

### Attendance

The student sees their own attendance records and attendance rate. The data is Secret, so export and print actions are blocked by flow policy even though the student can view their own record through the authorised projection.

### Courses and enrollment

The catalog shows course information. Enrollment actions are subject to the current UI support and the student's linked record.

### Role request

A student may request a TA or Instructor role. The student supplies a reason. The request is visible with a status of Pending, Approved, or Denied. See [16 · Role workflow](16-role-workflow.md).

### GPA

The GPA calculator converts letter grades to grade points and computes a cumulative GPA. It uses only grades visible to the student. The result is advisory; the registrar remains authoritative.

### Transcript

The transcript view builds a term-by-term record from visible grades. Export and print are subject to flow control. Secret-classified grade context blocks export.

### Notifications

The notification centre shows user-scoped messages. Mark one or all as read. Notifications are not a secure channel for sensitive data.

### Export and print

Export, print, copy, and save are not universally available. The flow controller blocks actions based on classification. A blocked action is expected behaviour, not a bug.

---

## Guest

The guest dashboard demonstrates public-only access.

- The page explains the access level.
- The course catalog uses the public projection: code, name, public information, department, and credits.
- No student, instructor, grade, attendance, user, request, or audit data is available.
- A guest cannot submit a role request.

---

## Common tasks

### Change a password

Use the profile area where available. A production system must require a strong password policy, re-authentication, and an audit event. The demo does not implement a complete credential lifecycle.

### Unlock an account

An admin can reset the lock state. The action should be audited. A production system should also notify the user and apply a cooldown.

### Publish grades

An instructor publishes grades for an assigned course. Students see only published grades. Publishing is a state change and should be audited.

### Export data

Admin and authorised roles may see export actions. The flow controller checks the classification first. If an action is blocked, review [03 · Security models](03-security-models.md) rather than trying another menu path.

### Find a record

Use the role's searchable roster or catalog. Cross-entity search results are filtered by role and redacted where required.

---

## Keyboard and accessibility

The UI uses standard Tkinter widgets. Basic tab navigation should work, but a formal accessibility audit has not been completed. Known improvements are listed in the [roadmap](12-roadmap.md):

- Focus order and visible focus indicators.
- Screen-reader labels.
- Contrast review.
- Reduced-motion handling.
- Scalable fonts.

---

## UI expectations during review

| Scenario | Expected |
| :-- | :-- |
| Guest opens courses | Public rows only |
| Guest tries another area | Denied or not exposed |
| TA opens grades | No grade data or an explicit denial |
| Student opens another student | Not possible through the dashboard |
| Instructor edits an unassigned course | Denied |
| Admin approves a request | Role and clearance update; audit event |
| Small aggregate query | Blocked with an explanation |
| Export of Secret data | Blocked |
| Five failed logins | Account locked |

If behaviour differs, record the role, action, observed result, and relevant audit entry. Use the [testing guide](07-testing.md) for a structured report.

---

## Related reading

- [03 · Security models](03-security-models.md)
- [07 · Testing](07-testing.md)
- [10 · Troubleshooting](10-troubleshooting.md)
- [16 · Role workflow](16-role-workflow.md)
