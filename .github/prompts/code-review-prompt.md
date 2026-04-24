# 完整的编码规范审查 Prompt

## 📋 使用说明

这个 Prompt 用于全面审查代码，包括三个层次的检查，最后生成详细报告。

直接复制下面的内容到 Copilot Chat 中，或根据需要调整。

---

## 🎯 完整审查 Prompt

```
【任务】请对当前项目的所有代码进行全面的编码规范审查。

【项目位置】VedaAide.py 项目，src/ 和 tests/ 目录

【审查三个层次】

## 第一层：make verify 能检查的项目

这些项目可以通过运行以下命令检查：
- make format (black + isort) → 检查代码格式和行长
- make lint (pylint) → 检查命名规范、缺少文档
- make type-check (mypy) → 检查类型注解
- make test (pytest) → 检查单元测试

请检查以下项目：
1. 【代码格式】
   - 行长是否超过 100 字符
   - 缩进是否正确（4 空格）
   - 空格使用是否符合 PEP8

2. 【Import 顺序】
   - 是否按顺序：标准库 → 第三方库 → 本地模块
   - 是否使用了 isort 推荐的排列

3. 【命名规范】
   - 类名是否为 PascalCase
   - 函数/变量是否为 snake_case
   - 常量是否为 UPPER_SNAKE_CASE
   - 私有成员是否有 _ 前缀
   - 测试文件是否为 test_*.py
   - 测试函数是否为 test_<action>_<scenario>()

4. 【类型注解】
   - 所有函数/方法是否有参数类型注解
   - 所有函数/方法是否有返回值类型注解
   - 复杂类型是否使用 typing 模块（List, Dict, Optional 等）
   - 是否漏掉了任何必要的注解

5. 【文档字符串】
   - 所有公开函数是否有文档字符串
   - 所有公开类是否有文档字符串
   - 文档是否为 Google 风格（Args, Returns, Raises）
   - 文档是否准确描述了功能

6. 【单元测试】
   - 关键函数是否有单元测试
   - 测试覆盖率是否 >= 80%
   - 测试是否涵盖异常情况

---

## 第二层：make verify 检查不到的规范项目

以下项目需要代码审查检查：

1. 【模块大小】
   - 文件是否超过 300 行（必须拆分）
   - 类是否超过 250 行（应该拆分）
   - 方法是否超过 50 行（应该拆分）
   - 是否遵循 SRP（单一职责原则）

2. 【依赖注入】
   - ❌ 禁止在 __init__ 中硬编码创建外部服务
   - ✅ 应该通过构造函数注入依赖
   - ✅ 示例错误：self.llm = AzureOpenAI(api_key="...")
   - ✅ 示例正确：def __init__(self, llm: LLMProvider)

3. 【配置管理】
   - ❌ 禁止直接使用 os.getenv("KEY")
   - ✅ 应该使用 ConfigManager.get("key")
   - 检查是否有硬编码的 API 密钥或敏感信息

4. 【日志使用】
   - ❌ 禁止使用 print() 语句
   - ✅ 应该使用 logging 模块
   - logger = logging.getLogger(__name__)

5. 【异常处理】
   - ❌ 禁止裸露的 except Exception as e: pass
   - ✅ 应该捕获具体异常，记录日志，然后重新抛出或包装
   - 检查是否有 except: 或 except Exception:

6. 【异步编程】
   - I/O 操作是否使用了 async/await
   - 是否有在异步函数中使用阻塞调用（如 requests.get）
   - 是否正确使用了 asyncio

7. 【模块组织】
   - 相关的类/函数是否组织在一起
   - 是否遵循了 src/core/module/ 的组织结构
   - __init__.py 是否正确导出了公开接口

8. 【代码重复】
   - 是否有明显的代码重复
   - 是否应该提取为共享函数或基类

9. 【类的设计】
   - 类的职责是否单一
   - 是否适当使用了继承和接口
   - 公开方法和私有方法的划分是否合理

10. 【错误消息】
    - 错误消息是否清晰有用
    - 是否包含足够的上下文信息

---

## 第三层：生成详细报告

请生成一份结构化的审查报告，包括：

### 报告格式

```
# 编码规范审查报告

## 📊 总体概览
- 扫描的文件总数：X 个
- 发现的问题总数：Y 个
- 严重问题：Z 个
- 通过率：XX%

