## Summary

Describe the change and the problem it solves.

## Type of change

- [ ] Security policy or enforcement
- [ ] Database schema, view, procedure, or role
- [ ] Desktop application
- [ ] Documentation or diagrams
- [ ] Website
- [ ] Tests or CI
- [ ] Release engineering
- [ ] Maintenance

## Security review

- [ ] I identified any role, clearance, ownership, inference, flow, encryption, or audit impact.
- [ ] I updated both the application policy and the SQL Server mirror where applicable.
- [ ] I added or updated a denial test for the change.
- [ ] I did not add real student data, secrets, keys, or production credentials.
- [ ] I checked that demo credentials and connection settings remain clearly labelled as demo-only.

## Validation

- [ ] `python .github/scripts/check_static.py`
- [ ] `python -m compileall -q config.py launch.py run.py db_viewer.py web_viewer.py verify_project.py src`
- [ ] Documentation links and diagrams render.
- [ ] The website was reviewed at desktop and mobile widths.
- [ ] Runtime security tests were run, or the reason they were not run is stated below.

## Test evidence

List test IDs, commands, screenshots, or audit events. Do not include personal data, credentials, or secrets.

## Related issues

Closes #
