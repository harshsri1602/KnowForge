import { JobStatus } from "../models/ingestion-models.js";
import { getProvider } from "../providers/provider-registry.js";

export class JobProcessor {
  constructor({ repository }) {
    this.repository = repository;
  }

  async process(jobId) {
    const job = await this.repository.getJob(jobId);
    if (!job) {
      throw new Error(`Ingestion job ${jobId} not found.`);
    }

    await this.repository.updateJob(jobId, {
      status: JobStatus.PROCESSING,
      detail: null
    });

    try {
      const provider = getProvider(job.source);
      const documents = await provider.fetchDocuments({
        source: job.source,
        eventName: job.eventName,
        payload: job.payload,
        headers: job.headers
      });

      await this.repository.saveDocuments(jobId, documents);
      await this.repository.updateJob(jobId, {
        status: JobStatus.COMPLETED,
        detail: `Stored ${documents.length} normalized document(s).`
      });

      return {
        jobId,
        status: JobStatus.COMPLETED
      };
    } catch (error) {
      await this.repository.updateJob(jobId, {
        status: JobStatus.FAILED,
        detail: error.message
      });
      throw error;
    }
  }
}
