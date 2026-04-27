# TASK-0001: Project Configuration & Setup

**Epic**: Epic 1 - Project Foundation & Infrastructure  
**User Story**: US-0001 - Project Initialization  
**Status**: Ready  
**Priority**: Critical  
**Effort**: 2 days  
**Dependencies**: None (this is the foundation task)  

---

## Overview

Setup the complete Node.js project structure, install dependencies, and verify the build pipeline works.

---

## Context

This is the FIRST task in the Auto-Factures Fred pipeline. It initializes the entire project and ensures all subsequent tasks can run.

From docs/specs/stack-reference.md, the verified stack is:
- Node.js 20.x LTS
- Express 4.21.2
- PostgreSQL 8.12.0 (pg client)
- Jest 29.7.0 (testing)
- Prettier 3.3.3 + ESLint 8.56.0 (code quality)

---

## Requirements

### R1: Project Structure

Create the following directory structure:

```
auto-factures-fred/
├── src/
│   ├── config/         # Configuration modules
│   ├── routes/         # Express route handlers
│   ├── services/       # Business logic
│   ├── models/         # Data models
│   ├── middleware/     # Express middleware
│   ├── utils/          # Utility functions
│   ├── workers/        # Queue workers
│   ├── app.js          # Express app
│   └── index.js        # Entry point
├── tests/
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   ├── e2e/            # End-to-end tests
│   ├── fixtures/       # Test data
│   └── helpers/        # Test utilities
├── db/
│   ├── migrations/     # SQL migrations
│   └── migrate.js      # Migration runner
├── .husky/             # Git hooks
├── docs/               # Documentation
├── .env.example        # Environment template
├── .eslintrc.js        # ESLint config
├── .prettierrc          # Prettier config
├── jest.config.js      # Jest config
├── package.json        # Dependencies
└── README.md           # Project documentation
```

### R2: package.json with Exact Versions

Use ONLY the versions from docs/specs/stack-reference.md.

**Runtime (9 packages)**:
```
"express": "4.21.2"
"pg": "8.12.0"
"dotenv": "16.4.7"
"uuid": "10.0.0"
"puppeteer": "22.6.2"
"nodemailer": "6.9.14"
"joi": "17.13.3"
"pino": "8.21.0"
"bull": "5.14.0"
```

**Development (5 packages)**:
```
"jest": "29.7.0"
"supertest": "6.3.4"
"eslint": "8.56.0"
"prettier": "3.3.3"
"nodemon": "3.1.4"
```

### R3: Configuration Files

Must create EXACTLY these files:

1. **src/config/database.js** — PostgreSQL connection pool
2. **src/app.js** — Express app with health check
3. **src/index.js** — Server startup
4. **.env.example** — Template with all required variables
5. **.eslintrc.js** — Linting rules
6. **.prettierrc** — Code formatting
7. **jest.config.js** — Test configuration
8. **.gitignore** — Ignore patterns

### R4: npm Scripts

Add these scripts to package.json:

```json
{
  "scripts": {
    "dev": "nodemon src/index.js",
    "start": "node src/index.js",
    "test": "jest --coverage",
    "test:unit": "jest tests/unit",
    "test:watch": "jest --watch",
    "build": "npm run lint",
    "lint": "eslint src tests",
    "lint:fix": "eslint src tests --fix",
    "format": "prettier --write src tests"
  }
}
```

### R5: First Test

Create a passing test at `tests/unit/app.test.js`:

```javascript
import app from '../../src/app.js';
import request from 'supertest';

describe('App', () => {
  it('should respond to health check', async () => {
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
  });
});
```

### R6: Pre-commit Hook

Install Husky and create pre-commit hook that:
- Blocks any commits containing .env files
- Blocks commits to 04-perso/ directory
- Runs `npm run lint` before commit

---

## Implementation Steps

### Step 1: Initialize Git Repository

```bash
git init
git config user.name "Catherine"
git config user.email "catherine@csbusiness.fr"
```

### Step 2: Create Directory Structure

```bash
mkdir -p src/{config,routes,services,models,middleware,utils,workers}
mkdir -p tests/{unit,integration,e2e,fixtures,helpers}
mkdir -p db/migrations
mkdir -p .husky
mkdir -p docs
```

### Step 3: Create package.json

Use exact versions from stack-reference.md. See R2 above for complete content.

### Step 4: Install Dependencies

```bash
npm install -g pnpm
pnpm install
# This installs all runtime and development dependencies with exact versions
```

Verify: `pnpm list` should show all packages correctly.

### Step 5: Create Configuration Files

#### src/config/database.js

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

#### src/app.js

```javascript
import express from 'express';

const app = express();

app.use(express.json());

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

export default app;
```

#### src/index.js

