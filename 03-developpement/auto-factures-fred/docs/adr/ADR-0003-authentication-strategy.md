# ADR-0003: Authentication and Authorization Strategy

**Date**: 2026-04-26  
**Status**: Proposed  
**Deciders**: Security Team  
**Decision**: Implement JWT-based authentication with role-based access control (RBAC)

## Context

Auto-Factures Fred API must:
- Authenticate API clients (internal and external partners)
- Authorize operations based on user roles (admin, accountant, viewer)
- Support both user sessions and service-to-service authentication
- Comply with security best practices (token rotation, expiration)

**Evaluated Options**:
1. **JWT + OAuth2 (Selected)**: Industry standard, stateless, scalable
2. **Session-based + Cookies**: Better for browser clients, requires session store
3. **API Keys only**: Simple, insufficient for user authentication

## Decision

**Implement JWT authentication with OAuth2-inspired refresh token pattern + RBAC**

### Architecture

```
┌─ User Login / Service Auth ─┐
│  Credentials (username/password or client credentials)
└──────────────┬──────────────┘
               ↓
        [JWT Issuer]
        ├─ Issue Access Token (short-lived, 15m)
        ├─ Issue Refresh Token (long-lived, 30d)
        └─ Sign with HS256 (symmetric) or RS256 (asymmetric)
               ↓
        API Request with:
        Authorization: Bearer {access_token}
               ↓
        [JWT Middleware]
        ├─ Verify signature
        ├─ Check expiration
        ├─ Extract claims (user_id, roles)
        └─ Allow/deny based on RBAC rules
```

## Implementation Details

### JWT Token Structure

```javascript
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user-uuid",        // subject (user ID)
    "iat": 1698321600,         // issued at
    "exp": 1698325200,         // expires in 1 hour
    "iss": "auto-factures-fred",
    "aud": "api.auto-factures",
    "roles": ["accountant", "invoicing"],
    "customer_id": "cust-uuid" // optional: scoped to customer
  },
  "signature": "HMAC256(...)"
}
```

### Authentication Types

#### 1. User Authentication (Username/Password)

```javascript
// POST /auth/login
{
  "username": "fred@example.com",
  "password": "secure_password"
}

// Response
{
  "success": true,
  "data": {
    "access_token": "eyJhbGc...",      // expires in 15 minutes
    "refresh_token": "eyJhbGc...",     // expires in 30 days
    "token_type": "Bearer",
    "expires_in": 900
  }
}
```

#### 2. Service-to-Service Authentication (Client Credentials)

```javascript
// POST /auth/token (OAuth2 Client Credentials Grant)
{
  "grant_type": "client_credentials",
  "client_id": "service-xyz",
  "client_secret": "secret_key"
}

// Response
{
  "access_token": "eyJhbGc...",
  "token_type": "Bearer",
  "expires_in": 3600  // 1 hour
}
```

#### 3. Token Refresh

```javascript
// POST /auth/refresh
{
  "refresh_token": "eyJhbGc..."
}

// Response
{
  "access_token": "eyJhbGc...",
  "expires_in": 900
}
```

### Middleware Implementation

```javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');

module.exports = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({
      success: false,
      error: { code: 'MISSING_TOKEN', message: 'Authorization header required' },
    });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({
        success: false,
        error: { code: 'TOKEN_EXPIRED', message: 'Token has expired' },
      });
    }
    return res.status(401).json({
      success: false,
      error: { code: 'INVALID_TOKEN', message: 'Invalid token' },
    });
  }
};
```

### Role-Based Access Control (RBAC)

```javascript
// middleware/authorize.js
const authorize = (...allowedRoles) => {
  return (req, res, next) => {
    const userRoles = req.user.roles || [];

    if (!allowedRoles.some(role => userRoles.includes(role))) {
      return res.status(403).json({
        success: false,
        error: { code: 'FORBIDDEN', message: 'Insufficient permissions' },
      });
    }

    next();
  };
};

// Usage in routes
router.post(
  '/invoices/generate',
  authenticate,
  authorize('accountant', 'admin'),
  generateInvoice
);

router.get(
  '/audit-logs',
  authenticate,
  authorize('admin'),
  getAuditLogs
);
```

### Role Definitions

| Role | Permissions | Use Case |
|------|-------------|----------|
| `viewer` | GET invoices, transactions, customers | Finance reporting, dashboards |
| `accountant` | All viewer + POST/PATCH invoices, email | Invoice generation and sending |
| `admin` | All operations + create users, audit logs | Full system management |

### Key Rotation Strategy

```javascript
// config/jwt.js
module.exports = {
  algorithm: 'HS256',
  secretKey: process.env.JWT_SECRET,
  accessTokenExpiry: '15m',    // short-lived
  refreshTokenExpiry: '30d',   // long-lived
  issuer: 'auto-factures-fred',
  audience: 'api.auto-factures',
};
```

**Rotation Policy**:
- Access tokens: Auto-refresh via refresh token (no manual rotation needed)
- Refresh tokens: Rotate every 30 days (automated or manual)
- Secret key: Rotate annually or if compromised (requires re-issuing all tokens)

## Consequences

### Positive
- ✓ Stateless (no session store needed)
- ✓ Scalable (works with multiple API servers)
- ✓ Standard (JWT is widely supported)
- ✓ Secure (token expiration, refresh token pattern)
- ✓ Flexible (easy to add roles, scopes)
- ✓ Auditable (token claims include user ID, roles)

### Negative
- ✗ Token revocation difficult (user logout doesn't immediately invalidate token)
- ✗ Token size grows with claims (use minimal claims)
- ✗ Requires secure storage of secret key (environment variable)
- ✗ Refresh token management adds complexity

## Mitigations

1. **Revocation**: Implement token blacklist (Redis) for logout if needed
2. **Token Size**: Keep claims minimal (avoid large JSON objects)
3. **Secret Management**: Use cloud secret manager (AWS Secrets Manager, Vault)
4. **Rotation**: Automate via CI/CD; document manual process

## Security Checklist

- [ ] Use HTTPS only (JWT vulnerable over HTTP)
- [ ] Validate token signature (verify.jwt)
- [ ] Check token expiration (handled by jwt.verify)
- [ ] Implement CSRF protection if using cookies (not applicable for API-first)
- [ ] Rate limit auth endpoints (prevent brute force)
- [ ] Log all auth failures
- [ ] Implement logout endpoint (invalidate refresh token)
- [ ] Secrets stored in environment variables, never in code

## Dependencies

### Libraries
- **jsonwebtoken**: JWT creation and verification
- **passport** (optional): Flexible auth middleware

### Infrastructure
- **Redis** (optional): Token blacklist for revocation

## Related Decisions

- **ADR-0004**: Security and PII handling
- **ADR-0005**: Audit logging strategy

## Future Enhancements

### Phase 2
- OAuth2 with external identity providers (Google, GitHub)
- Multi-factor authentication (MFA) support
- API key authentication (for legacy integrations)

### Phase 3
- Single Sign-On (SSO) integration
- Scoped tokens (per-customer access isolation)

---

**Decision Owner**: Security Lead  
**Review Date**: 2026-06-26 (security audit before production)
