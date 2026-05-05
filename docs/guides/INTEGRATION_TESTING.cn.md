# VedaAide 集成测试架构

## 概述

VedaAide 实现了全面的集成测试策略，清晰地区分**单元测试**（模拟依赖）和**集成测试**（真实服务/数据）。

### 为什么要分离单元测试和集成测试？

| 方面 | 单元测试 | 集成测试 |
|------|--------|--------|
| **目的** | 验证逻辑隔离 | 验证系统组件协同工作 |
| **依赖** | 全部模拟 | 真实服务/数据 |
| **执行时间** | 快速（~100ms每个） | 较慢（~1-5s每个） |
| **CI/CD** | 总是运行 | 有条件运行 |
| **价值** | 高（提前发现bugs） | 关键（确保真实环境工作） |

**要避免的反模式**：完全模拟的集成测试失去了集成测试的价值，同时增加测试维护负担。

## 目录结构

```
tests/
├── unit/                                    # 模拟单元测试
│   ├── test_indexer.py                     # DocumentIndexer单元测试
│   ├── test_deidentification.py            # 去标识化单元测试
│   └── ...
├── integration/                            # 真实服务集成测试
│   ├── conftest.py                         # Fixtures和pytest配置
│   ├── test_data/                          # 真实测试数据
│   │   ├── resumes.json                    # 示例简历
│   │   └── job_postings.json               # 示例职位
│   ├── core/
│   │   └── retrieval/
│   │       └── test_document_loader_and_indexer.py  # 19个集成测试
│   └── ...
└── common/
    └── check_dependencies.py               # 可重用依赖检查
```

## 单元测试：使用模拟

位于 `tests/unit/`，这些测试模拟所有外部依赖：

```python
# tests/unit/test_indexer.py
@patch("src.core.retrieval.document_indexer.QdrantClient")
@patch("src.core.retrieval.document_indexer.embed_and_index")
def test_indexing_with_mocks(mock_embed, mock_qdrant):
    """单元测试：验证索引逻辑隔离"""

    indexer = DocumentIndexer(collection_name="test_vedaaide_unit")

    # 所有外部调用都被模拟
    indexer.embed_and_index(documents=[...])

    # 验证模拟被正确调用
    mock_embed.assert_called_once()
```

**优点**:
- ✅ 快速执行（~50ms）
- ✅ 无外部服务依赖
- ✅ 结果确定
- ✅ 适合CI/CD

**局限**:
- ❌ 不测试真实Qdrant集成
- ❌ 不能发现真实embedding失败
- ❌ 可能遗漏数据类型不匹配

## 集成测试：使用真实服务

位于 `tests/integration/`，这些测试使用真实服务：

```python
# tests/integration/core/retrieval/test_document_loader_and_indexer.py
@pytest.mark.integration
@pytest.mark.requires_qdrant
def test_full_indexing_pipeline(isolated_indexer, test_data_dir):
    """集成测试：验证端到端索引工作"""

    # 加载真实数据
    documents = DocumentLoader().load_from_directory(
        directory=test_data_dir / "resumes.json"
    )

    # 索引到真实Qdrant
    indexed_docs = isolated_indexer.index_documents(documents)

    # 验证真实结果
    assert len(indexed_docs) == 3
    collection_stats = isolated_indexer.get_collection_stats()
    assert collection_stats.vector_count > 0
```

**优点**:
- ✅ 测试真实embedding质量
- ✅ 测试真实Qdrant操作
- ✅ 发现数据类型不匹配
- ✅ 确保端到端工作流

**权衡**:
- ⏱️ 执行较慢（~2-5s每个）
- 🔗 需要Qdrant服务运行
- 🔄 可能有间歇性失败

## Collection 隔离模式

### 问题：防止测试相互干扰

多个并发测试可能：
1. 使用相同的Collection名称 → 数据损坏
2. 留下过时的Collections → 清理开销
3. 与生产数据干扰 → 灾难

### 解决方案：唯一、隔离的Collections

#### 1. 生成唯一的Collection名称

