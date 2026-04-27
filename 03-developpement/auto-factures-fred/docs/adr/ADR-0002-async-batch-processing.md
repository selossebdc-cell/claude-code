# ADR-0002: Asynchronous Batch Processing Architecture

**Date**: 2026-04-26  
**Status**: Proposed  
**Deciders**: Architecture Team  
**Decision**: Use Redis + Bull message queue for asynchronous invoice batch processing

## Context

Auto-Factures Fred must meet:
- **Throughput**: Process 100+ invoices per minute
- **Latency**: Complete batch within 1 minute
- **Reliability**: No lost transactions
- **Scalability**: Support growth to 1000+ invoices/batch

**Problem**: Synchronous HTTP request → PDF generation → Email is slow (10-20 seconds per invoice with Puppeteer).

If we process 100 invoices synchronously:
- Time: 100 × 15s = 25 minutes (violates 1-minute SLA)
- Risk: Long-running requests timeout

## Decision

**Implement asynchronous batch processing using Redis + Bull message queue**

### Architecture

```
API Request
    ↓
[Queue Job] → Redis Bull Queue → Job Status: "PENDING"
    ↓
Return immediately with Job ID (202 Accepted)
    ↓
[Worker Process] (separate thread/process)
    ├─ Fetch job from queue
    ├─ Generate PDF (Puppeteer)
    ├─ Send email (Nodemailer)
    ├─ Update database (Invoice status → SENT)
    └─ Mark job complete
    ↓
Client polls `/jobs/{jobId}` for status
```

### Components

1. **Job Queue** (Redis + Bull)
   - Stores pending jobs
   - Provides job status API
   - Automatic retry on failure
   - Job persistence

2. **Worker Process**
   - Dedicated Node.js worker pool
   - Processes jobs concurrently (configurable concurrency)
   - Handles failures gracefully
   - Logs all operations

3. **Status API**
   - Client can query job status
   - Provides progress metrics
   - WebSocket support for real-time updates (optional, Phase 2)

## Implementation Details

### Redis Configuration

```javascript
// config/redis.js
const Redis = require('ioredis');

const redis = new Redis({
  host: process.env.REDIS_HOST || 'localhost',
  port: process.env.REDIS_PORT || 6379,
  password: process.env.REDIS_PASSWORD,
  maxRetriesPerRequest: null, // required for Bull
});

module.exports = redis;
```

### Bull Queue Setup

```javascript
// services/queue.js
const Queue = require('bull');
const redis = require('../config/redis');

const invoiceQueue = new Queue('invoice-generation', {
  redis: {
    host: process.env.REDIS_HOST,
    port: process.env.REDIS_PORT,
  },
  defaultJobOptions: {
    attempts: 3, // retry up to 3 times
    backoff: {
      type: 'exponential',
      delay: 2000, // 2 seconds, doubles on each retry
    },
    removeOnComplete: {
      age: 3600, // keep completed jobs for 1 hour
    },
  },
});

module.exports = invoiceQueue;
```

### API Endpoint: Enqueue Job

```javascript
// routes/invoices.js
router.post('/invoices/generate', async (req, res) => {
  const { transaction_ids, template_id } = req.body;
  
  try {
    const job = await invoiceQueue.add({
      transaction_ids,
      template_id,
    });

    res.status(202).json({
      success: true,
      data: {
        job_id: job.id,
        status: 'PENDING',
        message: 'Invoice generation job queued',
        status_url: `/api/v1/jobs/${job.id}`,
      },
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      error: { message: error.message },
    });
  }
});
```

### Worker Implementation

