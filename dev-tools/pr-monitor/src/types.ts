/**
 * Type definitions for PR Monitor
 */

export interface PullRequest {
  number: number;
  title: string;
  body: string;
  state: "open" | "closed";
  headRefName: string;
  baseRefName: string;
  author: string;
  url: string;
}

export interface Review {
  id: string;
  body: string;
  author: string;
  createdAt: string;
  authorAssociation: string;
}

export interface CommentContext {
  pr_number: number;
  pr_title: string;
  pr_body: string;
  pr_branch: string;
  pr_author: string;
  issue_number: number;
  issue_title: string;
  issue_body: string;
  comment_author: string;
  comment_body: string;
  repository: string;
}

export interface EvaluationResult {
  is_actionable: boolean;
  action_type: string;
  confidence: number;
  reason: string;
  suggested_changes: string;
  risk_level: "low" | "medium" | "high";
  safety_concerns: string[];
  requires_manual_review: boolean;
}

export interface ImplementationResult {
  implementation: string;
  error?: string;
}

export interface ExecutionResult {
  success: boolean;
  error?: string;
  changes_applied?: number;
  commit_message?: string;
  dry_run?: boolean;
}

export interface MonitorConfig {
  copilot_chat_url: string;
  poll_interval_seconds: number;
  auto_commit: boolean;
  auto_push: boolean;
  verify_before_commit: boolean;
  trusted_users: string[];
}

export interface ProcessedComment {
  comment_id: string;
  pr_number: number;
  timestamp: string;
  result: ExecutionResult;
}
