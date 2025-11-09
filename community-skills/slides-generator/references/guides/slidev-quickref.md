# Slidev 快速参考

> 精简的核心语法参考，完整文档参见 @slidev-docs/

## 基础语法

### 分页

```markdown
# 第一页

---

# 第二页
```

**规则**: `---` 前后必须有空行

### Headmatter

```yaml
---
theme: default
title: 演示标题
transition: slide-left
---
```

### 单页 Frontmatter

```yaml
---
layout: center
background: /image.jpg
class: overflow-y-auto  # 启用滚动 (推荐)
# 或使用 zoom: 0.85 缩小内容 (兜底方案)
---
```

**防止内容溢出 (优先级)**:
1. 拆分到多页 (最佳)
2. `class: overflow-y-auto` (推荐)
3. `zoom: 0.85-0.9` (兜底)

## 常用布局

| 布局 | 用途 |
|------|------|
| `cover` | 封面页 |
| `center` | 居中内容 |
| `two-cols` | 两列布局 |
| `image-left` | 左图右文 |
| `quote` | 引用 |
| `section` | 章节分隔 |
| `end` | 结束页 |

**完整列表**: @slidev-docs/builtin/layouts.md

## 代码块

### 基础

````markdown
```typescript
function hello() {
  console.log('Hello')
}
```
````

### 行高亮

````markdown
```typescript {2,5-8}
// 高亮第 2 行和第 5-8 行
```
````

### 点击高亮

````markdown
```typescript {2|5-8|all}
// 第一次点击高亮第 2 行
// 第二次点击高亮第 5-8 行
// 第三次点击高亮全部
```
````

### 长代码滚动

````markdown
```typescript {maxHeight:'400px'}
// 超过 400px 的代码会出现滚动条
// 防止代码溢出屏幕
```
````

**详细说明**: @slidev-docs/features/line-highlighting.md

## Two Cols 布局

```markdown
---
layout: two-cols
---

# 左侧

左侧内容

::right::

# 右侧

右侧内容
```

**详细说明**: @slidev-docs/features/slot-sugar.md

## 动画

### 过渡效果

```yaml
---
transition: slide-left
---
```

### 点击动画

```markdown
<v-click>

点击后显示

</v-click>
```

**详细说明**: @slidev-docs/guide/animations.md

## 图表

### Mermaid

````markdown
```mermaid {scale: 0.75}
graph LR
  A[开始] --> B[结束]
```
````

**缩放建议**:
- 复杂图表: `scale: 0.7-0.8`
- 简单图表: `scale: 0.8-1.0`

**详细说明**: @slidev-docs/features/mermaid.md

### LaTeX

```markdown
行内: $E = mc^2$

块级:
$$
\int_a^b f(x)dx
$$
```

**详细说明**: @slidev-docs/features/latex.md

## 备注

```markdown
# 内容

<!-- 演讲者备注 -->
```

**规则**: 必须在幻灯片末尾

## 参考

- 完整语法: @slidev-docs/guide/syntax.md
- 布局列表: @slidev-docs/builtin/layouts.md
- 组件列表: @slidev-docs/builtin/components.md
- 文档索引: @references/guides/slidev-index.md
