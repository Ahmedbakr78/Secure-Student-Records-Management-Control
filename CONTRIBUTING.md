# Contributing to Secure Student Records Management Control

Thank you for your interest in improving SRMS. This repository is an educational database-security project, and contributions that improve clarity, correctness, safety, accessibility, or test coverage are welcome.

---

## Code of conduct

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md). Be respectful, constructive, and precise. Security research must follow [SECURITY.md](SECURITY.md).

---

## Ways to contribute

| Contribution | Best entry point |
| :-- | :-- |
| Report a bug | Open a Bug Report issue |
| Suggest a feature | Open a Feature Request issue |
| Improve documentation | Edit a Markdown file in `documentation/` or the website in `docs/` |
| Improve a diagram | Edit a `.mmd` file in `documentation/diagrams/` |
| Add a test | Add a test under `tests/` once the test harness exists |
| Report a vulnerability | Follow [SECURITY.md](SECURITY.md) — do not open a public issue |

---

## Development workflow

1. Fork the repository.
2. Create a focused branch:

   ```bash
   git checkout -b feat/clear-description
   ```

3. Make the smallest change that solves the problem.
4. Do not commit secrets, database dumps with real records, or credentials.
5. Update documentation and the changelog when behaviour changes.
6. Open a pull request using the repository template.

---

## Commit style

Use Conventional Commits:

```
feat(security): add parameterised query guard
fix(mls): correct no-write-down boundary check
docs(readme): clarify SQL Server bootstrap order
test(rbac): cover guest course visibility
```

Allowed types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `build`, `ci`, `chore`, `security`.

---

## Documentation style

- Write in clear, direct English.
- Prefer tables and diagrams over long prose.
- Use the canonical project name: **Secure Student Records Management Control**.
- Use `SRMS` as the short name.
- Keep commands copy-pasteable.
- Document the difference between the **database layer** (SQL Server) and the **application layer** (Python/Tkinter).
- When a feature is a simulation, say so explicitly.

---

## Security rules

- Never commit production credentials, private keys, or real student data.
- Demo credentials are allowed only because this is a classroom project; mark them clearly.
- All SQL in pull requests must use parameters or stored procedures.
- New security checks must have a corresponding test case or a documented manual verification step.
- Do not weaken an existing access-control check without an explicit threat-model justification.

---

## Pull request checklist

- [ ] The change has a single clear purpose.
- [ ] Documentation is updated.
- [ ] The changelog is updated under `Unreleased`.
- [ ] No secrets or personal data are included.
- [ ] Security implications are described.
- [ ] Screenshots or diagrams are included for UI changes where practical.
- [ ] The CI workflow passes.

---

## Licensing

By contributing, you agree that your contribution is licensed under the repository's **GNU Affero General Public License v3.0 (AGPL-3.0)**.
