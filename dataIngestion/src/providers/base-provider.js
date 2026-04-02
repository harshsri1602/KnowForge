export class BaseProvider {
  parseRequest() {
    throw new Error("parseRequest() must be implemented.");
  }

  fetchDocuments() {
    throw new Error("fetchDocuments() must be implemented.");
  }
}
