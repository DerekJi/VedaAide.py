# Integration Test 快速参考指南

## 📋 快速命令

```bash
# 运行所有测试
poetry run pytest tests/ -v

# 运行集成测试
poetry run pytest tests/integration/ -v

# 运行单元测试
poetry run pytest tests/unit/ -v

# 仅运行需要Qdrant的集成测试
poetry run pytest -m requires_qdrant tests/integration/ -v

# 并发运行测试（8个进程）
poetry run pytest tests/ -n 8

# 显示覆盖率
poetry run pytest tests/ --cov=src --cov-report=html

# 查看具体隔离测试
poetry run pytest tests/integration/core/retrieval/test_document_loader_and_indexer.py::TestQdrantWithIsolatedCollections -v
```

## 🎯 何时使用什么

### 写单元测试

```python
# 文件: tests/unit/test_myfeature.py
from unittest.mock import patch, MagicMock

@patch("src.core.retrieval.document_indexer.QdrantClient")
def test_indexing_logic(mock_qdrant):
    """测试逻辑，模拟外部依赖"""
    indexer = DocumentIndexer()
    # ... 测试代码
```

### 写集成测试

```python
# 文件: tests/integration/core/retrieval/test_myfeature.py
@pytest.mark.integration
@pytest.mark.requires_qdrant
def test_full_workflow(isolated_indexer, test_data_dir):
    """测试真实端到端流程"""
    loader = DocumentLoader()
    docs = loader.load_from_directory(test_data_dir)
    # ... 测试代码，使用isolated_indexer
```

## 📊 隔离机制一览

| 功能 | 代码 | 说明 |
|------|------|------|
| 生成隔离名称 | `isolated_collection_name` | Fixture返回`test_vedaaide_uuid` |
| 使用隔离indexer | `isolated_indexer` | Fixture提供自动清理的indexer |
| 获取测试数据 | `test_data_dir` | Fixture返回tests/integration/test_data/ |
| 获取Qdrant客户端 | `qdrant_client` | Fixture提供，不可用时跳过 |

## 🏗️ 常见任务

### 添加新的集成测试

```python
# 1. 在 tests/integration/core/ 下创建文件
# tests/integration/core/data/test_myloader.py

@pytest.mark.integration
@pytest.mark.requires_qdrant
class TestMyLoader:
    def test_feature_1(self, isolated_indexer, test_data_dir):
        """测试特性1"""
        # 使用 isolated_indexer 和 test_data_dir
        pass

    def test_feature_2(self, isolated_indexer):
        """测试特性2"""
        # 自动生成唯一的collection名称
        # 测试前后自动清理
        pass
```

### 调试隔离Collection

```bash
# 1. 启动Qdrant
docker-compose up -d qdrant

# 2. 查看当前collections
curl http://localhost:6333/collections | jq

# 3. 运行测试
poetry run pytest tests/integration/test_*.py -v

# 4. 验证collections是否被清理
curl http://localhost:6333/collections | jq
# 不应该有 test_vedaaide_* 的collections

# 5. 手动删除孤立collections
curl -X DELETE http://localhost:6333/collections/test_vedaaide_old
```

### 添加新的测试数据

```bash
# 1. 将JSON文件放在 tests/integration/test_data/
# 文件: tests/integration/test_data/my_data.json
# 格式: [{"id": "...", "content": "...", "metadata": {...}}, ...]

# 2. 在测试中使用
def test_with_my_data(test_data_dir):
    loader = DocumentLoader()
    docs = loader.load_documents(test_data_dir / "my_data.json")
    assert len(docs) > 0
```

## 🔍 故障排查速查表

| 问题 | 症状 | 解决方案 |
|------|------|--------|
| Qdrant不可用 | 测试被SKIPPED | 运行`docker-compose up -d qdrant` |
| Collection已存在 | 400错误 | 手动删除或清理孤立collections |
| 测试超时 | Timeout错误 | 检查embedding服务，增加timeout |
| 测试互干扰 | 不稳定 | 确保使用`isolated_indexer` fixture |
| 覆盖率低 | <50% | 添加更多集成测试用例 |

## 📁 关键文件位置

```
tests/
├── unit/                     # 单元测试（模拟）
├── integration/              # 集成测试（真实）
│   ├── conftest.py          # ⭐ 隔离fixtures定义
│   ├── test_data/
│   │   ├── resumes.json     # ⭐ 样本简历
│   │   └── job_postings.json # ⭐ 样本职位
│   └── core/
│       └── retrieval/
│           └── test_document_loader_and_indexer.py  # ⭐ 隔离验证测试
└── common/
    └── check_dependencies.py  # ⭐ 依赖检查模块

docs/
├── guides/
│   ├── INTEGRATION_TESTING.md   # ⭐ 详细文档（英文）
│   └── INTEGRATION_TESTING.cn.md # ⭐ 详细文档（中文）

.temp/
└── integration-isolation-completion-report.md  # ⭐ 完成报告
```

## ✨ 关键概念速记

### Collection隔离四柱

1. **命名隔离**: `test_vedaaide_{uuid}` vs `vedaaide_docs`
2. **时间隔离**: 清理前 → 运行 → 清理后
3. **并发隔离**: 每个测试唯一UUID，支持-n并发
4. **依赖隔离**: 缺服务时优雅跳过

### 两类测试对比

```
单元测试 (tests/unit/)
├─ 模拟所有外部依赖
├─ 快速（~50ms）
├─ 适合CI/CD
└─ 验证逻辑正确性

集成测试 (tests/integration/)
├─ 使用真实服务
├─ 较慢（~2-5s）
├─ 需要环境
└─ 验证端到端工作
```

## 🚀 快速开始

### 第一次运行

```bash
# 1. 启动依赖
docker-compose up -d

# 2. 验证Qdrant
curl http://localhost:6333/health

# 3. 运行所有测试
poetry run pytest tests/ -v

# 4. 查看覆盖率
open htmlcov/index.html
```

### 日常开发

```bash
# 写代码
# ... 修改 src/core/...

# 运行相关单元测试
poetry run pytest tests/unit/test_myunit.py -v

# 运行相关集成测试
poetry run pytest tests/integration/core/test_myintegration.py -v

# 检查全量通过
poetry run pytest tests/ -q
```

## 📞 故障快速代码

```bash
# 重置所有测试collections
curl http://localhost:6333/collections | jq -r '.result.collections[].name' | \
  grep "test_vedaaide_" | \
  xargs -I {} curl -X DELETE http://localhost:6333/collections/{}

# 显示所有test collections
curl http://localhost:6333/collections | jq '.result.collections[] | select(.name | startswith("test_vedaaide_"))'

# 实时监控collection数量
watch -n 1 'curl -s http://localhost:6333/collections | jq ".result.collections | length"'
```

## 📚 进阶参考

完整详情参见：
- 📖 [INTEGRATION_TESTING.md](docs/guides/INTEGRATION_TESTING.md) - 详细架构说明
- 📖 [COLLECTION_ISOLATION.md](tests/integration/COLLECTION_ISOLATION.md) - 隔离机制详解
- 📝 [完成报告](.temp/integration-isolation-completion-report.md) - 实现细节

---

**最后更新**: 2026-04-22
**状态**: ✅ 完成验证

**快速链接**:
- 🔧 [如何运行测试](#快速命令)
- 🎯 [何时使用什么](#何时使用什么)
- 🐛 [故障排查](#故障排查速查表)
- 📍 [关键文件](#关键文件位置)
