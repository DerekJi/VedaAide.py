# 开发环境设置指南

本指南将帮助你完成 VedaAide 开发环境的配置。

## 前置条件

- Python 3.9 或更高版本
- Poetry（依赖管理工具）
- Git
- Make（可选，但推荐使用）

## 安装步骤

### 1. 克隆仓库

```bash
git clone <repository-url>
cd VedaAide.py
```

### 2. 安装 Poetry

如果你还没有安装 Poetry：

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Windows PowerShell:
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

验证安装：
```bash
poetry --version
```

### 3. 安装项目依赖

```bash
poetry install
```

这个命令会：
- 创建虚拟环境
- 安装 `pyproject.toml` 中列出的所有依赖
- 安装开发工具（ruff、mypy、pytest 等）

### 4. (可选) 设置 Pre-commit Hooks

为了在提交代码前自动检查代码质量：

```bash
make pre-commit
# 或手动：
poetry run pre-commit install
```

## 开发工作流程

### 运行代码质量检查

```bash
# 运行所有检查（代码检查 + 格式化 + 类型检查 + 测试）
make verify

# 或单毯运行：
make format       # 自动格式化代码（ruff format）
make lint         # 检查代码风格（ruff check）
make type-check   # 检查类型（mypy）
make test         # 运行测试并生成覆盖率报告
```

### 编写代码

1. **创建新分支**：
   ```bash
   git checkout -b feature/my-feature
   ```

2. **按照 [Python 编码规范](.github/instructions/coding-standards.instructions.md) 编写代码**

3. **格式化代码**：
   ```bash
   make format
   ```

4. **在提交前检查代码质量**：
   ```bash
   make verify
   ```

5. **提交代码**：
   ```bash
   git add .
   git commit -m "feat: add my feature"
   ```

6. **推送并创建 Pull Request**：
   ```bash
   git push origin feature/my-feature
   ```

## 项目结构

```
VedaAide.py/
├── src/                          # 源代码
│   └── core/
│       ├── data/                 # 数据加载模块
│       └── retrieval/            # 检索和反识别模块
├── scripts/                      # 工具脚本
│   └── data/                     # 数据生成脚本
├── tests/                        # 测试套件
│   └── unit/
├── docs/                         # 文档
│   ├── guides/
│   ├── planning/
│   └── architecture/
├── infra/                        # 基础设施配置
├── .github/                      # GitHub 配置
│   ├── instructions/             # 开发指南
│   ├── skills/                   # 可复用的技能模块
│   └── workflows/                # CI/CD 工作流
├── pyproject.toml               # 项目配置
├── Makefile                     # 开发命令
└── README.md                    # 项目说明
```

## 常见任务

### 运行测试

```bash
# 运行所有测试
poetry run pytest

# 运行特定测试文件
poetry run pytest tests/unit/test_deidentification.py

# 运行并生成覆盖率报告
poetry run pytest --cov=src

# 监视模式（需要 pytest-watch）
poetry run ptw
```

### 类型检查

```bash
# 检查 src/ 的类型
poetry run mypy src

# 检查特定文件
poetry run mypy src/core/retrieval/deidentifier.py
```

### 代码格式化

```bash
# 格式化所有 Python 文件
make format

# 格式化特定目录
poetry run ruff format src/core/data/
```

### 运行数据生成脚本

```bash
# 运行演示生成脚本（基础示例）
poetry run python scripts/data/demo_generation.py

# 运行高级配置
poetry run python -m scripts.data.advanced_generator --help
```

## 编码规范

### 类型提示（强制）

所有函数必须有完整的类型提示：

```python
# ✅ 正确
def retrieve_documents(query: str, top_k: int = 5) -> List[Document]:
    """检索与查询匹配的前K个文档。"""
    ...

# ❌ 错误
def retrieve_documents(query, top_k=5):
    ...
```

### 文档字符串（Google 风格，强制）

所有公共函数和类必须有文档字符串：

```python
def process_resume(resume_data: Dict[str, Any]) -> Resume:
    """处理并验证简历数据。

    Args:
        resume_data: 原始简历数据字典。

    Returns:
        处理后的 Resume 对象。

    Raises:
        ValueError: 如果简历数据无效。
    """
    ...
```

### 文件大小

- 目标：**< 200 行每个文件**
- 最大：**300 行每个文件**
- 超过 300 行时必须拆分

更多详情见 [编码规范](../.github/instructions/coding-standards.instructions.md)。

## 常见问题排除

### Windows Bash 中 Python 未找到

如果在 Git Bash 中出现"Python was not found"错误：

```bash
# 使用 Poetry 运行 Python
poetry run python --version

# 或使用完整路径
/c/Program\ Files/Python311/python --version
```

详见 [Windows 开发设置指南](.github/instructions/windows-dev-setup.instructions.md)。

### 虚拟环境问题

```bash
# 重新创建虚拟环境
poetry env remove python3.11
poetry install

# 显示当前环境信息
poetry env info
```

### Poetry 锁定文件问题

```bash
# 更新锁定文件
poetry lock --no-update

# 从头重建锁定文件
poetry lock --no-cache
```

## 编辑器配置

### VS Code

推荐安装以下扩展：
- Python
- Pylance
- Ruff
- autoDocstring

创建 `.vscode/settings.json`：
```json
{
    "python.linting.enabled": true,
    "python.formatting.provider": "none",
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll": "explicit"
        }
    },
    "editor.rulers": [100]
}
```

### PyCharm

1. Settings → Project → Python Interpreter
2. 选择 Poetry 解释器
3. Settings → Editor → Code Style → Python
   - 行长度：100
   - 制表符大小：4

## 获取帮助

- 查看 [编码规范](.github/instructions/coding-standards.instructions.md)
- 查看 `tests/` 中的现有测试了解示例
- 查看 `docs/` 中的项目文档
- 在项目讨论或 Issues 中提问

## 下一步

配置完成后，考虑以下步骤：

1. 阅读 [项目背景](.github/instructions/project-context.instructions.md)
2. 查看 [编码规范](.github/instructions/coding-standards.instructions.md)
3. 探索 `src/` 中的现有代码
4. 运行演示脚本：`poetry run python scripts/data/demo_generation.py`
5. 运行测试：`make test`
