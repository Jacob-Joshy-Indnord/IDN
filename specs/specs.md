# Approved Specifications: IDN-001

Authoritative specs are written under /workspace/openspec/ in OpenSpec format: capability specs in openspec/specs/<capability>/spec.md (requirements + scenarios) and the implementation checklist in openspec/changes/<change>/tasks.md. A JSON copy is at /workspace/specs/spec_project.json. Implement ONLY the approved items below and satisfy every acceptance scenario.

If you build a runnable web app, serve it on 0.0.0.0:8080 so it can be opened in the Live Preview (the platform proxies that port).

## Build protocol
- Maintain a machine-readable build report at /workspace/specs/build_report.json with this exact shape: {"tasks": [{"id": "task-…", "status": "done", "files": ["path/to/file", "…"]}]}. Update it EVERY time you finish a task: set its status to "done" and list every file you created or modified for it (repo-relative paths). The platform reads this file back to mark tasks done and to link the produced code into the traceability graph.
- When delegating to sub-agents, include the task id (task-…) and its acceptance scenarios verbatim in the delegation message, and record the files they report back in the build report.

## Items marked “needs a look”
The BRD covers these only loosely, so the spec writer had to interpret them. For each one, decide the interpretation you build, record it in the build report as an "assumptions" list next to "tasks" — [{"id": "<node id>", "assumption": "…"}] — and state it in your final message so the reviewer can check it.
- Task `task-tDK6PMDCpSY`: Store refresh token hash only — BRD says only a hash is stored but does not name the hash algorithm; assumed a fast one-way hash (e.g. SHA-256) is adequate since tokens are high-entropy.
- Task `task-h1U-5fLc9bw`: Revoke session on reuse — BRD requires a 'distinct error code' but does not define its value or HTTP status; assumed a dedicated code (e.g. token_reuse_detected) different from expired/invalid.
- Task `task-HcaYBbNiC54`: List own active sessions — BRD does not say how the current session is identified; assumed from the session id carried by the caller's access token.
- Story `story-AVGzm0Tt8t8`: Admin revokes user sessions — BRD names the security admin role but not how admin rights are granted or checked.
- Spec `spec-DtlCsx5Szuk`: Admin session API — Endpoint shape is not specified; assumed mirrors of the user endpoints keyed by user id.

## Epic: Token issuance and sessions
Issue access/refresh token pairs on sign-in and record a session for each sign-in.
### Story: Receive token pair on sign-in
_As an end user, I want to receive an access token and a refresh token when I sign in, so that I can keep using apps without re-login._
#### Spec: Token pair issue
On sign-in, issue a 15-minute access token and a 30-day opaque refresh token; store only a hash of the refresh token.
- **Task** (`task-cHgUvqYYnQA`): Generate opaque refresh token
  - Generate refresh tokens from a cryptographically secure source with at least 256 bits of entropy.
  - [ ] WHEN a refresh token is generated THEN it is an opaque random string encoding at least 256 bits
- **Task** (`task-tDK6PMDCpSY`): Store refresh token hash only
  - Persist a hash of the refresh token for lookup and comparison; never persist the plaintext token.
  - [ ] WHEN a refresh token is issued and the datastore is inspected THEN the plaintext token appears nowhere and only its hash is stored
- **Task** (`task-3YJhfIL5-As`): Issue token pair on sign-in
  - On successful sign-in return an access token valid 15 minutes and a refresh token valid 30 days.
  - [ ] WHEN a user signs in successfully THEN the response contains an access token expiring in 15 minutes and a refresh token expiring in 30 days
#### Spec: Session record
Create a session record at sign-in holding device label, IP, created time and last-used time.
- **Task** (`task-lzd1yF83_aY`): Create session on sign-in
  - Persist a session with a stable id, client-supplied device label, IP, created time and last-used time, and link the first refresh token to it.
  - [ ] WHEN a user signs in with a device label from an IP THEN a session exists with that device label, IP, created time and last-used time set

## Epic: Rotation and reuse detection
Make refresh tokens single-use, rotate them atomically, and revoke the session on reuse.
### Story: Rotate refresh token on exchange
_As a client application, I want to exchange a refresh token for a new pair, so that the user stays signed in with single-use tokens._
#### Spec: Rotation exchange
Exchange endpoint validates the presented token, marks it used, issues a new access token and new refresh token in the same session, and updates last-used time.
- **Task** (`task-15u7cm1yA4s`): Exchange refresh token for new pair
  - Validate the presented token, mark it used, and return a new access token and new refresh token bound to the same session id.
  - [ ] WHEN a valid refresh token is exchanged once THEN a new access token and new refresh token are returned and the old token is marked used
  - [ ] WHEN a token is rotated THEN the new token belongs to the same session id
