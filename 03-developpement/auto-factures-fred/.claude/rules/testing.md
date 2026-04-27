# Testing Rules — Auto-Factures Fred

## Testing Strategy

### Test Pyramid

```
        △
       △ △      E2E Tests (UI + real DB)
      △ △ △     Integration Tests (API + real DB)
     △ △ △ △    Unit Tests (isolated functions)
    △ △ △ △ △   
```

**Distribution**: 60% unit, 25% integration, 15% E2E

### Coverage Targets

- **Overall**: >80% statement coverage
- **Critical paths**: >95% (invoice generation, auth, payments)
- **Utils**: >90%
- **Routes**: >80%
- **Services**: >85%

## Unit Tests

### Test Structure

```javascript
// tests/services/invoice-generator.test.js
const { generateInvoice, calculateTax } = require('../../src/services/invoice-generator');

describe('Invoice Generator Service', () => {
  describe('calculateTax', () => {
    it('should calculate tax correctly with 20% rate', () => {
      const result = calculateTax(100, 0.20);
      expect(result).toBe(20);
    });

    it('should round to 2 decimal places', () => {
      const result = calculateTax(10.555, 0.20);
      expect(result).toBe(2.11);
    });

    it('should return 0 for 0% rate', () => {
      const result = calculateTax(100, 0);
      expect(result).toBe(0);
    });
  });

  describe('generateInvoice', () => {
    it('should throw error if amount is negative', async () => {
      const txn = { amount: -100, customer_id: 'uuid' };
      await expect(generateInvoice(txn)).rejects.toThrow('Amount must be positive');
    });
  });
});
```

### Mocking Rules

```javascript
// Mock external dependencies
jest.mock('../../src/config/redis');
jest.mock('../../src/services/email-service');

// Provide mock implementations
const mockEmail = require('../../src/services/email-service');
mockEmail.send.mockResolvedValue({ success: true });

// In tests:
it('should send email after invoice generation', async () => {
  await generateInvoice(txn);
  expect(mockEmail.send).toHaveBeenCalledWith(expect.objectContaining({
    to: txn.customer.email,
  }));
});
```

### Test Utilities

Create helpers for common test setup:

```javascript
// tests/helpers.js
const createMockTransaction = (overrides = {}) => ({
  id: 'txn-uuid',
  date: new Date(),
  amount: 1000,
  currency: 'EUR',
  customer_id: 'cust-uuid',
  product_id: 'prod-uuid',
  status: 'PENDING',
  ...overrides,
});

const createMockInvoice = (overrides = {}) => ({
  id: 'inv-uuid',
  invoice_number: 'INV-2026-00001',
  ...overrides,
});

module.exports = { createMockTransaction, createMockInvoice };
```

## Integration Tests

### Database Test Fixtures

```javascript
// tests/fixtures/db.js
const db = require('../../src/config/database');

// Before each test: insert test data
beforeEach(async () => {
  await db.query('TRUNCATE customers CASCADE');
  await db.query(`
    INSERT INTO customers (id, name, email) VALUES
    ('cust-1', 'Acme Corp', 'billing@acme.com')
  `);
});

// After each test: cleanup
afterEach(async () => {
  await db.query('TRUNCATE customers CASCADE');
});
```

### API Integration Tests

```javascript
// tests/routes/invoices.integration.test.js
const request = require('supertest');
const app = require('../../src/app');
const db = require('../../src/config/database');

describe('POST /invoices', () => {
  beforeEach(async () => {
    // Setup test data
    await db.query('INSERT INTO transactions ...');
  });

  it('should generate invoice and return 202 Accepted', async () => {
    const res = await request(app)
      .post('/api/v1/invoices/generate')
      .set('Authorization', 'Bearer test-token')
      .send({
        transaction_id: 'txn-uuid',
        template_id: 'tmpl-uuid',
      });

    expect(res.status).toBe(202);
    expect(res.body.data.job_id).toBeDefined();
  });

  it('should fail with 404 if transaction not found', async () => {
    const res = await request(app)
      .post('/api/v1/invoices/generate')
      .set('Authorization', 'Bearer test-token')
      .send({
        transaction_id: 'non-existent',
      });

    expect(res.status).toBe(404);
    expect(res.body.error.code).toBe('TRANSACTION_NOT_FOUND');
  });
});
```

## Authentication Testing

### JWT Token Generation for Tests

```javascript
// tests/helpers/auth.js
const jwt = require('jsonwebtoken');

const createTestToken = (overrides = {}) => {
  const payload = {
    sub: 'test-user-uuid',
    roles: ['accountant'],
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + 3600,
    ...overrides,
  };
  return jwt.sign(payload, process.env.JWT_SECRET || 'test-secret');
};

const createAdminToken = () => createTestToken({ roles: ['admin'] });
const createViewerToken = () => createTestToken({ roles: ['viewer'] });

module.exports = { createTestToken, createAdminToken, createViewerToken };
```

### Role-Based Access Control Testing

```javascript
describe('Authorization', () => {
  it('should allow admin to view audit logs', async () => {
    const token = createAdminToken();
    const res = await request(app)
      .get('/api/v1/audit-logs')
      .set('Authorization', `Bearer ${token}`);

    expect(res.status).toBe(200);
  });

  it('should deny viewer access to audit logs', async () => {
    const token = createViewerToken();
    const res = await request(app)
      .get('/api/v1/audit-logs')
      .set('Authorization', `Bearer ${token}`);

    expect(res.status).toBe(403);
  });

  it('should deny unauthenticated access', async () => {
    const res = await request(app)
      .get('/api/v1/audit-logs');

    expect(res.status).toBe(401);
  });
});
```

