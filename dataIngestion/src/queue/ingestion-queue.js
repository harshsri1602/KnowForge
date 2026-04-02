import { Queue } from "bullmq";

import { env } from "../config/env.js";
import { redisConnection } from "./redis.js";

export const ingestionQueue = new Queue(env.ingestionQueue, {
  connection: redisConnection
});
