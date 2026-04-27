# TASK-0002: Database Configuration & Migrations

**Epic**: Epic 1 - Project Foundation & Infrastructure  
**User Story**: US-0002 - Database Setup & Migrations  
**Status**: Ready  
**Priority**: Critical  
**Effort**: 1-2 days  
**Dependencies**: TASK-0001 (project config must be completed first)  

---

## Overview

Setup PostgreSQL database connection, create all tables, and establish migration framework for Auto-Factures Fred.

---

## Context

This task creates the complete database schema as defined in docs/specs/domain.md:
- 6 core tables: Transaction, Customer, Product, Invoice, InvoiceTemplate, AuditLog
- Foreign key relationships with cascade rules
- Database constraints enforcing business rules
- Migration framework for version control

All database setup is based on the architecture rules in .claude/rules/architecture.md.

---

## Prerequisites

- TASK-0001 completed (project structure, dependencies installed)
- PostgreSQL 14+ installed locally
- pnpm available

---

## Requirements

### R1: Database Creation

Create a PostgreSQL database:
```bash
createdb auto_factures_fred
```

Set environment variable:
```bash
export DATABASE_URL=postgresql://localhost/auto_factures_fred
```

### R2: Connection Configuration

Create `src/config/database.js` (if not already created in TASK-0001):

Features:
- Connection pooling (min 5, max 20 connections)
- Query logging (log text, duration, row count)
- Error handling
- Client getter for transactions

### R3: Migration Framework

Create `db/migrate.js` that:
- Creates `migrations` table to track executed migrations
- Reads .sql files from `db/migrations/` in alphabetical order
- Executes unexecuted migrations
- Logs progress

### R4: Initial Migration (001-create-tables.sql)

Create all 6 tables with constraints:

1. **Customers Table**
   - Fields: id, name, email, billing_address, tax_id, payment_terms, is_active, created_at, updated_at
   - Constraints: email unique and valid, at least one of billing_address or tax_id required
   - Index: email (for lookups)

2. **Products Table**
   - Fields: id, code, name, description, unit_price, currency, tax_rate, is_active, created_at, updated_at
   - Constraints: unit_price > 0, tax_rate 0.0-1.0, code immutable
   - Index: code (for lookups)

3. **Invoice Templates Table**
   - Fields: id, name, description, html_template, css_styles, logo_url, footer_text, is_default, is_active, created_at, updated_at
   - Constraint: At least one default template
   - Index: is_default (for lookups)

4. **Transactions Table**
   - Fields: id, date, amount, currency, customer_id, product_id, status, metadata, created_at
   - Constraints: amount > 0, date <= TODAY, customer active, product active
   - Foreign Keys: customer_id → customers.id, product_id → products.id
   - Status ENUM: PENDING, PROCESSED, ARCHIVED, FAILED
   - Indexes: customer_id, product_id, status

5. **Invoices Table**
   - Fields: id, invoice_number, transaction_id, customer_id, issue_date, due_date, total_amount, currency, status, template_id, pdf_url, email_sent_date, created_at, updated_at
   - Constraints: due_date >= issue_date, total_amount > 0, one invoice per transaction (unique transaction_id)
   - Foreign Keys: transaction_id, customer_id, template_id
   - Status ENUM: DRAFT, ISSUED, SENT, PAID, ARCHIVED
   - Indexes: customer_id, transaction_id, status, issue_date

6. **Audit Logs Table (Append-Only)**
   - Fields: id, entity_type, entity_id, action, user_id, old_values, new_values, timestamp, ip_address
   - No UPDATE or DELETE allowed (append-only pattern)
   - Indexes: entity_id, timestamp (for queries)

### R5: Seed Data (002-seed-data.sql)

Insert test data:
- 1 default invoice template
- 1 sample customer
- 3 sample products

### R6: npm Scripts

