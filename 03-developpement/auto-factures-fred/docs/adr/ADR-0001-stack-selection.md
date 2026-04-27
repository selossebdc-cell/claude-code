# ADR-0001: Technology Stack Selection

**Date**: 2026-04-26  
**Status**: Proposed  
**Deciders**: Architecture Team  
**Decision**: Select Node.js/Express + PostgreSQL + Puppeteer for Auto-Factures Fred V1

## Context

Auto-Factures Fred requires an automated invoicing system with the following constraints:
- Fast invoice generation (<1 minute per batch of 100)
- High reliability (no transaction loss)
- Easy integration with existing workflows
- Scalable to 10x current volume
- Audit compliance (7-year record retention)

The team evaluated three technology stacks:

### Option A: Node.js + Express + PostgreSQL (Selected)
- Lightweight, fast HTTP server
- Easy JSON API development
- Proven for batch processing
- Rich npm ecosystem (validation, PDF, email)

### Option B: Python + FastAPI + PostgreSQL
- Good for data processing
- Excellent PDF libraries
- Slower startup for serverless deployments
- More verbose for simple CRUD operations

### Option C: .NET + SQL Server
- Enterprise-grade stability
- More infrastructure overhead
- Licensing costs
- Overkill for current scale

## Decision

**We select Option A: Node.js + Express + PostgreSQL**

### Rationale

1. **Performance**: Node.js event-driven architecture ideal for I/O-bound invoice operations
2. **Development Velocity**: Express simplifies REST API implementation; rich npm ecosystem
3. **Cost**: Open-source stack, minimal infrastructure overhead
4. **Scalability**: Horizontal scaling proven; PostgreSQL handles concurrent writes
5. **Familiarity**: Team experience with JavaScript/Node.js
6. **Ecosystem**:
   - Express for HTTP routing
   - Puppeteer for PDF generation
   - Nodemailer for email delivery
   - Joi for validation
   - Pino for structured logging
   - Jest for testing

### Database Choice: PostgreSQL

- **ACID transactions**: Prevents invoice duplication/loss
- **JSON support**: Flexible metadata storage
- **Proven**: Used in financial systems globally
- **Audit**: Native support for audit trails via table inheritance or triggers
- **Compatibility**: Works with all ORM/query builders

## Consequences

### Positive
- ✓ Fast development cycle
- ✓ Minimal operational overhead
- ✓ Easy to onboard new developers (JavaScript knowledge widespread)
- ✓ Excellent testing ecosystem (Jest, Supertest)
- ✓ Good monitoring/observability (Pino logging)

### Negative
- ✗ Single-threaded (Node.js) requires careful async/await management
- ✗ Memory usage scaling (large batches require clustering or queue-based processing)
- ✗ PDF generation via Puppeteer not ideal for extreme scale (headless browser overhead)

### Mitigations

1. **Memory/Scale**: Implement bull-queue for async batch processing
2. **Async/Await**: Code review standards, linting rules (no floating promises)
3. **PDF Performance**: Cache template rendering; consider alternative (like html2pdf) if bottleneck emerges

## Alternative Mitigation: PDF Generation

If Puppeteer becomes a bottleneck in production (>1000 invoices/batch):

**Alternative Option**: 
- Replace Puppeteer with html2pdf library (lighter) OR
- Offload PDF to external service (AWS Lambda, third-party PDF API)

Decision deferred until metrics show bottleneck.

## Dependencies

### Hard Dependencies
- Node.js 20.x (LTS) or 22.x
- PostgreSQL 14+ (tested with 15)
- npm 10.x+

### Soft Dependencies
- SMTP server for email (third-party or local)
- Docker (optional, for containerization)

## Verification Checklist

- [ ] Express version 4.21.2 verified via npm
- [ ] PostgreSQL version constraints documented
- [ ] Puppeteer tested for PDF rendering quality
- [ ] Email configuration tested (SMTP)
- [ ] Batch processing performance benchmarked (<1 min for 100 invoices)
- [ ] Async/await patterns validated in code review

## Related Decisions

- **ADR-0002**: Database schema design (transaction normalization)
- **ADR-0003**: Async batch processing with message queue
- **ADR-0004**: Logging and monitoring strategy
- **ADR-0005**: Security and authentication (JWT vs API keys)

## References

- Node.js LTS Release Schedule: https://nodejs.org/en/about/releases/
- PostgreSQL Stability: https://www.postgresql.org/support/versioning/
- Express.js Performance: https://expressjs.com/

---

**Decision Owner**: Architecture Lead  
**Review Date**: 2026-06-26 (before production deployment)
