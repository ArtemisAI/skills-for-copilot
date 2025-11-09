# Step 2: 技术栈识别

## 目标

自动识别项目的技术栈,加载对应的缺陷检测规则和最佳实践。

## 支持的技术栈

| 技术栈 | 识别特征 | 规则模板 |
|--------|---------|---------|
| Java + SpringBoot | pom.xml + @SpringBootApplication | @templates/java-springboot/ |

> 🚀 **扩展性**: 架构支持多语言扩展,参见主文档 ARCHITECTURE.md "扩展示例"章节

## 识别流程

### 1. 扫描项目根目录

检查标志性文件:

```bash
# Java 项目
ls pom.xml build.gradle
```

### 2. Java + SpringBoot 识别

**必要条件**:

- 存在 `pom.xml` 或 `build.gradle`
- 包含 `spring-boot-starter` 依赖

**检测命令**:

```bash
# Maven 项目
grep -q "spring-boot-starter" pom.xml && echo "SpringBoot"

# Gradle 项目
grep -q "spring-boot-starter" build.gradle && echo "SpringBoot"

# 检查代码中是否有 @SpringBootApplication
grep -r "@SpringBootApplication" src/
```

**版本检测**:

```bash
# Maven
grep "<spring-boot.version>" pom.xml

# Gradle
grep "springBootVersion" build.gradle
```

## 加载规则模板

根据识别结果,加载对应的规则模板:

### Java + SpringBoot

```
templates/java-springboot/
└── defect-rules.md         # 8大缺陷检测规则
```

## 混合技术栈处理

如果项目包含多种技术栈:

1. 按变更文件的扩展名分组
2. 对每组应用对应的规则
3. 汇总所有检测结果

**示例**: 前后端分离项目

```
src/
├── backend/  (Java + SpringBoot) → 使用 java-springboot 规则
└── frontend/ (React + TypeScript) → 暂不支持,仅记录变更
```

## 输出

识别结果:

```json
{
  "techstack": "java-springboot",
  "version": "3.2.0",
  "build_tool": "maven",
  "template_path": "templates/java-springboot/",
  "confidence": "high",
  "evidence": [
    "pom.xml exists",
    "spring-boot-starter-web found in dependencies",
    "@SpringBootApplication found in src/main/java/Application.java"
  ]
}
```

## MCP 工具使用

**不使用 MCP**: 此步骤仅使用文件扫描和 grep 即可完成。

## 注意事项

1. **多模块项目**: 分别识别每个模块的技术栈
2. **版本兼容**: 注意 SpringBoot 2.x 和 3.x 的差异
3. **微服务**: 如果是微服务,需要识别每个服务的技术栈
4. **本地检查**: 基于本地代码库识别,不需要网络请求

## 常见问题

**Q: 如果识别失败怎么办?**

A: 要求用户明确指定技术栈或提供识别特征。

**Q: 如何支持新的技术栈?**

A: 参见 ARCHITECTURE.md "扩展示例"章节,在 templates/ 目录下新增对应模板。

## 下一步

→ **Step 3**: 缺陷检测 (@step3-defect-detect.md)
