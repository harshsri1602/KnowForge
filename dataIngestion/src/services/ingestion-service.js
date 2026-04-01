import { v4 as uuidv4 } from "uuid";

import { JobStatus, createIngestionJob } from "../models/ingestion-models.js";
import { getProvider } from "../providers/provider-registry.js";

export class IngestionService {
  constructor({ repository, queue, queueName }) {
    this.repository = repository;
    this.queue = queue;
    this.queueName = queueName;
  }

  async receiveRequest(request) {
    const provider = getProvider(request.source);
    const metadata = provider.parseRequest(request);
    const now = new Date().toISOString();

    const job = createIngestionJob({
      id: uuidv4(),
      source: request.source,
      eventName: request.eventName,
      status: JobStatus.RECEIVED,
      payload: request.payload,
      headers: request.headers,
      externalId: metadata.externalId || null,
      detail: null,
      createdAt: now,
      updatedAt: now
    });

    await this.repository.createJob(job);
    await this.repository.updateJob(job.id, {
      status: JobStatus.QUEUED,
      externalId: job.externalId
    });

    await this.queue.add("process-ingestion-job", { jobId: job.id });

    return {
      jobId: job.id,
      status: JobStatus.QUEUED,
      queueName: this.queueName
    };
  }
}
