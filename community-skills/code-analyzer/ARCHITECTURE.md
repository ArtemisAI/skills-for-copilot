# Code Analyzer 架构设计

## 核心概念

### 1. 测试左移工具

**定位**: 提测前代码审查工具,面向测试工程师

**核心价值**:
- 在提测前识别缺陷,而非测试阶段
- 自动确定回归测试范围
- 生成结构化测试分析报告

### 2. 两阶段工作流

```
第一次使用 (初始化阶段)
├─ 扫描项目结构
├─ 识别技术栈
├─ 建立 Serena 索引 (2-5分钟)
├─ 生成项目上下文
└─ 保存到 .code-analyzer/project-context.json

后续使用 (分析阶段)
├─ 读取项目上下文
├─ 增量更新 Serena 索引 (10-30秒)
├─ 执行 6 步分析工作流
└─ 生成测试分析报告
```

### 3. 项目上下文

**概念**: 项目的元信息和配置,避免重复扫描

**内容示例**:

```json
{
  "project_name": "user-service",
  "techstack": "java-springboot",
  "framework_version": "3.2.0",
  "build_tool": "maven",
  "key_packages": {
    "controller": "com.example.controller",
    "service": "com.example.service",
    "repository": "com.example.repository"
  },
  "serena_indexed": true,
  "last_index_time": "2025-10-27T10:30:00",
  "template_path": "templates/java-springboot/"
}
```

**存储位置**: `{被分析项目}/.code-analyzer/project-context.json`

---

## 核心架构

### 1. 模块化设计

```
code-analyzer/
├── SKILL.md                    # 主入口文档
├── README.md                   # 快速开始指南
├── ARCHITECTURE.md             # 本文档
│
├── references/
│   ├── workflows/              # 6步分析工作流
│   │   ├── step1-code-change.md
│   │   ├── step2-techstack-detect.md
│   │   ├── step3-defect-detect.md
│   │   ├── step4-requirement-verify.md
│   │   ├── step5-impact-analysis.md
│   │   └── step6-report-generate.md
│   │
│   ├── integrations/           # MCP工具集成
│   │   ├── serena-mcp.md
│   │   └── sequential-mcp.md
│   │
│   └── specs/
│       └── report-format.md    # 报告格式规范
│
├── templates/                  # 技术栈模板
│   ├── registry.json           # 模板注册表
│   └── java-springboot/
│       └── defect-rules.md     # Java缺陷检测规则
│
└── examples/
    └── project-context.json    # 项目上下文示例
```

### 2. 技术栈扩展机制

#### 模板注册表

**文件**: `templates/registry.json`

```json
{
  "templates": [
    {
      "id": "java-springboot",
      "name": "Java + SpringBoot",
      "detect_files": ["pom.xml", "build.gradle"],
      "detect_dependencies": ["spring-boot-starter"],
      "detect_annotations": ["@SpringBootApplication"],
      "paths": {
        "defect_rules": "templates/java-springboot/defect-rules.md"
      },
      "priority": 1
    }
  ]
}
```

#### 添加新语言

**步骤**:

1. 创建模板目录: `templates/{language}/`
2. 编写缺陷检测规则: `defect-rules.md`
3. 注册到 `registry.json`
4. 无需修改核心工作流代码

**示例** - 添加 Python/Django:

```bash
mkdir -p templates/python-django
# 编写 defect-rules.md
# 在 registry.json 中添加配置
```

### 3. 6步分析工作流

| 步骤 | 职责 | 输入 | 输出 | 工具 |
|------|------|------|------|------|
| 1 | 代码变更提取 | Git范围 | 变更文件列表 | git diff |
| 2 | 技术栈识别 | 项目文件 | 技术栈ID | registry.json |
| 3 | 缺陷检测 | 变更代码 | 缺陷清单 | Serena MCP |
| 4 | 需求验证 | 需求文档 | 实现情况 | Sequential MCP |
| 5 | 影响范围分析 | 变更函数 | 影响模块 | Serena MCP |
| 6 | 报告生成 | 以上结果 | Markdown报告 | 模板渲染 |

**详细说明**: 参见 `references/workflows/` 目录

---

## MCP工具集成

### 1. Serena MCP (必需)

**用途**:
- 项目代码索引
- 符号级代码理解
- 调用链追踪
- 依赖关系分析

**核心功能**:
- `find_symbol`: 查找函数/类定义
- `find_referencing_symbols`: 查找调用位置
- `get_symbols_overview`: 文件结构概览
- `search_for_pattern`: 文本模式搜索

