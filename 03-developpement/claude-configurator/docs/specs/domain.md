# Domain Model — Authentication & Stripe Integration

**Document Type**: Domain Model & Entities  
**Date**: 2026-04-27  
**Status**: Ready for ACT phase  
**Audience**: Engineering, Product

---

## Bounded Context: Payment-Gated Chat

**Domain**: E-commerce + Authentication  
**Subdomain**: User authentication via Stripe payment, access control to chat service

---

## Core Entities

### 1. User

**Description**: A person who wants to use CS Business's diagnostic chat service

**Properties**:
- `id` (UUID): Unique identifier (managed by Supabase)
- `email` (VARCHAR, UNIQUE): Contact address, used for magic link sign-in
- `created_at` (TIMESTAMP): Account creation time
- `email_confirmed_at` (TIMESTAMP, nullable): When user clicked magic link

**Lifecycle**:
1. **Signup**: Email collected at `/pricing.html`
2. **Payment**: Stripe checkout initiated via POST /create-checkout
3. **User Creation**: Supabase inviteUserByEmail() called automatically by webhook
4. **Confirmation**: User clicks magic link, email_confirmed_at set
5. **Access**: User can access /chat with valid JWT
6. **Retention**: User record kept forever (allows re-purchase)

**Invariants**:
- Email must be valid (RFC 5322)
- Email must be unique across all users
- email_confirmed_at only set after magic link verification
- User cannot access /chat without confirmed email + valid payment

**Note**: User is **not** responsible for setting a password (magic link auth only)

---

### 2. Payment Session (Stripe)

**Description**: A checkout session representing one attempted or completed payment

**Stripe-managed Properties**:
- `session_id` (VARCHAR): Checkout session ID (e.g., `cs_...`)
- `customer_email` (VARCHAR): Email entered at checkout
- `payment_status` (ENUM): "unpaid", "paid", "expired"
- `created_at` (TIMESTAMP): Stripe creation time
- `expires_at` (TIMESTAMP): When session expires (24h default)

**CS Business Properties** (stored in `diagnostics` table):
- `stripe_session_id` (VARCHAR, UNIQUE): Stripe session ID
- `client_id` (UUID FK): Link to User.id
- `paid_at` (TIMESTAMP): When payment completed (NOW() at webhook processing)

**Lifecycle**:
1. **Initiation**: Frontend calls POST /create-checkout (email)
2. **Redirect**: Frontend redirected to Stripe Checkout URL
3. **User Payment**: User enters payment details (handled by Stripe)
4. **Completion**: Stripe event `checkout.session.completed` fired
5. **Webhook**: Edge Function receives webhook, verifies signature
6. **User Creation**: inviteUserByEmail() called (if not already exists)
7. **Recording**: Diagnostic row inserted with stripe_session_id + client_id + paid_at

**Invariants**:
- Session ID is globally unique (Stripe guarantee)
- One session_id → at most one User (idempotence via UNIQUE constraint)
- paid_at is set exactly once at webhook processing
- paid_at is immutable (cannot be updated later)

---

### 3. Diagnostic Record

**Description**: A record of a user's diagnostic chat session and results

**Properties**:
- `id` (UUID): Unique diagnostic record identifier
- `stripe_session_id` (VARCHAR, UNIQUE): Link to Payment Session (idempotence key)
- `client_id` (UUID FK): Link to User (ownership for RLS)
- `paid_at` (TIMESTAMP WITH TZ): Payment timestamp (retention window anchor)
- `created_at` (TIMESTAMP WITH TZ): When diagnostic was created
- `content` (JSONB): Diagnostic data (analysis results, responses, etc.)
- `metadata` (JSONB): Additional context (tags, status, etc.)

**Lifecycle**:
1. **Creation**: Inserted by stripe-webhook Edge Function after payment
2. **Updates**: Modified by /chat Edge Function as user interacts
3. **Retention**: Kept for 30 days from paid_at
4. **Cleanup**: Automatically deleted by pg_cron after 30 days

**Invariants**:
- stripe_session_id must be unique (prevents duplicate rows from webhook replay)
- client_id must exist in auth.users (referential integrity)
- paid_at never null, never updated
- created_at never updated
- Only owner (client_id) or admin can view/update (RLS enforced)

**Access Control**:
- **Read**: `auth.uid() = client_id OR auth.role() = 'admin'`
- **Insert**: `auth.uid() IS NOT NULL` (authenticated users only)
- **Update**: `auth.uid() = client_id OR auth.role() = 'admin'`
- **Delete**: `auth.uid() = client_id OR auth.role() = 'admin'`

