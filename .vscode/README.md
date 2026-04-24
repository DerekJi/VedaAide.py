# VS Code 配置说明

本目录包含 VedaAide.py 项目的 VS Code 工作区配置。

## 文件说明

### `settings.json`

- **Pylance**: 启用 Python 类型检查
- **pylint**: 代码风格检查
- **mypy**: 严格类型检查
- **Black**: 代码格式化（100 字符行长）
- **isort**: Import 自动排序

### `extensions.json`

推荐安装的 VS Code 扩展：

- Python 官方扩展
- Pylance（类型检查）
- Ruff（快速 linter）
- GitLens（Git 集成）

### `launch.json`

调试配置：

- 调试当前文件
- 运行测试
- 运行特定测试

## 问题诊断说明

### 能在 IDE 中看到的问题：

✅ **Type Hints 缺失** - Pylance/mypy 会显示红色波浪线  
✅ **Line Length > 100** - 在第 100 列会显示标尺  
✅ **未使用的导入** - Pylance 会标记  
✅ **类型不匹配** - Pylance/mypy 会显示错误

### 看不到的问题（需要运行检查工具）：

❌ **print() 使用** - 仅自定义检查工具能检查  
❌ **File Size > 300 行** - 仅自定义检查工具能检查

运行这些命令来检查：

```bash
make audit      # 完整代码审查
make format     # 自动格式化
make verify     # 验证所有检查通过
```

## 首次使用

1. **重启 VS Code** 或按 `Ctrl+Shift+P` → `Developer: Reload Window`
2. **安装扩展**：VS Code 会提示安装推荐的扩展（click "Install All"）
3. **等待索引**：Pylance 会进行初始代码分析（几秒钟）
4. **查看问题**：`View` → `Problems` 或按 `Ctrl+Shift+M`

## 快捷键

- `Shift+Alt+F` - 格式化当前文件
- `Ctrl+K Ctrl+X` - 删除末尾空格
- `Ctrl+Shift+M` - 显示问题面板
- `F5` - 开始调试
