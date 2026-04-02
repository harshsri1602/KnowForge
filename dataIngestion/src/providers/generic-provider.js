import { BaseProvider } from "./base-provider.js";
import { DocumentStatus } from "../models/ingestion-models.js";

export class GenericProvider extends BaseProvider {
  constructor(source) {
    super();
    this.source = source;
  }

  parseRequest(request) {
    const externalId =
      request.payload.id ||
      request.payload.event_id ||
      request.payload.page_id ||
      request.payload.document_id ||
      null;

    return {
      externalId: externalId ? String(externalId) : null
    };
  }

  async fetchDocuments(request) {
    const externalId =
      request.payload.id ||
      request.payload.event_id ||
      request.payload.page_id ||
      request.payload.document_id ||
      `${this.source}:${request.eventName}`;

    return [
      {
        externalId: String(externalId),
        source: this.source,
        status: DocumentStatus.PENDING,
        title: `${this.source.replaceAll("_", " ")} ${request.eventName}`,
        content: JSON.stringify(request.payload, null, 2),
        metadata: {
          eventName: request.eventName
        }
      }
    ];
  }
}
