# Slidev 规范检查清单

## 文件格式

- [ ] UTF-8 编码
- [ ] LF 换行符
- [ ] 开头有 Headmatter
- [ ] Frontmatter 与内容间空一行

## 分页规范

- [ ] `---` 前后有空行
- [ ] 第一个 `---` 块是 headmatter

## Frontmatter 规范

- [ ] YAML 语法正确
- [ ] 包含必需字段: `theme`, `title`
- [ ] 布局名称有效

## 代码块规范

- [ ] 所有代码块有语言标识
- [ ] 代码块正确闭合
- [ ] 行高亮语法正确

## 布局规范

- [ ] 使用有效的布局名称
- [ ] Slot 语法正确 (`::right::`)

## 动画规范

- [ ] 过渡效果名称有效
- [ ] v-click 组件正确使用

## 备注规范

- [ ] 演讲者备注在幻灯片末尾
- [ ] 使用 `<!-- -->` 注释

## 内容溢出检查

**优先级检查**:

1. **首选: 内容拆分**
   - [ ] 内容是否可以拆分到多页？

2. **次选: 启用滚动**
   - [ ] 添加 `class: overflow-y-auto` 到单页 frontmatter
   - [ ] 或在 headmatter 的 `defaults` 中全局启用

3. **兜底: 内容缩放**
   - [ ] 大型 Mermaid 图 + 文字列表: 添加 `zoom: 0.85`
   - [ ] 5+ 行表格: 添加 `zoom: 0.9`
   - [ ] 10+ 项列表: 添加 `zoom: 0.9`
   - [ ] 代码块 + 3+ 段落: 添加 `zoom: 0.9`

4. **配合优化**
   - [ ] Mermaid scale 设置为 0.7-0.8

## 参考资源

- 核心规则: @references/specs/slidev-core-rules.md
- 官方文档: @slidev-docs/guide/syntax.md
- 快速参考: @references/guides/slidev-quickref.md
