# Epics — Auto-Factures Fred V1

**Version**: v1  
**Planning Phase**: 2026-04-27  
**Status**: In Planning  

---

## Overview

This document defines the top-level epics that structure the Auto-Factures Fred V1 implementation. Each epic groups related user stories and serves as a planning horizon for development sprints.

---

## Epic 1: Project Foundation & Infrastructure

**Description**: Establish project structure, tooling, and infrastructure to support development.

**Scope**:
- Project initialization (package.json, build tools, dev dependencies)
- Configuration management (env files, secrets handling)
- Database setup (PostgreSQL, migrations framework)
- Monitoring & logging infrastructure (Pino, application health)
- Testing framework setup (Jest, test utilities)

**Type**: Architecture / Infrastructure  
**Priority**: Critical (Blocking all development)  
**Estimated Effort**: 3-5 days  

**Acceptance Criteria**:
- [ ] Project builds successfully (pnpm build)
- [ ] All tests pass (pnpm test)
- [ ] Database migrations can run (init + sample data)
- [ ] Logging works in all environments (dev, staging, prod)
- [ ] Pre-commit hooks prevent accidental commits of secrets

**Related ADRs**: ADR-0001 (Stack Selection)

**User Stories**:
- US-E1-001: Initialize Node.js project with Express
- US-E1-002: Configure database with PostgreSQL
- US-E1-003: Setup testing framework (Jest)
- US-E1-004: Implement logging with Pino
- US-E1-005: Configure environment management

---

## Epic 2: Core Domain Implementation

**Description**: Implement the core domain entities (Transaction, Customer, Product, Invoice) and their persistence layer.

**Scope**:
- Database schema for all core entities
- Entity models and validators
- Migration scripts for schema creation
- Domain business logic (invoice numbering, status transitions)
- Audit logging infrastructure

**Type**: Domain / Data Layer  
**Priority**: Critical (Required for all invoice operations)  
**Estimated Effort**: 5-7 days  

**Acceptance Criteria**:
- [ ] All 6 entities modeled and persisted (Transaction, Invoice, Customer, Product, Template, AuditLog)
- [ ] Business rules enforced at database level (constraints, triggers)
- [ ] Invoice numbering works correctly (INV-2026-XXXXX format)
- [ ] Status transitions validated and tested
- [ ] Audit log captures all changes
- [ ] All domain validations pass test suite (>90% coverage)

**Related ADRs**: ADR-0003 (Authentication Strategy includes RBAC for audit)

**User Stories**:
- US-E2-001: Create Transaction entity and persistence
- US-E2-002: Create Customer entity and persistence
- US-E2-003: Create Product entity and persistence
- US-E2-004: Create Invoice entity and persistence
- US-E2-005: Create InvoiceTemplate entity and persistence
- US-E2-006: Implement AuditLog (append-only)
- US-E2-007: Implement invoice numbering logic
- US-E2-008: Implement domain validators

---

## Epic 3: Invoice Generation Engine

**Description**: Implement the core invoice generation process, from transaction to PDF.

**Scope**:
- Invoice generation service (calculate tax, apply business rules)
- Template rendering engine
- PDF generation via Puppeteer
- Batch processing orchestration (Bull queue)
- Error handling and retry logic

**Type**: Processing / Business Logic  
**Priority**: Critical (Core feature)  
**Estimated Effort**: 7-10 days  

**Acceptance Criteria**:
- [ ] Single invoice generation completes <500ms
- [ ] Batch processing (100 invoices) completes <1 minute
- [ ] Tax calculation correct for all products
- [ ] PDF generated with correct template rendering
- [ ] Failed invoices retry up to 3 times, then alert
- [ ] Queue maintains FIFO ordering
- [ ] Concurrent processing limit (5 workers) enforced

**Related ADRs**: ADR-0002 (Async Batch Processing)

**User Stories**:
- US-E3-001: Implement invoice generation service
- US-E3-002: Implement tax calculation
- US-E3-003: Implement PDF generation (Puppeteer)
- US-E3-004: Implement Bull queue integration
- US-E3-005: Implement batch processing orchestration
- US-E3-006: Implement error handling and retry logic

---

## Epic 4: REST API Layer

**Description**: Build the REST API endpoints for all invoice operations.

**Scope**:
- CRUD endpoints for transactions, customers, products
- Invoice generation endpoints (single + batch)
- Invoice retrieval and filtering
- Report endpoints (audit logs, statistics)
- API validation (Joi schemas)
- Error handling and response formatting

**Type**: API / Integration  
**Priority**: High (Required for frontend + integrations)  
**Estimated Effort**: 5-7 days  

**Acceptance Criteria**:
- [ ] All 25+ endpoints implemented per api.md
- [ ] All endpoints require authentication (JWT)
- [ ] Response format standardized (success, data, error, meta)
- [ ] Pagination implemented (limit/offset)
- [ ] Rate limiting enforced (if applicable)
- [ ] OpenAPI/Swagger documentation generated
- [ ] API integration tests >80% coverage

**Related ADRs**: ADR-0003 (Authentication Strategy)

**User Stories**:
- US-E4-001: Implement transaction endpoints (CRUD)
- US-E4-002: Implement customer endpoints (CRUD)
- US-E4-003: Implement product endpoints (CRUD)
- US-E4-004: Implement invoice generation endpoints
- US-E4-005: Implement invoice retrieval endpoints
- US-E4-006: Implement audit log endpoints
- US-E4-007: Implement pagination and filtering
- US-E4-008: Implement API error handling

---

