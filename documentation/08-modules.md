# 08 · Modules

This guide maps the source tree to responsibilities. Use it to find the right file before changing behaviour.

---

## Root modules

| File | Purpose | Entry point |
| :-- | :-- | :-- |
| `config.py` | Classification levels, role clearance, permission matrix, inference threshold, blocked actions, theme colors | Imported by security managers and models |
| `launch.py` | Master launcher: checks Docker, opens DBeaver, starts Flask, starts GUI | `python launch.py` |
| `run.py` | DBeaver + GUI launcher | `python run.py` |
| `run_all.sh` | Shell workflow around Docker, viewer, and GUI | `bash run_all.sh` |
| `run_with_dbeaver.sh` | DBeaver helper | `bash run_with_dbeaver.sh` |
| `db_viewer.py` | Flask read-only database inspector | `python db_viewer.py` |
| `web_viewer.py` | Copy of the Flask viewer | `python web_viewer.py` |
| `verify_project.py` | Import, schema, security, auth, and asset checks | `python verify_project.py` |
| `requirements.txt` | Python dependencies | `pip install -r requirements.txt` |

`db_viewer.py` and `web_viewer.py` are duplicates. Treat `db_viewer.py` as the documented entry point and keep the copies aligned if you change the viewer.

---

## `src/database/`

### `connection.py`

| Class / function | Responsibility |
| :-- | :-- |
| `SQLServerConnection` | Singleton pymssql connection, parameterised execute, fetch helpers, commit/rollback |
| `SQLiteConnection` | Singleton SQLite connection, schema bootstrap, fetch helpers |
| `get_database()` | Return the configured backend singleton |
| `get_database_type()` | Report `sqlserver` or `sqlite` |
| `is_sqlserver()` | Backend predicate |
| `DatabaseConnection` | Compatibility wrapper |

Configuration constants:

```python
DATABASE_TYPE = "sqlserver"
SQLSERVER_CONFIG = {
    "server": "localhost",
    "port": 1433,
    "database": "SRMS_SecureDB",
    "user": "SA",
    "password": "Srms@2024!",
}
```

This is the first file to change for a local database setup and a priority hardening target for production.

### `db_switcher.py`

| Function | Purpose |
| :-- | :-- |
| `get_connection()` | Return a connection wrapper for the active type |
| `get_sqlite_connection()` / `get_sqlserver_connection()` | Explicit backend factories |
| `set_database_type(type)` | Switch active backend |
| `get_database_type()` | Read active type |
| `configure_sqlserver(server, database, username, password)` | Update connection settings |
| `test_connection()` | Check connectivity |
| `use_sqlite()` / `use_sqlserver()` | Convenience switches |

The switcher changes the active Python backend. It does not migrate data between SQL Server and SQLite.

### `sqlserver_connection.py`

An alternate SQL Server connection layer with lightweight model helpers:

- `SQLServerConnection`
- `SQLServerUserModel`
- `SQLServerGradeModel`
- `SQLServerRoleRequestModel`
- `get_sqlserver_connection(config=None)`

The main application primarily uses `connection.py` and `models.py`. Review both when changing database behaviour.

### `sqlserver_auth.py`

| Method | Responsibility |
| :-- | :-- |
| `authenticate(username, password)` | Dispatch to the SQL Server or SQLite path |
| `_authenticate_sqlserver()` | SHA-256 + salt verification, lockout, last login |
| `_authenticate_sqlite()` | bcrypt verification |
| `_log_action()` | Write login outcome to `AUDIT_LOG` |
| `get_user_by_id()` | Return a safe user projection |
| `get_all_users()` | Admin user list |

The SQL Server path reads `PasswordHash`, `PasswordSalt`, account state, and linked record. It returns role and clearance on success. Failure after five attempts sets `IsLocked`.

### `models.py`

| Class | Domain |
| :-- | :-- |
| `SecureModel` | Shared security and audit helpers |
| `UserModel` | User accounts, roles, clearance, lock state |
| `StudentModel` | Student identity and enrollment state |
| `InstructorModel` | Instructor identity |
| `CourseModel` | Course catalog |
| `GradesModel` | Grade records, publication, encryption |
| `AttendanceModel` | Attendance records |
| `RoleRequestModel` | Submission, listing, approval, denial |
| `NotificationModel` | Per-user notifications |
| `AnnouncementModel` | Broadcast announcements |
| `EnrollmentModel` | Student-course enrollment |
| `SystemSettingsModel` | Application settings |

