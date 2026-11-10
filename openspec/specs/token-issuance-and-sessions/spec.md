# Token issuance and sessions

## Purpose
Issue access/refresh token pairs on sign-in and record a session for each sign-in.

## Requirements

### Requirement: Generate opaque refresh token
The system SHALL generate refresh tokens from a cryptographically secure source with at least 256 bits of entropy.
_Story: Receive token pair on sign-in · Spec: Token pair issue · id: task-cHgUvqYYnQA_

#### Scenario: Refresh token has at least 256 bits of entropy
- **WHEN** a refresh token is generated
- **THEN** it is an opaque random string encoding at least 256 bits

### Requirement: Store refresh token hash only
The system SHALL persist a hash of the refresh token for lookup and comparison; never persist the plaintext token.
_Story: Receive token pair on sign-in · Spec: Token pair issue · id: task-tDK6PMDCpSY_

#### Scenario: Only hash persisted
- **WHEN** a refresh token is issued and the datastore is inspected
- **THEN** the plaintext token appears nowhere and only its hash is stored

### Requirement: Issue token pair on sign-in
The system SHALL on successful sign-in return an access token valid 15 minutes and a refresh token valid 30 days.
_Story: Receive token pair on sign-in · Spec: Token pair issue · id: task-3YJhfIL5-As_

#### Scenario: Pair issued with correct lifetimes
- **WHEN** a user signs in successfully
- **THEN** the response contains an access token expiring in 15 minutes and a refresh token expiring in 30 days

### Requirement: Create session on sign-in
The system SHALL persist a session with a stable id, client-supplied device label, IP, created time and last-used time, and link the first refresh token to it.
_Story: Receive token pair on sign-in · Spec: Session record · id: task-lzd1yF83_aY_

#### Scenario: Session recorded
- **WHEN** a user signs in with a device label from an IP
- **THEN** a session exists with that device label, IP, created time and last-used time set
