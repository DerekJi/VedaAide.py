/**
 * PR Monitor - Entry point
 */

import * as dotenv from "dotenv";
import * as path from "path";
import { Config } from "./config";
import { PRMonitor } from "./monitor";

// Load .env file
dotenv.config({ path: path.join(__dirname, "../.env") });
dotenv.config({ path: path.join(__dirname, "../.env.local") });

const logger = console;

async function main(): Promise<void> {
  try {
    // Load configuration
    const config = Config.fromEnv();

    // Get repository root
    const repoRoot = process.cwd();

    // Create and start monitor
    const monitor = new PRMonitor(config, repoRoot);
    await monitor.run();
  } catch (error) {
    logger.error(`Fatal error: ${error}`);
    process.exit(1);
  }
}

// Handle unhandled rejections
process.on("unhandledRejection", (reason, promise) => {
  logger.error(`Unhandled Rejection at:`, promise, `reason:`, reason);
  process.exit(1);
});

main();
