/**
 * Configuration management for PR Monitor
 * Reads from environment and provides centralized config
 */

import { MonitorConfig } from "./types";

export class Config implements MonitorConfig {
  copilot_chat_url: string;
  poll_interval_seconds: number;
  auto_commit: boolean;
  auto_push: boolean;
  verify_before_commit: boolean;
  trusted_users: string[];

  constructor() {
    this.copilot_chat_url =
      process.env.COPILOT_CHAT_URL || "http://localhost:3456";
    this.poll_interval_seconds =
      parseInt(process.env.PR_MONITOR_INTERVAL || "1800", 10);
    this.auto_commit = process.env.AUTO_COMMIT !== "false";
    this.auto_push = process.env.AUTO_PUSH !== "false";
    this.verify_before_commit = process.env.VERIFY_BEFORE_COMMIT !== "false";
    this.trusted_users = (process.env.TRUSTED_USERS || "").split(",").filter(Boolean);

    this.validate();
  }

  private validate(): void {
    if (!this.copilot_chat_url) {
      throw new Error(
        "COPILOT_CHAT_URL not set. Configure in environment or .env file"
      );
    }

    if (this.trusted_users.length === 0) {
      console.warn(
        "TRUSTED_USERS not set. No comments will be processed. Set comma-separated usernames."
      );
    }

    if (this.poll_interval_seconds < 60) {
      throw new Error(
        "PR_MONITOR_INTERVAL must be >= 60 seconds (1 minute)"
      );
    }
  }

  static fromEnv(): Config {
    return new Config();
  }
}

// Note: do NOT eagerly initialize config here.
// index.ts calls dotenv.config() first, then creates Config.fromEnv().
