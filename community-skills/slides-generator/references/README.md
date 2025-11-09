# References 导航

按需加载的参考文档目录。

## 目录结构

```
references/
├── workflows/          # 工作流程文档
├── specs/              # 规范文档
├── guides/             # 指南文档
└── slidev-docs/        # Slidev 官方文档 (81个)
```

## 工作流程 (workflows/)

按需加载详细的工作流程说明。

| 文档 | 说明 | 使用场景 |
|------|------|---------|
| `material-collection.md` | 素材获取流程 | 需要搜索和收集资料时 |
| `content-generation.md` | 内容生成策略 | 生成幻灯片内容时 |
| `validation-workflow.md` | 验证工作流程 | 运行验证脚本和处理反馈时 |

## 规范文档 (specs/)

按需加载规范和检查清单。

| 文档 | 说明 | 使用场景 |
|------|------|---------|
| `slidev-core-rules.md` | Slidev 核心规则 | 生成 Markdown 时 |
| `validation-checklist.md` | 规范检查清单 | 验证输出时 |

## 指南文档 (guides/)

按需加载快速参考和索引。

| 文档 | 说明 | 使用场景 |
|------|------|---------|
| `slidev-quickref.md` | Slidev 快速参考 | 快速查阅语法时 |
| `slidev-config.md` | 配置参数指南 | 调整字体、样式、布局等配置时 |
| `slidev-themes.md` | 主题选择指南 | 选择合适的主题风格时 |
| `slidev-index.md` | 文档分类索引 | 查找特定功能文档时 |
| `docs-structure.md` | 文档结构说明 | 了解文档组织时 |

## Slidev 官方文档 (slidev-docs/)

完整的 Slidev 官方文档 (81个)。

### 目录

- `guide/` - 使用指南 (14个)
- `builtin/` - 内置功能 (3个)
- `features/` - 特性详解 (44个)
- `custom/` - 自定义配置 (15个)
- `resources/` - 资源合集 (5个)

### 常用文档

| 文档 | 说明 |
|------|------|
| `guide/syntax.md` | Markdown 语法 |
| `guide/animations.md` | 动画效果 |
| `builtin/layouts.md` | 内置布局 |
| `builtin/components.md` | 内置组件 |
| `features/line-highlighting.md` | 代码高亮 |
| `features/mermaid.md` | Mermaid 图表 |

**完整索引**: 参见 `guides/slidev-index.md`

## 使用原则

### 按需加载

不要一次性加载所有文档，根据当前步骤按需引用：

**示例**:
```
步骤 1: 素材获取
→ 加载 @references/workflows/material-collection.md

步骤 3: 内容生成
→ 加载 @references/workflows/content-generation.md
→ 加载 @references/specs/slidev-core-rules.md
→ 需要语法时加载 @references/guides/slidev-quickref.md
```

### 优先级

1. **核心规则** - 必须加载
   - `specs/slidev-core-rules.md`

2. **工作流程** - 按步骤加载
   - `workflows/material-collection.md`
   - `workflows/content-generation.md`

3. **快速参考** - 需要时加载
   - `guides/slidev-quickref.md` - 语法参考
   - `guides/slidev-config.md` - 配置参数
   - `guides/slidev-themes.md` - 主题选择

4. **官方文档** - 具体问题时加载
   - `slidev-docs/guide/syntax.md`
   - `slidev-docs/builtin/layouts.md`

### 查找流程

```
需要功能/语法
    ↓
查看 guides/slidev-quickref.md
    ↓
找不到？
    ↓
查看 guides/slidev-index.md (按功能查找)
    ↓
找到对应的官方文档路径
    ↓
加载 slidev-docs/xxx.md
```

## 维护说明

### 添加新文档

1. 确��文档类型 (workflows/specs/guides)
2. 创建文件并使用祈使语气编写
3. 更新本 README.md

### 更新官方文档

```bash
cd slidev-docs
./sync-docs.sh
```

---

**更新**: 2025-10-26
