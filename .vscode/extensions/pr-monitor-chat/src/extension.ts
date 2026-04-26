import * as vscode from 'vscode';
import * as http from 'http';
import express from 'express';

const app = express();
app.use(express.json({ limit: '10mb' }));

const PORT = 3456;
let server: http.Server;

/**
 * 使用 Copilot Chat 进行评估或代码生成
 */
async function askCopilot(systemPrompt: string, userMessage: string): Promise<string> {
  try {
    // 获取 Copilot Chat 的 extension
    const copilotExt = vscode.extensions.getExtension('GitHub.copilot-chat');
    if (!copilotExt) {
      throw new Error('Copilot Chat extension not found');
    }

    // 如果还没激活，激活它
    if (!copilotExt.isActive) {
      await copilotExt.activate();
    }

    // 调用 Copilot Chat 的 chat 接口（如果可用）
    // 这需要使用 vscode.chat API（VS Code 1.84+）
    if (vscode.chat) {
      const result = await vscode.chat.requestChatResponse(
        [
          {
            content: systemPrompt,
            role: vscode.ChatMessageRole.System,
          },
          {
            content: userMessage,
            role: vscode.ChatMessageRole.User,
          },
        ],
        { model: 'auto' } // 使用 Auto 模式
      );

      if (result.response && result.response.length > 0) {
        return result.response
          .map((part) => (typeof part === 'string' ? part : part.value || ''))
          .join('\n');
      }
    }

    // Fallback: 如果 API 不可用，返回错误
    throw new Error('Copilot Chat API not available');
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    console.error('Copilot Chat error:', errorMessage);
    throw new Error(`Copilot Chat error: ${errorMessage}`);
  }
}

/**
 * HTTP 端点：评估 PR Comment
 */
app.post('/evaluate', async (req, res) => {
  try {
    const {
      pr_number,
      pr_title,
      pr_body,
      pr_branch,
      pr_author,
      issue_number,
      issue_title,
      issue_body,
      comment_author,
      comment_body,
      repository,
    } = req.body;

    const systemPrompt = `You are reviewing a GitHub PR comment to determine if it's a reasonable, actionable instruction.
Always respond with ONLY valid JSON, no other text.`;

    const userMessage = `Repository: ${repository}
PR #${pr_number}: ${pr_title}
PR Author: ${pr_author}
Comment Author: ${comment_author}

PR Description:
${pr_body || '(No description)'}

Comment:
${comment_body}

Evaluate this comment and respond with JSON:
{
  "is_actionable": boolean,
  "action_type": "docs_update|code_fix|config_change|test_addition|refactor|other",
  "confidence": 0.0-1.0,
  "reason": "Brief explanation",
  "suggested_changes": "What changes to make",
  "risk_level": "low|medium|high",
  "safety_concerns": [],
  "requires_manual_review": boolean
}`;

    const response = await askCopilot(systemPrompt, userMessage);
    const evaluation = JSON.parse(response);

    res.json(evaluation);
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    res.status(500).json({
      error: errorMessage,
      is_actionable: false,
    });
  }
});

/**
 * HTTP 端点：生成实现代码
 */
app.post('/generate-implementation', async (req, res) => {
  try {
    const { comment_body, evaluation } = req.body;

    const systemPrompt = `You are a code generation assistant for a PR automation system.
Generate specific file modifications based on the request.
Respond ONLY with FILE sections in this format, no other text:

FILE: path/to/file.py
ACTION: create|modify|delete
---
<file content>
---`;

    const userMessage = `Based on this request:
${comment_body}

Action type: ${evaluation.action_type}
Suggested changes: ${evaluation.suggested_changes}

Generate the exact file modifications needed. For each file, include FILE, ACTION, and content between --- markers.`;

    const response = await askCopilot(systemPrompt, userMessage);
    res.json({ implementation: response });
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    res.status(500).json({ error: errorMessage });
  }
});

/**
 * 健康检查端点
 */
app.get('/health', (req, res) => {
  res.json({ status: 'ok', message: 'PR Monitor Chat API is running' });
});

/**
 * 扩展激活函数
 */
export async function activate(context: vscode.ExtensionContext) {
  console.log('PR Monitor Chat extension activating...');

  // 启动 HTTP 服务器
  server = app.listen(PORT, 'localhost', () => {
    console.log(`PR Monitor Chat API listening on http://localhost:${PORT}`);
    vscode.window.showInformationMessage(
      `PR Monitor Chat API started on port ${PORT}`
    );
  });

  // 注册命令（可选，用于调试）
  let disposable = vscode.commands.registerCommand(
    'pr-monitor-chat.start',
    async () => {
      vscode.window.showInformationMessage('PR Monitor Chat is running');
    }
  );

  context.subscriptions.push(disposable);
}

/**
 * 扩展停用函数
 */
export function deactivate() {
  console.log('PR Monitor Chat extension deactivating...');
  if (server) {
    server.close();
  }
}
