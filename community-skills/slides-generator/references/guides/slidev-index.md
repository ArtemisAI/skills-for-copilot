# Slidev 官方文档分类索引

> 本文档提供 `slidev-docs/` 目录下所有官方文档的分类索引和快速导航

---

## 📖 文档结构

```
slidev-docs/
├── guide/          # 使用指南 (14个文档)
├── builtin/        # 内置功能 (3个文档)
├── features/       # 特性详解 (44个文档)
├── custom/         # 自定义配置 (15个文档)
└── resources/      # 资源合集 (5个文档)
```

---

## 🚀 使用指南 (guide/)

### 核心指南

| 文档 | 说明 | 优先级 |
|------|------|--------|
| `syntax.md` | **Markdown 语法规范** | ⭐⭐⭐ 必读 |
| `animations.md` | **动画和过渡效果** | ⭐⭐⭐ 必读 |
| `layout.md` | **布局系统** | ⭐⭐⭐ 必读 |
| `index.md` | 快速上手 | ⭐⭐ 推荐 |
| `ui.md` | 用户界面说明 | ⭐⭐ 推荐 |

### 进阶指南

| 文档 | 说明 | 适用场景 |
|------|------|---------|
| `component.md` | 组件使用 | 需要使用自定义组件 |
| `global-context.md` | 全局上下文 | 需要访问全局变量 |
| `theme-addon.md` | 主题和插件 | 需要使用主题或插件 |
| `write-layout.md` | 编写自定义布局 | 需要自定义布局 |
| `write-theme.md` | 编写自定义主题 | 需要自定义主题 |
| `write-addon.md` | 编写插件 | 需要开发插件 |

### 实用指南

| 文档 | 说明 |
|------|------|
| `exporting.md` | 导出 PDF/PNG/PPTX |
| `hosting.md` | 部署和托管 |
| `faq.md` | 常见问题 |
| `why.md` | 为什么选择 Slidev |

---

## 🛠️ 内置功能 (builtin/)

| 文档 | 说明 | 优先级 |
|------|------|--------|
| `layouts.md` | **内置布局完整列表** | ⭐⭐⭐ 必读 |
| `components.md` | **内置组件完整列表** | ⭐⭐⭐ 必读 |
| `cli.md` | CLI 命令参考 | ⭐⭐ 推荐 |

---

## ✨ 特性详解 (features/)

### 🎨 样式和布局

| 文档 | 说明 |
|------|------|
| `slide-scope-style.md` | 页面专属样式 |
| `canvas-size.md` | 画布尺寸配置 |
| `direction-variant.md` | 文本方向变体 |
| `global-layers.md` | 全局图层 |
| `slot-sugar.md` | Slot 语法糖 |

### 💻 代码功能

| 文档 | 说明 | 优先级 |
|------|------|--------|
| `line-highlighting.md` | **代码行高亮** | ⭐⭐⭐ 必读 |
| `code-block-line-numbers.md` | 代码行号 | ⭐⭐ 推荐 |
| `code-block-max-height.md` | 代码块最大高度 | ⭐⭐ 推荐 |
| `import-snippet.md` | 引入代码片段 | ⭐⭐ 推荐 |
| `shiki-magic-move.md` | **代码演进动画** | ⭐⭐ 推荐 |
| `monaco-editor.md` | Monaco 编辑器 | ⭐ 可选 |
| `monaco-run.md` | Monaco 代码运行 | ⭐ 可选 |
| `monaco-write.md` | Monaco 可写模式 | ⭐ 可选 |
| `twoslash.md` | TwoSlash 集成 | ⭐ 可选 |
| `code-groups.md` | 代码组 | ⭐ 可选 |

### 🎬 动画和交互

| 文档 | 说明 |
|------|------|
| `click-marker.md` | 点击标记 |
| `draggable.md` | 拖拽元素 |
| `drawing.md` | 绘图功能 |
| `rough-marker.md` | 粗糙标记 |
| `transform-component.md` | Transform 组件 |
| `zoom-slide.md` | 缩放幻灯片 |

### 📊 图表和公式

| 文档 | 说明 | 优先级 |
|------|------|--------|
| `mermaid.md` | **Mermaid 图表** | ⭐⭐⭐ 必读 |
| `latex.md` | **LaTeX 公式** | ⭐⭐ 推荐 |
| `plantuml.md` | PlantUML 图表 | ⭐ 可选 |

### 📝 内容组织

| 文档 | 说明 | 优先级 |
|------|------|--------|
| `importing-slides.md` | **引入外部幻灯片** | ⭐⭐⭐ 重要 |
| `frontmatter-merging.md` | Frontmatter 合并 | ⭐⭐ 推荐 |
| `block-frontmatter.md` | 代码块 Frontmatter | ⭐⭐ 推荐 |
| `mdc.md` | MDC 语法 | ⭐ 可选 |

### 🛠️ 开发工具

| 文档 | 说明 |
|------|------|
| `vscode-extension.md` | VSCode 扩展 |
| `side-editor.md` | 侧边编辑器 |
| `prettier-plugin.md` | Prettier 插件 |
| `slide-hook.md` | 幻灯片钩子 |

### 📤 导出和部署

| 文档 | 说明 |
|------|------|
| `build-with-pdf.md` | PDF 构建 |
| `bundle-remote-assets.md` | 打包远程资源 |
| `recording.md` | 录制功能 |
| `remote-access.md` | 远程访问 |

### 🎯 其他特性

| 文档 | 说明 |
|------|------|
| `icons.md` | 图标使用 |
| `timer.md` | 计时器 |
| `notes-auto-ruby.md` | 备注自动注音 |
| `seo-meta.md` | SEO 元数据 |
| `og-image.md` | OG 图片 |
| `eject-theme.md` | 弹出主题 |

