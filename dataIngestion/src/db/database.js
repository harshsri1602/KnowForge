import pg from "pg";

import { env } from "../config/env.js";

const { Pool } = pg;

export const pool = new Pool({
  connectionString: env.databaseUrl
});

export async function query(sql, params = []) {
  return pool.query(sql, params);
}

export function get(sql, params = []) {
  return query(sql, params).then((result) => result.rows[0] || null);
}

export async function initializeDatabase() {
  // the first table is used to track every incoming data event and its processing status
  // the second table is for Cleaned and structured data ready for NLP + graph building.
  await query(`
    CREATE TABLE IF NOT EXISTS ingestion_jobs (
      -- Unique internal id for each ingestion job.
      id TEXT PRIMARY KEY,
      -- Source system that sent the event, such as github or slack.
      source TEXT NOT NULL,
      -- Event type received from the source (commit, message, PR, etc.).
      event_name TEXT NOT NULL,
      -- Current processing state of the job (received,queued,processing,completed,failed).
      status TEXT NOT NULL,
      -- Original webhook or ingestion payload.
      payload JSONB NOT NULL,
      -- Request headers kept for tracing and debugging.
      headers JSONB NOT NULL,
      -- Optional id from the source system, such as commit SHA for github or page id.
      external_id TEXT,
      -- Human-readable success or failure note.
      detail TEXT,
      -- Time when the job record was first created.
      created_at TIMESTAMPTZ NOT NULL,
      -- Time when the job record was last updated.
      updated_at TIMESTAMPTZ NOT NULL
    )
  `);

  await query(`
    CREATE TABLE IF NOT EXISTS documents (
      -- Auto-incrementing database id for each stored document.
      id BIGSERIAL PRIMARY KEY,
      -- Ingestion job that produced this document.
      job_id TEXT NOT NULL,
      -- Original source-side id for the document or event.
      external_id TEXT NOT NULL,
      -- Source system the document came from.
      source TEXT NOT NULL,
      -- Current processing state of the job (pending,nlp_finished,graph_finished,failed).
      status TEXT NOT NULL,
      -- Short readable label for the stored document.
      title TEXT NOT NULL,
      -- Normalized text or serialized content to process later.
      content TEXT NOT NULL,
      -- Extra structured fields associated with the document.
      metadata JSONB NOT NULL,
      -- Time when the normalized document was stored.
      created_at TIMESTAMPTZ NOT NULL
    )
  `);
}
