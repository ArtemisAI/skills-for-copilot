---
name: code-analyzer
description: 测试左移工具 - 提测前代码审查,基于 Git diff 识别缺陷、分析影响范围、验证需求实现,自动确定回归测试范围。触发词:分析提交、代码审查、提测检查、回归范围分析。
license: Apache-2.0
---

# Code Analyzer - 精准测试代码审查工具

**测试左移工具** - 在提测前识别问题,确定回归测试范围,输出测试分析报告。

## 设计理念

```
Git 提交变更 → 缺陷检测 + 需求验证 + 影响分析 → 测试分析报告
```

**职责定位**:

- 面向测试工程师,不是开发代码质量工具
- 关注提测前最后一道防线
- 自动化确定回归测试范围

## 核心功能

基于 Git diff 分析代码变更:

1. 🔍 **缺陷识别** - N+1查询、SQL注入、空指针、事务失效等常见缺陷
2. 🎯 **需求验证** - 代码是否实现需求,是否有多余实现
3. 📊 **影响范围** - 直接影响/间接影响模块,确定回归测试范围
4. ⚠️ **风险评估** - 高/中/低风险分级,提供测试优先级建议
5. 📝 **测试报告** - 结构化测试分析报告,面向测试工程师

## 使用场景

**目标用户**: 测试工程师、测试开发、研发人员(提测前自查)

**典型场景**:

```
测试工程师收到提测单:
  - 开发说: "登录功能优化完成,可以测试了"
  - 使用 code-analyzer 分析近期提交
  - 查看报告:
    ✓ 发现2个SQL注入风险
    ✓ 发现1个N+1查询问题
    ✓ 影响3个模块: 登录、用户、订单
    ✓ 回归范围: 需重测登录、用户信息、订单创建
  - 结果: 打回开发修复缺陷,避免测试浪费
```

## 触发条件

```
分析本分支近3次提交

需求: 用户登录优化
【需求描述】
支持手机号+验证码登录,保留原有用户名密码登录...
```

或者:

```
分析 feature/login 分支的提交

需求: 登录优化
...
```

## 工作流程

### 步骤 1: 代码变更提取

提取 Git diff 变更信息,识别修改的文件和方法。

**详细流程**: @references/workflows/step1-code-change.md

### 步骤 2: 技术栈识别

自动识别项目技术栈,加载对应缺陷检测规则。

| 技术栈 | 识别特征 | 规则模板 |
|--------|---------|---------|
| Java + SpringBoot | pom.xml + @SpringBootApplication | @templates/java-springboot/ |

> 🚀 **扩展性**: 架构支持多语言扩展,详见 @ARCHITECTURE.md "扩展示例"

**详细流程**: @references/workflows/step2-techstack-detect.md

### 步骤 3: 缺陷检测

按技术栈规则检测常见缺陷(N+1、SQL注入等)。

**详细流程**: @references/workflows/step3-defect-detect.md

**检测规则**: 根据技术栈加载 templates/{techstack}/defect-rules.md

### 步骤 4: 需求验证

对比需求文档和代码实现,识别未实现/多余实现。

**详细流程**: @references/workflows/step4-requirement-verify.md

### 步骤 5: 影响范围分析

使用 Serena MCP 追踪调用链,确定回归测试范围。

**详细流程**: @references/workflows/step5-impact-analysis.md

**MCP 集成**: @references/integrations/serena-mcp.md

### 步骤 6: 风险评估与报告生成

综合评估风险等级,生成测试分析报告。

**详细流程**: @references/workflows/step6-report-generate.md

**报告格式**: @references/specs/report-format.md

## 输出

**测试分析报告** 保存到被分析项目的根目录:

```
{被分析项目根目录}/analysis-reports/{需求名称}/{分支名}-{日期时间}.md
```

**示例**:
```
实际项目: /home/user/myproject/
报告路径: /home/user/myproject/analysis-reports/用户登录优化/feature-login-20251026-153022.md
```

**报告内容**:

- 📋 基本信息(分支、提交、文件数)
- 🔍 缺陷清单(严重度分级)
- 🎯 需求实现情况
- 📊 影响范围分析
- ⚠️ 回归测试建议
- 💡 测试重点建议

## 技术栈支持

当前支持: **Java + SpringBoot**

识别特征:

- 存在 `pom.xml` 或 `build.gradle`
- 包含 `spring-boot-starter` 依赖
- 代码中有 `@SpringBootApplication` 注解

## MCP 工具集成

### Serena MCP 🔴 必需

**用途**:

- 代码索引(首次使用自动建立)
- 依赖分析(调用链、影响范围)
- 缺陷扫描(语义级检测)

**智能索引**:

- 首次: 自动全量索引(2-5分钟)
- 后续: 增量更新(10-30秒)

### Sequential MCP 🟡 推荐

**用途**:

- 需求验证推理
- 影响范围推导
- 风险评估决策

详细说明: @references/integrations/serena-mcp.md, @references/integrations/sequential-mcp.md

## 缺陷检测能力