- **Task** (`task-OfbXI2OqGrk`): Update session last-used time
  - Set the session last-used time on every successful exchange.
  - [ ] WHEN an exchange succeeds THEN the session last-used time equals the exchange time
- **Task** (`task-v1rkkUFleZ0`): Make rotation atomic
  - Mark-as-used must be a single atomic conditional operation so concurrent exchanges of one token yield exactly one success.
  - [ ] WHEN two exchanges of the same token run concurrently THEN exactly one succeeds and the other is treated as reuse
#### Spec: Exchange performance
Exchange endpoint meets the stated throughput and latency target.
- **Task** (`task-lA8B4me2sQA`): Verify exchange load target
  - Load-test the exchange endpoint at 500 requests per second and measure latency.
  - [ ] WHEN the endpoint is loaded at 500 requests per second THEN 99th percentile latency is under 100 ms
### Story: Detect refresh token reuse
_As a security admin, I want reuse of a rotated token to revoke the whole session, so that a leaked token is useless after its first use._
#### Spec: Reuse handling
Detect presentation of an already-used token, revoke its session, reject with a distinct error, and record a security event.
- **Task** (`task-h1U-5fLc9bw`): Revoke session on reuse
  - When an already-rotated token is presented, revoke the owning session and reject the request with a distinct error code.
  - [ ] WHEN an already-rotated refresh token is presented THEN the session is revoked and the request is rejected with the distinct reuse error code
  - [ ] WHEN the session was revoked by reuse and its latest refresh token is then presented THEN the exchange is rejected
- **Task** (`task-6BoO3EP4e2M`): Write reuse security event
  - On reuse, write a security event with the session id and presenting IP.
  - [ ] WHEN reuse is detected THEN one security event is stored with the session id and presenting IP
- **Task** (`task-CEfrOaJF9bk`): Retain security events one year
  - Apply a one-year retention policy to security events.
  - [ ] WHEN a security event is older than one year THEN it may be purged, and events younger than one year are never purged
- **Task** (`task-E2l-jLSt9sI`): Reject expired token without revoking
  - Reject tokens presented more than 30 days after issue as expired, leaving the session intact.
  - [ ] WHEN a refresh token is presented more than 30 days after issue THEN the request is rejected as expired and the session is not revoked

## Epic: Session management and limits
Let users and security admins list and end sessions, and cap active sessions per user.
### Story: End user manages own sessions
_As an end user, I want to list and end my sessions, so that I can cut off devices I no longer trust._
#### Spec: User session API
Authenticated endpoints to list the caller's active sessions and end one.
- **Task** (`task-HcaYBbNiC54`): List own active sessions
  - Return the caller's active sessions with device label, IP, created, last used and a current-session marker.
  - [ ] WHEN a user requests their sessions THEN each active session shows device label, IP, created, last used, and exactly one is marked current
- **Task** (`task-TTQj288JBPQ`): End own session
  - Revoke a chosen session of the caller, invalidating its refresh token immediately.
  - [ ] WHEN a user ends a session from their list and its refresh token is then exchanged THEN the exchange fails
  - [ ] WHEN a session is ended and an already-issued access token is used within its 15 minutes THEN the access token is still accepted
### Story: Admin revokes user sessions
_As a security admin, I want to list and end any user's sessions, so that I can respond to an incident._
#### Spec: Admin session API
Admin-only endpoints to list a user's sessions, end one, or end all.
- **Task** (`task-r1c4HYJosAE`): Enforce security admin authorization
  - Restrict admin session endpoints to callers holding the security admin role, as asserted by a role claim in the access token.
  - [ ] WHEN a caller without the security admin role calls an admin session endpoint THEN the request is rejected as forbidden
- **Task** (`task-hLzcSUBR0pg`): Admin list and end user sessions
  - Let a security admin list any user's sessions and end any single session.
  - [ ] WHEN an admin requests another user's sessions THEN that user's active sessions are returned
  - [ ] WHEN an admin ends one of that user's sessions THEN its refresh token is rejected on the next exchange
- **Task** (`task-2fzhOuV2qBo`): End all sessions of a user
  - Provide a single call that revokes every active session of a given user.
  - [ ] WHEN an admin ends all sessions of a user in one call THEN every session of that user is revoked and none can be exchanged
### Story: Cap active sessions per user
_As a security admin, I want each user limited to 10 active sessions, so that stale sessions do not accumulate._
#### Spec: Session limit
On sign-in, if the user already holds 10 active sessions, end the least recently used one.
- **Task** (`task-nkI776Wxz80`): Evict LRU session at limit
  - At sign-in, when the user has 10 active sessions, revoke the session with the oldest last-used time before creating the new one.
  - [ ] WHEN a user with 10 active sessions signs in an 11th time THEN the least recently used session is ended and exactly 10 active sessions remain