**索引机制**:
- 首次: 全量索引 (2-5分钟)
- 后续: 增量更新 (10-30秒)

**详细说明**: @references/integrations/serena-mcp.md

### 2. Sequential MCP (推荐)

**用途**:
- 需求验证推理
- 影响范围推导
- 风险评估决策

**详细说明**: @references/integrations/sequential-mcp.md

---

## 工作流程图

### 完整流程

```
用户触发
  ↓
检查 .code-analyzer/project-context.json
  ↓
不存在? → 初始化阶段
  ├─ 扫描项目
  ├─ 识别技术栈
  ├─ Serena索引 (2-5分钟)
  └─ 保存上下文
存在? → 分析阶段
  ├─ 读取上下文
  ├─ 增量索引 (10-30秒)
  ├─ Step 1: 提取Git变更
  ├─ Step 2: 加载技术栈规则
  ├─ Step 3: 缺陷检测
  ├─ Step 4: 需求验证
  ├─ Step 5: 影响分析
  └─ Step 6: 生成报告
  ↓
输出: {被分析项目}/analysis-reports/{需求名称}/报告.md
```

### 初始化检测逻辑

```python
if not exists(".code-analyzer/project-context.json"):
    print("首次使用,正在初始化项目...")
    # 执行初始化
    scan_project()
    detect_techstack()
    serena_index()
    save_context()
    print("✅ 项目初始化完成")
else:
    context = load_context()
    if is_stale(context.last_index_time, hours=24):
        print("索引过期,执行增量更新...")
        serena_incremental_update()
    # 继续分析
```

---

## 架构优势

### 1. 技术栈解耦

- 新增语言只需添加 template,不修改核心流程
- 缺陷规则独立维护,易于更新
- 模板优先级机制支持多语言项目

### 2. 状态持久化

- 项目上下文避免重复扫描
- Serena 索引支持增量更新
- 减少90%的准备时间 (首次5分钟 → 后续30秒)

### 3. 职责清晰

- 初始化和分析逻辑分离
- 每个工作流步骤独立文档
- MCP工具按职责分类使用

### 4. 自动化友好

- 自动检测是否需要初始化
- 自动识别技术栈
- 自动确定回归测试范围

### 5. 可扩展性

- 支持多语言 (当前Java,可扩展Python/Node.js)
- 支持多框架 (SpringBoot/Django/Express等)
- 支持自定义缺陷规则

---

## 输出规范

### 报告位置

```
{被分析项目}/
└── analysis-reports/
    ├── 用户登录优化/
    │   ├── feature-login-20251027-100030.md
    │   └── feature-login-20251027-153000.md
    └── 支付流程优化/
        └── feature-payment-20251027-143000.md
```

### 报告内容

- 📋 基本信息 (分支、提交数、变更文件)
- 🔴 缺陷清单 (按严重度分级)
- 🎯 需求实现情况 (已实现/未实现/多余)
- 📊 影响范围 (直接影响/间接影响模块)
- ⚠️ 风险评估 (综合风险等级)
- 💡 测试重点建议

**详细格式**: @references/specs/report-format.md

---

## 扩展示例

### 示例 1: 添加 Python/Django 支持

**步骤 1**: 创建模板

```bash
mkdir -p templates/python-django
```

**步骤 2**: 编写缺陷规则

创建 `templates/python-django/defect-rules.md`,参考 Java 模板结构:

```markdown
# Python + Django 缺陷检测规则

## 🔴 Blocker
### 1. SQL 注入
### 2. 敏感信息泄露

## 🟠 Critical
### 3. 资源泄漏
### 4. 异常处理缺失
...
```

**步骤 3**: 注册模板

编辑 `templates/registry.json`:

```json
{
  "templates": [
    {
      "id": "python-django",
      "name": "Python + Django",
      "detect_files": ["requirements.txt", "manage.py"],
      "detect_dependencies": ["Django"],
      "detect_code_patterns": ["from django", "import django"],
      "paths": {
        "defect_rules": "templates/python-django/defect-rules.md"
      },
      "priority": 2
    },
    ...
  ]
}
```

**步骤 4**: 验证

```bash
# 在 Django 项目中测试
cd /path/to/django-project
# 触发 code-analyzer
```

应自动识别为 Python/Django 并加载对应规则。

---

**版本**: 1.0.0
**创建**: 2025-10-27
