# IDN-001 — Initial Build

## Why
# Business Requirements Document — Identity Service (token rotation)

Project: **Identity Service** (code IDN) · Team: Platform · Department: Engineering
Scope of this BRD: **refresh-token rotation and session revocation**. Login,
password reset and SSO federation are already live and out of scope.

## Overview
Every Indnord application signs users in through the Identity Service and
receives a short-lived access token plus a long-lived refresh token. Refresh
tokens today live for 30 days and are reusable, so a stolen refresh token
gives an attacker a month of silent access. This slice makes refresh tokens
single-use, detects reuse, and lets a user or an administrator end sessions.

## Goals
- A leaked refresh token is useless after its first use.
- Reuse of an already-rotated token ends the whole session family within
  one request.
- A user can see and end their own sessions; an admin can end anyone's.

## Users
- **End user**: signs in, keeps using apps without re-login, reviews and
  ends their sessions.
- **Client application**: exchanges a refresh token for a new pair.
- **Security admin**: revokes a user's sessions after an incident.

## Functional requirements

1. **Token pair issue**
   - On sign-in the service issues an access token (15 minutes) and a
     refresh token (30 days) and records a **session** with device label,
     IP, created time and last-used time.
   - Refresh tokens are opaque random strings of at least 256 bits; only a
     hash is stored.

2. ** …

## What Changes
- Implement **Token issuance and sessions**
- Implement **Rotation and reuse detection**
- Implement **Session management and limits**

## Impact
- Affected capabilities: token-issuance-and-sessions, rotation-and-reuse-detection, session-management-and-limits
