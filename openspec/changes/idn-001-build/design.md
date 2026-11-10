# IDN-001 — Design

## Tech Stack
_Not specified._

## Architecture
_High-level components, their responsibilities, and how they interact._

## Key Decisions
_Significant technical decisions and trade-offs (with alternatives considered)._

- **Security admin authorization (task-r1c4HYJosAE): role claim in the access token.** Admin session endpoints authorize callers by checking for the security admin role claim in the validated access token. Alternatives considered and not chosen: scope checked against org IdP groups, separate admin API credentials, deferring to platform gateway policy.

## Data Model
_Main entities/tables and their relationships._

## Open Questions
_Anything unresolved to decide before or during the build._