```python
# tests/integration/conftest.py
@pytest.fixture
def isolated_collection_name() -> str:
    """生成隔离的collection: test_vedaaide_{uuid}"""
    unique_id = str(uuid.uuid4())[:8]
    return f"test_vedaaide_{unique_id}"
```

**格式**: `test_vedaaide_a1b2c3d4`

| 部分 | 示例 | 目的 |
|------|------|------|
| 前缀 | `test_vedaaide_` | 标识为自动化测试collection |
| UUID | `a1b2c3d4` | 为每个测试运行确保唯一性 |

#### 2. 自动清理

```python
@pytest.fixture
def isolated_indexer(isolated_collection_name):
    """提供隔离的indexer和自动清理"""
    indexer = DocumentIndexer(collection_name=isolated_collection_name)

    # 测试前清理
    try:
        indexer._delete_collection()
    except:
        pass  # Collection可能还不存在

    yield indexer  # 测试在这里运行

    # 测试后清理
    try:
        indexer._delete_collection()
    except:
        pass  # 服务可能无效，这没关系
```

**清理时机**:
- **之前**: 确保干净的状态
- **之后**: 防止测试数据污染

### 命名约定示例

```
生产环境:
  vedaaide_docs              ← 真实生产collection

开发环境:
  vedaaide_dev              ← 手动测试collection

自动化测试:
  test_vedaaide_a1b2c3d4    ← 测试运行1
  test_vedaaide_e5f6g7h8    ← 测试运行2
  test_vedaaide_i9j0k1l2    ← 测试运行3（并发）
```

## 依赖检查

### 问题：优雅地处理缺失的服务

当所需服务不可用时，测试应该跳过，而不是失败：

```python
# ❌ 坏：硬失败
def test_indexing():
    client = QdrantClient(url="http://localhost:6333")
    # → 如果Qdrant未运行则ConnectionError

# ✅ 好：优雅跳过
@pytest.mark.requires_qdrant
def test_indexing(isolated_indexer):
    # → 如果Qdrant不可用则自动跳过
```

### 实现

```python
# tests/common/check_dependencies.py
class DependencyError(Exception):
    """当服务不可用时抛出"""
    pass

def check_qdrant_availability(url: str = "http://localhost:6333",
                             timeout: int = 2) -> bool:
    """检查Qdrant是否健康"""
    try:
        response = requests.get(f"{url}/health", timeout=timeout)
        return response.status_code == 200
    except:
        return False
```

### pytest配置

```python
# tests/integration/conftest.py
def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "requires_qdrant: 标记为需要Qdrant服务的测试"
    )
    config.addinivalue_line(
        "markers",
        "integration: 标记为集成测试"
    )
```

### 使用方式

```bash
# 如果Qdrant不可用则跳过
poetry run pytest tests/integration/ -m requires_qdrant

# 仅运行集成测试
poetry run pytest tests/ -m integration

# 显示跳过的测试
poetry run pytest tests/ -v | grep SKIPPED
```

## 测试数据组织

```
tests/integration/test_data/
├── resumes.json                    # 3个现实样本简历
├── job_postings.json               # 3个现实样本职位
└── README.md                       # 数据源文档
```

### 示例数据格式

**resumes.json**:
```json
{
  "id": "resume_001",
  "name": "张三",
  "content": "...",
  "metadata": {
    "source": "test_data",
    "format": "json"
  }
}
```

**job_postings.json**:
```json
{
  "id": "job_001",
  "title": "软件工程师",
  "content": "...",
  "metadata": {
    "source": "test_data",
    "format": "json"
  }
}
```

## Pytest标记

```python
@pytest.mark.integration           # 集成测试（真实服务）
@pytest.mark.requires_qdrant       # 需要Qdrant服务
@pytest.mark.requires_ollama       # 需要Ollama服务
@pytest.mark.requires_azure_openai # 需要Azure OpenAI凭证
```

### 按标记运行测试

```bash
# 所有集成测试
poetry run pytest -m integration

# 仅Qdrant集成测试
poetry run pytest -m "integration and requires_qdrant"

# 排除集成测试
poetry run pytest -m "not integration"

# 显示可用的标记
poetry run pytest --markers
```

