import express from "express";

import { ingestionRouter } from "./routes/ingestion-routes.js";

export function createApp() {
  const app = express();
  app.use(express.json());

  app.get("/health", (_request, response) => {
    response.json({ ok: true });
  });

  app.use("/api/v1/ingestion", ingestionRouter);

  return app;
}
