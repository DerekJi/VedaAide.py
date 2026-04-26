/**
 * GitHub API client using gh CLI
 * Avoids need for GITHUB_TOKEN - uses existing gh auth
 */

import { execSync } from "child_process";
import { PullRequest, Review } from "./types";

const logger = console;

type RawPR = {
  number: number;
  title: string;
  body?: string;
  headRefName: string;
  baseRefName: string;
  author?: { login?: string };
  url: string;
};

type RawReview = {
  id: string;
  body: string;
  author?: { login?: string };
  createdAt: string;
  authorAssociation?: string;
};

export class GitHubClient {
  private repoPath: string;

  constructor(repoPath: string = ".") {
    this.repoPath = repoPath;
    this.verifyGhAuth();
  }

  private verifyGhAuth(): void {
    try {
      execSync("gh auth status", { stdio: "pipe" });
    } catch {
      throw new Error(
        "gh CLI not configured. Run: gh auth login"
      );
    }
  }

  /**
   * Get owner/repo from git remote
   */
  private getRepo(): string {
    try {
      const remote = execSync("git config --get remote.origin.url", {
        cwd: this.repoPath,
        encoding: "utf-8",
      }).trim();

      // Parse: git@github.com:owner/repo.git or https://github.com/owner/repo.git
      const match = remote.match(/[:/]([^/:]+)\/([^/]+?)(?:\.git)?$/);
      if (!match) {
        throw new Error(`Cannot parse repo from remote: ${remote}`);
      }

      return `${match[1]}/${match[2]}`;
    } catch (e) {
      throw new Error(`Failed to get repository info: ${e}`);
    }
  }

  /**
   * Get all open PRs
   */
  async getOpenPRs(): Promise<PullRequest[]> {
    try {
      const repo = this.getRepo();
      const output = execSync(
        `gh pr list --repo "${repo}" --state open --limit 50 --json number,title,body,state,headRefName,baseRefName,author,url`,
        { encoding: "utf-8" }
      );

      const prs = JSON.parse(output) as RawPR[];
      return prs.map((pr) => ({
        number: pr.number,
        title: pr.title,
        body: pr.body || "",
        state: "open" as const,
        headRefName: pr.headRefName,
        baseRefName: pr.baseRefName,
        author: pr.author?.login || "unknown",
        url: pr.url,
      }));
    } catch (e) {
      logger.error(`Failed to get PRs: ${e}`);
      return [];
    }
  }

  /**
   * Get reviews for a specific PR
   */
  async getPRReviews(prNumber: number): Promise<Review[]> {
    try {
      const repo = this.getRepo();
      const output = execSync(
        `gh pr view "${prNumber}" --repo "${repo}" --json reviews`,
        { encoding: "utf-8" }
      );

      const data = JSON.parse(output) as { reviews?: RawReview[] };
      return (data.reviews || []).map((review) => ({
        id: review.id,
        body: review.body,
        author: review.author?.login || "unknown",
        createdAt: review.createdAt,
        authorAssociation: review.authorAssociation || "NONE",
      }));
    } catch (e) {
      logger.error(
        `Failed to get reviews for PR #${prNumber}: ${e}`
      );
      return [];
    }
  }

  /**
   * Checkout a branch in the repo
   */
  async checkoutBranch(branch: string): Promise<void> {
    try {
      execSync(`git checkout "${branch}"`, { cwd: this.repoPath });
      logger.info(`Checked out branch: ${branch}`);
    } catch (e) {
      throw new Error(
        `Failed to checkout ${branch}: ${e}`
      );
    }
  }

  /**
   * Get current branch
   */
  getCurrentBranch(): string {
    try {
      return execSync("git rev-parse --abbrev-ref HEAD", {
        cwd: this.repoPath,
        encoding: "utf-8",
      }).trim();
    } catch {
      return "main";
    }
  }

  /**
   * Commit changes
   */
  async commitChanges(message: string): Promise<void> {
    try {
      execSync(`git add .`, { cwd: this.repoPath });
      execSync(`git commit -m "${message}"`, { cwd: this.repoPath });
      logger.info(`Committed: ${message}`);
    } catch (e) {
      throw new Error(
        `Failed to commit: ${e}`
      );
    }
  }

  /**
   * Push changes to remote
   */
  async pushChanges(branch: string): Promise<void> {
    try {
      execSync(`git push origin "${branch}"`, { cwd: this.repoPath });
      logger.info(`Pushed to origin/${branch}`);
    } catch (e) {
      throw new Error(
        `Failed to push: ${e}`
      );
    }
  }

  /**
   * Get changed files in the current branch vs main
   */
  async getChangedFiles(): Promise<string[]> {
    try {
      const output = execSync(
        "git diff --name-only main..HEAD",
        {
          cwd: this.repoPath,
          encoding: "utf-8",
        }
      );
      return output.split("\n").filter(Boolean);
    } catch {
      return [];
    }
  }
}
