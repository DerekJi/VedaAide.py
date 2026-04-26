"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const express_1 = __importDefault(require("express"));
const app = (0, express_1.default)();
app.use(express_1.default.json({ limit: '10mb' }));
const PORT = 3456;
let server;
/**
 * 使用 VS Code Language Model API (vscode.lm) 调用 Copilot
 * 需要 VS Code 1.90+ 和 GitHub Copilot Chat 扩展
 */
async function askCopilot(systemPrompt, userMessage) {
    if (!vscode.lm) {
        throw new Error('vscode.lm API not available. Requires VS Code 1.90+');
    }
    const models = await vscode.lm.selectChatModels({ vendor: 'copilot', family: 'gpt-4o' });
    if (!models || models.length === 0) {
        const allModels = await vscode.lm.selectChatModels();
        const modelNames = allModels.map(m => `${m.vendor}/${m.family}/${m.id}`).join(', ');
        throw new Error(`No Copilot chat model available. Available: [${modelNames || 'none'}]. ` +
            'Ensure GitHub Copilot Chat is installed, signed in, and VS Code >= 1.90.');
    }
    const model = models[0];
    console.log(`Using model: ${model.vendor}/${model.family}/${model.id}`);
    const messages = [
        vscode.LanguageModelChatMessage.Assistant(systemPrompt),
        vscode.LanguageModelChatMessage.User(userMessage),
    ];
    const response = await model.sendRequest(messages, {}, new vscode.CancellationTokenSource().token);
    const parts = [];
    for await (const chunk of response.text) {
        parts.push(chunk);
    }
    const result = parts.join('');
    if (!result.trim()) {
        throw new Error('Empty response from Copilot model');
    }
    return result;
}
/**
 * 剥掉 Copilot 经常输出的 markdown code fence
 * 例如 ```json\n{...}\n``` → {...}
 */
function stripCodeFence(text) {
    return text
        .replace(/^```(?:json|typescript|ts|js|javascript|python|bash|sh)?\s*\n?/m, '')
        .replace(/\n?```\s*$/m, '')
        .trim();
}
/**
 * HTTP 端点：评估 PR Comment
 */
app.post('/evaluate', async (req, res) => {
    try {
        const { pr_number, pr_title, pr_body, pr_branch, pr_author, issue_number, issue_title, issue_body, comment_author, comment_body, repository, } = req.body;
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
        const rawResponse = await askCopilot(systemPrompt, userMessage);
        const evaluation = JSON.parse(stripCodeFence(rawResponse));
        res.json(evaluation);
    }
    catch (error) {
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
        const { comment_body, evaluation, pr_branch, pr_title } = req.body;
        const systemPrompt = `You are a code generation assistant for a TypeScript/Node.js PR automation system.
The codebase is TypeScript. Generate file modifications in TypeScript (.ts) unless the PR comment explicitly requests a different language.
Do NOT wrap file content in markdown code fences (no \`\`\`).
Respond ONLY with FILE sections in this exact format, no other text:

FILE: path/to/file.ts
ACTION: create|modify|delete
---
<file content here, no code fences>
---`;
        const userMessage = `PR: ${pr_title || '(unknown)'}
Branch: ${pr_branch || '(unknown)'}

Comment requesting changes:
${comment_body}

Action type: ${evaluation.action_type}
Suggested changes: ${evaluation.suggested_changes}

Generate the exact TypeScript file modifications needed. For each file, include FILE, ACTION, and content between --- markers. Do NOT use markdown code fences inside the content.`;
        const response = await askCopilot(systemPrompt, userMessage);
        res.json({ implementation: response });
    }
    catch (error) {
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
async function activate(context) {
    console.log('PR Monitor Chat extension activating...');
    // 启动 HTTP 服务器
    server = app.listen(PORT, 'localhost', () => {
        console.log(`PR Monitor Chat API listening on http://localhost:${PORT}`);
        vscode.window.showInformationMessage(`PR Monitor Chat API started on port ${PORT}`);
    });
    // 注册命令（可选，用于调试）
    let disposable = vscode.commands.registerCommand('pr-monitor-chat.start', async () => {
        vscode.window.showInformationMessage('PR Monitor Chat is running');
    });
    context.subscriptions.push(disposable);
}
/**
 * 扩展停用函数
 */
function deactivate() {
    console.log('PR Monitor Chat extension deactivating...');
    if (server) {
        server.close();
    }
}
