# Slidev 配置参数指南

> 全面的 Slidev 配置参数参考文档，涵盖字体、样式、布局等常用配置

## 字体配置

### 基础字体设置

在 Headmatter 中配置字体:

```yaml
---
fonts:
  # 正文字体 (sans-serif)
  sans: Roboto
  # 衬线字体 (使用 font-serif CSS 类)
  serif: Roboto Slab
  # 代码字体 (代码块、行内代码等)
  mono: Fira Code
---
```

**说明**:
- 字体会自动从 Google Fonts CDN 导入
- 可以使用 Google Fonts 上的任何字体
- 默认导入 3 种字重: 200, 400, 600

### 常用中文字体推荐

```yaml
---
fonts:
  sans: 'Noto Sans SC'        # 思源黑体简体
  serif: 'Noto Serif SC'      # 思源宋体简体
  mono: 'Fira Code'           # 代码字体
---
```

**其他中文字体选项**:
- `Ma Shan Zheng` - 马善政毛笔楷书
- `Zhi Mang Xing` - 志莽行书
- `ZCOOL XiaoWei` - 站酷小薇

### 本地字体

如果要使用本地字体:

```yaml
---
fonts:
  sans: 'PingFang SC, Helvetica Neue, Roboto'
  # 标记为本地字体
  local: 'PingFang SC'
---
```

### 字重和斜体

```yaml
---
fonts:
  sans: Roboto
  # 自定义字重
  weights: '200,400,600,700'
  # 启用斜体
  italic: true
---
```

### 禁用备用字体

```yaml
---
fonts:
  mono: 'Fira Code, monospace'
  fallbacks: false
---
```

### 字体提供商

```yaml
---
fonts:
  provider: google  # google | coollabs | none
---
```

- `google` - Google Fonts (默认)
- `coollabs` - coolLabs 字体服务
- `none` - 不自动导入，仅使用本地字体

## 文字大小和样式

### UnoCSS 文字类

Slidev 使用 UnoCSS (兼容 Tailwind CSS)，可以直接使用以下类:

**字体大小**:
```markdown
<div class="text-xs">极小文字 (0.75rem)</div>
<div class="text-sm">小文字 (0.875rem)</div>
<div class="text-base">普通文字 (1rem)</div>
<div class="text-lg">大文字 (1.125rem)</div>
<div class="text-xl">特大文字 (1.25rem)</div>
<div class="text-2xl">超大文字 (1.5rem)</div>
<div class="text-3xl">巨大文字 (1.875rem)</div>
<div class="text-4xl">极巨文字 (2.25rem)</div>
```

**字体粗细**:
```markdown
<div class="font-thin">细体 (100)</div>
<div class="font-light">轻体 (300)</div>
<div class="font-normal">普通 (400)</div>
<div class="font-medium">中等 (500)</div>
<div class="font-semibold">半粗 (600)</div>
<div class="font-bold">粗体 (700)</div>
<div class="font-extrabold">超粗 (800)</div>
```

**行高**:
```markdown
<div class="leading-tight">紧凑行高 (1.25)</div>
<div class="leading-normal">普通行高 (1.5)</div>
<div class="leading-relaxed">宽松行高 (1.625)</div>
<div class="leading-loose">超宽松行高 (2)</div>
```

**字间距**:
```markdown
<div class="tracking-tight">紧密字距</div>
<div class="tracking-normal">普通字距</div>
<div class="tracking-wide">宽松字距</div>
```

**文字对齐**:
```markdown
<div class="text-left">左对齐</div>
<div class="text-center">居中对齐</div>
<div class="text-right">右对齐</div>
<div class="text-justify">两端对齐</div>
```

**文字颜色**:
```markdown
<div class="text-gray-500">灰色文字</div>
<div class="text-blue-600">蓝色文字</div>
<div class="text-red-500">红色文字</div>
<div class="text-green-600">绿色文字</div>
```

## 幻灯片全局配置

### 基本信息

```yaml
---
# 主题
theme: default
# 标题
title: 我的演示文稿
# 作者 (导出 PDF 时使用)
author: 张三
# 关键词 (导出 PDF 时使用)
keywords: 技术,教程,演示
---
```

### 显示配置

```yaml
---
# 宽高比
aspectRatio: 16/9  # 或 4/3, 16/10
# 画布实际宽度 (px)
canvasWidth: 980
# 颜色模式
colorSchema: auto  # auto | light | dark
# 代码行号
lineNumbers: true  # true | false
---
```

### 过渡动画

```yaml
---
# 全局过渡效果
transition: slide-left
---
```