---

## ⚙️ 自定义配置 (custom/)

### 配置索引

| 文档 | 说明 | 优先级 |
|------|------|--------|
| `index.md` | **配置总览** | ⭐⭐⭐ 必读 |
| `directory-structure.md` | **目录结构** | ⭐⭐⭐ 必读 |

### 代码相关

| 文档 | 说明 |
|------|------|
| `config-highlighter.md` | 配置代码高亮 |
| `config-monaco.md` | 配置 Monaco 编辑器 |
| `config-code-runners.md` | 配置代码运行器 |

### 样式相关

| 文档 | 说明 |
|------|------|
| `config-unocss.md` | 配置 UnoCSS |
| `config-fonts.md` | 配置字体 |

### 图表和公式

| 文档 | 说明 |
|------|------|
| `config-mermaid.md` | 配置 Mermaid |
| `config-katex.md` | 配置 KaTeX |

### 框架配置

| 文档 | 说明 |
|------|------|
| `config-vite.md` | 配置 Vite |
| `config-vue.md` | 配置 Vue |

### 高级配置

| 文档 | 说明 |
|------|------|
| `config-transformers.md` | 配置 Transformers |
| `config-parser.md` | 配置解析器 |
| `config-routes.md` | 配置路由 |
| `config-shortcuts.md` | 配置快捷键 |
| `config-context-menu.md` | 配置右键菜单 |

---

## 🎨 资源合集 (resources/)

| 文档 | 说明 |
|------|------|
| `theme-gallery.md` | 主题合集 |
| `addon-gallery.md` | 插件合集 |
| `showcases.md` | 案例展示 |
| `covers.md` | 精选封面 |
| `learning.md` | 学习资源 |

---

## 🎯 快速查找

### 按使用场景

#### 场景 1: 第一次使用 Slidev

**必读文档**:
1. `guide/index.md` - 快速上手
2. `guide/syntax.md` - 语法规范
3. `builtin/layouts.md` - 布局列表
4. `guide/animations.md` - 动画效果

#### 场景 2: 制作技术演示

**推荐文档**:
1. `features/line-highlighting.md` - 代码高亮
2. `features/shiki-magic-move.md` - 代码演进
3. `features/monaco-editor.md` - 可编辑代码
4. `features/mermaid.md` - 流程图

#### 场景 3: 制作教学课件

**推荐文档**:
1. `features/importing-slides.md` - 拆分章节
2. `features/drawing.md` - 标注功能
3. `features/latex.md` - 数学公式
4. `guide/exporting.md` - 导出PDF

#### 场景 4: 自定义样式

**推荐文档**:
1. `custom/config-unocss.md` - CSS 配置
2. `custom/config-fonts.md` - 字体配置
3. `features/slide-scope-style.md` - 页面样式
4. `guide/write-theme.md` - 自定义主题

#### 场景 5: 开发主题/插件

**必读文档**:
1. `guide/write-theme.md` - 编写主题
2. `guide/write-addon.md` - 编写插件
3. `guide/write-layout.md` - 编写布局
4. `custom/directory-structure.md` - 目录结构

### 按功能类别

#### 代码展示

- `features/line-highlighting.md` - 行高亮 ⭐⭐⭐
- `features/code-block-line-numbers.md` - 行号
- `features/shiki-magic-move.md` - 代码演进 ⭐⭐⭐
- `features/monaco-editor.md` - 编辑器
- `features/import-snippet.md` - 外部代码

#### 动画效果

- `guide/animations.md` - 动画总览 ⭐⭐⭐
- `features/click-marker.md` - 点击标记
- `features/draggable.md` - 拖拽
- `features/transform-component.md` - 变换

#### 图表绘制

- `features/mermaid.md` - Mermaid ⭐⭐⭐
- `features/plantuml.md` - PlantUML
- `features/latex.md` - LaTeX ⭐⭐⭐
- `features/drawing.md` - 手绘标注

#### 内容组织

- `features/importing-slides.md` - 引入幻灯片 ⭐⭐⭐
- `features/frontmatter-merging.md` - Frontmatter 合并
- `builtin/layouts.md` - 布局系统 ⭐⭐⭐

---

## 🔍 使用建议

### 初学者路径

1. **第1天**: 阅读 `guide/index.md`, `guide/syntax.md`
2. **第2天**: 阅读 `builtin/layouts.md`, `builtin/components.md`
3. **第3天**: 阅读 `guide/animations.md`, `features/line-highlighting.md`
4. **第4天**: 实践并查阅 `guide/faq.md`

### 进阶路径

1. 阅读 `features/` 目录下感兴趣的特性
2. 阅读 `custom/` 目录下的配置文档
3. 参考 `resources/showcases.md` 学习案例

### 开发者路径

1. 阅读 `guide/write-theme.md`
2. 阅读 `guide/write-addon.md`
3. 阅读 `custom/` 目录下的所有配置
4. 参考 `resources/theme-gallery.md` 学习优秀主题

---

## 📊 文档统计

- **总计**: 81 个官方文档
- **guide/**: 14 个
- **builtin/**: 3 个
- **features/**: 44 个
- **custom/**: 15 个
- **resources/**: 5 个

---

## 🔗 外部资源

- **在线文档**: https://cn.sli.dev
- **GitHub**: https://github.com/slidevjs/slidev
- **社区**: https://github.com/slidevjs/slidev/discussions

---

**最后更新**: 2025-10-26
**文档版本**: 基于 slidev-docs/ 本地副本
