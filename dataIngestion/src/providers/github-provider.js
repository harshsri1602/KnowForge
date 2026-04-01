import { BaseProvider } from "./base-provider.js";
import { DocumentStatus, SourceType } from "../models/ingestion-models.js";

export class GitHubProvider extends BaseProvider {
  constructor() {
    super();
    this.source = SourceType.GITHUB;
  }

  parseRequest(request) {
    const repository = request.payload.repository || {};
    const externalId =
      request.payload.after ||
      String(request.payload.pull_request?.id || "") ||
      String(request.payload.issue?.id || "") ||
      null;

    return {
      externalId,
      repository: repository.full_name || "unknown",
      eventName: request.eventName
    };
  }

  async fetchDocuments(request) {
    const repository = request.payload.repository || {};
    const repoName = repository.full_name || "unknown";
    const externalId =
      request.payload.after ||
      String(request.payload.pull_request?.id || "") ||
      String(request.payload.issue?.id || "") ||
      `${repoName}:${request.eventName}`;

    return [
      {
        externalId: String(externalId),
        source: this.source,
        status: DocumentStatus.PENDING,
        title: `GitHub ${request.eventName} event for ${repoName}`,
        content: JSON.stringify(
          {
            repository: repoName,
            eventName: request.eventName,
            payload: request.payload
          },
          null,
          2
        ),
        metadata: {
          repository: repoName,
          eventName: request.eventName
        }
      }
    ];
  }
}
