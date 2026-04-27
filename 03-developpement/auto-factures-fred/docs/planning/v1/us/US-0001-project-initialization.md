# US-0001: Project Initialization

**Epic**: Epic 1 - Project Foundation & Infrastructure  
**Status**: Ready  
**Priority**: Critical  
**Estimated Effort**: 2 days  

---

## Overview

Initialize a new Node.js + Express project with all required tooling, dependencies, and configuration infrastructure for Auto-Factures Fred V1 development.

---

## User Story

As a developer, I want to initialize the Node.js project with all necessary tooling so that I can begin development of the invoicing system.

**Acceptance Criteria**:
- [ ] package.json created with all runtime dependencies (exact versions from stack-reference.md)
- [ ] pnpm as package manager configured (pnpm install succeeds)
- [ ] Build tools configured (TypeScript compilation, if using; or equivalent)
- [ ] Development server runs (nodemon watching changes)
- [ ] .gitignore configured (excludes node_modules, .env*, logs)
- [ ] .env.example created with all required variables
- [ ] Pre-commit hook installed (blocks .env* and 04-perso/ commits)
- [ ] Project builds successfully (pnpm build)
- [ ] First test runs successfully (pnpm test)

---

## Technical Requirements

**Stack Reference**: docs/specs/stack-reference.md

**Runtime Dependencies**:
- express 4.21.2 (HTTP server)
- pg 8.12.0 (PostgreSQL client)
- dotenv 16.4.7 (Environment configuration)
- uuid 10.0.0 (ID generation)
- puppeteer 22.6.2 (PDF generation)
- nodemailer 6.9.14 (Email service)
- joi 17.13.3 (Validation)
- pino 8.21.0 (Structured logging)
- bull 5.14.0 (Queue processing) — if not already listed

**Development Dependencies**:
- jest 29.7.0 (Testing framework)
- supertest 6.3.4 (HTTP assertion)
- eslint 8.56.0 (Linting)
- prettier 3.3.3 (Code formatting)
- nodemon 3.1.4 (Development server)

---

## Detailed Steps

### Step 1: Create Project Structure

```bash
mkdir -p auto-factures-fred
cd auto-factures-fred

# Create directory structure
mkdir -p src/{routes,services,models,middleware,utils,workers,config}
mkdir -p tests/{unit,integration,e2e,fixtures,helpers}
mkdir -p docs/{specs,adr,planning}
```

### Step 2: Initialize package.json

Create `package.json` with exact versions from stack-reference.md.

```json
{
  "name": "auto-factures-fred",
  "version": "1.0.0",
  "description": "Automated invoicing system",
  "main": "src/index.js",
  "type": "module",
  "scripts": {
    "dev": "nodemon src/index.js",
    "build": "npm run lint",
    "start": "node src/index.js",
    "test": "jest --coverage",
    "test:watch": "jest --watch",
    "test:unit": "jest tests/unit",
    "test:integration": "jest tests/integration",
    "lint": "eslint src tests",
    "lint:fix": "eslint src tests --fix",
    "format": "prettier --write src tests"
  },
  "dependencies": {
    "express": "4.21.2",
    "pg": "8.12.0",
    "dotenv": "16.4.7",
    "uuid": "10.0.0",
    "puppeteer": "22.6.2",
    "nodemailer": "6.9.14",
    "joi": "17.13.3",
    "pino": "8.21.0",
    "bull": "5.14.0"
  },
  "devDependencies": {
    "jest": "29.7.0",
    "supertest": "6.3.4",
    "eslint": "8.56.0",
    "prettier": "3.3.3",
    "nodemon": "3.1.4"
  },
  "engines": {
    "node": ">=20.0.0"
  }
}
```

### Step 3: Install Dependencies

```bash
npm install -g pnpm  # Install pnpm globally if not present
pnpm install
```

Verify: `pnpm list` should show all dependencies correctly.

### Step 4: Create Configuration Files

#### .env.example

```
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/auto_factures_fred
DB_POOL_MIN=5
DB_POOL_MAX=20

# Server
PORT=3000
NODE_ENV=development

# JWT
JWT_SECRET=your-secret-key-change-in-production
JWT_EXPIRE_ACCESS=15m
JWT_EXPIRE_REFRESH=30d

# Email
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=user@example.com
SMTP_PASSWORD=password

# Logging
LOG_LEVEL=info
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

# Sensitive directories
04-perso/
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

### Step 5: Create Jest Configuration

Create `jest.config.js`:

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
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
};
```

### Step 6: Create Entry Point

Create `src/index.js`:

```javascript
import dotenv from 'dotenv';
import app from './app.js';

dotenv.config();

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### Step 7: Create Express App

Create `src/app.js`:

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

### Step 8: Create First Test

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

### Step 9: Install and Run Tests

```bash
pnpm install
pnpm test
# Should show: PASS tests/unit/app.test.js
```

### Step 10: Setup Pre-commit Hook

Create `.husky/pre-commit`:

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Block .env* files
if git diff --cached --name-only | grep -E '\.env' > /dev/null; then
  echo "Error: .env files cannot be committed"
  exit 1
fi

# Run linter
pnpm lint
```

Install Husky:

```bash
pnpm install husky --save-dev
npx husky install
chmod +x .husky/pre-commit
```

---

## Definition of Done

- [x] Repository structure created
- [x] All dependencies installed (exact versions from stack-reference.md)
- [x] Project builds without errors (`pnpm build`)
- [x] All tests pass (`pnpm test`)
- [x] Development server starts (`pnpm dev`)
- [x] Configuration template created (.env.example)
- [x] Linting and formatting configured
- [x] Pre-commit hooks prevent sensitive file commits
- [x] Git initialized and .gitignore configured
- [x] README created with setup instructions

---

## Testing

**Unit Tests**:
- [x] Health check endpoint responds with 200

**Manual Verification**:
```bash
pnpm dev
# Visit http://localhost:3000/health → should return {"status": "ok"}
```

---

## References

- Stack Reference: docs/specs/stack-reference.md
- Architecture Rules: .claude/rules/architecture.md
- Testing Rules: .claude/rules/testing.md

---

**Created**: 2026-04-27  
**Last Updated**: 2026-04-27