```javascript
// workers/invoice-generator.js
const invoiceQueue = require('../services/queue');

invoiceQueue.process(5, async (job) => {
  const { transaction_ids, template_id } = job.data;

  job.progress(0);

  for (let i = 0; i < transaction_ids.length; i++) {
    try {
      const txnId = transaction_ids[i];
      
      // 1. Generate PDF
      const invoice = await generateInvoice(txnId, template_id);
      job.progress(Math.floor((i / transaction_ids.length) * 50));

      // 2. Send email
      await sendInvoiceEmail(invoice);
      job.progress(50 + Math.floor(((i + 1) / transaction_ids.length) * 50));

      // 3. Update database
      await updateInvoiceStatus(invoice.id, 'SENT');

      logger.info(`Invoice ${invoice.id} processed successfully`);
    } catch (error) {
      logger.error(`Failed to process transaction ${txnId}:`, error);
      throw error; // Bull will retry
    }
  }

  return {
    processed: transaction_ids.length,
    completed_at: new Date(),
  };
});

invoiceQueue.on('failed', (job, err) => {
  logger.error(`Job ${job.id} failed:`, err);
  // Notify admin if all retries exhausted
  if (job.attemptsMade === job.opts.attempts) {
    alertAdmin(`Invoice batch ${job.id} failed after ${job.attemptsMade} attempts`);
  }
});

invoiceQueue.on('completed', (job) => {
  logger.info(`Job ${job.id} completed:`, job.returnvalue);
});
```

### Status Query Endpoint

```javascript
// routes/jobs.js
router.get('/jobs/:jobId', async (req, res) => {
  const job = await invoiceQueue.getJob(req.params.jobId);

  if (!job) {
    return res.status(404).json({
      success: false,
      error: { message: 'Job not found' },
    });
  }

  const state = await job.getState();
  const progress = job.progress();

  res.json({
    success: true,
    data: {
      job_id: job.id,
      state, // 'active', 'completed', 'failed', 'pending'
      progress, // 0-100
      result: job.returnvalue,
      error: job.failedReason,
      attempts: job.attemptsMade,
      max_attempts: job.opts.attempts,
    },
  });
});
```

## Consequences

### Positive
- ✓ Decouples API from PDF/Email processing
- ✓ Meets 1-minute batch SLA (job enqueued in <100ms)
- ✓ Automatic retry on transient failures
- ✓ Horizontal scaling: add more workers
- ✓ Observability: job status, progress tracking
- ✓ Reliability: job persistence in Redis

### Negative
- ✗ Adds infrastructure complexity (Redis required)
- ✗ Eventual consistency (invoice status updated async)
- ✗ Memory overhead (Redis + Bull)
- ✗ Requires monitoring (queue length, worker health)

## Mitigations

1. **Infrastructure**: Use managed Redis (AWS ElastiCache, Azure Cache)
2. **Consistency**: API clearly returns 202 (Accepted), client polls for final status
3. **Monitoring**: Dashboards for queue depth, job failure rate, worker health
4. **Fallback**: If Redis unavailable, fall back to synchronous processing (degraded mode)

## Performance Expectations

| Metric | Target | Rationale |
|--------|--------|-----------|
| Job enqueue latency | <100ms | API responsiveness |
| Batch throughput | 100 invoices/min | Business requirement |
| Worker concurrency | 5 parallel jobs | Prevents resource exhaustion |
| Retry backoff | Exponential (2s → 4s → 8s) | Avoid thundering herd |
| Job retention | 1 hour (completed) | Balance storage vs debugging |

## Dependencies

### New Dependencies
- **redis** (ioredis): Redis client
- **bull**: Message queue library

### Infrastructure
- **Redis 6+**: Persistence enabled, appendonly yes
- **Memory**: ~500MB for queue + worker state (at full scale)

## Related Decisions

- **ADR-0001**: Stack selection (Node.js + PostgreSQL)
- **ADR-0003**: Error handling and monitoring
- **ADR-0004**: Security (job data PII handling)

## Future Enhancements

### Phase 2
- WebSocket support for real-time progress
- Job priority levels (express batch vs standard)
- Rate limiting per customer (no queue hogging)

### Phase 3
- Distributed workers (Kubernetes)
- Job analytics (success rate, processing time trends)
- Dead letter queue for manual recovery

---

**Decision Owner**: Architecture Lead  
**Review Date**: 2026-06-26 (validate under production load)
