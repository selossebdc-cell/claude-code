# Architecture Rules — Auto-Factures Fred

## Core Principles

### 1. Spec-First Development
- No code without specifications
- Specs define acceptance criteria
- Architecture decisions documented in ADRs

### 2. API-First Design
- REST API is the system contract
- Backend and frontend develop against API spec
- Backward compatibility required for endpoint changes

### 3. Async-by-Default
- Long-running operations (PDF, email) must be async
- Use Bull queue for batch processing
- Return 202 (Accepted) for async operations

### 4. Database Constraints
- All business rules enforced at database level where possible
- Foreign keys, check constraints, triggers for audit
- No "trust the application" logic

## Code Organization

### Directory Structure

```
src/
├── routes/           # Express route handlers
│   ├── transactions.js
│   ├── invoices.js
│   ├── customers.js
│   └── auth.js
├── services/         # Business logic
│   ├── invoice-generator.js
│   ├── email-service.js
│   └── queue.js
├── models/           # Data models (ORM or raw queries)
│   ├── Invoice.js
│   ├── Transaction.js
│   └── Customer.js
├── middleware/       # Express middleware
│   ├── auth.js
│   ├── errorHandler.js
│   └── validation.js
├── utils/            # Helpers
│   ├── logger.js
│   ├── validators.js
│   └── formatters.js
├── workers/          # Background job processors
│   ├── invoice-generator.js
│   └── email-sender.js
└── config/           # Configuration
    ├── database.js
    ├── redis.js
    ├── email.js
    └── jwt.js
```

### Module Exports Pattern

```javascript
// Each module should export:
// - Main function/class
// - Helper functions if any
// - Clear interface

// Good:
module.exports = {
  generateInvoice,      // primary export
  calculateTax,         // helper
  validateAmount,       // helper
};

// Bad:
module.exports = generateInvoice; // unclear what else is exported
```

## Coding Standards

### Error Handling

```javascript
// Always use try-catch for async operations
try {
  const invoice = await generateInvoice(txnId);
} catch (error) {
  logger.error('Invoice generation failed:', error);
  throw new ApiError('INVOICE_GEN_FAILED', error.message, 500);
}

// Never silently catch errors
// WRONG: } catch (e) { } // ❌

// Always log errors with context
// WRONG: throw error; // ❌
// RIGHT: throw new ApiError(...) with logger.error() ✓
```

### Async/Await Rules

```javascript
// Never use floating promises
// WRONG:
invoiceQueue.add({ txnId });  // no await ❌

// RIGHT:
await invoiceQueue.add({ txnId }); ✓

// Use Promise.all for concurrent operations
// WRONG:
await sendEmail(inv1);
await sendEmail(inv2);

// RIGHT:
await Promise.all([sendEmail(inv1), sendEmail(inv2)]); ✓
```

### Validation Rules

```javascript
// Always validate input at route level
router.post('/invoices', async (req, res) => {
  // Use Joi schema
  const schema = Joi.object({
    transaction_id: Joi.string().uuid().required(),
    template_id: Joi.string().uuid().optional(),
  });
  
  const { error, value } = schema.validate(req.body);
  if (error) {
    return res.status(400).json({
      success: false,
      error: { message: error.message },
    });
  }
  
  // Proceed with validated `value`
});
```

### Database Access

```javascript
// Use parameterized queries to prevent SQL injection
// WRONG:
const sql = `SELECT * FROM invoices WHERE id = '${invoiceId}'`; ❌

// RIGHT:
const { rows } = await db.query(
  'SELECT * FROM invoices WHERE id = $1',
  [invoiceId]
); ✓
```

### Logging Standards

```javascript
// Use Pino structured logging
logger.info('Invoice generated', {
  invoice_id: inv.id,
  customer_id: inv.customer_id,
  amount: inv.total_amount,
  status: inv.status,
});

// Log levels:
// - logger.debug() - development details
// - logger.info()  - important business events
// - logger.warn()  - recoverable issues
// - logger.error() - failures requiring attention
```

### Testing Requirements

```javascript
// Every route must have tests
// Every service must have tests
// Test coverage target: >80%

// Test structure:
describe('POST /invoices', () => {
  it('should generate invoice from transaction', async () => {
    const res = await request(app)
      .post('/api/v1/invoices')
      .send({ transaction_id: 'uuid', template_id: 'uuid' });
    
    expect(res.status).toBe(200);
    expect(res.body.data.invoice_number).toMatch(/INV-\d+-\d+/);
  });

  it('should reject invalid transaction ID', async () => {
    const res = await request(app)
      .post('/api/v1/invoices')
      .send({ transaction_id: 'invalid' });
    
    expect(res.status).toBe(400);
  });
});
```

