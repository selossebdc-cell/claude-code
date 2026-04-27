# API Specification — Auto-Factures Fred

## Overview

RESTful API for the Auto-Factures Fred invoicing system. All endpoints require standard HTTP methods and return JSON responses.

**API Version**: 1.0  
**Base URL**: `/api/v1`  
**Content Type**: `application/json`

## Authentication

All endpoints require either:
1. Bearer token in Authorization header: `Authorization: Bearer {jwt_token}`
2. API key in header: `X-API-Key: {api_key}`

Status code: 401 Unauthorized if missing/invalid.

## Response Format

### Success Response (2xx)

```json
{
  "success": true,
  "data": { /* resource data */ },
  "meta": {
    "timestamp": "2026-04-26T10:30:00Z",
    "requestId": "req-uuid"
  }
}
```

### Error Response (4xx, 5xx)

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "amount",
        "message": "must be greater than 0"
      }
    ]
  },
  "meta": {
    "timestamp": "2026-04-26T10:30:00Z",
    "requestId": "req-uuid"
  }
}
```

## Endpoints

### Transactions

#### POST /transactions
Create a new transaction that triggers invoice generation.

**Request**:
```json
{
  "date": "2026-04-26T10:00:00Z",
  "amount": 1500.50,
  "currency": "EUR",
  "customer_id": "uuid",
  "product_id": "uuid",
  "metadata": {
    "order_id": "ORD-123",
    "description": "Service delivery Q2 2026"
  }
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "data": {
    "id": "txn-uuid",
    "date": "2026-04-26T10:00:00Z",
    "amount": 1500.50,
    "currency": "EUR",
    "customer_id": "uuid",
    "product_id": "uuid",
    "status": "PENDING",
    "created_at": "2026-04-26T10:30:00Z"
  }
}
```

**Errors**:
- 400: Invalid amount, currency, or date format
- 404: Customer or product not found
- 422: Business rule violation (e.g., customer inactive)

---

#### GET /transactions/{id}
Retrieve a specific transaction.

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": "txn-uuid",
    "date": "2026-04-26T10:00:00Z",
    "amount": 1500.50,
    "currency": "EUR",
    "customer_id": "uuid",
    "product_id": "uuid",
    "status": "PROCESSED",
    "created_at": "2026-04-26T10:30:00Z"
  }
}
```

---

#### GET /transactions
List transactions with pagination and filters.

**Query Parameters**:
```
?status=PROCESSED&customer_id=uuid&limit=20&offset=0
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    { /* transaction */ },
    { /* transaction */ }
  ],
  "meta": {
    "total": 150,
    "limit": 20,
    "offset": 0,
    "hasMore": true
  }
}
```

### Invoices

#### POST /invoices/generate
Generate an invoice from a transaction (or batch).

**Request** (single):
```json
{
  "transaction_id": "txn-uuid",
  "template_id": "template-uuid" (optional, uses default if omitted)
}
```

**Request** (batch):
```json
{
  "transaction_ids": ["txn-uuid-1", "txn-uuid-2"],
  "template_id": "template-uuid" (optional)
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "invoices": [
      {
        "id": "inv-uuid",
        "invoice_number": "INV-2026-00001",
        "transaction_id": "txn-uuid",
        "customer_id": "cust-uuid",
        "total_amount": 1500.50,
        "currency": "EUR",
        "status": "DRAFT",
        "pdf_url": "/api/v1/invoices/inv-uuid/pdf",
        "created_at": "2026-04-26T10:30:00Z"
      }
    ],
    "processed": 1,
    "failed": 0
  }
}
```

**Errors**:
- 400: Invalid transaction_id or template_id
- 404: Transaction or template not found
- 422: Business rule violation (customer inactive, duplicate invoice, etc.)

---

#### GET /invoices/{id}
Retrieve a specific invoice.

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": "inv-uuid",
    "invoice_number": "INV-2026-00001",
    "customer_id": "cust-uuid",
    "issue_date": "2026-04-26",
    "due_date": "2026-05-26",
    "total_amount": 1500.50,
    "currency": "EUR",
    "status": "ISSUED",
    "template_id": "template-uuid",
    "pdf_url": "/api/v1/invoices/inv-uuid/pdf",
    "email_sent_date": "2026-04-26T11:00:00Z",
    "created_at": "2026-04-26T10:30:00Z",
    "updated_at": "2026-04-26T11:00:00Z"
  }
}
```

---

#### GET /invoices/{id}/pdf
Download invoice as PDF.

**Response** (200 OK): Binary PDF file with headers:
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="INV-2026-00001.pdf"
```

---

#### PATCH /invoices/{id}
Update an invoice (status, template, etc.). Only DRAFT invoices can be modified.

**Request**:
```json
{
  "status": "ISSUED",
  "template_id": "new-template-uuid" (optional)
}
```

