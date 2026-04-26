/**
 * PR Executor
 * Applies changes to the codebase based on approved evaluations
 */

import axios from "axios";
import { promises as fs } from "fs";
import * as path from "path";
import { GitHubClient } from "./github-client";
import { EvaluationResult, ExecutionResult } from "./types";

const logger = console;

export class PRExecutor {
  private gitClient: GitHubClient;
  private copilotChatUrl: string;

  constructor(repoPath: string, copilotChatUrl: string) {
    this.gitClient = new GitHubClient(repoPath);
    this.copilotChatUrl = copilotChatUrl;
  }

  /**
   * Execute changes based on evaluation
   */
  async executeChanges(
    prBranch: string,
    commentBody: string,
    evaluation: EvaluationResult,
    dryRun: boolean = false
  ): Promise<ExecutionResult> {
    try {
      // Checkout PR branch
      await this.gitClient.checkoutBranch(prBranch);

      // Get implementation from Copilot Chat
      const implementation = await this.getImplementation(
        commentBody,
        evaluation
      );

      if (!implementation) {
        return {
          success: false,
          error: "Could not generate implementation",
        };
      }

      // Parse the implementation
      const changes = this.parseImplementation(implementation);

      if (dryRun) {
        logger.info(`DRY RUN: Would apply ${changes.length} changes:`);
        changes.forEach((change) => {
          logger.info(`  - ${change.file}: ${change.action}`);
        });
        return {
          success: true,
          dry_run: true,
          changes_applied: changes.length,
        };
      }

      // Apply changes
      for (const change of changes) {
        await this.applyChange(change);
      }

      // Commit and push
      const commitMsg = `Auto: ${evaluation.action_type}`;
      await this.gitClient.commitChanges(commitMsg);
      await this.gitClient.pushChanges(prBranch);

      return {
        success: true,
        changes_applied: changes.length,
        commit_message: commitMsg,
      };
    } catch (error) {
      logger.error(`Execution error: ${error}`);
      return {
        success: false,
        error: String(error),
      };
    }
  }

  /**
   * Get implementation from Copilot Chat
   */
  private async getImplementation(
    commentBody: string,
    evaluation: EvaluationResult
  ): Promise<string | null> {
    try {
      const response = await axios.post(
        `${this.copilotChatUrl}/generate-implementation`,
        {
          comment_body: commentBody,
          evaluation,
        },
        { timeout: 30000 }
      );

      return response.data.implementation || null;
    } catch (error) {
      logger.error(`Error getting implementation: ${error}`);
      return null;
    }
  }

  /**
   * Parse implementation output into file changes
   * Expected format:
   * FILE: path/to/file.ts
   * ACTION: create|modify|delete
   * ---
   * <content>
   * ---
   */
  private parseImplementation(
    implementation: string
  ): Array<{
    file: string;
    action: string;
    content: string;
  }> {
    const changes = [];
    const fileBlocks = implementation.split(/^FILE:\s*/m).filter(Boolean);

    for (const block of fileBlocks) {
      const lines = block.split("\n");
      if (lines.length < 2) continue;

      const filePath = lines[0].trim();
      const actionLine = lines.find((l) =>
        l.toLowerCase().startsWith("action:")
      );

      if (!actionLine) continue;

      const action = actionLine
        .substring(7)
        .trim()
        .toLowerCase();
      // Match content between --- delimiters; tolerate CRLF and leading/trailing spaces on the --- lines
      const contentMatch = block.match(/^-{3,}\s*\r?\n([\s\S]*?)\r?\n-{3,}\s*(?:\r?\n|$)/m);
      if (!contentMatch) {
        logger.warn(`Could not extract content for ${filePath} — skipping`);
        continue;
      }
      const content = contentMatch[1];

      changes.push({
        file: filePath,
        action,
        content,
      });
    }

    return changes;
  }

  /**
   * Apply a single change to the repository
   */
  private async applyChange(change: {
    file: string;
    action: string;
    content: string;
  }): Promise<void> {
    // Safety: block overwriting critical project config files
    const BLOCKED_FILES = new Set([
      'package.json',
      'package-lock.json',
      'tsconfig.json',
      'pyproject.toml',
      'poetry.lock',
      '.gitignore',
      'docker-compose.yml',
      'Makefile',
    ]);
    const basename = path.basename(change.file);
    if (BLOCKED_FILES.has(basename)) {
      logger.warn(`Blocked: not allowed to ${change.action} protected file ${change.file}`);
      return;
    }

    // Safety: this is a TypeScript/Node.js project — block Python files
    if (change.file.endsWith('.py')) {
      logger.warn(`Blocked: Python files are not allowed in this TypeScript project (${change.file}). Generate .ts files instead.`);
      return;
    }

    try {
      switch (change.action) {
        case "create":
        case "modify": {
          const dir = path.dirname(change.file);
          await fs.mkdir(dir, { recursive: true });
          await fs.writeFile(change.file, change.content, "utf-8");
          logger.info(`${change.action.toUpperCase()} ${change.file}`);
          break;
        }

        case "delete":
          await fs.unlink(change.file);
          logger.info(`DELETE ${change.file}`);
          break;

        default:
          logger.warn(`Unknown action: ${change.action}`);
      }
    } catch (error) {
      logger.error(`Error applying change to ${change.file}: ${error}`);
      throw error;
    }
  }
}
