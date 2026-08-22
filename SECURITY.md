# Security Policy

## Reporting a vulnerability

Please report suspected vulnerabilities privately through the repository's GitHub Security tab. Do not disclose credentials, customer data, or exploit details in a public issue.

Supported versions are the latest commit on `main` until a release policy is established.

## Security controls

- CI runs `pip-audit` and Bandit on every push and pull request.
- GitHub Actions use read-only repository permissions and pinned action commits.
- Dependabot monitors Python and GitHub Actions dependencies.
- The container runs as an unprivileged user.