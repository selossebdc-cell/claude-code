# Domain Model — Auto-Factures Fred

## Overview

The Auto-Factures Fred domain model defines the core business entities, their relationships, and the rules governing invoice generation and management.

**Evolution Mode**: Greenfield (V1)

## Core Entities

### Transaction
Represents a business transaction that triggers invoice generation.

```
Transaction
├── id (UUID)
├── date (DateTime)
├── amount (Decimal)
├── currency (String, e.g., "EUR")
├── customer_id (FK → Customer)
├── product_id (FK → Product)
├── status (ENUM: PENDING, PROCESSED, ARCHIVED)
├── metadata (JSON)
└── created_at (DateTime)
```

**Rules**:
- Transaction amount must be positive
- Date cannot be in the future
- Customer and product must exist and be active
- Status transitions: PENDING → PROCESSED → ARCHIVED (unidirectional)

### Invoice
The generated invoice document.

```
Invoice
├── id (UUID)
├── invoice_number (String, unique)
├── transaction_id (FK → Transaction)
├── customer_id (FK → Customer)
├── issue_date (Date)
├── due_date (Date)
├── total_amount (Decimal)
├── currency (String)
├── status (ENUM: DRAFT, ISSUED, SENT, PAID, ARCHIVED)
├── template_id (FK → InvoiceTemplate)
├── pdf_url (String)
├── email_sent_date (DateTime, nullable)
├── created_at (DateTime)
└── updated_at (DateTime)
```

**Rules**:
- Due date must be ≥ issue date
- Invoice number must follow organization's numbering scheme
- Only DRAFT invoices can be modified
- Status transitions: DRAFT → ISSUED → SENT → PAID → ARCHIVED
- One invoice per transaction (no duplicates)

### Customer
Represents a business customer.

```
Customer
├── id (UUID)
├── name (String)
├── email (String, unique)
├── billing_address (String)
├── tax_id (String, optional)
├── payment_terms (String, e.g., "NET_30")
├── is_active (Boolean)
├── created_at (DateTime)
└── updated_at (DateTime)
```

**Rules**:
- Email must be valid and unique
- At least one of billing_address or tax_id must be provided
- Only active customers can have new invoices created

### Product
Represents a product or service being invoiced.

```
Product
├── id (UUID)
├── code (String, unique)
├── name (String)
├── description (String, optional)
├── unit_price (Decimal)
├── currency (String)
├── tax_rate (Decimal, 0.0 to 1.0)
├── is_active (Boolean)
├── created_at (DateTime)
└── updated_at (DateTime)
```

**Rules**:
- Unit price must be positive
- Tax rate must be between 0.0 and 1.0
- Only active products can be invoiced
- Code must be unique and immutable

### InvoiceTemplate
Defines how invoices are formatted and rendered.

```
InvoiceTemplate
├── id (UUID)
├── name (String)
├── description (String)
├── html_template (Text)
├── css_styles (Text, optional)
├── logo_url (String, optional)
├── footer_text (String, optional)
├── is_default (Boolean)
├── is_active (Boolean)
├── created_at (DateTime)
└── updated_at (DateTime)
```

**Rules**:
- At least one template must exist and be marked as default
- Template HTML must contain placeholders: {{invoice_number}}, {{customer_name}}, {{amount}}, {{due_date}}
- Only active templates can be used for new invoices

### AuditLog
Immutable record of all invoice operations.

```
AuditLog
├── id (UUID)
├── entity_type (String, e.g., "Invoice", "Transaction")
├── entity_id (UUID)
├── action (String, e.g., "CREATE", "UPDATE", "DELETE", "EMAIL_SENT")
├── user_id (String, optional)
├── old_values (JSON)
├── new_values (JSON)
├── timestamp (DateTime)
└── ip_address (String, optional)
```

**Rules**:
- All changes must be logged
- Old values only populated for updates
- Immutable after creation
- Retention: minimum 7 years (for tax compliance)

## Domain Processes

### Invoice Generation Process

```
Transaction (PENDING)
    ↓
[Validate Transaction Data]
    ↓ (success)
[Calculate Invoice Amount] (with tax)
    ↓
[Apply Business Rules]
  - Check customer is active
  - Check product is active
  - Validate payment terms
    ↓
[Generate Invoice Number] (using sequence)
    ↓
[Create Invoice Record] (status: DRAFT)
    ↓
[Render Invoice] (using template)
    ↓
[Generate PDF]
    ↓
[Mark Invoice as ISSUED]
    ↓ (optional)
[Send Email to Customer] (mark as SENT)
    ↓
[Update Transaction Status to PROCESSED]
```

### Business Rules

1. **Invoice Number Generation**
   - Format: `INV-{YEAR}-{SEQUENTIAL}`
   - Example: `INV-2026-00001`
   - Auto-increment sequence per year

2. **Tax Calculation**
   - Tax = Amount × Product.tax_rate
   - Total = Amount + Tax
   - Display both gross and net amounts

3. **Due Date Calculation**
   - Based on customer's payment_terms (e.g., NET_30)
   - Due date = issue_date + payment_terms_days

4. **Error Handling**
   - Invalid transaction → Mark transaction as FAILED, log error, alert admin
   - Customer inactive → Skip invoice generation, log warning
   - Template missing → Use default template
   - PDF generation failure → Retry up to 3 times, then alert admin

## Constraints & Validations

### Data Constraints
- Amount: Must be > 0, precision to 2 decimal places
- Currency: Must be ISO 4217 code
- Email: RFC 5322 compliant
- Tax rate: 0.0 ≤ rate ≤ 1.0

### Business Constraints
- No concurrent modifications to the same invoice
- Invoice deletion only allowed if status is DRAFT
- Audit log is append-only

## Relationships

```
Transaction (1) ──→ (1) Customer
Transaction (1) ──→ (1) Product
Transaction (1) ──→ (1) Invoice
Invoice (1) ──→ (1) Customer
Invoice (1) ──→ (1) InvoiceTemplate
Invoice (N) ←─── (1) AuditLog
Transaction (N) ←─── (1) AuditLog
```

## State Diagrams

### Invoice Lifecycle
```
DRAFT ──[ISSUE]──→ ISSUED ──[SEND]──→ SENT ──[PAY]──→ PAID ──[ARCHIVE]──→ ARCHIVED
                        ↓
                    ──[DELETE]──→ (destroyed)
```

### Transaction Lifecycle
```
PENDING ──[PROCESS]──→ PROCESSED ──[ARCHIVE]──→ ARCHIVED
   ↓
[FAIL]──→ FAILED (terminal state)
```

## Data Integrity Rules

1. **Referential Integrity**
   - All FK references must exist
   - Deleting a customer cascades to their invoices
   - Deleting a template prevents its future use

2. **Consistency**
   - Invoice.customer_id = Transaction.customer_id (after creation)
   - Invoice.total_amount = Calculated from Transaction + Tax
   - Exactly one invoice per transaction

3. **Immutability**
   - Transaction data cannot be modified after PROCESSED
   - Invoice number cannot be changed
   - Audit logs are permanent

---

**Version**: 1.0  
**Created**: 2026-04-26  
**Status**: Draft
