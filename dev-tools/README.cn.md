# Translation Tools

自动翻译目录中的markdown文件。支持两种方案：

## 🔹 方案1：translate_with_ollama.py（推荐 ⭐）

使用本地 **Ollama 模型** 进行翻译（完全离线）。

### 特点
- ✅ 完全本地离线运行
- ✅ 隐私保护，数据不离机器
- ✅ 翻译质量高（支持大模型）
- ❌ 需要 Ollama 服务运行
- ❌ 翻译较慢（30-60秒/文件）
- ❌ 需要大模型（4-19GB）

### 快速开始

```bash
# 启动 Ollama 服务（在另一个终端）
ollama serve

# 翻译目录中所有 .md 文件
python translate_with_ollama.py .github/prompts

# 指定使用特定模型
python translate_with_ollama.py .github/prompts --model deepseek-r1:32b

# 干跑模式（不保存变更）
python translate_with_ollama.py .github/prompts --dry-run
```

### 推荐模型

脚本会按优先级自动选择可用的模型：

| 模型 | 大小 | 翻译质量 | 速度 | 备注 |
|------|------|--------|------|------|
| `deepseek-r1:32b` | 19 GB | ⭐⭐⭐ | 慢 | 最佳质量（需要 50GB内存） |
| `qwen2.5-coder:7b` | 4.7 GB | ⭐⭐ | 中等 | ✅ **推荐**（内存紧张时使用） |
| `llama3.2:latest` | 2.0 GB | ⭐⭐ | 快 | 快速翻译 |
| `qwen3:8b` | 5.2 GB | ⭐⭐ | 中等 | 多语言支持 |

**当前系统使用**：`qwen2.5-coder:7b`（自动选择，因为内存限制）

---

## 🔹 方案2：translate.py

使用 **translatepy**（在线翻译服务）。

### 特点
- ✅ 快速翻译（几秒/文件）
- ✅ 无需大模型
- ✅ 设置简单
- ❌ 需要网络连接
- ❌ 隐私：数据经过第三方服务
- ❌ 翻译质量取决于后端服务

### 快速开始

```bash
# 安装依赖
pip install -r dev-tools/requirements.txt

# 翻译目录
python translate.py .github/prompts

# 干跑模式
python translate.py .github/prompts --dry-run
```

### 完整选项

```
positional arguments:
  directory             需要翻译的目录

optional arguments:
  --lang LANG          目标语言代码（默认：en）
  --ext EXT            文件扩展名（默认：.md）
  --dry-run            干跑模式，不保存变更
  -h, --help           显示帮助信息
```

---

## 特性对比

| 特性 | Ollama | translatepy |
|------|--------|-------------|
| 离线运行 | ✅ | ❌ |
| 翻译质量 | ⭐⭐⭐ | ⭐⭐ |
| 速度 | 慢 | 快 |
| 隐私 | ✅ | ❌ |
| 依赖配置 | 复杂 | 简单 |
| 模型大小 | 4-19GB | 无需 |

---

## 工作流程

### Ollama 工作流程

1. **启动Ollama服务** - `ollama serve`
2. **检查Ollama状态** - 脚本自动验证
3. **模型选择** - 自动选择最佳可用模型
4. **文件扫描** - 找到目录中所有需要翻译的文件
5. **中文检测** - 跳过不包含中文的文件
6. **分块翻译** - 对大文件进行分块处理（2000字符/块）
7. **保存结果** - 覆盖原文件或干跑模式预览

### translatepy 工作流程

1. **文件扫描** - 找到目录中所有需要翻译的文件
2. **中文检测** - 跳过不包含中文的文件
3. **在线翻译** - 调用 translatepy（使用 Google、Bing 等后端）
4. **保存结果** - 覆盖原文件或干跑模式预览

---

## 使用示例

### 例1：使用 Ollama 翻译 VedaAide 项目

