import { SourceType } from "../models/ingestion-models.js";
import { GenericProvider } from "./generic-provider.js";
import { GitHubProvider } from "./github-provider.js";

const providers = new Map([
  [SourceType.GITHUB, new GitHubProvider()],
  [SourceType.SLACK, new GenericProvider(SourceType.SLACK)],
  [SourceType.JIRA, new GenericProvider(SourceType.JIRA)],
  [SourceType.GOOGLE_DOCS, new GenericProvider(SourceType.GOOGLE_DOCS)],
  [SourceType.NOTION, new GenericProvider(SourceType.NOTION)]
]);

export function getProvider(source) {
  const provider = providers.get(source);
  if (!provider) {
    throw new Error(`Unsupported source: ${source}`);
  }
  return provider;
}