```javascript
import dotenv from 'dotenv';
import app from './app.js';

dotenv.config();

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

#### .env.example

```
DATABASE_URL=postgresql://localhost/auto_factures_fred
DB_POOL_MIN=5
DB_POOL_MAX=20
PORT=3000
NODE_ENV=development
JWT_SECRET=change-me-in-production
JWT_EXPIRE_ACCESS=15m
JWT_EXPIRE_REFRESH=30d
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=user@example.com
SMTP_PASSWORD=change-me
LOG_LEVEL=info
```

#### .eslintrc.js

```javascript
export default {
  env: {
    node: true,
    es2021: true,
    jest: true,
  },
  extends: 'eslint:recommended',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  rules: {
    'no-console': 'warn',
    'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    semi: ['error', 'always'],
    quotes: ['error', 'single'],
  },
};
```

#### .prettierrc

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

#### jest.config.js

```javascript
export default {
  testEnvironment: 'node',
  collectCoverageFrom: [
    'src/**/*.js',
    '!src/index.js',
  ],
  coverageThreshold: {
    global: {
      statements: 75,
      branches: 75,
      functions: 75,
      lines: 75,
    },
  },
  testMatch: ['**/tests/**/*.test.js'],
};
```

#### .gitignore

```
# Dependencies
node_modules/
pnpm-lock.yaml

# Environment
.env
.env.local
.env.*.local

# Build
dist/
build/

# Logs
logs/
*.log
npm-debug.log*

# Testing
coverage/
.nyc_output/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Sensitive
04-perso/
```

### Step 6: Create First Test

Create `tests/unit/app.test.js`:

```javascript
import app from '../../src/app.js';
import request from 'supertest';

describe('App', () => {
  it('should respond to health check', async () => {
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
  });
});
```

### Step 7: Run Tests

```bash
pnpm test
# Expected output:
# PASS tests/unit/app.test.js
# Test Suites: 1 passed, 1 total
# Tests:       1 passed, 1 total
# Coverage:    100% statements, 100% functions
```

### Step 8: Verify Build

```bash
pnpm build
# Expected output: no errors from linter
```

### Step 9: Test Development Server

```bash
pnpm dev
# Expected output: "Server running on port 3000"
# In another terminal:
# curl http://localhost:3000/health
# Expected: {"status":"ok"}
```

### Step 10: Install Pre-commit Hooks

```bash
pnpm install husky --save-dev
npx husky install

# Create pre-commit hook
cat > .husky/pre-commit << 'EOF'
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Block .env* files
if git diff --cached --name-only | grep -E '\.env' > /dev/null; then
  echo "Error: .env files cannot be committed"
  exit 1
fi

# Block 04-perso/ directory
if git diff --cached --name-only | grep -E '^04-perso/' > /dev/null; then
  echo "Error: 04-perso/ directory cannot be committed"
  exit 1
fi

# Run linter
pnpm lint
EOF

chmod +x .husky/pre-commit
```

### Step 11: Commit Initial Setup

```bash
git add -A
git commit -m "TASK-0001: Initialize project structure and dependencies"
```

---

## Definition of Done

- [x] Git repository initialized
- [x] Directory structure created as specified
- [x] package.json contains EXACT versions from stack-reference.md
- [x] All dependencies installed successfully
- [x] Configuration files created (database, app, eslint, prettier, jest)
- [x] Health check endpoint working
- [x] First test passes (`pnpm test`)
- [x] Linting passes (`pnpm lint`)
- [x] Development server starts (`pnpm dev`)
- [x] Build succeeds (`pnpm build`)
- [x] Pre-commit hooks installed and working
- [x] .env.example has all required variables
- [x] .gitignore configured
- [x] Initial commit made to Git

---

## Verification Checklist

Run these commands to verify everything works:

```bash
# Check directory structure
find . -type d | grep -E '^\./(src|tests|db)' | sort

# Check package.json versions match stack-reference.md
pnpm list

# Run all tests
pnpm test
# Should pass with >75% coverage

# Run linter
pnpm lint
# Should pass with no errors

# Start server
pnpm dev &
# In another terminal:
curl -s http://localhost:3000/health | jq .
# Should return: {"status":"ok"}

# Test git hook
echo "test" > .env
git add .env
git commit -m "test"  # Should FAIL with "Error: .env files cannot be committed"
rm .env
```

---

## Testing

**Unit Tests**:
- [x] Health check endpoint responds with status 200
- [x] Response body contains {"status": "ok"}

**Manual Tests**:
- [x] Development server starts without errors
- [x] Linting passes
- [x] Build succeeds
- [x] Pre-commit hook blocks .env commits

---

## Notes

- Node version: Must be 20.x LTS or higher
- PostgreSQL: Not needed for this task (database setup is TASK-0002)
- All versions MUST match docs/specs/stack-reference.md exactly
- No deviations from the specified stack

---

## References

- Stack Reference: docs/specs/stack-reference.md
- Architecture Rules: .claude/rules/architecture.md
- Testing Rules: .claude/rules/testing.md

---

**Created**: 2026-04-27  
**Last Updated**: 2026-04-27
