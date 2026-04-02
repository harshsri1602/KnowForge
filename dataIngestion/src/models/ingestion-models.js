export const SourceType = Object.freeze({
  GITHUB: "github",
  SLACK: "slack",
  JIRA: "jira",
  GOOGLE_DOCS: "google_docs",
  NOTION: "notion"
});

export const JobStatus = Object.freeze({
  RECEIVED: "received",
  QUEUED: "queued",
  PROCESSING: "processing",
  COMPLETED: "completed",
  FAILED: "failed"
});

export const DocumentStatus = Object.freeze({
  PENDING: "pending",
  NLP_FINISHED: "nlp_finished",
  GRAPH_FINISHED: "graph_finished",
  FAILED: "failed"
});

export function createIngestionJob({
  id,
  source,
  eventName,
  status,
  payload,
  headers,
  externalId = null,
  detail = null,
  createdAt,
  updatedAt
}) {
  return {
    id,
    source,
    eventName,
    status,
    payload,
    headers,
    externalId,
    detail,
    createdAt,
    updatedAt
  };
}
