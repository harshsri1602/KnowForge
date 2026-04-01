// this file defines how data enters your system and what happens to it
import { Router } from "express";

import { env } from "../../config/env.js";
import { initializeDatabase } from "../../db/database.js";
import { SourceType } from "../../models/ingestion-models.js";
import { ingestionQueue } from "../../queue/ingestion-queue.js";
import { IngestionRepository } from "../../repositories/ingestion-repository.js";
import { IngestionService } from "../../services/ingestion-service.js";

export const ingestionRouter = Router();

const repository = new IngestionRepository();
const service = new IngestionService({
  repository,
  queue: ingestionQueue,
  queueName: env.ingestionQueue
});

function resolveEventName(request) {
  return (
    request.header("X-GitHub-Event") ||
    request.header("X-Slack-Event-Type") ||
    request.header("X-Notion-Event") ||
    request.body.event ||
    request.body.type ||
    "unknown"
  );
}

function assertValidSource(source) {
  const validSources = new Set(Object.values(SourceType));
  return validSources.has(source);
}

// Make sure system is ready before doing anything
ingestionRouter.use(async (_request, _response, next) => {
  try {
    await initializeDatabase();
    next();
  } catch (error) {
    next(error);
  }
});

ingestionRouter.post("/webhooks/:source", async (request, response, next) => {
  try {
    const { source } = request.params;
    if (!assertValidSource(source)) {
      response.status(400).json({ error: `Unsupported source: ${source}` });
      return;
    }

    const result = await service.receiveRequest({
      source,
      eventName: resolveEventName(request),
      payload: request.body || {},
      headers: request.headers || {}
    });

    response.status(202).json(result);
  } catch (error) {
    next(error);
  }
});

ingestionRouter.get("/jobs/:jobId", async (request, response, next) => {
  try {
    const job = await repository.getJob(request.params.jobId);
    if (!job) {
      response.status(404).json({ error: "Job not found." });
      return;
    }

    response.json({
      jobId: job.id,
      source: job.source,
      eventName: job.eventName,
      status: job.status,
      detail: job.detail,
      externalId: job.externalId,
      createdAt: job.createdAt,
      updatedAt: job.updatedAt
    });
  } catch (error) {
    next(error);
  }
});

ingestionRouter.use((error, _request, response, _next) => {
  response.status(500).json({
    error: error.message || "Internal server error."
  });
});