The model layer is where domain rules meet policy and persistence. When adding a write, preserve the order: authorization, classification, flow, encryption, commit, audit.

### `seed_data.py`

`seed_database()` populates the SQLite fallback with demo users, courses, students, grades, attendance, requests, and support data. It is not used to initialize SQL Server; that is the job of `sql/sqlserver_sample_data.sql`.

---

## `src/security/`

### `rbac.py`

`RBACManager` implements the application permission matrix.

Key methods:

| Method | Purpose |
| :-- | :-- |
| `has_permission()` | Boolean decision with ownership support |
| `check_access()` | Structured decision with a reason |
| `grant()`, `revoke()`, `deny()` | Simulate SQL permission operations |
| `get_role_permissions()` | Inspect a role's matrix |
| `get_table_permissions()` | Inspect a table's role grants |
| `can_access_own_data_only()` | Determine own-row restriction |
| `get_rbac_manager()` | Process singleton |

Explicit denials live in `_denied_permissions` and are not persisted.

### `mls.py`

`MLSManager` implements Bell–LaPadula.

Key methods:

- `can_read(clearance, classification)`
- `can_write(clearance, classification)`
- `check_access(role, table, operation)`
- `get_accessible_tables(role, operation)`
- `filter_records_by_clearance(records, clearance)`
- `enforce_read_access()` / `enforce_write_access()`

It raises `MLSViolationError` when enforcement is requested and the decision is negative.

### `inference_control.py`

`InferenceController` prevents small-set and tracker disclosures.

| Method | Purpose |
| :-- | :-- |
| `check_query_set_size()` | Minimum size check |
| `validate_aggregate_query()` | Aggregate-specific validation |
| `track_query()` | Store recent query sets per user |
| `check_tracker_attack()` | Detect complementary queries |
| `create_restricted_view()` | Remove role-restricted columns |
| `anonymize_results()` | Redact caller-specified fields |
| `enforce_query_set_size()` | Raise on a blocked set |

History is capped at 50 queries per user and is process-local.

### `flow_control.py`

`FlowController` enforces directional flow and action policy.

| Method | Purpose |
| :-- | :-- |
| `can_flow(source, target)` | Upflow/horizontal allowed, downflow blocked |
| `check_flow()` | Structured decision |
| `is_action_blocked()` / `check_action()` | Export, print, copy, paste, save, screenshot |
| `can_export()`, `can_print()`, `can_copy()`, `can_save()` | Convenience predicates |
| `lock_clipboard()` / `unlock_clipboard()` | Sensitive-context state |
| `get_allowed_actions()` / `get_flow_matrix()` | Inspection |
| `enforce_flow()` / `enforce_action()` | Raise `FlowControlError` |

### `encryption.py`

`EncryptionManager` provides:

- `encrypt(plaintext)` / `decrypt(ciphertext)`
- `hash_password(password)` / `verify_password(password, hash)`
- `generate_salt()`
- `encrypt_column(value)` / `decrypt_column(value)`
- `get_encryption_manager()` singleton

It uses Fernet, PBKDF2-HMAC-SHA256 (100,000 iterations), and bcrypt cost 12. The fallback master key is published and must be replaced.

### `advanced_security.py`

| Class | Responsibility |
| :-- | :-- |
| `TwoFactorAuth` | Six-digit simulation, expiry, attempts |
| `TwoFactorDialog` | Tkinter dialog |
| `SessionManager` | Hashed session IDs, validation, refresh, expiry |
| `GPACalculator` | Letter-to-points conversion, GPA, standing |
| `TranscriptGenerator` | Build and export a text transcript |
| `BulkOperations` | Publish grades, mark attendance, bulk notifications |
| `get_tfa_manager()` / `get_session_manager()` | Singletons |

Two-factor and email are simulations. Do not describe them as production MFA or delivery.

---

## `src/gui/`

