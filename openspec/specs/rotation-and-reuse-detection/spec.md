# Rotation and reuse detection

## Purpose
Make refresh tokens single-use, rotate them atomically, and revoke the session on reuse.

## Requirements

### Requirement: Exchange refresh token for new pair
The system SHALL validate the presented token, mark it used, and return a new access token and new refresh token bound to the same session id.
_Story: Rotate refresh token on exchange · Spec: Rotation exchange · id: task-15u7cm1yA4s_

#### Scenario: New pair returned, old token used
- **WHEN** a valid refresh token is exchanged once
- **THEN** a new access token and new refresh token are returned and the old token is marked used
#### Scenario: Session id stable
- **WHEN** a token is rotated
- **THEN** the new token belongs to the same session id

### Requirement: Update session last-used time
The system SHALL set the session last-used time on every successful exchange.
_Story: Rotate refresh token on exchange · Spec: Rotation exchange · id: task-OfbXI2OqGrk_

#### Scenario: Last-used updated
- **WHEN** an exchange succeeds
- **THEN** the session last-used time equals the exchange time

### Requirement: Make rotation atomic
The system SHALL mark-as-used must be a single atomic conditional operation so concurrent exchanges of one token yield exactly one success.
_Story: Rotate refresh token on exchange · Spec: Rotation exchange · id: task-v1rkkUFleZ0_

#### Scenario: Concurrent double exchange
- **WHEN** two exchanges of the same token run concurrently
- **THEN** exactly one succeeds and the other is treated as reuse

### Requirement: Verify exchange load target
The system SHALL load-test the exchange endpoint at 500 requests per second and measure latency.
_Story: Rotate refresh token on exchange · Spec: Exchange performance · id: task-lA8B4me2sQA_

#### Scenario: Meets p99 target
- **WHEN** the endpoint is loaded at 500 requests per second
- **THEN** 99th percentile latency is under 100 ms

### Requirement: Revoke session on reuse
The system SHALL when an already-rotated token is presented, revoke the owning session and reject the request with a distinct error code.
_Story: Detect refresh token reuse · Spec: Reuse handling · id: task-h1U-5fLc9bw_

#### Scenario: Reuse revokes session
- **WHEN** an already-rotated refresh token is presented
- **THEN** the session is revoked and the request is rejected with the distinct reuse error code
#### Scenario: Newest token also dead
- **WHEN** the session was revoked by reuse and its latest refresh token is then presented
- **THEN** the exchange is rejected

### Requirement: Write reuse security event
The system SHALL on reuse, write a security event with the session id and presenting IP.
_Story: Detect refresh token reuse · Spec: Reuse handling · id: task-6BoO3EP4e2M_

#### Scenario: Event written
- **WHEN** reuse is detected
- **THEN** one security event is stored with the session id and presenting IP

### Requirement: Retain security events one year
The system SHALL apply a one-year retention policy to security events.
_Story: Detect refresh token reuse · Spec: Reuse handling · id: task-CEfrOaJF9bk_

#### Scenario: One-year retention
- **WHEN** a security event is older than one year
- **THEN** it may be purged, and events younger than one year are never purged

### Requirement: Reject expired token without revoking
The system SHALL reject tokens presented more than 30 days after issue as expired, leaving the session intact.
_Story: Detect refresh token reuse · Spec: Reuse handling · id: task-E2l-jLSt9sI_

#### Scenario: Expired rejected, session kept
- **WHEN** a refresh token is presented more than 30 days after issue
- **THEN** the request is rejected as expired and the session is not revoked
