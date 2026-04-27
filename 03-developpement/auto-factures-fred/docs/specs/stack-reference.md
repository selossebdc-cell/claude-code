# Stack Reference — Auto-Factures Fred

## Overview

This document defines the exact versions, dependencies, and configurations for the Auto-Factures Fred invoicing system. All subsequent specifications and development must reference the versions and configurations documented here.

**Last Verified**: 2026-04-26  
**Verification Status**: Preliminary (Core dependencies verified via npm registry)

## Runtime Dependencies

| Package | Version | Install Command | Source | Purpose |
|---------|---------|-----------------|--------|---------|
| express | 4.21.2 | `npm install express@4.21.2` | https://npmjs.com/package/express | HTTP API server framework |
| node | 20.x+ | N/A (runtime) | https://nodejs.org | Runtime environment |
| pg | 8.12.0 | `npm install pg@8.12.0` | https://npmjs.com/package/pg | PostgreSQL client |
| dotenv | 16.4.7 | `npm install dotenv@16.4.7` | https://npmjs.com/package/dotenv | Environment variable management |
| uuid | 10.0.0 | `npm install uuid@10.0.0` | https://npmjs.com/package/uuid | UUID generation for entities |
| puppeteer | 22.6.2 | `npm install puppeteer@22.6.2` | https://npmjs.com/package/puppeteer | PDF generation from HTML |
| nodemailer | 6.9.14 | `npm install nodemailer@6.9.14` | https://npmjs.com/package/nodemailer | Email delivery |
| joi | 17.13.3 | `npm install joi@17.13.3` | https://npmjs.com/package/joi | Data validation |
| pino | 8.21.0 | `npm install pino@8.21.0` | https://npmjs.com/package/pino | Structured logging |

## Development Dependencies

| Package | Version | Install Command | Purpose |
|---------|---------|-----------------|---------|
| jest | 29.7.0 | `npm install --save-dev jest@29.7.0` | Unit and integration testing |
| supertest | 6.3.4 | `npm install --save-dev supertest@6.3.4` | HTTP assertion library for API tests |
| eslint | 8.56.0 | `npm install --save-dev eslint@8.56.0` | Code linting |
| prettier | 3.3.3 | `npm install --save-dev prettier@3.3.3` | Code formatting |
| nodemon | 3.1.4 | `npm install --save-dev nodemon@3.1.4` | Development auto-reload |

## Core Configuration Files

### 1. Database Configuration (`db/config.js`)

**Technology**: PostgreSQL 15+

```javascript
// db/config.js
module.exports = {
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || 5432,
  database: process.env.DB_NAME || 'auto_factures_fred',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD,
  max: 20, // connection pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
};
```

**Schema**: See `schema.sql` for full DDL

### 2. Server Configuration (`config/server.js`)

```javascript
// config/server.js
module.exports = {
  port: process.env.PORT || 3000,
  environment: process.env.NODE_ENV || 'development',
  apiPrefix: '/api/v1',
  requestTimeout: 30000, // 30 seconds
  maxRequestBodySize: '10mb',
  cors: {
    origin: process.env.CORS_ORIGIN || 'http://localhost:3001',
    credentials: true,
  },
};
```

### 3. Email Configuration (`config/email.js`)

**Technology**: Nodemailer with SMTP

```javascript
// config/email.js
module.exports = {
  service: process.env.EMAIL_SERVICE || 'smtp',
  host: process.env.SMTP_HOST,
  port: process.env.SMTP_PORT || 587,
  secure: process.env.SMTP_SECURE === 'true', // TLS
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASSWORD,
  },
  from: process.env.EMAIL_FROM || 'noreply@auto-factures-fred.local',
  replyTo: process.env.EMAIL_REPLY_TO,
};
```

### 4. PDF Generation Configuration (`config/pdf.js`)

**Technology**: Puppeteer

```javascript
// config/pdf.js
module.exports = {
  headless: true,
  timeout: 30000, // 30 seconds per PDF
  format: 'A4',
  margin: {
    top: '20mm',
    bottom: '20mm',
    left: '15mm',
    right: '15mm',
  },
  printBackground: true,
  scale: 1,
  // Chrome launch options
  launchOptions: {
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-gpu',
    ],
  },
};
```

### 5. Logging Configuration (`config/logging.js`)

**Technology**: Pino

```javascript
// config/logging.js
const pino = require('pino');

module.exports = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: {
    target: 'pino-pretty',
    options: {
      colorize: true,
      translateTime: 'SYS:standard',
      ignore: 'pid,hostname',
    },
  },
});
```

### 6. Validation Schemas (`config/schemas.js`)

**Technology**: Joi

```javascript
// config/schemas.js (excerpt)
const joi = require('joi');

const transactionSchema = joi.object({
  date: joi.date().iso().required(),
  amount: joi.number().positive().precision(2).required(),
  currency: joi.string().length(3).uppercase().required(),
  customer_id: joi.string().uuid().required(),
  product_id: joi.string().uuid().required(),
  metadata: joi.object().optional(),
});

const invoiceSchema = joi.object({
  transaction_id: joi.string().uuid().required(),
  template_id: joi.string().uuid().optional(),
});

module.exports = { transactionSchema, invoiceSchema };
```

## Environment Variables

### Required (.env file - do NOT commit)

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=auto_factures_fred
DB_USER=postgres
DB_PASSWORD=<secure_password>

# Server
NODE_ENV=production
PORT=3000
API_PREFIX=/api/v1

# Email
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=<sender_email>
SMTP_PASSWORD=<secure_password>
EMAIL_FROM=noreply@auto-factures-fred.local

# Logging
LOG_LEVEL=info
```

## Compatibility Notes

### Version Constraints

- **Node.js**: 20.x or 22.x (LTS)
- **PostgreSQL**: 14+ (tested with 15)
- **Express 4.21**: Supports Node 18+
- **Puppeteer 22**: Requires Node 18+

### Breaking Changes & Migration Path

None applicable for V1 (greenfield project).

## Package Maintenance

### Regular Updates (Quarterly)
- Monitor security advisories: `npm audit`
- Update patch versions: `npm update`
- Test thoroughly in staging before promoting to production

### Major Version Upgrades (Biannually)
- Plan upgrades during planned maintenance windows
- Test against full test suite
- Update documentation accordingly

## Verification Summary

| Category | Count | Status |
|----------|-------|--------|
| Runtime packages verified | 8 | ✓ Complete |
| Dev packages verified | 5 | ✓ Complete |
| Configuration templates | 6 | ✓ Draft |
| Breaking changes documented | 0 | N/A (greenfield) |

---

**Status**: Draft  
**Next Steps**: Create sample `.env.example`, establish npm scripts in package.json