## 当前测试套件状态

### 测试数量

| 类别 | 数量 | 状态 |
|------|------|------|
| 单元测试 | 81 | ✅ 81个通过 |
| 集成测试 | 19 | ✅ 19个通过 |
| 总计 | 100 | ✅ 全部通过 |
| 跳过 | 4 | ⏭️ 缺少服务 |

### 代码覆盖率

```
src/core/
├── data/
│   ├── deidentifier.py          87%  ✅ 很好
│   ├── document_loader.py       64%  ✅ 可接受
│   └── document_record.py       45%  ⚠️ 需要更多测试
└── retrieval/
    └── document_indexer.py      84%  ✅ 很好

总体: 58% 代码覆盖率
```

## 最佳实践

### ✅ 应该做

1. **为Qdrant操作使用 `isolated_indexer` fixture**:
   ```python
   def test_indexing(isolated_indexer):  # ✅ 正确
       collection_name = isolated_indexer.collection_name
   ```

2. **在集成测试中加载真实数据**:
   ```python
   @pytest.mark.requires_qdrant
   def test_document_loading(test_data_dir):
       loader = DocumentLoader()
       docs = loader.load_from_directory(test_data_dir)  # ✅ 真实文件
   ```

3. **正确标记测试**:
   ```python
   @pytest.mark.integration
   @pytest.mark.requires_qdrant
   def test_indexing():  # ✅ 清晰的意图
       pass
   ```

4. **根据真实期望检查结果**:
   ```python
   stats = indexer.get_collection_stats()
   assert stats.vector_count > 0  # ✅ 验证真实输出
   ```

### ❌ 不应该做

1. **混合单元和集成测试**:
   ```python
   # ❌ 错误：集成测试中有模拟
   @pytest.mark.integration
   @patch("QdrantClient")
   def test_indexing(mock_client):
       pass
   ```

2. **使用硬编码的Collection名称**:
   ```python
   # ❌ 错误：测试碰撞
   def test_first(isolated_indexer):
       indexer = DocumentIndexer(collection_name="test_vedaaide_fixed")

   def test_second(isolated_indexer):
       indexer = DocumentIndexer(collection_name="test_vedaaide_fixed")
       # 相同的collection名称 → 干扰
   ```

3. **跳过清理**:
   ```python
   # ❌ 错误：Collection污染
   @pytest.fixture
   def my_indexer():
       indexer = DocumentIndexer(collection_name="test")
       yield indexer
       # 无清理 → 残留
   ```

4. **加载假数据/模拟数据**:
   ```python
   # ❌ 错误：失去集成测试价值
   @pytest.mark.integration
   @patch("DocumentLoader")
   def test_indexing(mock_loader):
       mock_loader.return_value = [MagicMock()]  # 假数据
   ```

## 故障排查

### 问题："Qdrant不可用"

```bash
# 通过Docker Compose启动Qdrant
docker-compose up -d qdrant

# 验证正在运行
curl http://localhost:6333/health

# 重新运行测试
poetry run pytest tests/integration/
```

### 问题："Collection已存在"

**症状**: `QdrantException: status code 400, ...collection_name...already exists`

**原因**: 前面的测试没有正确清理

**解决方案**:
```bash
# 手动删除孤立的collections
curl -X DELETE http://localhost:6333/collections/test_vedaaide_old

# 或运行清理并重试
poetry run pytest tests/integration/ --cleanup-orphans
```

### 问题：测试超时失败

**原因**: Embedding服务缓慢或不可用

**解决方案**:
```bash
# 使用本地Ollama而不是Azure OpenAI
export EMBEDDING_PROVIDER=ollama
poetry run pytest tests/integration/

# 或增加超时
poetry run pytest tests/integration/ --timeout=30
```

## 后续步骤

- 📊 将DocumentRecord覆盖率从45%增加到70%+
- 🧪 添加更多真实场景测试（大型数据集、PDF解析）
- 🔄 实现CI/CD与条件集成测试运行
- 📈 为索引操作添加性能基准测试
