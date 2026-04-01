# KnowForge Data Ingestion

This module implements the ingestion workflow in Node.js:

`Express API -> Redis queue -> BullMQ worker -> database -> downstream NLP queue`

## What it does

- receives webhook events from GitHub, Slack, Jira, Google Docs, and Notion
- normalizes source-specific payloads
- stores a durable ingestion job
- queues the job in Redis
- processes the job in a worker
- stores normalized documents for downstream indexing or NLP

## Run locally

1. Install dependencies:

```bash
npm install
```

2. Copy `.env.example` to `.env`.
3. Start Redis.
4. Start PostgreSQL and create the target database.
5. Start the API:

```bash
npm run dev
```

6. Start the worker in a separate terminal:

```bash
npm run worker
```

## Example request

```bash
curl -X POST http://localhost:8000/api/v1/ingestion/webhooks/github \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: push" \
  -d "{\"repository\":{\"full_name\":\"acme/knowforge\"},\"after\":\"abc123\"}"
```

## Structure

```text
dataIngestion/
  src/
    api/         # Express routes and HTTP app
    config/      # Environment configuration
    db/          # PostgreSQL connection and schema
    models/      # Shared constants and helpers
    providers/   # Source-specific adapters
    queue/       # Redis and BullMQ setup
    repositories/# Data access layer
    services/    # Ingestion orchestration
    workers/     # Background job processing
```

## Notes

- PostgreSQL is a better default for multi-worker ingestion workloads.
- BullMQ is a great fit for Redis-backed background jobs in Node.js.
- The GitHub adapter is concrete; the others are intentionally simple and ready to extend.
