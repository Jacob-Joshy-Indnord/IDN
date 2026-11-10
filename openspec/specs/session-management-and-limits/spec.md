# Session management and limits

## Purpose
Let users and security admins list and end sessions, and cap active sessions per user.

## Requirements

### Requirement: List own active sessions
The system SHALL return the caller's active sessions with device label, IP, created, last used and a current-session marker.
_Story: End user manages own sessions · Spec: User session API · id: task-HcaYBbNiC54_

#### Scenario: Sessions listed with fields
- **WHEN** a user requests their sessions
- **THEN** each active session shows device label, IP, created, last used, and exactly one is marked current

### Requirement: End own session
The system SHALL revoke a chosen session of the caller, invalidating its refresh token immediately.
_Story: End user manages own sessions · Spec: User session API · id: task-TTQj288JBPQ_

#### Scenario: Next exchange fails
- **WHEN** a user ends a session from their list and its refresh token is then exchanged
- **THEN** the exchange fails
#### Scenario: Access token stays valid
- **WHEN** a session is ended and an already-issued access token is used within its 15 minutes
- **THEN** the access token is still accepted

### Requirement: Enforce security admin authorization
The system SHALL restrict admin session endpoints to callers holding the security admin role, as asserted by a role claim in the access token.
_Story: Admin revokes user sessions · Spec: Admin session API · id: task-r1c4HYJosAE_

#### Scenario: Non-admin denied
- **WHEN** a caller without the security admin role calls an admin session endpoint
- **THEN** the request is rejected as forbidden

### Requirement: Admin list and end user sessions
The system SHALL let a security admin list any user's sessions and end any single session.
_Story: Admin revokes user sessions · Spec: Admin session API · id: task-hLzcSUBR0pg_

#### Scenario: Admin lists sessions
- **WHEN** an admin requests another user's sessions
- **THEN** that user's active sessions are returned
#### Scenario: Admin ends a session
- **WHEN** an admin ends one of that user's sessions
- **THEN** its refresh token is rejected on the next exchange

### Requirement: End all sessions of a user
The system SHALL provide a single call that revokes every active session of a given user.
_Story: Admin revokes user sessions · Spec: Admin session API · id: task-2fzhOuV2qBo_

#### Scenario: All sessions ended
- **WHEN** an admin ends all sessions of a user in one call
- **THEN** every session of that user is revoked and none can be exchanged

### Requirement: Evict LRU session at limit
The system SHALL at sign-in, when the user has 10 active sessions, revoke the session with the oldest last-used time before creating the new one.
_Story: Cap active sessions per user · Spec: Session limit · id: task-nkI776Wxz80_

#### Scenario: 11th sign-in evicts LRU
- **WHEN** a user with 10 active sessions signs in an 11th time
- **THEN** the least recently used session is ended and exactly 10 active sessions remain
