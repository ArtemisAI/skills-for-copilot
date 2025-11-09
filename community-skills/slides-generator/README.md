# Slides Generator

通用幻灯片生成器 - 将任意输入智能转换为 Slidev 幻灯片。

## 核心理念

```
用户需求 → Slidev Markdown → 原生 Slidev 渲染
```

**职责分离**:
- 生成符合 Slidev 规范的 Markdown
- 使用原生 Slidev 工具渲染

## 目录结构

```
slides-generator/
├── SKILL.md                  # Skill 主文档
├── README.md                 # 本文件
├── templates/                # 场景模板
│   ├── teaching.md          # 教学场景
│   ├── research.md          # 调研场景
│   ├── algorithm.md         # 算法场景
│   └── project-analysis.md  # 项目解析场景
├── references/               # 参考文档 (按需加载)
│   ├── README.md            # 导航文件
│   ├── workflows/           # 工作流程
│   ├── specs/               # 规范文档
│   ├── guides/              # 指南文档
│   └── slidev-docs/         # Slidev 官方文档 (81个)
└── slidev-docs/             # Slidev 官方文档源文件
```

## 使用方法

### 触发条件

**明确触发**:
- "生成幻灯片"
- "制作 PPT"
- "转换为 slides"

**隐含触发**:
- "把 XXX 做成可展示的"
- "学习 XXX,需要材料"

### 场景类型

| 场景 | 触发特征 | 输出规模 |
|------|---------|---------|
| 教学 | 库名/框架 + "教程"/"学习" | 100-150张 |
| 调研 | "调研"/"分析"/"对比" | 50-80张 |
| 算法 | "LeetCode"/"算法题" | 30-50张 |
| 项目 | "源码"/"架构"/"解析" | 80-120张 |

### 输出位置

生成的幻灯片保存到: `~/note-vsc/slides/`

文件命名格式: `主题-场景-日期.md`

### 自动预览

生成完成后会自动在浏览器中打开预览:

```bash
cd ~/note-vsc/slides
slidev 文件名.md --open
```

**特性**:
- 自动打开默认浏览器
- 热更新支持
- 演讲者模式 (按 `o` 键)

## 工作流程

1. **素材获取** - 根据输入类型选择工具
2. **场景识别** - 识别内容类型并加载模板
3. **内容生成** - 按模板策略生成 Markdown
4. **规范检查** - 验证 Slidev 规范符合性
5. **输出保存** - 保存到 `~/note-vsc/slides/`
6. **Slidev 渲染** - 使用原生 Slidev 渲染

详细说明参见 `SKILL.md`。

## 按需加载设计

本 Skill 采用按需加载架构:

- **SKILL.md** (3.3KB) - 核心流程和引用
- **references/** - 分类文档，根据需要加载
- **@引用语法** - 明确标注加载路径

这种设计将 Token 消耗降低 50-70%。

详细说明参见 `references/README.md`。

## 配置定制

### 字体和样式

需要调整字体、文字大小、颜色等配置时，参考:

**配置指南**: `references/guides/slidev-config.md`

包含:
- 字体配置 (中文字体推荐、本地字体)
- 文字样式 (大小、粗细、行高、对齐)
- 主题颜色
- 布局配置
- 实用示例 (技术演讲、商业演示、教学课件)

详细说明参见 `references/README.md`。

## Slidev 文档

完整的 Slidev 官方文档位于 `slidev-docs/` (81个文档)。

快速查找:
- 语法: `slidev-docs/guide/syntax.md`
- 布局: `slidev-docs/builtin/layouts.md`
- 动画: `slidev-docs/guide/animations.md`

在线文档: https://cn.sli.dev

## 质量标准

生成的幻灯片必须满足:

1. **规范性** - 符合 Slidev 核心规则
2. **完整性** - 内容完整，逻辑清晰
3. **实用性** - 代码可运行，概念准确
4. **美观性** - 布局合理，视觉清晰

### 辅助工具

提供 2 个简单可靠的脚本:

#### 1. 验证规范 ✅

```bash
# 基础验证
./scripts/validate-slides.sh ~/note-vsc/slides/你的幻灯片.md

# 详细模式 (显示具体行号)
./scripts/validate-slides.sh ~/note-vsc/slides/你的幻灯片.md --verbose
```

**功能**: 7大类检查,为 Agent 提供质量反馈

**核心价值**: Agent 根据验证反馈改进生成策略,而不是依赖脚本修复

#### 2. 快速预览 🚀

```bash
./scripts/preview.sh ~/note-vsc/slides/你的幻灯片.md
```

**功能**: 快速启动 Slidev 预览服务器

**详细文档**: `scripts/README.md`

## 使用示例

### 示例 1: 教学场景

```
"生成 FastAPI 依赖注入教学 PPT"
```

输出: `~/note-vsc/slides/fastapi-teaching-20251026.md` (约 120 张)

### 示例 2: 调研场景

```
"调研 Serverless 架构用于技术选型"
```

输出: `~/note-vsc/slides/serverless-research-20251026.md` (约 65 张)

### 示例 3: 算法场景

```
"LeetCode 二叉树中序遍历, 多种解法对比"
```

输出: `~/note-vsc/slides/inorder-algorithm-20251026.md` (约 35 张)

## 添加新模板

当需要添加新的场景模板时，按以下步骤操作：

### 1. 创建模板文件

在 `templates/` 目录创建新模板文件：

```bash
templates/新场景.md
```

### 2. 编写模板内容

参考现有模板结构，包含以下部分：
- 场景识别条件
- 触发特征
- 内容生成策略
- 章节结构
- 质量标准

### 3. 更新 SKILL.md

在 `SKILL.md` 的"步骤 2: 场景识别"表格中添加新行：

```markdown
| 场景 | 触发特征 | 模板 |
|------|---------|------|
| 新场景 | "关键词1"/"关键词2" | @templates/新场景.md |
```

在"场景模板"部分添加引用：

```markdown
- 新场景: @templates/新场景.md
```

### 4. 更新 README.md

在"场景类型"表格中添加新行：

```markdown
| 场景 | 触发特征 | 输出规模 |
|------|---------|---------|
| 新场景 | "关键词1"/"关键词2" | XX-XX张 |
```

在"使用示例"部分添加示例：

```markdown
### 示例 X: 新场景

\```
"用户输入示例"
\```

输出: `~/note-vsc/slides/主题-新场景-日期.md` (约 XX 张)
```

### 5. 测试新模板

使用新的触发关键词测试模板是否正常工作。

### 需要修改的文件清单

- ✅ `templates/新场景.md` - 创建模板
- ✅ `SKILL.md` - 添加场景识别条目和模板引用
- ✅ `README.md` - 添加场景类型和使用示例

## 版本

**当前版本**: 1.0.0

**更新日期**: 2025-10-26

## 许可证

Apache-2.0