---

### 4. Authentication Token (JWT)

**Description**: Stateless token issued by Supabase auth, used to authenticate /chat requests

**Properties**:
- `sub` (UUID): Subject (User.id)
- `email` (VARCHAR): User email
- `aud` (VARCHAR): Audience ("authenticated")
- `iat` (Unix timestamp): Issued at
- `exp` (Unix timestamp): Expiration (iat + 3600 seconds)
- `role` (VARCHAR): User role ("authenticated", "admin", etc.)

**Lifecycle**:
1. **Issuance**: Supabase issues JWT after user clicks magic link (verifyOtp)
2. **Storage**: Frontend stores in localStorage
3. **Usage**: Sent in every /chat request via Authorization header
4. **Validation**: Server validates signature & expiry on every request
5. **Expiration**: After 1 hour, token invalid (401 on /chat)
6. **Renewal**: User must re-authenticate (no refresh token mechanism)

**Invariants**:
- JWT is cryptographically signed (HMAC-SHA256)
- Signature verified via Supabase secret (server-side only)
- Expiry exactly 1 hour (3600 seconds)
- Token is stateless (no server session table)
- Expiry never extended (no refresh token)

**Note**: JWT does NOT contain paid_at; paid status checked on every /chat request (not cached)

---

### 5. Stripe Webhook Event

**Description**: Event sent by Stripe when a payment completes; triggers user creation and diagnostic record

**Properties**:
- `id` (VARCHAR): Unique Stripe event ID (e.g., `evt_...`)
- `type` (VARCHAR): Event type (e.g., `checkout.session.completed`)
- `data.object.id` (VARCHAR): Stripe session ID (e.g., `cs_...`)
- `data.object.customer_email` (VARCHAR): Customer email
- `created` (Unix timestamp): When event created
- `request.id` (VARCHAR, nullable): API request ID (if triggered by API)

**Lifecycle**:
1. **Generation**: Stripe generates event after payment completion
2. **Delivery**: Stripe sends POST to /functions/v1/stripe-webhook (up to 5 retries)
3. **Signature**: Included as `stripe-signature: t=<timestamp>,v1=<hmac>`
4. **Reception**: Edge Function receives event
5. **Validation**: Signature verified via Stripe.webhooks.constructEvent()
6. **Processing**: If valid, user created + diagnostic inserted
7. **Idempotence**: Replayed webhooks detected via stripe_session_id UNIQUE check

**Invariants**:
- Event is cryptographically signed (HMAC-SHA256)
- Signature must be verified before processing
- Replayed events (same event_id) detected and skipped
- Event is immutable from Stripe's perspective (not modified by CS Business)

**Error Handling**:
- Invalid signature → 400 Bad Request, log attempt
- User creation failure (3 retries) → 500 Internal Server Error, log error, let Stripe retry
- Database INSERT failure → 500, log error

---

## Value Objects

### Email Address

**Description**: A valid RFC 5322 email address

**Properties**:
- `address` (VARCHAR): Email string

**Constraints**:
- Must match pattern: `^[^\s@]+@[^\s@]+\.[^\s@]+$` (basic validation)
- Must be unique across all users
- Used as sign-in identifier (magic link sent here)

---

### Timestamp (with Time Zone)

**Description**: A moment in time, always UTC

**Properties**:
- `value` (TIMESTAMP WITH TIME ZONE): ISO 8601 format

**Constraints**:
- Always UTC (no local timezones)
- Used for: user creation, payment time, retention window
- Immutable once set

---

### Retention Window

**Description**: A 30-day period starting from paid_at

**Calculation**:
- Window start: `paid_at`
- Window end: `paid_at + '30 days'::interval`
- User in window: `NOW() < paid_at + '30 days'::interval`
- User expired: `NOW() >= paid_at + '30 days'::interval`

**Constraints**:
- Fixed duration (not configurable per user)
- Checked on every /chat request
- Window expiry triggers automatic cleanup (pg_cron)

---

## Aggregates

### Payment Aggregate

**Root**: Payment Session (stripe_session_id)

**Children**:
- User (created by webhook)
- Diagnostic Record (created by webhook)

**Invariants**:
1. One session_id → exactly one user (via idempotence)
2. One session_id → exactly one diagnostic row (UNIQUE constraint)
3. Payment session always has associated user
4. Diagnostic row always has associated payment session (stripe_session_id NOT NULL)