## API Design Rules

### Response Format

All API responses must follow standard format:

```json
{
  "success": true|false,
  "data": { /* resource or array */ },
  "error": { /* only if success=false */ },
  "meta": { "timestamp": "ISO8601", "requestId": "uuid" }
}
```

### HTTP Status Codes

- 200 OK: GET, PATCH success
- 201 Created: POST success
- 202 Accepted: Async operation started
- 400 Bad Request: Invalid input
- 401 Unauthorized: Auth failure
- 403 Forbidden: Authorization failure
- 404 Not Found: Resource missing
- 409 Conflict: State conflict (e.g., can't modify issued invoice)
- 422 Unprocessable Entity: Business rule violation
- 500 Internal Server Error: Unexpected server error

### Pagination

```javascript
// Always use limit/offset pagination
GET /invoices?limit=20&offset=0

// Response includes metadata:
{
  "data": [ ... ],
  "meta": {
    "total": 500,
    "limit": 20,
    "offset": 0,
    "hasMore": true
  }
}
```

## Security Rules

### Secrets Management

- **NEVER** hardcode secrets (passwords, API keys, JWT secret)
- **ALWAYS** use environment variables
- **NEVER** commit .env files
- Use .env.example for documentation

### Authentication & Authorization

- All endpoints require `authenticate` middleware
- Role-based access control via `authorize()` middleware
- JWT tokens expire: access 15 minutes, refresh 30 days
- Log all auth failures

### Data Protection

- No PII in logs (emails, tax IDs, customer names)
- Use parameterized queries (prevent SQL injection)
- Validate all external input
- HTTPS only in production

### Audit Logging

- Log all invoice creation, modification, deletion
- Log all auth attempts (success and failure)
- Retention: minimum 7 years for tax compliance
- Immutable audit table (append-only)

## Database Rules

### Transactions

```sql
-- All invoice generation must be in a transaction
BEGIN;
  INSERT INTO invoices (...) RETURNING id;
  INSERT INTO audit_log (...);
  UPDATE transactions SET status = 'PROCESSED';
COMMIT;
```

### Foreign Keys

```sql
-- All FK relationships must have constraints
ALTER TABLE invoices
ADD CONSTRAINT fk_customer
FOREIGN KEY (customer_id) REFERENCES customers(id);
```

### Naming Conventions

- Tables: `invoice_templates`, `audit_logs` (snake_case, plural)
- Columns: `created_at`, `updated_at`, `is_active` (snake_case)
- Constraints: `pk_invoices`, `fk_customer`, `uk_email` (type prefix)
- Indexes: `idx_invoice_customer_id` (idx_ prefix)

## Performance Guidelines

### Batch Processing

- Process invoices in batches of 50-100 (balance throughput vs memory)
- Use Bull queue with concurrency = 5 (prevent resource exhaustion)
- Timeout per job: 5 minutes (prevents hanging)

### Caching

- Cache invoice templates (in-memory)
- Cache customer data (5-minute TTL)
- Invalidate cache on updates
- No caching of invoice data (always fresh from DB)

### Database Queries

- Index all foreign keys and filter columns
- Avoid SELECT * (specify columns)
- Use EXPLAIN ANALYZE for slow queries
- Connection pool: min 5, max 20

## Deployment Rules

### Environment Management

- Three environments: development, staging, production
- Environment-specific configs in `config/environments/`
- Staging identical to production (test real behavior)
- Blue-green deployment for zero-downtime updates

### Database Migrations

- Use numbered migrations: `001-create-invoices.sql`
- Always include rollback script
- Test rollback in staging
- Run migrations before app startup

## Monitoring & Observability

### Key Metrics

- Request latency (p50, p95, p99)
- Invoice generation throughput (invoices/min)
- Queue depth (pending, processing)
- Error rate (by endpoint)
- PDF generation time (Puppeteer performance)

### Alerting

- Alert on error rate > 5%
- Alert on queue depth > 1000
- Alert on PDF generation time > 30s
- Alert on database connection pool exhaustion

---

**Version**: 1.0  
**Status**: Active  
**Last Updated**: 2026-04-26