## Queue & Worker Testing

### Bull Queue Testing

```javascript
// tests/services/queue.test.js
const Queue = require('bull');
const invoiceQueue = require('../../src/services/queue');

describe('Invoice Queue', () => {
  beforeEach(async () => {
    await invoiceQueue.clean(0, 'completed');
    await invoiceQueue.clean(0, 'failed');
  });

  afterEach(async () => {
    await invoiceQueue.close();
  });

  it('should enqueue job and track progress', async () => {
    const job = await invoiceQueue.add({
      transaction_ids: ['txn-1'],
    });

    expect(job.id).toBeDefined();
    expect(job.data.transaction_ids).toContain('txn-1');
  });

  it('should retry failed jobs', async () => {
    invoiceQueue.process(async () => {
      throw new Error('Temporary failure');
    });

    const job = await invoiceQueue.add({ transaction_ids: ['txn-1'] });

    // Wait for retry
    await new Promise(resolve => setTimeout(resolve, 3000));

    const updatedJob = await invoiceQueue.getJob(job.id);
    expect(updatedJob.attemptsMade).toBeGreaterThan(0);
  });
});
```

## Error Handling Testing

### Exception Testing

```javascript
describe('Error Handling', () => {
  it('should catch and log database errors', async () => {
    const mockDb = jest.mock('../../src/config/database');
    mockDb.query.mockRejectedValue(new Error('Connection timeout'));

    const res = await request(app)
      .get('/api/v1/invoices');

    expect(res.status).toBe(500);
    expect(res.body.error.code).toBe('DATABASE_ERROR');
    expect(logger.error).toHaveBeenCalled();
  });

  it('should return 422 for business rule violations', async () => {
    // Try to mark an already-paid invoice as draft
    const res = await request(app)
      .patch('/api/v1/invoices/inv-uuid')
      .set('Authorization', `Bearer ${token}`)
      .send({ status: 'DRAFT' });

    expect(res.status).toBe(422);
    expect(res.body.error.code).toBe('INVALID_STATE_TRANSITION');
  });
});
```

## Data Validation Testing

### Input Validation

```javascript
describe('Input Validation', () => {
  it('should reject invalid email', async () => {
    const res = await request(app)
      .post('/api/v1/customers')
      .set('Authorization', `Bearer ${token}`)
      .send({
        name: 'Test',
        email: 'not-an-email',
      });

    expect(res.status).toBe(400);
    expect(res.body.error.details).toContainEqual(
      expect.objectContaining({
        field: 'email',
        message: expect.stringContaining('valid email'),
      })
    );
  });

  it('should reject negative amount', async () => {
    const res = await request(app)
      .post('/api/v1/transactions')
      .set('Authorization', `Bearer ${token}`)
      .send({
        amount: -100,
        currency: 'EUR',
      });

    expect(res.status).toBe(400);
  });

  it('should reject future date', async () => {
    const futureDate = new Date();
    futureDate.setDate(futureDate.getDate() + 1);

    const res = await request(app)
      .post('/api/v1/transactions')
      .set('Authorization', `Bearer ${token}`)
      .send({
        date: futureDate.toISOString(),
      });

    expect(res.status).toBe(400);
  });
});
```

## Performance Testing

### Load Testing (Jest + Artillery)

```bash
# artillery run tests/performance/invoice-generation.yml
```

```yaml
# tests/performance/invoice-generation.yml
config:
  target: 'http://localhost:3000'
  phases:
    - duration: 60
      arrivalRate: 10
      name: 'Ramp-up'
    - duration: 300
      arrivalRate: 10
      name: 'Sustained'
scenarios:
  - name: 'Generate Invoice Batch'
    flow:
      - post:
          url: '/api/v1/invoices/generate'
          headers:
            Authorization: 'Bearer {{ token }}'
          json:
            transaction_ids: ['txn-1', 'txn-2']
```

## Test Organization

```
tests/
├── unit/
│   ├── services/
│   │   ├── invoice-generator.test.js
│   │   ├── email-service.test.js
│   │   └── queue.test.js
│   ├── utils/
│   │   ├── validators.test.js
│   │   └── formatters.test.js
│   └── middleware/
│       ├── auth.test.js
│       └── errorHandler.test.js
├── integration/
│   ├── routes/
│   │   ├── invoices.integration.test.js
│   │   ├── transactions.integration.test.js
│   │   └── auth.integration.test.js
│   └── database/
│       ├── migrations.test.js
│       └── constraints.test.js
├── e2e/
│   ├── invoice-generation-flow.test.js
│   └── batch-processing.test.js
├── fixtures/
│   ├── db.js
│   ├── data.js
│   └── mocks.js
└── helpers/
    ├── auth.js
    ├── request.js
    └── setup.js
```

## Running Tests

```bash
# Unit tests only
npm run test:unit

# Integration tests only
npm run test:integration

# All tests
npm run test

# With coverage
npm run test:coverage

# Watch mode
npm run test:watch

# Performance tests
npm run test:perf
```

---

**Version**: 1.0  
**Status**: Active  
**Last Updated**: 2026-04-26
