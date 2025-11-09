# Slidev 核心规则

> 生成 Slidev Markdown 时必须遵循的核心规则

## 分页规则

- 使用 `---` 分隔幻灯片
- `---` 前后必须有空行
- 第一个 `---` 块是 headmatter (全局配置)

## Frontmatter 规则

- YAML 格式
- 页面配置在内容前
- 支持布局、背景、类名、过渡等

**必需字段**: `theme`, `title`

### 默认 Headmatter 配置

每个生成的幻灯片应包含以下默认配置:

```yaml
---
theme: seriph
highlighter: shiki
lineNumbers: false
title: 演示文稿标题
transition: slide-left
fonts:
  sans: 'Noto Sans SC'
  serif: 'Noto Serif SC'
  mono: 'Fira Code'
  weights: '300,400,600'
canvasWidth: 980
---
```

**配置说明**:
- `theme: seriph`: 优雅专业的主题，适合大部分场景 (详见 @references/guides/slidev-themes.md)
- `fonts.sans`: 中文友好的正文字体 (思源黑体)
- `fonts.weights`: 包含轻体(300)、常规(400)、半粗(600)
- `canvasWidth: 980`: 默认画布宽度，适配大部分屏幕

**主题选择**: 参见 @references/guides/slidev-themes.md

### 内容溢出防止规则

**问题**: 当单页内容过多时，会超出屏幕且无法下拉查看

**解决方案优先级**:

#### 方案 1: 启用页面滚动 ⭐ 推荐

在单页 frontmatter 中添加 CSS 样式启用滚动:

```yaml
---
class: overflow-y-auto
---

## 页面标题

大量内容...
可以向下滚动查看
```

**全局启用滚动** (在 headmatter 添加):
```yaml
---
theme: seriph
# ... 其他配置
defaults:
  class: overflow-y-auto
---
```

**自定义滚动样式** (可选，创建 `style.css`):
```css
.slidev-layout {
  overflow-y: auto !important;
  padding-bottom: 2rem;
}

/* 隐藏滚动条，但保留滚动功能 */
.slidev-layout::-webkit-scrollbar {
  width: 4px;
}

.slidev-layout::-webkit-scrollbar-thumb {
  background: rgba(0,0,0,0.2);
  border-radius: 2px;
}
```

#### 方案 2: 内容缩放 (兜底方案)

当无法启用滚动或需要全屏展示时使用:

| 情况 | zoom 值 | 判断标准 |
|------|---------|---------|
| 大型 Mermaid 图 + 文字列表 | 0.85 | 图表 + 5+ 行文字 |
| 大型表格 (5+ 行) | 0.9 | 表格行数 ≥ 5 |
| 长列表 (10+ 项) | 0.9 | 列表项 ≥ 10 |
| 代码块 + 多段说明 | 0.9 | 代码块 + 3+ 段落 |

**语法**:
```yaml
---
zoom: 0.85
---

## 页面标题
内容...
```

#### 方案 3: 内容拆分 (最佳实践)

优先将内容拆分到多张幻灯片:

```markdown
---

## 部分 1: 概念介绍

核心概念说明...

---

## 部分 2: 实现细节

详细实现...
```

**最佳实践总结**:
1. **首选**: 拆分内容到多页
2. **次选**: 启用滚动 (`class: overflow-y-auto`)
3. **兜底**: 使用 zoom 缩小 (0.8-0.95)
4. **配合**: Mermaid 图表使用 `{scale: 0.7-0.8}`

## 代码块规则

- 必须指定语言: ` ```typescript `
- 支持行高亮: ` ```ts {2,5-8} `
- 支持点击高亮: ` ```ts {2|5|all} `
- 长代码块滚动: ` ```ts {maxHeight:'400px'} ` (超过屏幕高度时使用)

## 布局规则

- 使用语义化布局: `cover`, `center`, `two-cols` 等
- 使用 slot 语法分隔内容: `::right::`

**完整布局列表**: 参见 @slidev-docs/builtin/layouts.md

## 动画规则

- 全局过渡: headmatter 中配置 `transition`
- 单页过渡: frontmatter 中配置
- 元素动画: `<v-click>` 组件

**详细说明**: 参见 @slidev-docs/guide/animations.md

## 备注规则

- 演讲者备注在幻灯片末尾
- 使用 `<!-- -->` 注释
- 支持 Markdown 格式

**详细语法**: 参见 @slidev-docs/guide/syntax.md

## Mermaid 图表规则

- 使用 scale 参数控制大小: ` ```mermaid {scale: 0.75} `
- 复杂图表推荐 scale: 0.7-0.8
- 简单图表推荐 scale: 0.8-1.0
- 避免图表溢出屏幕导致无法查看

**详细说明**: 参见 @slidev-docs/features/mermaid.md