**Response** (200 OK): Updated invoice object.

**Errors**:
- 400: Cannot modify DRAFT invoice when locked
- 409: Invoice already ISSUED or later state

---

#### POST /invoices/{id}/send-email
Send invoice to customer via email.

**Request**:
```json
{
  "recipient_email": "customer@example.com" (optional, uses customer's email if omitted),
  "message": "Please find your invoice attached" (optional)
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": "inv-uuid",
    "status": "SENT",
    "email_sent_date": "2026-04-26T11:00:00Z"
  }
}
```

**Errors**:
- 400: Invalid email address
- 503: Email service unavailable (transient, retry-safe)

---

#### GET /invoices
List invoices with pagination and filters.

**Query Parameters**:
```
?status=ISSUED&customer_id=uuid&from_date=2026-04-01&to_date=2026-04-30&limit=20&offset=0
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": [ /* array of invoices */ ],
  "meta": {
    "total": 250,
    "limit": 20,
    "offset": 0,
    "hasMore": true
  }
}
```

### Customers

#### POST /customers
Create a new customer.

**Request**:
```json
{
  "name": "Acme Corp",
  "email": "billing@acme.com",
  "billing_address": "123 Main St, City, Country",
  "tax_id": "FR12345678901",
  "payment_terms": "NET_30"
}
```

**Response** (201 Created): Customer object with auto-generated ID.

---

#### GET /customers/{id}
Retrieve a customer.

**Response** (200 OK): Customer object.

---

#### PATCH /customers/{id}
Update customer details.

**Request**:
```json
{
  "payment_terms": "NET_60",
  "is_active": true
}
```

**Response** (200 OK): Updated customer object.

---

#### GET /customers
List customers.

**Query Parameters**:
```
?is_active=true&limit=20&offset=0
```

### Products

#### POST /products
Create a new product.

**Request**:
```json
{
  "code": "SVC-001",
  "name": "Consulting Service",
  "description": "Professional consulting services",
  "unit_price": 150.00,
  "currency": "EUR",
  "tax_rate": 0.20
}
```

**Response** (201 Created): Product object.

---

#### GET /products/{id}
Retrieve a product.

---

#### PATCH /products/{id}
Update product (except code and currency).

---

#### GET /products
List active products.

### Templates

#### POST /templates
Create an invoice template.

**Request**:
```json
{
  "name": "Standard Invoice",
  "description": "Default template for invoices",
  "html_template": "<html>...<div>Invoice #{{invoice_number}}</div>...</html>",
  "css_styles": "body { font-family: Arial; }",
  "logo_url": "https://example.com/logo.png",
  "footer_text": "Thank you for your business",
  "is_default": false
}
```

**Response** (201 Created): Template object.

---

#### GET /templates/{id}
Retrieve a template.

---

#### PATCH /templates/{id}
Update template.

---

#### GET /templates
List templates.

### Audit & Reporting

#### GET /audit-logs
Retrieve audit trail.

**Query Parameters**:
```
?entity_type=Invoice&entity_id=inv-uuid&action=EMAIL_SENT&limit=100
```

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": "log-uuid",
      "entity_type": "Invoice",
      "entity_id": "inv-uuid",
      "action": "EMAIL_SENT",
      "timestamp": "2026-04-26T11:00:00Z",
      "user_id": "user-uuid",
      "old_values": null,
      "new_values": { "email_sent_date": "2026-04-26T11:00:00Z" }
    }
  ],
  "meta": { "total": 50 }
}
```

---

#### GET /reports/revenue-summary
Business intelligence endpoint.

**Query Parameters**:
```
?from_date=2026-04-01&to_date=2026-04-30&group_by=customer
```

**Response**:
```json
{
  "success": true,
  "data": {
    "period": "2026-04-01 to 2026-04-30",
    "total_revenue": 45000.00,
    "invoice_count": 32,
    "by_customer": [
      { "customer_id": "uuid", "name": "Acme Corp", "total": 15000.00 }
    ]
  }
}
```

## HTTP Status Codes

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Successful GET, PATCH |
| 201 | Created | Successful POST |
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | State conflict (e.g., can't modify issued invoice) |
| 422 | Unprocessable Entity | Business rule violation |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Error | Server error |
| 503 | Service Unavailable | Temporary (email service down, etc.) |

## Rate Limiting

All endpoints limited to:
- **1000 requests per hour** per API key
- **10 requests per second** per IP

Response includes:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1698321600
```

## Pagination

List endpoints use cursor-based pagination:
```
?limit=20&offset=0
```

Response metadata:
```json
{
  "meta": {
    "total": 500,
    "limit": 20,
    "offset": 0,
    "hasMore": true
  }
}
```

## Sorting

List endpoints support sorting:
```
?sort=created_at:desc,name:asc
```

---

**Version**: 1.0  
**Status**: Draft  
**Last Updated**: 2026-04-26
