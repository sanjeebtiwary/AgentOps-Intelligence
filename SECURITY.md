# Security Policy

## Project status

AgentOps Intelligence is an experimental prototype. It is not intended to be treated as a production security boundary without additional engineering, testing, and deployment safeguards.

## Supported versions

Security fixes should target the current maintained branch unless a release-support policy is introduced.

| Version | Support status |
|---|---|
| Current development version | Best-effort review |
| Older versions | No formal support commitment |

Update this table if the project adopts formal versioned releases.

## Reporting a vulnerability

If you discover a security issue, avoid publishing exploit details or sensitive information in a public issue before the maintainers have had an opportunity to assess it.

Use GitHub's private vulnerability reporting feature if it is enabled for the repository. Otherwise, contact the repository maintainer through an appropriate private channel.

Include:

- A description of the issue
- The affected component or version
- Steps to reproduce the issue
- Potential impact
- A suggested mitigation, if known

Do not include real credentials, private user data, or sensitive production information.

## Security considerations

### Tool execution

Tools may perform operations with effects beyond the application. Future tools that access files, networks, databases, or external services require appropriate permission boundaries.

### Policy enforcement

Application-level policy checks do not replace operating-system isolation, access control, or sandboxing. Verify that every execution path passes through the intended controls.

### Input validation

Treat user inputs, planner outputs, and external tool responses as untrusted. Validate arguments before execution.

### Secrets

Do not commit API keys, passwords, tokens, private keys, or environment files containing secrets.

### Resource exhaustion

Future tools and planners should use appropriate execution timeouts, input limits, and resource bounds.

### Logging

Avoid storing secrets or unnecessary sensitive data in logs and benchmark reports.

### Dependencies

Review dependencies and apply updates as appropriate. Validate compatibility with the project's supported Python version.

## Responsible disclosure

Please provide enough information to reproduce and understand the issue. Allow reasonable time for assessment and remediation before disclosing sensitive details publicly.

## Disclaimer

This document describes intended reporting practices, not a guarantee of a formal security response time or service-level agreement.