```bash
cd /path/to/VedaAide.py

# 终端1：启动 Ollama
ollama serve

# 终端2：运行翻译脚本
python dev-tools/translate_with_ollama.py .github/prompts
```

输出示例：
```
Checking Ollama service... ✓
Using model: deepseek-r1:32b

Found 5 .md file(s) to translate

[1/5] cloud-native.md
  Translating chunk 1/3... ✓
  Translating chunk 2/3... ✓
  Translating chunk 3/3... ✓
  ✓ Saved

[2/5] rag-development.md
  Skipped (no Chinese content)

[3/5] evaluation-strategy.md
  Translating chunk 1/2... ✓
  Translating chunk 2/2... ✓
  ✓ Saved

Summary: 3/5 files processed successfully
```

### 例2：使用 translatepy 翻译（快速模式）

```bash
python dev-tools/translate.py .github/prompts
```

### 例3：翻译特定文件类型

```bash
# 翻译 .cn.md 文件
python dev-tools/translate_with_ollama.py docs/planning --ext .cn.md

# 使用特定模型
python dev-tools/translate_with_ollama.py docs/planning --ext .cn.md --model qwen2.5-coder:7b
```

### 例4：干跑模式预览（不保存）

```bash
python dev-tools/translate_with_ollama.py .github/prompts --dry-run
```

---

## 故障排查

### Ollama 相关

#### 问题：Ollama 服务连接失败

```bash
# 启动 Ollama 服务
ollama serve

# 在另一个终端验证 Ollama 运行
curl http://localhost:11434/api/tags
```

#### 问题：模型不可用

```bash
# 查看已安装模型
ollama list

# 拉取推荐模型
ollama pull deepseek-r1:32b
ollama pull qwen2.5-coder:7b
```

#### 问题：翻译效果不理想

尝试使用性能更好的模型：
```bash
python dev-tools/translate_with_ollama.py <dir> --model deepseek-r1:32b
```

#### 问题：文件太大，翻译超时

程序自动分块处理（2000字符/块）。如果仍然超时，手动分割文件后重新翻译。

### translatepy 相关

#### 问题：网络连接失败

```bash
# 检查网络连接
ping google.com

# 尝试重新运行（可能是网络不稳定）
python dev-tools/translate.py <dir>
```

#### 问题："No service has returned a valid result"

translatepy 所有翻译后端（Google、Bing等）都不可用，通常由以下原因引起：
- 网络连接问题
- 被翻译服务限流
- 翻译服务暂时不可用

**解决方案**：切换到 Ollama 方案

---

## 注意事项

- ⚠️ 翻译后会**覆盖原文件**，建议先备份重要文件
- ⚠️ 使用 `--dry-run` 预览效果后再正式运行
- ⚠️ Ollama 翻译较慢（30-60秒/文件），耐心等待
- ⚠️ translatepy 需要网络连接
- ⚠️ 翻译质量取决于选定的方案

---

## 开发者笔记

### 文件列表

```
dev-tools/
├── translate_with_ollama.py  # Ollama 翻译工具（推荐）
├── translate.py              # translatepy 翻译工具（快速）
├── requirements.txt          # 依赖配置（用于 translate.py）
└── README.md                 # 本文档
```

### 配置参数

**Ollama 工具**:
- 温度设置（Temperature）：0.3 用于提高翻译一致性
- API 超时：120秒/请求
- 分块大小：2000字符/块

**translatepy 工具**:
- 自动重试：内置重试机制
- 文件编码：UTF-8
- 支持的目标语言：所有 ISO 639-1 代码

### 两个工具的选择建议

**使用 Ollama 如果**:
- 你想要最好的翻译质量
- 你关心数据隐私
- 你不在乎等待时间
- 你有足够的磁盘空间（4-19GB）

**使用 translatepy 如果**:
- 你想要快速翻译
- 网络连接稳定
- 翻译质量要求不高
- 你想要最简单的设置
