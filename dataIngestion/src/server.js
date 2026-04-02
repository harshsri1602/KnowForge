import { createApp } from "./api/app.js";
import { env } from "./config/env.js";
import { initializeDatabase } from "./db/database.js";

//console.log("DB URL:", env.databaseUrl);
await initializeDatabase();

const app = createApp();

app.listen(env.port, () => {
  console.log(`KnowForge ingestion API listening on port ${env.port}`);
});
