# Security

**Classification:** RESEARCH. Not an operating system. Not a production service.

## Scope

RealityOS keeps organizations in process memory. Restart drops them. There is no login, no OAuth, and no database. `connector_config` is stored and ignored.

Do not send real customer records, credentials, or production forecasts to this API.

## Reporting

Open a GitHub issue on `beyond-repair/RealityOS`. Do not include secrets in the issue body.

## Known non-claims

- No authentication or tenant isolation.
- No secret scanning result is recorded in this file.
- A green `research-guard` run is a pytest result, not a security audit.