## 🔴 严重问题（必须修复）
### 类型1：问题描述
- 文件：xxx.py，行号：XXX
  问题：具体描述
  修复建议：...
  
## 🟡 警告问题（应该修复）
### 类型1：问题描述
- 文件：xxx.py，行号：XXX
  问题：具体描述
  修复建议：...

## 🟢 建议（可选改进）
### 类型1：建议描述
- 文件：xxx.py，行号：XXX
  建议：具体描述

## 📋 按文件分组的问题汇总

### src/core/agent.py
- [严重] 缺少类型注解（第 45 行）
- [警告] 文件超过 300 行（共 350 行）
- [建议] 可以提取为独立方法（第 120 行）

...

## ✅ 修复优先级建议

### 优先级1（立即修复）
1. 修复类型注解
2. 修复命名规范
3. 修复异常处理

### 优先级2（本周修复）
1. 拆分超大文件
2. 修复依赖注入
3. 移除 print 语句

### 优先级3（后续改进）
1. 提取重复代码
2. 优化代码结构
3. 改进文档

## 🎯 后续行动

1. 运行 make format 自动修复格式问题
2. 根据报告修复代码风格问题
3. 添加缺失的类型注解
4. 添加缺失的文档字符串
5. 重构超大的文件/类/方法
6. 运行 make verify 确保所有检查通过
```

---

## 【额外说明】

### 提供的信息

请在你的审查中包含：
1. 具体的文件名和行号
2. 当前代码示例
3. 修复后的代码示例
4. 每个问题的严重程度（严重/警告/建议）

### 审查范围

- 扫描目录：src/ 和 tests/
- 排除目录：__pycache__，.venv，.temp

### 输出格式

使用 Markdown 格式，便于阅读和复制

---

## 【编码规范参考】

【命名规范】
- 类：PascalCase（MyClass）
- 函数/方法/变量：snake_case（my_function）
- 常量：UPPER_SNAKE_CASE（MAX_COUNT）
- 私有成员：_leading_underscore（_internal_state）
- 测试：test_<action>_<scenario>（test_retrieve_documents_with_query）

【类型注解强制要求】
def retrieve_documents(query: str, top_k: int = 5) -> List[Document]:
    """Retrieve documents from vector store.
    
    Args:
        query: Search query string.
        top_k: Number of results to return.
        
    Returns:
        List of retrieved documents.
        
    Raises:
        ValueError: If query is empty.
    """

【文件大小限制】
- 文件：< 300 行
- 类：< 250 行
- 方法：< 50 行

【禁止事项】
- ❌ print() → 使用 logging
- ❌ 硬编码依赖 → 使用依赖注入
- ❌ os.getenv() → 使用 ConfigManager
- ❌ 裸露 except → 捕获具体异常
- ❌ 阻塞 I/O → 使用 async/await

---

请开始审查，并生成详细的报告。
```

---

## 📌 使用方式

### 方式1：直接复制到 Copilot Chat
1. 复制上面的 Prompt
2. 打开 Copilot Chat（Ctrl+I）
3. 粘贴 Prompt
4. 等待 AI 生成报告

### 方式2：保存为文件（推荐）
已经为你创建了这个文件：`.temp/code-review-prompt.md`

可以：
- 直接在这个文件中编辑和使用
- 定期运行此审查
- 跟踪改进进展

### 方式3：针对特定文件审查
如果只想审查某个文件，修改 Prompt：
```
【项目位置】src/core/agent.py

【审查范围】仅审查此文件
```

---

## 🎯 一次性完整审查流程

```bash
# 1️⃣ 先运行自动工具
make verify

# 2️⃣ 如果有失败，查看具体错误
make format        # 查看格式问题
make lint          # 查看代码风格
make type-check    # 查看类型问题

# 3️⃣ 然后使用 Prompt 进行人工审查
# 复制上面的 Prompt 到 Copilot Chat

# 4️⃣ 根据报告修复问题
# 最后再运行一次 make verify 确保通过
```

---

## 💡 优化建议

如果 Prompt 太长，可以分两步：
1. **第一步**：只审查第一和第二层（核心问题）
2. **第二步**：针对具体文件进行深度审查

这样可以更快地得到反馈。
