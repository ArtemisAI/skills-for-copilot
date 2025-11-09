---
name: slides-generator
description: 通用幻灯片生成器 - 将任意输入智能转换为 Slidev 幻灯片。触发词：生成幻灯片、制作PPT、做个PPT、根据XXX做PPT、把XXX做成幻灯片、XXX的教程、讲解XXX。支持教学、调研、算法、项目解析等场景，自动识别需求类型，生成符合规范的幻灯片并预览。
license: Apache-2.0
---

# Slides Generator

将任意输入智能转换为 Slidev 幻灯片的通用生成器。

## 设计理念

```
用户需求 → Slidev Markdown → 原生 Slidev 渲染
```

**职责分离**:
- 生成符合 Slidev 规范的 Markdown
- 使用原生 Slidev 工具渲染

## 工作流程

### 步骤 1: 素材获取

根据输入类型选择工具获取素材。

**详细流程**: @references/workflows/material-collection.md

### 步骤 2: 场景识别

识别内容类型并加载对应模板。

| 场景 | 触发特征 | 模板 |
|------|---------|------|
| 教学 | 库名/框架 + "教程"/"学习" | @templates/teaching.md |
| 调研 | "调研"/"分析"/"对比" | @templates/research.md |
| 算法 | "LeetCode"/"算法题" | @templates/algorithm.md |
| 项目 | "源码"/"架构"/"解析" | @templates/project-analysis.md |

### 步骤 3: 内容生成

按模板策略生成 Slidev Markdown。

**生成策略**: @references/workflows/content-generation.md

**必须符合**: @references/specs/slidev-core-rules.md

### 步骤 4: 规范检查

验证生成的 Markdown 是否符合 Slidev 规范。

**检查清单**: @references/specs/validation-checklist.md

### 步骤 5: 输出保存

生成的幻灯片保存到统一目录。

**输出目录**: `~/note-vsc/slides/`

**文件命名**: `主题-场景-日期.md` (例: `fastapi-teaching-20251026.md`)

### 步骤 6: 规范验证

使用验证脚本检查生成的幻灯片是否符合 Slidev 规范。

**验证命令**: `./scripts/validate-slides.sh ~/note-vsc/slides/文件名.md`

**验证项目**:
- 文件格式 (UTF-8 编码、换行符)
- Frontmatter 配置 (theme, title, fonts)
- 分页规则 (---前后空行)
- 代码块规范 (语言标识)
- Mermaid 图表 (scale 参数)
- 内容溢出防止 (滚动/缩放)
- 内容质量 (空白页、标题)

**处理结果**:
- ❌ 失败: 根据提示修复后重新验证
- ⚠️ 警告: 记录改进建议,可选择性修复
- ✅ 通过: 进入下一步

### 步骤 7: 自动打开预览

生成完成后自动使用 Slidev 打开预览。

**命令**: `cd ~/note-vsc/slides && slidev 文件名.md --open`

**说明**:
- `--open` 参数会自动在默认浏览器中打开幻灯片
- Slidev 会启动开发服务器 (通常在 http://localhost:3030)
- 支持热更新，修改文件会实时刷新

**CLI 参考**: @slidev-docs/builtin/cli.md

## Slidev 规范

### 快速参考

**核心语法**: @references/guides/slidev-quickref.md

**配置参数**: @references/guides/slidev-config.md

**核心规则**: @references/specs/slidev-core-rules.md

### 完整文档

**官方文档**: @slidev-docs/

**文档索引**: @references/guides/slidev-index.md

**快速查找**:
- 语法: @slidev-docs/guide/syntax.md
- 布局: @slidev-docs/builtin/layouts.md
- 动画: @slidev-docs/guide/animations.md
- 代码: @slidev-docs/features/line-highlighting.md

## 场景模板

- 教学: @templates/teaching.md
- 调研: @templates/research.md
- 算法: @templates/algorithm.md
- 项目: @templates/project-analysis.md

## 质量标准

生成的幻灯片必须满足:

1. **规范性**: 符合 @references/specs/slidev-core-rules.md
2. **完整性**: 内容完整，逻辑清晰
3. **实用性**: 代码可运行，概念准确
4. **美观性**: 布局合理，视觉清晰

**详细标准**: @references/workflows/content-generation.md

## 资源引用

### 工作流程

- 素材获取: @references/workflows/material-collection.md
- 内容生成: @references/workflows/content-generation.md

### 规范文档

- 核心规则: @references/specs/slidev-core-rules.md
- 检查清单: @references/specs/validation-checklist.md

### 快速参考

- Slidev 语法: @references/guides/slidev-quickref.md
- 配置参数: @references/guides/slidev-config.md
- 文档索引: @references/guides/slidev-index.md

### 官方文档

- 完整文档: @slidev-docs/
- 在线文档: https://cn.sli.dev

---

**版本**: 1.0.0
**更新**: 2025-10-26
