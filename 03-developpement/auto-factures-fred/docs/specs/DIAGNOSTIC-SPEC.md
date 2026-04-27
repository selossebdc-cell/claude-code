# Diagnostic Specification — Auto-Factures Fred

**Phase**: MODEL (Comprehensive diagnostic from requirements)  
**Version**: 1.0  
**Date**: 2026-04-26  
**Status**: Draft

---

## Executive Summary

Auto-Factures Fred is a greenfield invoicing automation platform designed to eliminate manual invoice generation overhead. The specification encompasses 4 system layers (data, processing, delivery, integration), 6 core entities (Transaction, Invoice, Customer, Product, Template, Audit), 3 architectural decision records (stack, async processing, authentication), and comprehensive validation/testing rules.

This diagnostic provides:
1. **Adaptive diagnostic prompt** (9 implicit blocks for system context)
2. **Enriched metadata schema** (pain points, patterns, opportunities)
3. **Strategic synthesis** (guide for implementation)

---

## Part 1: Adaptive Diagnostic Prompt

### Block 1: System Intention & Vision
"Auto-Factures Fred eliminates manual invoice generation. Current state: batch invoicing 1-2 hours/day, manual errors 5-10%, no audit trail. Target state: <1 minute per 100 invoices, zero errors, complete audit compliance."

### Block 2: Core Process Model
"Process: Transaction (PENDING) → Validation → Invoice (DRAFT) → Rendering → PDF → Email → Transaction (PROCESSED). Critical path duration: <1 minute for batch of 100. Batch processing via Bull queue (5 concurrent workers). Idempotent invoice numbering."

### Block 3: Data & State Model
"Entities: Transaction (source), Invoice (output), Customer, Product, Template, AuditLog. Immutability: Transactions frozen after PROCESSED. Invoice status transitions: DRAFT → ISSUED → SENT → PAID → ARCHIVED. No deletes (soft deletes via status field)."

### Block 4: Integration Boundaries
"External systems: SMTP email service (async), PDF generation (Puppeteer headless), external ERP (future phase). Data flows: Inbound transactions (batch/API), outbound invoices (PDF archive, email notifications). Idempotency key: transaction_id (no duplicates)."

### Block 5: Quality & Non-Functional Requirements
"Performance: Batch throughput 100 invoices/min, response time <200ms (single invoice lookup). Availability: 99% uptime business hours. Data consistency: ACID transactions. Audit: 7-year retention. Security: JWT auth, role-based access (viewer/accountant/admin)."

### Block 6: Error Handling & Resilience
"Transient failures: Exponential backoff retry (2s → 4s → 8s). Permanent failures: Dead letter queue, admin alert. Missing data: Validate before queuing (fail-fast at API). Resource exhaustion: Queue depth monitoring, circuit breaker for email service. Graceful degradation: Fall back to synchronous if Redis unavailable."

### Block 7: Deployment & Operations
"Environments: dev → staging → production (blue-green). Database: PostgreSQL 15+ with migrations. Infrastructure: Container-ready (Docker), horizontal scaling (stateless API). Monitoring: Prometheus metrics, error rate alerts. Backup: Daily snapshots, 30-day retention."

### Block 8: Evolution & Future
"Phase 1 (current): Core invoice generation, basic API. Phase 2: Real-time progress (WebSocket), advanced filtering, payment tracking. Phase 3: Multi-tenant isolation, SaaS pricing, external OAuth2 integrations."

### Block 9: Success Criteria & Validation
"Acceptance: Manual testing → Integration tests (80%+ coverage) → E2E batch processing → Performance baseline. Sign-off: Operations validation (uptime, backup restore, disaster recovery). Rollback plan: Blue-green switch in <5 minutes."

---

## Part 2: Enriched Metadata Schema

### Pain Points Analysis

| Category | Pain Point | Severity | Current Solution | Proposed Solution |
|----------|-----------|----------|------------------|-------------------|
| **Manual Effort** | Invoice generation 1-2 hours/day | Critical | Spreadsheet + copy-paste | Automated batch generation |
| **Data Quality** | Human errors (5-10% invoices) | Critical | Manual reviews | Input validation + template constraints |
| **Audit Trail** | No record of who did what when | High | Paper logs (untrustable) | Immutable database audit table |
| **Scalability** | Adding invoices → adding staff | High | Hire more accountants | Horizontal scaling (Bull workers) |
| **Integration** | Disparate systems (ERP, email) | Medium | Manual data entry | REST API + SMTP integration |
| **Tax Compliance** | 7-year retention burden | Medium | Manual file management | Database with automated backup |