| File | Main classes | Notes |
| :-- | :-- | :-- |
| `main.py` | `PremiumApp` | Shell, login, routing, session |
| `login.py` | `EnhancedLoginFrame` | Credentials, demo shortcuts, guest |
| `admin_dashboard.py` | `AdminDashboard` | Full administrative console |
| `instructor_dashboard.py` | `InstructorDashboard` | Assigned courses and grades |
| `ta_dashboard.py` | `TADashboard` | Attendance and roster |
| `student_dashboard.py` | `StudentDashboard` | Own records and academic tools |
| `guest_dashboard.py` | `GuestDashboard` | Public catalog |
| `security_dashboard.py` | `SecurityDashboard` | Model status and tests |
| `analytics.py` | `AnalyticsDashboard`, `SettingsPage` | Charts and settings |
| `profile_manager.py` | `ProfileDialog`, `ThemeManager`, `ReportGenerator` | Profile and reports |
| `student_features.py` | `GPAViewer`, `TranscriptViewer`, `CourseEnrollmentManager`, `AttendanceViewer`, `NotificationCenter` | Student tools |
| `components.py` | `SearchableTreeview`, `StatsCard`, `NotificationBell`, `PasswordStrengthMeter`, `DatePicker`, `StatusBar`, `ConfirmDialog` | Reusable widgets |
| `components/search_bar.py` | `SearchBar`, `AdvancedSearchDialog` | Search widgets |
| `dashboard_components.py` | `EnhancedHeader`, `EnhancedStatusBar`, `QuickActionsPanel`, `WelcomeCard`, `DashboardSummary` | Dashboard chrome |
| `widgets.py` | `ActivityTracker`, `QuickStats`, `ProgressWidget`, `CalendarWidget`, `DataVisualization`, `HelpWidget`, `QuickActions`, `Breadcrumb` | Presentation widgets |
| `modern_theme.py` | `ColorThemes`, `ModernStyle`, `GlassCard`, `ToastNotification`, `AnimatedBackground`, theme helpers | Visual system |

The GUI imports the security and database layers. Avoid introducing a second policy implementation in a dashboard; call the shared manager.

---

## `src/utils/`

### `export.py`

- `export_to_csv(data, columns, filename=None, classified=False)`
- `export_to_excel(...)`
- `export_to_pdf(...)`
- `ExportDialog`

Flow checks must happen before export. The `classified` flag is a signal, not a substitute for `FlowController` policy.

### `data_tools.py`

| Class | Responsibility |
| :-- | :-- |
| `DataImportWizard` | CSV/JSON import, preview, mapping, confirmation |
| `DataExportWizard` | CSV, JSON, TXT, HTML, Excel, PDF |
| `EmailNotificationManager` | Template-based local email simulation |
| `SearchManager` | Cross-entity search with role-aware filtering |
| `BackupManager` | Create and list database backups |
| `get_email_manager()`, `get_search_manager()`, `get_backup_manager()` | Singletons |

### `shortcuts.py`

- `KeyboardShortcuts` — shortcut definitions and help.
- `ShortcutManager` — binding manager.

---

## `sql/` and `database/`

The SQL directory is the canonical source:

| File | Purpose |
| :-- | :-- |
| `sqlserver_schema.sql` | Encryption hierarchy, classification table, 11 core tables |
| `sqlserver_roles.sql` | Five database roles with grants/denials |
| `sqlserver_views.sql` | 11 secure views |
| `sqlserver_procedures.sql` | 14 canonical procedures |
| `sqlserver_procedures_fixed.sql` | Legacy compatibility procedures |
| `sqlserver_sample_data.sql` | Demo SQL Server data |
| `sqlserver_roles_views.sql` | Combined convenience script |
| `schema.sql` | SQLite schema |
| `security_checker.sql` | Optional verification queries |

`database/` contains copies used by the app plus `srms.db`. See [04 · Database reference](04-database-reference.md) for object-level details.

---

## Documentation and website

| Path | Purpose |
| :-- | :-- |
| `documentation/*.md` | Long-form guides |
| `documentation/diagrams/*.mmd` | Mermaid sources |
| `docs/*.html` | Static GitHub Pages site |
| `docs/styles.css` | Site theme |
| `docs/script.js` | Navigation and interaction |
| `docs/assets/brand/` | Logo and favicon |
| `docs/assets/diagrams/` | Rendered diagrams |
| `docs/.nojekyll` | Disable Jekyll processing |

---

## Change map

| If you change… | Also update… |
| :-- | :-- |
| A permission | `config.py`, SQL grants, docs, test matrix |
| A classification | `config.py`, `SECURITY_CLASSIFICATION`, views, docs |
| A table | SQL schema, SQLite schema, models, views, ERD, docs |
| A stored procedure | `sql/`, database copy if used, database docs |
| A password scheme | Auth path, seed data, docs, threat model |
| A flow action | `config.py`, `FlowController`, UI action state, tests |
| A dashboard tab | Role routing, user guide, website feature table |
| The Flask viewer | Both viewer copies, route table, security warning |

---

## Related reading

- [02 · Architecture](02-architecture.md)
- [04 · Database reference](04-database-reference.md)
- [15 · Project structure](15-project-structure.md)
