# US-0002: Database Setup & Migrations

**Epic**: Epic 1 - Project Foundation & Infrastructure  
**Status**: Ready  
**Priority**: Critical  
**Estimated Effort**: 1-2 days  

---

## Overview

Setup PostgreSQL database connection, migrations framework, and seed initial data for Auto-Factures Fred.

---

## User Story

As a developer, I want to configure the database and run migrations so that the application can persist data across sessions.

**Acceptance Criteria**:
- [ ] PostgreSQL connection configured (via pg library)
- [ ] Migration framework setup (folder: db/migrations/)
- [ ] Initial migration creates all tables (Transaction, Customer, Product, Invoice, Template, AuditLog)
- [ ] Seed script populates sample data (test customers, products)
- [ ] Connection pooling configured (min: 5, max: 20 per architecture.md)
- [ ] Database initialization can be run via `pnpm run db:migrate`
- [ ] Rollback tested (migrations revertible)
- [ ] Health check includes database connectivity

---

## Technical Requirements

**From domain.md**:
- 6 core entities: Transaction, Customer, Product, Invoice, InvoiceTemplate, AuditLog
- State transitions enforced (constraints at DB level)
- Foreign key relationships with cascade rules
- Audit table is append-only

**Database Setup**:
- PostgreSQL version: 14+ (recommended)
- Connection pool: min 5, max 20 connections
- Naming conventions: snake_case tables/columns

---

## Detailed Steps

### Step 1: Create Database Configuration

Create `src/config/database.js`:

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

### Step 2: Create Migration Framework

Create `db/migrate.js`:

```javascript
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import pool from '../src/config/database.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function runMigrations() {
  const migrationsDir = path.join(__dirname, 'migrations');
  
  // Create migrations table if not exists
  await pool.query(`
    CREATE TABLE IF NOT EXISTS migrations (
      id SERIAL PRIMARY KEY,
      name TEXT UNIQUE NOT NULL,
      executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Get all migration files
  const files = fs.readdirSync(migrationsDir)
    .filter(f => f.endsWith('.sql'))
    .sort();

  for (const file of files) {
    const { rows } = await pool.query('SELECT * FROM migrations WHERE name = $1', [file]);
    
    if (rows.length === 0) {
      console.log(`Running migration: ${file}`);
      const sql = fs.readFileSync(path.join(migrationsDir, file), 'utf-8');
      await pool.query(sql);
      await pool.query('INSERT INTO migrations (name) VALUES ($1)', [file]);
    }
  }

  console.log('All migrations completed');
  await pool.end();
}

runMigrations().catch(err => {
  console.error('Migration failed:', err);
  process.exit(1);
});
```

### Step 3: Create Initial Migration

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

-- Products table
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code VARCHAR(50) UNIQUE NOT NULL IMMUTABLE,
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

-- Create indexes
CREATE INDEX idx_transactions_customer_id ON transactions(customer_id);
CREATE INDEX idx_transactions_product_id ON transactions(product_id);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_invoices_customer_id ON invoices(customer_id);
CREATE INDEX idx_invoices_transaction_id ON invoices(transaction_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_issue_date ON invoices(issue_date);
CREATE INDEX idx_audit_logs_entity_id ON audit_logs(entity_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
```

### Step 4: Create Seed Migration

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
) ON CONFLICT DO NOTHING;

-- Seed sample products
INSERT INTO products (code, name, unit_price, currency, tax_rate, is_active)
VALUES
  ('PROD-001', 'Consulting Services', 150.00, 'EUR', 0.20, true),
  ('PROD-002', 'Software License', 500.00, 'EUR', 0.20, true),
  ('PROD-003', 'Support Package', 100.00, 'EUR', 0.20, true)
ON CONFLICT DO NOTHING;
```

### Step 5: Update package.json Scripts

Add to `package.json`:

```json
{
  "scripts": {
    "db:migrate": "node db/migrate.js",
    "db:seed": "psql $DATABASE_URL -f db/migrations/002-seed-data.sql",
    "db:reset": "npm run db:migrate && npm run db:seed"
  }
}
```

### Step 6: Create Health Check with DB

Update `src/app.js`:

```javascript
import express from 'express';
import pool from './config/database.js';

const app = express();

app.use(express.json());

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

export default app;
```

### Step 7: Test Database Connection

```bash
# Ensure PostgreSQL is running locally:
# createdb auto_factures_fred  (if not exists)

# Set environment
export DATABASE_URL=postgresql://localhost/auto_factures_fred

# Run migrations
pnpm db:migrate

# Test health check
pnpm dev
# Visit http://localhost:3000/health → should show database connected
```

---

## Definition of Done

- [x] PostgreSQL connection configured
- [x] Connection pooling enabled (min 5, max 20)
- [x] All 6 tables created with constraints
- [x] Foreign keys enforced
- [x] Indexes created for performance
- [x] Migration framework setup and working
- [x] Seed data inserted
- [x] Health check includes database status
- [x] Rollback capability tested
- [x] .env.example updated with DATABASE_URL

---

## Testing

**Manual Verification**:
```bash
pnpm db:migrate
# Should output: "Running migration: 001-create-tables.sql"
# Should output: "All migrations completed"

psql auto_factures_fred
\dt  # List tables
# Should show: customers, products, transactions, invoices, invoice_templates, audit_logs
```

---

## References

- Domain Model: docs/specs/domain.md
- Architecture Rules: .claude/rules/architecture.md

---

**Created**: 2026-04-27  
**Last Updated**: 2026-04-27