## Epic 5: Authentication & Authorization

**Description**: Implement JWT-based authentication and role-based access control (RBAC).

**Scope**:
- JWT token generation and validation
- Login endpoint and token refresh
- Role-based access control (admin, accountant, viewer)
- Password management (hashing, complexity validation)
- Session management and token expiration
- Authorization middleware

**Type**: Security / Cross-cutting  
**Priority**: Critical (All APIs require auth)  
**Estimated Effort**: 3-5 days  

**Acceptance Criteria**:
- [ ] JWT tokens issued with 15m expiration (access) + 30d refresh
- [ ] Token validation on all protected endpoints
- [ ] Role-based access enforced (admin > accountant > viewer)
- [ ] Login endpoint tested with valid/invalid credentials
- [ ] Refresh token logic prevents token reuse
- [ ] Authorization tests >90% coverage
- [ ] No passwords in logs or error messages

**Related ADRs**: ADR-0003 (Authentication Strategy)

**User Stories**:
- US-E5-001: Implement JWT token generation
- US-E5-002: Implement token validation middleware
- US-E5-003: Implement login endpoint
- US-E5-004: Implement refresh token endpoint
- US-E5-005: Implement role-based access control
- US-E5-006: Implement password hashing

---

## Epic 6: Email Delivery & Notifications

**Description**: Implement email delivery system for invoice notifications.

**Scope**:
- Email service integration (Nodemailer)
- Email template management
- Batch email sending via queue
- Delivery tracking and retries
- Email formatting (HTML + plain text)
- Unsubscribe/preference management

**Type**: Delivery / External Integration  
**Priority**: High (Customer communication)  
**Estimated Effort**: 3-4 days  

**Acceptance Criteria**:
- [ ] Emails sent via Nodemailer (SMTP configured)
- [ ] Email templates support personalization
- [ ] Batch email processing via queue (non-blocking)
- [ ] Failed email delivery retried up to 3 times
- [ ] Audit log tracks email send events
- [ ] Email tests validate template rendering

**Related ADRs**: ADR-0002 (Async Batch Processing)

**User Stories**:
- US-E6-001: Implement email service (Nodemailer)
- US-E6-002: Implement email templates
- US-E6-003: Implement email queue integration
- US-E6-004: Implement delivery tracking
- US-E6-005: Implement retry logic for failed sends

---

## Epic 7: Monitoring, Observability & Operations

**Description**: Implement operational tooling for monitoring, debugging, and system health.

**Scope**:
- Application health checks
- Metrics collection (throughput, latency, error rate)
- Log aggregation and searching
- Alert management
- Dashboard for system status
- Performance profiling

**Type**: Operations / Non-functional  
**Priority**: Medium (Important for production support)  
**Estimated Effort**: 4-6 days  

**Acceptance Criteria**:
- [ ] Health check endpoint returns system status
- [ ] Key metrics exposed (invoice generation rate, queue depth)
- [ ] Structured logging captures all important events
- [ ] Alerts fired for error rate >5%, queue depth >1000
- [ ] Performance profiling identifies slow queries
- [ ] Operational runbook created

**Related ADRs**: All (cross-cutting concern)

**User Stories**:
- US-E7-001: Implement health check endpoint
- US-E7-002: Implement metrics collection (Pino structured logs)
- US-E7-003: Implement alert thresholds
- US-E7-004: Implement performance monitoring
- US-E7-005: Create operational runbook

---

## Epic 8: Testing & Quality Assurance

**Description**: Implement comprehensive testing across all layers.

**Scope**:
- Unit tests (services, utils, domain models)
- Integration tests (API endpoints, database)
- End-to-end tests (full invoice workflow)
- Performance tests (batch throughput, PDF generation)
- Test fixtures and helpers
- Coverage reporting

**Type**: Quality / Cross-cutting  
**Priority**: High (Required for all features)  
**Estimated Effort**: Ongoing (parallel with development)  

**Acceptance Criteria**:
- [ ] Unit test coverage >85% (services, utils)
- [ ] Integration test coverage >80% (API routes)
- [ ] Critical path coverage >95% (invoice generation, auth)
- [ ] E2E tests for main workflow (transaction → invoice → email)
- [ ] Performance tests validate SLAs (1 minute per 100 invoices)
- [ ] All tests pass on CI/CD pipeline

**Related Documentation**: .claude/rules/testing.md

**User Stories**:
- US-E8-001: Implement unit test framework and utilities
- US-E8-002: Implement integration test framework
- US-E8-003: Implement E2E test suite
- US-E8-004: Implement performance tests
- US-E8-005: Setup coverage reporting

---

## Epic Ordering & Dependencies

```
1. Epic 1 (Foundation) → All others depend on this
   ↓
2. Epic 2 (Domain) ← Must exist before any operations
   ↓
3. Parallel: Epic 3 (Generation), Epic 5 (Auth), Epic 6 (Email)
   ↓
4. Epic 4 (API) ← Needs both generation and auth ready
   ↓
5. Epic 7 (Monitoring), Epic 8 (Testing) ← Throughout development

Sprint Suggested Order:
- Sprint 1: Epic 1 + Epic 2
- Sprint 2: Epic 3 + Epic 5
- Sprint 3: Epic 4 + Epic 6
- Sprint 4: Epic 7 + Epic 8 (final polish & deployment prep)
```

---

**Version**: 1.0  
**Status**: Draft - Ready for Planning Sprint  
**Next Step**: Decompose each epic into User Stories (US-XXXX) and Tasks (TASK-XXXX)