### Architectural Patterns

| Pattern | Rationale | Implementation |
|---------|-----------|-----------------|
| **Async-by-Default** | Long operations (PDF, email) block API | Bull queue + worker pool |
| **Immutable Audit Log** | Tax compliance requires forensics | Append-only audit table |
| **Idempotent Operations** | Network retries shouldn't create duplicates | Idempotency key via transaction_id |
| **Graceful Degradation** | Partial failures shouldn't crash entire system | Transient retry + DLQ for permanent failures |
| **ACID Transactions** | Financial data requires consistency | Database-level constraints |
| **Horizontal Scalability** | Growth to 10x volume requires scale-out | Stateless API + managed Redis |

### Opportunities

| Opportunity | Impact | Timeline | Effort |
|-------------|--------|----------|--------|
| **Real-time Progress** | Users see batch status live (WebSocket) | Phase 2 | Medium |
| **Smart Templates** | Auto-select template by customer/product | Phase 2 | Low |
| **Payment Integration** | Track payment status per invoice | Phase 2 | High |
| **Tax Calculations** | Auto-compute tax by region | Phase 2 | Medium |
| **SaaS Model** | Multi-tenant isolation + per-org storage | Phase 3 | High |
| **External Integrations** | OAuth2 with QuickBooks, Xero | Phase 3 | High |
| **Analytics Dashboard** | Revenue trends, customer insights | Phase 2 | Medium |

---

## Part 3: Strategic Synthesis

### Technology Stack Rationale

**Why Node.js + Express + PostgreSQL?**

The chosen stack balances three competing constraints:

1. **Speed**: Event-driven Node.js ideal for I/O-bound operations (network requests, file I/O)
2. **Cost**: Open-source, minimal infrastructure overhead, easy to horizontally scale
3. **Familiarity**: JavaScript widely known, rich ecosystem (express, puppeteer, nodemailer)

**Alternative stacks considered and rejected**:
- Python/FastAPI: Better for data processing, but slower API startup (critical for serverless)
- .NET: Overkill for current scale, licensing costs
- Go: Fast, but steeper learning curve

### Async Processing Architecture

**Why Bull Queue instead of synchronous processing?**

The 1-minute SLA for batch of 100 invoices requires careful optimization:

- **Synchronous**: 100 × 15s (Puppeteer PDF) = 25 minutes ❌
- **Async + workers**: Enqueue in 100ms, process parallel = <2 minutes ✓

By returning 202 (Accepted) immediately and processing async, we decouple client from server performance.

**Trade-off**: Eventual consistency (invoice status updated async, not immediate).

### Security Strategy

**JWT + Role-Based Access Control**

Three roles with explicit permissions:

- `viewer`: Read-only access (reporting, dashboards)
- `accountant`: Full invoice operations (create, send, archive)
- `admin`: System management (users, audit logs, config)

**Token lifecycle**:
- Access token: 15 minutes (short-lived, frequent refresh)
- Refresh token: 30 days (long-lived, enables user persistence)

This approach is stateless (no session store) and scales horizontally.

### Data Model Philosophy

**Immutability First, Deletion Last**

The data model follows financial auditing best practices:

- Transactions never modified (frozen after PROCESSED)
- Invoices use status transitions (never deleted in DRAFT state)
- Audit log is append-only (no UPDATE/DELETE)
- Tax calculations stored in invoice (not recalculated later)

This prevents historical revisions and ensures reproducibility.

### Implementation Roadmap

#### Phase 1 (Current): Core Platform
- [ ] API (transactions, invoices, customers, products, templates)
- [ ] Invoice generation + PDF rendering
- [ ] Email delivery (async via Bull)
- [ ] Audit logging
- [ ] Authentication (JWT)
- [ ] Test coverage >80%

**Validation**: Manual testing + batch processing load test

#### Phase 2: Intelligence & Scale
- [ ] Real-time progress (WebSocket)
- [ ] Advanced filtering & reporting
- [ ] Smart templates (auto-selection)
- [ ] Payment tracking
- [ ] Analytics dashboard
- [ ] Horizontal scaling (Kubernetes)

