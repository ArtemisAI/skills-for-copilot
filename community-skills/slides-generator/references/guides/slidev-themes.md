# Slidev 主题选择指南

> 官方和社区主题推荐，帮助选择最适合的演示风格

## 官方主题

### 1. **default** - 默认主题
**适用场景**: 通用演示、快速原型

**特点**:
- 简洁干净
- 开箱即用
- 适合各种场景

**配置**:
```yaml
---
theme: default
---
```

### 2. **seriph** - 优雅主题 ⭐ 推荐
**适用场景**: 技术演讲、产品发布、专业演示

**特点**:
- 现代设计风格
- 视觉效果出色
- 适合正式场合
- 内置多种精美布局

**配置**:
```yaml
---
theme: seriph
---
```

**安装**:
```bash
npm install @slidev/theme-seriph
```

### 3. **apple-basic** - Apple 风格
**适用场景**: 产品发布、设计展示、品牌演示

**特点**:
- 模仿 Apple 发布会风格
- 极简主义设计
- 大字体、大图片
- 适合视觉冲击力强的内容

**配置**:
```yaml
---
theme: apple-basic
---
```

**安装**:
```bash
npm install slidev-theme-apple-basic
```

### 4. **shibainu** - 柴犬主题
**适用场景**: 轻松活泼的演示、教学课件

**特点**:
- 可爱风格
- 适合非正式场合
- 活泼色彩

**配置**:
```yaml
---
theme: shibainu
---
```

**安装**:
```bash
npm install slidev-theme-shibainu
```

### 5. **bricks** - 砖块主题
**适用场景**: 技术文档、开发者分享

**特点**:
- 底部工具栏
- 紫色配色
- 代码友好

**配置**:
```yaml
---
theme: bricks
---
```

**安装**:
```bash
npm install slidev-theme-bricks
```

## 社区主题推荐

### **vercel** - Vercel 设计系统
**适用场景**: Web 开发演示、技术分享

**特点**:
- 基于 Vercel 设计系统
- 现代化界面
- 适合前端开发者

**配置**:
```yaml
---
theme: '@jcamp/slidev-theme-vercel'
---
```

### **purplin** - 紫色主题
**适用场景**: 创意演示、设计分享

**特点**:
- 紫色配色
- 简洁风格
- 专注内容

**配置**:
```yaml
---
theme: 'slidev-theme-purplin'
---
```

## 场景推荐

### 🎓 教学课件
**推荐**: `default` 或 `seriph`

```yaml
---
theme: seriph
fonts:
  sans: 'Noto Sans SC'
  mono: 'Fira Code'
  weights: '300,400,600'
highlighter: shiki
lineNumbers: true
---
```

### 💼 商业演示
**推荐**: `apple-basic` 或 `seriph`

```yaml
---
theme: apple-basic
fonts:
  sans: 'Roboto'
  weights: '300,400,700'
transition: fade
---
```

### 👨‍💻 技术分享
**推荐**: `seriph` 或 `bricks`

```yaml
---
theme: seriph
fonts:
  sans: 'Noto Sans SC'
  mono: 'Fira Code'
highlighter: shiki
lineNumbers: true
monaco: true
---
```

### 🎨 设计展示
**推荐**: `apple-basic`

```yaml
---
theme: apple-basic
aspectRatio: 16/9
transition: fade
---
```

## 使用主题

### 方法 1: 自动安装
在 headmatter 中指定主题名称，启动时会提示安装:

```yaml
---
theme: seriph
---
```

### 方法 2: 手动安装
```bash
# 安装主题
npm install @slidev/theme-seriph

# 或使用 pnpm
pnpm add @slidev/theme-seriph
```

### 方法 3: 本地主题
使用相对路径引用本地主题:

```yaml
---
theme: ../my-theme
---
```

## 主题配置

### 主题颜色
大部分主题支持自定义主色:

```yaml
---
theme: seriph
themeConfig:
  primary: '#5d8392'
  secondary: '#f59e0b'
---
```

### 字体配置
覆盖主题默认字体:

```yaml
---
theme: seriph
fonts:
  sans: 'Noto Sans SC'
  serif: 'Noto Serif SC'
  mono: 'Fira Code'
---
```

## 更多主题

### 查找主题
- NPM 搜索: https://www.npmjs.com/search?q=keywords:slidev-theme
- 官方画廊: https://sli.dev/resources/theme-gallery
- GitHub: https://github.com/slidevjs/themes

### 创建主题
参考官方文档: @slidev-docs/guide/write-theme.md

## 推荐的默认配置

### 通用配置 (推荐)

```yaml
---
theme: seriph
highlighter: shiki
lineNumbers: false
transition: slide-left
fonts:
  sans: 'Noto Sans SC'
  serif: 'Noto Serif SC'
  mono: 'Fira Code'
  weights: '300,400,600'
canvasWidth: 980
---
```

**为什么选择 seriph?**
- ✅ 视觉效果专业
- ✅ 布局丰富多样
- ✅ 适合大部分场景
- ✅ 官方维护，稳定可靠
- ✅ 中英文混排效果好

## 参考资源

- 主题合集: https://sli.dev/resources/theme-gallery
- 主题仓库: https://github.com/slidevjs/themes
- 编写主题: @slidev-docs/guide/write-theme.md
- 主题配置: @slidev-docs/custom/index.md

---

**更新日期**: 2025-10-26