**可用过渡效果**:
- `slide-left` - 左滑
- `slide-right` - 右滑
- `slide-up` - 上滑
- `slide-down` - 下滑
- `fade` - 淡入淡出
- `fade-out` - 仅淡出
- `zoom` - 缩放
- `view-transition` - 视图过渡 (实验性)

### 演讲者模式

```yaml
---
# 启用演讲者模式
presenter: true  # true | false | 'dev' | 'build'
# 启用绘图
drawings:
  enabled: true
  persist: false        # 保持绘图
  presenterOnly: false  # 仅演讲者可见
---
```

### 导出配置

```yaml
---
# 启用下载
download: true  # true | false
# 导出文件名
exportFilename: my-presentation
# 导出选项
export:
  format: pdf     # pdf | png | md
  timeout: 30000
  dark: false     # 暗色模式
  withClicks: false  # 包含点击动画
---
```

## 单页配置

### 布局

```yaml
---
layout: center  # 应用到当前幻灯片
background: /image.jpg
class: text-white
---
```

**常用布局**:
- `default` - 默认布局
- `center` - 居中内容
- `cover` - 封面页
- `intro` - 介绍页
- `section` - 章节分隔
- `two-cols` - 两列布局
- `image-left` - 左图右文
- `image-right` - 右图左文
- `quote` - 引用
- `fact` - 事实陈述
- `statement` - 声明
- `end` - 结束页

### 缩放

```yaml
---
# 内容过多时缩小
zoom: 0.8
---
```

### 过渡

```yaml
---
# 单页过渡效果 (覆盖全局设置)
transition: fade
---
```

## 代码块配置

### 高亮器

```yaml
---
highlighter: shiki  # shiki | prism
---
```

### Monaco 编辑器

```yaml
---
# 启用 Monaco 编辑器 (可编辑代码块)
monaco: true  # true | false | 'dev' | 'build'
---
```

## 自定义样式

### 创建全局样式

创建 `style.css` 或 `styles/index.css`:

```css
/* 自定义全局样式 */
.slidev-layout {
  font-size: 1.1rem;
}

/* 自定义标题样式 */
h1 {
  font-size: 3rem !important;
  color: #2c3e50;
}

/* 自定义代码块样式 */
pre {
  border-radius: 8px;
  padding: 1.5rem !important;
}
```

### UnoCSS 自定义

创建 `uno.config.ts`:

```typescript
import { defineConfig } from 'unocss'

export default defineConfig({
  shortcuts: {
    // 自定义快捷类
    'bg-main': 'bg-white text-[#181818] dark:(bg-[#121212] text-[#ddd])',
    'btn': 'px-4 py-2 rounded bg-blue-500 text-white hover:bg-blue-600',
  },
  theme: {
    colors: {
      primary: '#5d8392',
      secondary: '#f59e0b',
    }
  }
})
```

## 主题颜色

### 主题配置

```yaml
---
themeConfig:
  primary: '#5d8392'      # 主色
  secondary: '#f59e0b'    # 次要色
---
```

### CSS 变量

在自定义 CSS 中使用主题变量:

```css
.custom-element {
  color: var(--slidev-theme-primary);
  background: var(--slidev-theme-secondary);
}
```

## 实用示例

### 技术演讲配置

```yaml
---
theme: default
title: TypeScript 深入浅出
author: 张三
fonts:
  sans: 'Noto Sans SC'
  mono: 'Fira Code'
highlighter: shiki
lineNumbers: true
aspectRatio: 16/9
colorSchema: light
transition: slide-left
---
```

### 商业演示配置

```yaml
---
theme: seriph
title: 2024 年度业务报告
author: 公司名称
fonts:
  sans: 'Roboto'
  weights: '300,400,600,700'
aspectRatio: 16/9
colorSchema: light
transition: fade
themeConfig:
  primary: '#1e40af'
---
```

### 教学课件配置

```yaml
---
theme: default
title: 算法与数据结构
fonts:
  sans: 'Noto Sans SC'
  mono: 'Fira Code'
  weights: '400,600,700'
highlighter: shiki
lineNumbers: true
monaco: true
drawings:
  enabled: true
  persist: true
aspectRatio: 16/9
---
```

## 参考资源

### 官方文档
- 完整配置选项: @slidev-docs/custom/index.md
- 字体配置: @slidev-docs/custom/config-fonts.md
- UnoCSS 配置: @slidev-docs/custom/config-unocss.md
- 目录结构: @slidev-docs/custom/directory-structure.md

### 在线资源
- UnoCSS 文档: https://unocss.dev
- Google Fonts: https://fonts.google.com
- Slidev 官方文档: https://cn.sli.dev

---

**更新日期**: 2025-10-26