支持检测的常见缺陷(Java + SpringBoot):

**🔴 Blocker (阻断级)**:
- ✅ **SQL 注入** - 字符串拼接构造 SQL,动态 ORDER BY
- ✅ **敏感信息泄露** - 硬编码密码、API密钥、加密密钥

**🟠 Critical (严重级)**:
- ✅ **NPE 风险** - 未检查 null、Optional.get()、集合操作
- ✅ **资源泄漏** - 数据库连接、文件流、HTTP客户端未关闭

**🟡 Major (重要级)**:
- ✅ **事务失效** - 同类内部调用、private方法、异常吞没
- ✅ **异常吞没** - 空catch块、仅打印日志
- ✅ **并发问题** - 竞态条件、非线程安全集合、双重检查锁

**🟢 Minor (次要级)**:
- ✅ **N+1 查询** - 循环中执行数据库查询、JPA懒加载

**功能缺陷检测**:
- ✅ **功能完全缺失** - 需求要求的功能未实现
- ✅ **功能实现不完整** - 缺少逻辑分支或边界条件
- ✅ **业务逻辑错误** - 流程顺序错误、规则实现错误

详细规则: @templates/java-springboot/defect-rules.md

## 报告示例

```markdown
# 测试分析报告: 用户登录优化

## 📋 基本信息

- 分支: feature/login-opt
- 提交数: 3 次
- 变更文件: 8 个
- 分析时间: 2025-10-26 15:30

## 🔴 发现缺陷(3个)

### 高风险(2个)

**1. SQL 注入风险**

- 文件: `UserRepository.java:78`
- 代码: `String sql = "SELECT * FROM user WHERE name = '" + name + "'";`
- 影响: 恶意输入可绕过认证
- 建议: 使用参数化查询 `@Query("... WHERE name = :name")`

**2. N+1 查询问题**

- 文件: `OrderService.java:45`
- 代码: 循环中调用 `userRepository.findById()`
- 影响: 性能严重下降
- 建议: 使用批量查询 `findAllById()`

### 中风险(1个)

**3. 事务可能失效**

- 文件: `UserService.java:23`
- 问题: 同类内部调用 @Transactional 方法
- 建议: 拆分到不同 Service 或注入自身代理

## 🎯 需求实现情况

✅ **已实现**(2/3)

- ✅ 支持手机号登录
- ✅ 支持验证码登录

❌ **未实现**(1/3)

- ❌ 第三方登录(微信、支付宝)

## 📊 影响范围分析

**直接影响模块**(3个):

- `UserController` - 新增手机号登录接口
- `UserService` - 登录逻辑变更
- `SmsService` - 验证码发送

**间接影响模块**(2个):

- `OrderController` - 调用了 UserService
- `AdminController` - 调用了 UserService

**回归测试建议范围**:

1. ✅ 登录功能(用户名密码登录、手机号登录)
2. ✅ 用户信息查询
3. ✅ 订单创建(依赖登录态)
4. ⚠️ 管理后台登录(受影响但优先级低)

## ⚠️ 风险评估

**综合风险等级**: 🔴 高风险

**原因**:

- 存在2个高风险缺陷(SQL注入、N+1查询)
- 核心登录逻辑变更,影响面大
- 未实现部分需求

**测试建议**:

1. **优先**: 修复SQL注入和N+1查询问题
2. **重点**: 全面测试登录功能(各种场景)
3. **回归**: 测试订单、用户信息等依赖模块
4. **补充**: 确认第三方登录是否必需

## 💡 测试重点

1. **安全测试**: SQL注入、XSS、认证绕过
2. **性能测试**: 大量用户并发登录
3. **功能测试**: 手机号登录各种场景(验证码过期、重复发送等)
4. **兼容测试**: 原有用户名密码登录不受影响
```

## 使用示例

### 示例 1: 分析近期提交

```
分析本分支近5次提交

需求: 支付流程优化
优化支付流程,支持微信、支付宝、银行卡三种支付方式...
```

**执行流程**:

1. 解析 Git 范围: `HEAD~5..HEAD`
2. Serena 索引检查(如需要则自动索引)
3. 分析变更 + 识别缺陷 + 影响分析
4. 生成报告: `./analysis-reports/支付流程优化/feature-payment-20251026-153022.md`

### 示例 2: 分析特定分支

```
对比 feature/cache 和 main 分支

需求: 引入 Redis 缓存,优化查询性能
```

## 注意事项

1. **首次使用**: Serena MCP 需要建立索引,耗时 2-5 分钟
2. **需求文档**: 提供详细需求可提高验证准确度
3. **报告位置**: 在**被分析项目的根目录**下的 `analysis-reports/` 目录(不是 skill 目录)
4. **技术栈**: 当前仅支持 Java + SpringBoot

## 资源引用

- 工作流程: @references/workflows/
- 缺陷检测规则: @templates/java-springboot/defect-rules.md
- MCP 使用说明: @references/integrations/

---

**版本**: 1.0.0
**创建**: 2025-10-27
**定位**: 测试左移工具,提测前代码审查
