# Implementation Tasks

## Token issuance and sessions
### Receive token pair on sign-in
- [ ] Generate opaque refresh token (`task-cHgUvqYYnQA`)
  - [ ] Refresh token has at least 256 bits of entropy
- [ ] Store refresh token hash only (`task-tDK6PMDCpSY`)
  - [ ] Only hash persisted
- [ ] Issue token pair on sign-in (`task-3YJhfIL5-As`)
  - [ ] Pair issued with correct lifetimes
- [ ] Create session on sign-in (`task-lzd1yF83_aY`)
  - [ ] Session recorded

## Rotation and reuse detection
### Rotate refresh token on exchange
- [ ] Exchange refresh token for new pair (`task-15u7cm1yA4s`)
  - [ ] New pair returned, old token used
  - [ ] Session id stable
- [ ] Update session last-used time (`task-OfbXI2OqGrk`)
  - [ ] Last-used updated
- [ ] Make rotation atomic (`task-v1rkkUFleZ0`)
  - [ ] Concurrent double exchange
- [ ] Verify exchange load target (`task-lA8B4me2sQA`)
  - [ ] Meets p99 target
### Detect refresh token reuse
- [ ] Revoke session on reuse (`task-h1U-5fLc9bw`)
  - [ ] Reuse revokes session
  - [ ] Newest token also dead
- [ ] Write reuse security event (`task-6BoO3EP4e2M`)
  - [ ] Event written
- [ ] Retain security events one year (`task-CEfrOaJF9bk`)
  - [ ] One-year retention
- [ ] Reject expired token without revoking (`task-E2l-jLSt9sI`)
  - [ ] Expired rejected, session kept

## Session management and limits
### End user manages own sessions
- [ ] List own active sessions (`task-HcaYBbNiC54`)
  - [ ] Sessions listed with fields
- [ ] End own session (`task-TTQj288JBPQ`)
  - [ ] Next exchange fails
  - [ ] Access token stays valid
### Admin revokes user sessions
- [ ] Enforce security admin authorization (`task-r1c4HYJosAE`)
  - [ ] Non-admin denied
- [ ] Admin list and end user sessions (`task-hLzcSUBR0pg`)
  - [ ] Admin lists sessions
  - [ ] Admin ends a session
- [ ] End all sessions of a user (`task-2fzhOuV2qBo`)
  - [ ] All sessions ended
### Cap active sessions per user
- [ ] Evict LRU session at limit (`task-nkI776Wxz80`)
  - [ ] 11th sign-in evicts LRU

