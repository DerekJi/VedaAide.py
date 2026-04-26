/**
 * PR Monitor
 * Main monitoring daemon loop
 */

import * as fs from "fs";
import * as path from "path";
import { GitHubClient } from "./github-client";
import { PRCommentEvaluator } from "./evaluator";
import { PRExecutor } from "./executor";
import { CommentContext, Review, ExecutionResult } from "./types";
import { MonitorConfig } from "./types";

const logger = console;

export class PRMonitor {
  private config: MonitorConfig;
  private gitClient: GitHubClient;
  private evaluator: PRCommentEvaluator;
  private executor: PRExecutor;
  private processedComments: Set<string>;
  private running: boolean = true;
  private stateDir: string;
  private processedCommentsFile: string;

  constructor(
    config: MonitorConfig,
    repoPath: string = "."
  ) {
    this.config = config;
    this.gitClient = new GitHubClient(repoPath);
    this.evaluator = new PRCommentEvaluator(config.copilot_chat_url);
    this.executor = new PRExecutor(repoPath, config.copilot_chat_url);
    this.stateDir = path.join(repoPath, ".pr-monitor-state");
    this.processedCommentsFile = path.join(
      this.stateDir,
      "processed-comments.json"
    );
    this.processedComments = this.loadProcessedComments();

    // Handle graceful shutdown
    process.on("SIGINT", () => this.handleShutdown());
    process.on("SIGTERM", () => this.handleShutdown());
  }

  /**
   * Start the monitoring loop
   */
  async run(): Promise<void> {
    logger.info(
      `Starting PR Monitor (interval: ${this.config.poll_interval_seconds}s)`
    );
    logger.info(
      `Trusted users: ${this.config.trusted_users.join(", ")}`
    );

    // Verify Copilot Chat is reachable
    if (!(await this.verifyCopilotChatConnection())) {
      logger.error(
        `Cannot connect to Copilot Chat at ${this.config.copilot_chat_url}`
      );
      return;
    }

    while (this.running) {
      try {
        await this.checkPRs();
      } catch (error) {
        logger.error(`Error in monitoring loop: ${error}`);
      }

      if (this.running) {
        logger.info(
          `Sleeping for ${this.config.poll_interval_seconds}s...`
        );
        await this.sleep(this.config.poll_interval_seconds * 1000);
      }
    }

    logger.info("PR Monitor stopped");
  }

  /**
   * Verify Copilot Chat is reachable
   */
  private async verifyCopilotChatConnection(): Promise<boolean> {
    try {
      const response = await import("axios").then((axios) =>
        axios.default.get(`${this.config.copilot_chat_url}/health`, {
          timeout: 5000,
        })
      );
      logger.info(
        `✓ Connected to Copilot Chat API at ${this.config.copilot_chat_url}`
      );
      return true;
    } catch {
      logger.error(
        `Cannot reach Copilot Chat API at ${this.config.copilot_chat_url}`
      );
      return false;
    }
  }

  /**
   * Check all open PRs for new comments
   */
  private async checkPRs(): Promise<void> {
    logger.info("Checking PRs...");

    const prs = await this.gitClient.getOpenPRs();
    if (prs.length === 0) {
      logger.info("No open PRs found");
      return;
    }

    logger.info(`Found ${prs.length} open PRs`);

    for (const pr of prs) {
      await this.processPR(pr);
    }
  }

  /**
   * Process a single PR
   */
  private async processPR(pr: {
    number: number;
    title: string;
    body: string;
    headRefName: string;
    author: string;
  }): Promise<void> {
    logger.info(
      `Processing PR #${pr.number}: ${pr.title}`
    );

    const reviews = await this.gitClient.getPRReviews(pr.number);

    for (const review of reviews) {
      if (!review.body) continue;
      await this.processComment(pr, review);
    }
  }

  /**
   * Process a single comment
   */
  private async processComment(
    pr: {
      number: number;
      title: string;
      body: string;
      headRefName: string;
      author: string;
    },
    review: Review
  ): Promise<void> {
    const commentId = review.id;

    // Skip if already processed
    if (this.processedComments.has(commentId)) {
      return;
    }

    // Skip if not from trusted user
    if (!this.config.trusted_users.includes(review.author)) {
      logger.info(
        `    Skipping comment from untrusted user: ${review.author}`
      );
      this.markProcessed(commentId, { success: false, error: "Untrusted user" });
      return;
    }

    logger.info(
      `    Evaluating comment #${commentId} by ${review.author}`
    );

    // Evaluate the comment
    const context: CommentContext = {
      pr_number: pr.number,
      pr_title: pr.title,
      pr_body: pr.body,
      pr_branch: pr.headRefName,
      pr_author: pr.author,
      issue_number: pr.number,
      issue_title: pr.title,
      issue_body: pr.body,
      comment_author: review.author,
      comment_body: review.body,
      repository: "", // Will be determined by git
    };

    const evaluation = await this.evaluator.evaluate(context);

    logger.info(
      `    Evaluation: actionable=${evaluation.is_actionable} confidence=${evaluation.confidence} risk=${evaluation.risk_level}`
    );

    // Check if we should execute
    if (!evaluation.is_actionable) {
      logger.info(`    Not actionable, skipping`);
      this.markProcessed(commentId, { success: false, error: "Not actionable" });
      return;
    }

    if (evaluation.confidence < 0.7) {
      logger.info(
        `    Confidence too low (${evaluation.confidence}), skipping`
      );
      this.markProcessed(commentId, {
        success: false,
        error: "Confidence too low",
      });
      return;
    }

    if (evaluation.risk_level === "high") {
      logger.info(`    Risk too high, skipping`);
      this.markProcessed(commentId, { success: false, error: "Risk too high" });
      return;
    }

    // Execute
    logger.info(`    Executing changes...`);
    const result = await this.executor.executeChanges(
      pr.headRefName,
      review.body,
      evaluation,
      !(this.config.auto_commit && this.config.auto_push)
    );

    if (result.success) {
      logger.info(`    ✓ Successfully executed changes`);
    } else {
      logger.error(`    ✗ Execution failed: ${result.error}`);
    }

    this.markProcessed(commentId, result);
  }

  /**
   * Load processed comments from state file
   */
  private loadProcessedComments(): Set<string> {
    try {
      if (!fs.existsSync(this.processedCommentsFile)) {
        return new Set();
      }

      const data = JSON.parse(
        fs.readFileSync(this.processedCommentsFile, "utf-8")
      );
      return new Set(data.processed || []);
    } catch (error) {
      logger.warn(`Failed to load processed comments: ${error}`);
      return new Set();
    }
  }

  /**
   * Mark a comment as processed
   */
  private markProcessed(commentId: string, result: ExecutionResult): void {
    this.processedComments.add(commentId);

    try {
      fs.mkdirSync(this.stateDir, { recursive: true });
      fs.writeFileSync(
        this.processedCommentsFile,
        JSON.stringify({
          processed: Array.from(this.processedComments),
          last_updated: new Date().toISOString(),
        }),
        "utf-8"
      );
    } catch (error) {
      logger.error(`Failed to save processed comments: ${error}`);
    }
  }

  /**
   * Handle shutdown
   */
  private handleShutdown(): void {
    logger.info("Shutdown signal received, stopping monitor...");
    this.running = false;
  }

  /**
   * Sleep helper
   */
  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}
