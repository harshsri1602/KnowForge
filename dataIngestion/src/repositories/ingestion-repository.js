import { get, query } from "../db/database.js";
import { DocumentStatus } from "../models/ingestion-models.js";

export class IngestionRepository {
  async createJob(job) {
    await query(
      `
        INSERT INTO ingestion_jobs (
          id, source, event_name, status, payload, headers,
          external_id, detail, created_at, updated_at
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
      `,
      [
        job.id,
        job.source,
        job.eventName,
        job.status,
        job.payload,
        job.headers,
        job.externalId,
        job.detail,
        job.createdAt,
        job.updatedAt
      ]
    );
  }

  async updateJob(jobId, { status, detail = null, externalId = null }) {
    await query(
      `
        UPDATE ingestion_jobs
        SET status = $1, detail = $2, external_id = COALESCE($3, external_id), updated_at = $4
        WHERE id = $5
      `,
      [status, detail, externalId, new Date().toISOString(), jobId]
    );
  }

  async getJob(jobId) {
    const row = await get(`SELECT * FROM ingestion_jobs WHERE id = $1`, [jobId]);
    if (!row) {
      return null;
    }

    return {
      id: row.id,
      source: row.source,
      eventName: row.event_name,
      status: row.status,
      payload: row.payload,
      headers: row.headers,
      externalId: row.external_id,
      detail: row.detail,
      createdAt: row.created_at,
      updatedAt: row.updated_at
    };
  }

  async saveDocuments(jobId, documents) {
    for (const document of documents) {
      await query(
        `
          INSERT INTO documents (
            job_id, external_id, source, status, title, content, metadata, created_at
          ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        `,
        [
          jobId,
          document.externalId,
          document.source,
          document.status || DocumentStatus.PENDING,
          document.title,
          document.content,
          document.metadata || {},
          new Date().toISOString()
        ]
      );
    }
  }
}
