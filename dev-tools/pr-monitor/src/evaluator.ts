/**
 * PR Comment Evaluator
 * Uses Copilot Chat to assess comment clarity and safety
 */

import axios from "axios";
import { CommentContext, EvaluationResult } from "./types";

const logger = console;

export class PRCommentEvaluator {
  private copilotChatUrl: string;

  constructor(copilotChatUrl: string) {
    this.copilotChatUrl = copilotChatUrl;
  }

  /**
   * Evaluate a PR comment using Copilot Chat
   */
  async evaluate(context: CommentContext): Promise<EvaluationResult> {
    const systemPrompt = `You are evaluating a GitHub PR review comment.
Determine if the comment is:
1. Actionable (clear, specific, implementable)
2. Safe (no malicious intent, doesn't break protected paths)
3. Reasonable (aligns with the PR scope)

Respond with JSON containing:
{
  "is_actionable": boolean,
  "action_type": "code_change" | "documentation" | "test" | "config" | "other",
  "confidence": 0.0-1.0,
  "reason": "explanation",
  "suggested_changes": "summary of what needs to be done",
  "risk_level": "low" | "medium" | "high",
  "safety_concerns": ["concern1", "concern2"],
  "requires_manual_review": boolean
}`;

    const userMessage = `PR #${context.pr_number}: ${context.pr_title}
Branch: ${context.pr_branch}
Author: ${context.pr_author}

Comment from @${context.comment_author}:
${context.comment_body}

Evaluate this comment.`;

    try {
      const response = await axios.post(
        `${this.copilotChatUrl}/evaluate`,
        {
          pr_number: context.pr_number,
          pr_title: context.pr_title,
          pr_body: context.pr_body,
          pr_branch: context.pr_branch,
          pr_author: context.pr_author,
          comment_author: context.comment_author,
          comment_body: context.comment_body,
          repository: context.repository,
          system_prompt: systemPrompt,
          user_message: userMessage,
        },
        { timeout: 30000 }
      );

      return this.ensureResponseFormat(response.data);
    } catch (error) {
      if (axios.isAxiosError(error) && error.code === "ECONNREFUSED") {
        // API server is completely down — return gracefully, no point retrying this poll
        logger.error(
          `Cannot connect to Copilot Chat API at ${this.copilotChatUrl}`
        );
        return {
          is_actionable: false,
          action_type: "unknown",
          confidence: 0,
          reason: "Copilot Chat API unavailable",
          suggested_changes: "",
          risk_level: "high",
          safety_concerns: ["API unavailable"],
          requires_manual_review: true,
        };
      }

      // For HTTP 5xx or other transient errors, re-throw so the caller can decide whether to retry
      const statusCode = axios.isAxiosError(error) ? error.response?.status : undefined;
      const responseBody = axios.isAxiosError(error) ? JSON.stringify(error.response?.data) : '';
      logger.error(`Error evaluating comment (status=${statusCode ?? 'N/A'}): ${error} — response: ${responseBody}`);
      throw error;
    }
  }

  /**
   * Ensure response has all expected fields
   */
  private ensureResponseFormat(
    response: Partial<EvaluationResult>
  ): EvaluationResult {
    const defaults: EvaluationResult = {
      is_actionable: false,
      action_type: "unknown",
      confidence: 0,
      reason: "",
      suggested_changes: "",
      risk_level: "medium",
      safety_concerns: [],
      requires_manual_review: true,
    };

    return {
      ...defaults,
      ...response,
    };
  }
}