**Lifecycle**:
- Created: Webhook reception
- Updated: Diagnostic row modified by /chat requests
- Deleted: After 30 days (diagnostic row only; user kept)

---

### User Aggregate

**Root**: User (id)

**Children**:
- Payment Sessions (client_id FK)
- Diagnostic Records (client_id FK)
- JWT tokens (generated on demand, not stored)

**Invariants**:
1. One user → many payment sessions (multiple purchases allowed)
2. One user → many diagnostic records (multiple diagnostics per payment)
3. User email must be unique
4. User is kept forever (allows re-purchase)

**Lifecycle**:
- Created: inviteUserByEmail() called by webhook
- Confirmed: Magic link clicked (email_confirmed_at set)
- Active: Has valid JWT + paid_at within 30 days
- Stale: No valid JWT or paid_at > 30 days old (can re-purchase)

---

## Business Rules

### Authentication Rules

1. **Magic Link Authentication**: User must click email link to confirm identity (no password required)
2. **JWT Validity**: JWT expires after 1 hour; no refresh token
3. **Server-side Validation**: JWT signature validated server-side only; never decoded client-side
4. **No Session Table**: JWT is stateless; no server-side session storage

### Payment Rules

1. **Stripe Only**: Only Stripe webhooks create new users (no manual signup)
2. **Automatic User Creation**: inviteUserByEmail() called automatically; user does not manually sign up
3. **Payment-Gated Access**: /chat requires valid JWT + payment within 30 days
4. **No Refunds**: Refund logic not handled in this phase (out of scope)

### Data Retention Rules

1. **Diagnostic Cleanup**: Diagnostic rows deleted after 30 days from paid_at
2. **User Retention**: Users kept forever to allow re-purchase
3. **Automated Deletion**: pg_cron job runs daily at 2 AM UTC
4. **No Manual Cleanup**: Application does not trigger deletions

### Idempotence Rules

1. **Webhook Replay Safe**: Replayed webhooks do not create duplicate users
2. **stripe_session_id Uniqueness**: Database constraint prevents duplicates
3. **Idempotence Check**: Query diagnostics before user creation
4. **Atomic Insertion**: Diagnostic row inserted atomically with user creation

### RLS Rules

1. **Own Data Only**: Users see only their own diagnostic records
2. **Admin Override**: Admin role can see all records (set via Supabase)
3. **Database Enforcement**: RLS enforced at Postgres layer (not application-level)
4. **Policy Application**: All SELECT/INSERT/UPDATE/DELETE queries filtered by RLS

---

## Domain Concepts Glossary

| Term | Definition |
|------|-----------|
| **Checkout Session** | Stripe's representation of a payment attempt; identified by session_id |
| **Magic Link** | Email-based authentication token; user clicks link to sign in without password |
| **JWT** | JSON Web Token; stateless, cryptographically signed auth token issued by Supabase |
| **RLS** | Row-Level Security; Postgres feature that filters data based on user identity |
| **Idempotence** | Property that replayed actions have same effect as single execution |
| **Retention Window** | 30-day period from paid_at; after which diagnostic data deleted |
| **Auth.users** | Supabase-managed user table (not in public schema) |
| **Client ID** | UUID of User; used in RLS and as FK in diagnostics table |
| **Paid At** | Timestamp when payment completed; used for retention window calculation |

---

## Relationships Diagram

```
┌──────────────────┐
│   auth.users     │
│   (Supabase)     │
├──────────────────┤
│ id (PK)          │
│ email (UNIQUE)   │
│ created_at       │
│ email_confirmed  │
└────────┬─────────┘
         │ 1
         │
         │ N
         │
    ┌────▼──────────────────────┐
    │   diagnostics (public)     │
    ├────────────────────────────┤
    │ id (PK)                    │
    │ stripe_session_id (UNIQUE) │───┐
    │ client_id (FK → auth.users)│   │
    │ paid_at                    │   │
    │ created_at                 │   │
    │ content                    │   │
    │ metadata                   │   │
    └────────────────────────────┘   │
                                      │
                    ┌─────────────────┘
                    │
                    │ 1:1
                    │
            ┌───────▼──────────────┐
            │  Payment Session     │
            │  (Stripe-managed)    │
            ├──────────────────────┤
            │ session_id (PK)      │
            │ customer_email       │
            │ payment_status       │
            │ created_at           │
            │ expires_at           │
            └──────────────────────┘
```

---

**Document Version**: 1.0  
**Last Updated**: 2026-04-27  
**Domain Expert Review**: Required before ACT phase
