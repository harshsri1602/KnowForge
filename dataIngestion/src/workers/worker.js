import { Worker } from "bullmq";

import { env } from "../config/env.js";
import { initializeDatabase } from "../db/database.js";
import { redisConnection } from "../queue/redis.js";
import { IngestionRepository } from "../repositories/ingestion-repository.js";
import { JobProcessor } from "./job-processor.js";

await initializeDatabase();

const repository = new IngestionRepository();
const processor = new JobProcessor({ repository });

const worker = new Worker(
  env.ingestionQueue,
  async (job) => processor.process(job.data.jobId),
  { connection: redisConnection }
);

worker.on("completed", (job) => {
  console.log(`Completed ingestion job ${job.data.jobId}`);
});

worker.on("failed", (job, error) => {
  console.error(`Failed ingestion job ${job?.data?.jobId}:`, error.message);
});

console.log(`Worker listening on queue "${env.ingestionQueue}"`);
