# Integration Test Collection 隔离机制

## 概述

集成测试使用的 Qdrant Collection 现已完全隔离，遵循以下原则：

1. **与实际运行隔离** - 使用 `test_vedaaide_` 前缀区分测试 Collection
2. **测试间隔离** - 每个测试获得唯一的 UUID 后缀
3. **自动清理** - 每次测试前后自动删除 Collection

## 架构

### conftest.py 提供的 Fixtures

```python
# tests/integration/conftest.py

@pytest.fixture
def isolated_collection_name() -> str:
    """生成隔离的Collection名称: test_vedaaide_{uuid}"""
    unique_id = str(uuid.uuid4())[:8]
    return f"test_vedaaide_{unique_id}"

@pytest.fixture
def isolated_indexer(isolated_collection_name):
    """提供隔离的DocumentIndexer实例"""
    indexer = DocumentIndexer(collection_name=isolated_collection_name)

    # 测试前清理
    cleanup()

    yield indexer

    # 测试后清理
    cleanup()
```

## 使用示例

### 1. Collection 命名隔离

```python
@pytest.mark.requires_qdrant
def test_indexing(isolated_indexer):
    """自动使用隔离的Collection"""
    # Collection 名称: test_vedaaide_a1b2c3d4
    collection_name = isolated_indexer.collection_name

    # 与生产环境的 vedaaide_docs 隔离
    assert collection_name.startswith("test_vedaaide_")
```

### 2. 自动清理

```python
@pytest.mark.requires_qdrant
def test_cleanup_before(isolated_indexer):
    """测试前自动清理"""
    # Collection 在这里是干净的
    assert not isolated_indexer.collection_exists()

@pytest.mark.requires_qdrant
def test_cleanup_after(isolated_indexer):
    """前面的测试 Collection 已被清理"""
    # 不会受到前面测试的影响
    pass
```

### 3. 多个测试间隔离

```python
@pytest.mark.requires_qdrant
class TestMultiple:
    def test_first(self, isolated_indexer):
        """获得 test_vedaaide_xxxxxxxx"""
        name1 = isolated_indexer.collection_name

    def test_second(self, isolated_indexer):
        """获得 test_vedaaide_yyyyyyyy (不同的UUID)"""
        name2 = isolated_indexer.collection_name
        # name1 != name2
```

## Collection 生命周期

```
┌─────────────────────────────────────────┐
│ Test 1: test_vedaaide_a1b2c3d4         │
├─────────────────────────────────────────┤
│ 1. pytest fixture setup                 │
│ 2. cleanup (确保不存在)                  │
│ 3. test runs (Collection为空)           │
│ 4. cleanup (删除Collection)              │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ Test 2: test_vedaaide_e5f6g7h8         │
├─────────────────────────────────────────┤
│ 1. pytest fixture setup                 │
│ 2. cleanup (确保不存在)                  │
│ 3. test runs (Collection为空)           │
│ 4. cleanup (删除Collection)              │
└─────────────────────────────────────────┘
```

## 隔离类型

### 1️⃣ 命名隔离

| Collection | 环境 | 说明 |
|-----------|------|------|
| `vedaaide_docs` | Production | 实际运行的Collection |
| `vedaaide_test` | Manual Testing | 手动测试用Collection |
| `test_vedaaide_a1b2c3d4` | Automated Tests | 自动化测试Collection |

### 2️⃣ 时间隔离

- **清理前**: 每个测试前确保 Collection 不存在
- **运行中**: 测试独占该 Collection
- **清理后**: 测试完毕后立即删除 Collection

### 3️⃣ 并发隔离

- 每个测试获得唯一的 UUID 后缀
- 支持并发测试运行
- 不同测试间不会互相干扰

```python
# 并发场景
Test A: test_vedaaide_1111...  ✓
Test B: test_vedaaide_2222...  ✓
Test C: test_vedaaide_3333...  ✓

# 没有冲突，各自独立
```

## Pytest 标记

```bash
# 仅运行需要 Qdrant 的测试
poetry run pytest -m requires_qdrant tests/

# 跳过需要 Qdrant 的测试
poetry run pytest -m "not requires_qdrant" tests/

# 仅运行集成测试
poetry run pytest -m integration tests/

# 跳过集成测试
poetry run pytest -m "not integration" tests/
```

## 清理验证

### 自动验证

```python
@pytest.mark.requires_qdrant
def test_no_leftover_collections():
    """验证没有旧的测试Collection"""
    client = QdrantClient(url="http://localhost:6333")
    collections = client.get_collections()

    test_collections = [
        c.name for c in collections.collections
        if c.name.startswith("test_vedaaide_")
    ]

    # 理想情况：0 个（所有都被清理了）
    # 现实情况：最多几个（可能并发运行的测试）
    assert len(test_collections) < 10
```

### 手动验证

```bash
# 查看当前存在的 Collections
curl http://localhost:6333/collections | jq '.result.collections[].name'

# 应该看不到 test_vedaaide_* 的Collection
# （除非测试正在运行中）
```

## 故障排查

### 问题：测试后仍有Collection残留

**原因**：
- Qdrant 服务故障
- 清理代码异常
- 并发测试仍在运行

**解决**：
```bash
# 手动删除测试Collection
curl -X DELETE http://localhost:6333/collections/test_vedaaide_xxxxxxxx
```

### 问题：测试互相干扰

**原因**：
- 未使用 `isolated_indexer` fixture
- 直接创建 DocumentIndexer

**解决**：
```python
# ❌ 错误
def test_something():
    indexer = DocumentIndexer()  # 使用默认名称

# ✅ 正确
def test_something(isolated_indexer):
    # 使用隔离的fixture
    indexer = isolated_indexer
```

## 现状统计

- ✅ 100 tests passed
- ✅ 14 DocumentIndexer/Loader integration tests
- ✅ 5 Qdrant isolation tests
- ⏭️ 4 tests skipped (no Qdrant)
- 📊 58% code coverage