**Validation**: Performance under 10x load

#### Phase 3: Enterprise & Integration
- [ ] Multi-tenant isolation
- [ ] SaaS pricing model
- [ ] OAuth2 external integrations (QuickBooks, Xero)
- [ ] Advanced tax calculation
- [ ] White-label support

**Validation**: Security audit, SOC2 certification

### Critical Success Factors

1. **Database Design**: Foreign keys + check constraints prevent invalid states at DB level
2. **Error Handling**: Structured logging + alerting enable fast incident response
3. **Testing**: >80% coverage + integration tests prevent regressions
4. **Documentation**: API spec, ADRs, architecture rules enable team alignment
5. **Monitoring**: Key metrics (queue depth, error rate, latency) detect issues early

### Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| **PDF generation bottleneck** | Medium | High | Implement html2pdf fallback, offload to Lambda |
| **Database connection exhaustion** | Low | High | Connection pooling (min 5, max 20), monitoring |
| **Email delivery failures** | Medium | Medium | Exponential backoff, DLQ for manual recovery |
| **Redis unavailability** | Low | Medium | Fall back to synchronous mode (degraded) |
| **Data loss in transaction** | Very Low | Critical | ACID constraints, daily backups, automated restore testing |
| **Security breach (auth bypass)** | Low | Critical | Code review, penetration testing, OAuth2 audit |

---

## Part 4: Implementation Guide

### For the Architect (ADR Author)

Focus on:
1. ✓ Technology choices rationale (why Node.js, why PostgreSQL)
2. ✓ Scalability story (how to handle 10x growth)
3. ✓ Resilience patterns (retry, circuit breaker, graceful degradation)
4. ✓ Security model (auth, data protection, audit)

Avoid:
1. ✗ Implementation details (those belong in code)
2. ✗ Changing decisions based on "what's trending"
3. ✗ Over-engineering (YAGNI principle)

### For the Developer (Code Implementation)

Follow:
1. ✓ API spec in `docs/specs/api.md` (contract first)
2. ✓ Architecture rules in `.claude/rules/architecture.md` (style guide)
3. ✓ ADRs in `docs/adr/` (decision context)
4. ✓ Domain model in `docs/specs/domain.md` (entity relationships)

Never:
1. ✗ Invent requirements not in spec
2. ✗ Skip error handling
3. ✗ Commit secrets (.env files)
4. ✗ Leave TODOs without a task

### For QA (Testing & Validation)

Test against:
1. ✓ System spec (Block 1-3: does it do what it's supposed to?)
2. ✓ API spec (Block 4: does it integrate correctly?)
3. ✓ Quality attributes (Block 5: does it meet performance/security SLAs?)
4. ✓ Error scenarios (Block 6: does it fail gracefully?)

---

## Part 5: Document Cross-References

| Document | Purpose | Owner | Review Cadence |
|----------|---------|-------|-----------------|
| `docs/specs/system.md` | Architecture overview | Architect | Quarterly |
| `docs/specs/domain.md` | Entity model & business rules | PM + Architect | Quarterly |
| `docs/specs/api.md` | API contract | Architect | Before each release |
| `docs/specs/stack-reference.md` | Dependency versions | DevOps | Monthly |
| `docs/adr/ADR-000X.md` | Decision rationale | Decision Owner | Once (immutable) |
| `.claude/rules/architecture.md` | Coding standards | Tech Lead | Quarterly |
| `.claude/rules/testing.md` | Test requirements | QA Lead | Quarterly |
| `DIAGNOSTIC-SPEC.md` | This document | Architect | At phase milestones |

---

## Conclusion

The Auto-Factures Fred specification balances three critical dimensions:

1. **Speed to Market**: Greenfield, focused scope, clear acceptance criteria
2. **Operational Excellence**: ACID database, audit trails, monitoring
3. **Future Readiness**: Horizontal scaling, async patterns, clear phase gates

Success depends on rigorous adherence to specifications (no "but the user said..."), comprehensive testing (>80% coverage), and proactive monitoring (detect issues before users do).

**Next Step**: Proceed to PLAN phase (create epics/user stories) using this diagnostic as context.

---

**Diagnostic Author**: Architecture Lead  
**Approval Date**: 2026-04-26  
**Review Date**: 2026-06-26 (post-Phase 1 validation)