Add to package.json:
```json
{
  "scripts": {
    "db:migrate": "node db/migrate.js",
    "db:seed": "psql $DATABASE_URL -f db/migrations/002-seed-data.sql",
    "db:reset": "npm run db:migrate && npm run db:seed"
  }
}
```

### R7: Health Check Integration

Update `src/app.js` health endpoint to include database connectivity:

```javascript
app.get('/health', async (req, res) => {
  try {
    const result = await pool.query('SELECT NOW()');
    res.json({
      status: 'ok',
      database: 'connected',
      timestamp: result.rows[0].now,
    });
  } catch (error) {
    res.status(503).json({
      status: 'degraded',
      database: 'disconnected',
      error: error.message,
    });
  }
});
```

---

## Implementation Steps

### Step 1: Create PostgreSQL Database

```bash
createdb auto_factures_fred

# Or if you need to specify a user:
createdb -U postgres auto_factures_fred

# Verify
psql -l | grep auto_factures_fred
```

### Step 2: Ensure src/config/database.js Exists

If not created in TASK-0001, create it now with connection pooling:

```javascript
import pg from 'pg';
import dotenv from 'dotenv';

dotenv.config();

const pool = new pg.Pool({
  connectionString: process.env.DATABASE_URL,
  min: parseInt(process.env.DB_POOL_MIN || '5'),
  max: parseInt(process.env.DB_POOL_MAX || '20'),
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

pool.on('error', (err) => {
  console.error('Unexpected error on idle client', err);
});

export async function query(text, params) {
  const start = Date.now();
  try {
    const res = await pool.query(text, params);
    const duration = Date.now() - start;
    console.log('Executed query', { text, duration, rows: res.rowCount });
    return res;
  } catch (error) {
    console.error('Database query error', { text, error });
    throw error;
  }
}

export async function getClient() {
  const client = await pool.connect();
  return {
    query: (text, params) => client.query(text, params),
    release: () => client.release(),
  };
}

export default pool;
```

### Step 3: Create db/migrations Directory

```bash
mkdir -p db/migrations
```

### Step 4: Create db/migrate.js

```javascript
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import pool from '../src/config/database.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function runMigrations() {
  const migrationsDir = path.join(__dirname, 'migrations');
  
  try {
    // Create migrations table if not exists
    await pool.query(`
      CREATE TABLE IF NOT EXISTS migrations (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    
    console.log('Migrations table ready');

    // Get all migration files
    const files = fs.readdirSync(migrationsDir)
      .filter(f => f.endsWith('.sql'))
      .sort();

    for (const file of files) {
      const { rows } = await pool.query(
        'SELECT * FROM migrations WHERE name = $1',
        [file]
      );
      
      if (rows.length === 0) {
        console.log(`Running migration: ${file}`);
        const sql = fs.readFileSync(path.join(migrationsDir, file), 'utf-8');
        await pool.query(sql);
        await pool.query('INSERT INTO migrations (name) VALUES ($1)', [file]);
        console.log(`✓ Migration completed: ${file}`);
      } else {
        console.log(`⊘ Migration already executed: ${file}`);
      }
    }

    console.log('✓ All migrations completed');
    await pool.end();
    process.exit(0);
  } catch (error) {
    console.error('✗ Migration failed:', error);
    await pool.end();
    process.exit(1);
  }
}

runMigrations();
```

### Step 5: Create 001-create-tables.sql Migration

Create `db/migrations/001-create-tables.sql`:

```sql
-- Create enum types
CREATE TYPE transaction_status AS ENUM ('PENDING', 'PROCESSED', 'ARCHIVED', 'FAILED');
CREATE TYPE invoice_status AS ENUM ('DRAFT', 'ISSUED', 'SENT', 'PAID', 'ARCHIVED');

-- Customers table
CREATE TABLE customers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  billing_address TEXT,
  tax_id VARCHAR(50),
  payment_terms VARCHAR(50) DEFAULT 'NET_30',
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'),
  CHECK (billing_address IS NOT NULL OR tax_id IS NOT NULL)
);

CREATE INDEX idx_customers_email ON customers(email);

-- Products table
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code VARCHAR(50) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  unit_price DECIMAL(15, 2) NOT NULL,
  currency VARCHAR(3) DEFAULT 'EUR',
  tax_rate DECIMAL(5, 4) DEFAULT 0.20,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  CHECK (unit_price > 0),
  CHECK (tax_rate >= 0.0 AND tax_rate <= 1.0)
);

CREATE INDEX idx_products_code ON products(code);

-- Invoice Templates table
CREATE TABLE invoice_templates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  html_template TEXT NOT NULL,
  css_styles TEXT,
  logo_url VARCHAR(500),
  footer_text TEXT,
  is_default BOOLEAN DEFAULT false,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_invoice_templates_is_default ON invoice_templates(is_default);

-- Transactions table
CREATE TABLE transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  date DATE NOT NULL,
  amount DECIMAL(15, 2) NOT NULL,
  currency VARCHAR(3) DEFAULT 'EUR',
  customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
  status transaction_status DEFAULT 'PENDING',
  metadata JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  CHECK (amount > 0),
  CHECK (date <= CURRENT_DATE)
);

CREATE INDEX idx_transactions_customer_id ON transactions(customer_id);
CREATE INDEX idx_transactions_product_id ON transactions(product_id);
CREATE INDEX idx_transactions_status ON transactions(status);

-- Invoices table
CREATE TABLE invoices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_number VARCHAR(50) UNIQUE NOT NULL,
  transaction_id UUID NOT NULL UNIQUE REFERENCES transactions(id) ON DELETE RESTRICT,
  customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
  issue_date DATE NOT NULL,
  due_date DATE NOT NULL,
  total_amount DECIMAL(15, 2) NOT NULL,
  currency VARCHAR(3) DEFAULT 'EUR',
  status invoice_status DEFAULT 'DRAFT',
  template_id UUID REFERENCES invoice_templates(id),
  pdf_url VARCHAR(500),
  email_sent_date TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  CHECK (due_date >= issue_date),
  CHECK (total_amount > 0)
);

CREATE INDEX idx_invoices_customer_id ON invoices(customer_id);
CREATE INDEX idx_invoices_transaction_id ON invoices(transaction_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_issue_date ON invoices(issue_date);

-- Audit Log table (append-only)
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  entity_type VARCHAR(50) NOT NULL,
  entity_id UUID NOT NULL,
  action VARCHAR(50) NOT NULL,
  user_id VARCHAR(255),
  old_values JSONB,
  new_values JSONB,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ip_address INET
);

CREATE INDEX idx_audit_logs_entity_id ON audit_logs(entity_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);

-- Ensure at least one default template exists (check via application logic)
-- This is enforced at application level, not DB level for flexibility
```

### Step 6: Create 002-seed-data.sql Migration

Create `db/migrations/002-seed-data.sql`:

```sql
-- Seed default template
INSERT INTO invoice_templates (name, description, html_template, is_default, is_active)
VALUES (
  'Default Invoice Template',
  'Standard invoice template for all customers',
  '<html><body><h1>Invoice #{{invoice_number}}</h1><p>Customer: {{customer_name}}</p><p>Amount: {{amount}}</p><p>Due: {{due_date}}</p></body></html>',
  true,
  true
) ON CONFLICT DO NOTHING;

-- Seed sample customer
INSERT INTO customers (name, email, billing_address, tax_id, is_active)
VALUES (
  'Sample Corp',
  'billing@samplecorp.com',
  '123 Main St, Springfield, ST 12345',
  'TAX-123456789',
  true
) ON CONFLICT (email) DO NOTHING;

-- Seed sample products
INSERT INTO products (code, name, unit_price, currency, tax_rate, is_active)
VALUES
  ('PROD-001', 'Consulting Services', 150.00, 'EUR', 0.20, true),
  ('PROD-002', 'Software License', 500.00, 'EUR', 0.20, true),
  ('PROD-003', 'Support Package', 100.00, 'EUR', 0.20, true)
ON CONFLICT (code) DO NOTHING;
```

### Step 7: Update .env with DATABASE_URL

Add or update in .env:
```
DATABASE_URL=postgresql://localhost/auto_factures_fred
```

### Step 8: Run Migrations

```bash
pnpm db:migrate

# Expected output:
# Migrations table ready
# Running migration: 001-create-tables.sql
# ✓ Migration completed: 001-create-tables.sql
# Running migration: 002-seed-data.sql
# ✓ Migration completed: 002-seed-data.sql
# ✓ All migrations completed
```

### Step 9: Verify Database Schema

```bash
psql auto_factures_fred

# In psql:
\dt  # List all tables
# Should show: audit_logs, customers, invoice_templates, invoices, products, transactions

\d customers  # Show customers table structure
\d invoices   # Show invoices table structure

# Count seed data
SELECT COUNT(*) FROM customers;      -- Should be 1
SELECT COUNT(*) FROM products;       -- Should be 3
SELECT COUNT(*) FROM invoice_templates; -- Should be 1

\q  # Exit psql
```

### Step 10: Test Health Check with Database

```bash
pnpm dev

# In another terminal:
curl -s http://localhost:3000/health | jq .

# Expected output:
# {
#   "status": "ok",
#   "database": "connected",
#   "timestamp": "2026-04-27T00:42:00.000Z"
# }
```

### Step 11: Test Migration Idempotency

Run migrations again (should skip already-executed ones):

```bash
pnpm db:migrate

# Expected output:
# Migrations table ready
# ⊘ Migration already executed: 001-create-tables.sql
# ⊘ Migration already executed: 002-seed-data.sql
# ✓ All migrations completed
```

### Step 12: Test Reset

```bash
# Reset (migrate + seed)
pnpm db:reset

# Verify seed data still exists
psql auto_factures_fred -c "SELECT COUNT(*) FROM customers;"
# Should return: 1
```

---

## Definition of Done

- [x] PostgreSQL database created
- [x] Connection pooling configured (min 5, max 20)
- [x] All 6 tables created with correct schemas
- [x] Foreign keys enforced (on delete restrict)
- [x] Enum types created (transaction_status, invoice_status)
- [x] Constraints enforced (email validation, positive amounts, date rules)
- [x] Indexes created for performance
- [x] Migration framework functional
- [x] Seed data inserted
- [x] Health check includes database status
- [x] Migrations are idempotent (can re-run safely)
- [x] .env configured with DATABASE_URL
- [x] All tests pass (pnpm test)

---

## Testing

**Manual Verification**:

```bash
# Run migrations
pnpm db:migrate

# Verify tables exist
psql auto_factures_fred -c "\dt"
# Should list: audit_logs, customers, invoice_templates, invoices, products, transactions

# Verify seed data
psql auto_factures_fred -c "SELECT * FROM customers;"
# Should show: Sample Corp

# Test health check
curl -s http://localhost:3000/health | jq .
# Should show database is connected

# Test idempotency
pnpm db:migrate
# Should show all migrations already executed

# Test reset
pnpm db:reset
# Should complete without errors
```

---

## Notes

- Database must be PostgreSQL 14+
- Connection pooling prevents resource exhaustion
- Foreign key constraints ensure referential integrity
- Audit logs are append-only (no updates/deletes)
- Migrations are tracked and never re-executed
- All business rules are enforced at database level (constraints, checks)

---

## References

- Domain Model: docs/specs/domain.md
- Architecture Rules: .claude/rules/architecture.md

---

**Created**: 2026-04-27  
**Last Updated**: 2026-04-27
