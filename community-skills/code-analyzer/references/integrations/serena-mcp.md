# Serena MCP 集成指南

## 简介

Serena 是基于 LSP (Language Server Protocol) 的代码理解工具,提供符号级的代码分析能力。

**核心优势**:
- ✅ 符号级理解 (像 IDE 一样理解代码)
- ✅ 精确的引用查找 (调用链追踪)
- ✅ 节省 Token (社区报告节省 70% token)
- ✅ 多语言支持 (Python, Java, TypeScript, Go, Rust等)

## 在 code-analyzer 中的使用

### Step 3: 缺陷检测 (Level 2 深度检测)

使用 Serena 进行语义级缺陷检测。

### Step 4: 需求验证

使用 Serena 查找需求相关的代码实现。

### Step 5: 影响范围分析

使用 Serena 追踪调用链和依赖关系。

---

## 项目初始化

### 检查项目是否已索引

```
检查当前项目索引状态
```

### 建立项目索引 (首次使用)

**命令行方式** (推荐在项目初始化时执行):

```bash
uvx --from git+https://github.com/oraios/serena serena project index
```

**耗时**: 2-5 分钟 (取决于项目大小)

**后续使用**: 自动增量更新 (10-30秒)

### 项目激活

Serena 需要激活项目才能使用:

```
激活项目 /path/to/project
```

或者在 MCP 配置时使用 `--project $(pwd)` 自动激活。

---

## 核心工具

### 1. 符号查找 - find_symbol

**用途**: 查找函数、类、变量的定义

**code-analyzer 使用场景**:

#### Step 3: 缺陷检测

**查找循环中的数据库查询** (N+1 问题):

```
使用 find_symbol 查找所有名为 "findById" 或 "findByXxx" 的方法调用
```

**查找字符串拼接的 SQL** (SQL 注入):

```
使用 search_for_pattern 查找包含 "SELECT.*+" 或 "String.format.*SELECT" 的代码
然后用 find_symbol 定位到具体的函数
```

**查找事务方法** (事务失效):

```
使用 find_symbol 查找所有带 @Transactional 注解的方法
```

#### Step 4: 需求验证

**查找需求相关的代码**:

```
需求: "支持手机号登录"

任务:
1. 使用 find_symbol 查找名为 "phone" 或 "mobile" 的方法
2. 使用 find_symbol 查找名为 "sms" 或 "verificationCode" 的方法
3. 使用 find_symbol 查找名为 "login" 相关的方法
```

**返回结果示例**:

```
找到的符号:
1. loginByPhone() - src/controller/UserController.java:45
2. sendSmsCode() - src/service/SmsService.java:23
3. verifySmsCode() - src/service/UserService.java:67
```

### 2. 引用查找 - find_referencing_symbols

**用途**: 查找谁调用了这个函数/类

**code-analyzer 使用场景**:

#### Step 5: 影响范围分析

**向上追踪** (谁调用了它):

```
变更: UserService.login() 方法修改

任务:
使用 find_referencing_symbols 查找所有调用 UserService.login() 的代码
```

**返回结果示例**:

```
引用位置:
1. UserController.login() - line 123
2. AdminController.adminLogin() - line 45
3. OAuth2Handler.handleCallback() - line 89
```

**多层追踪**:

```
任务:
1. UserController.login() 被谁调用? → API Gateway
2. UserService 被谁调用? → OrderService, AdminService
3. OrderService 被谁调用? → OrderController
```

### 3. 文件符号概览 - get_symbols_overview

**用途**: 快速了解文件结构

**code-analyzer 使用场景**:

#### Step 1: 代码变更分析

```
任务:
对于变更的文件 UserController.java,
使用 get_symbols_overview 获取文件的顶层结构
```

**返回示例**:

```
文件: UserController.java

Class: UserController (line 10-150)
  Method: loginByPassword (line 25-35)
  Method: loginByPhone (line 40-55)
  Method: logout (line 60-70)

Class: LoginRequest (line 155-170)
  Field: username (line 157)
  Field: password (line 158)
```

### 4. 文本搜索 - search_for_pattern

**用途**: 搜索文本模式

**code-analyzer 使用场景**:

#### Step 3: 缺陷检测

**查找 SQL 注入模式**:

```
使用 search_for_pattern 在项目中搜索:
- 模式: "SELECT.*\\+"
- 模式: "String\\.format.*SELECT"
- 路径: src/
```

**查找硬编码密码**:

```
使用 search_for_pattern 搜索:
- 模式: "password\\s*=\\s*\"[^\"]+\""
- 模式: "apiKey\\s*=\\s*\"[^\"]+\""
```

---

## 使用模式

### 模式 1: 缺陷检测 (Step 3)

**Level 1: 快速文本扫描**

```bash
git diff HEAD~3..HEAD | grep -E "SQL.*\+"
```

**Level 2: Serena 语义分析**

```
任务: 深度检测 N+1 查询问题

步骤:
1. 使用 find_symbol 查找所有 Repository 方法
2. 使用 find_referencing_symbols 查找这些方法的调用位置
3. 分析调用位置是否在循环内 (通过 get_symbols_overview 查看上下文)
4. 识别 N+1 查询模式
```

### 模式 2: 需求验证 (Step 4)

```
需求: "支持手机号登录"

Serena 验证流程:
1. 使用 find_symbol 查找 "phone" 或 "mobile" 相关的方法
   → 找到: loginByPhone(), validatePhone()

2. 使用 find_symbol 查找 "sms" 或 "verificationCode" 相关的方法
   → 找到: sendSmsCode(), verifySmsCode()

3. 使用 find_referencing_symbols 验证这些方法是否被调用
   → loginByPhone() 被 UserController 调用 ✓
   → sendSmsCode() 被 UserService 调用 ✓

结论: ✅ 需求已实现
```

### 模式 3: 影响范围分析 (Step 5)

```
变更: UserService.login() 方法修改

Serena 影响分析:
1. 使用 find_referencing_symbols 查找直接调用者
   → UserController, AdminController

2. 对每个调用者,继续使用 find_referencing_symbols
   → UserController 被 API Gateway 调用
   → AdminController 被 AdminAPI 调用

3. 使用 find_symbol 查找 UserService 的其他方法
   → getUser(), validateUser()

4. 使用 find_referencing_symbols 查找这些方法的调用者
   → OrderService, ReportService

结论:
- 直接影响: UserController, AdminController
- 间接影响: OrderService, ReportService
```

---

## 最佳实践

### 1. 项目准备

```bash
# 1. 首次使用时建立索引
uvx --from git+https://github.com/oraios/serena serena project index

# 2. 激活项目 (如果配置了 --project 则自动激活)
# 否则手动激活:
激活项目 /path/to/project
```

### 2. 高效查询

**✅ 好的查询**:

```
使用 find_symbol 查找名为 "authenticate" 的函数
然后使用 find_referencing_symbols 查找所有调用位置
```

**❌ 低效查询**:

```
帮我看看整个项目的认证代码  # 太宽泛,会读取大量文件
```

### 3. 分步骤执行

```
步骤 1: 使用 find_symbol 查找函数定义
步骤 2: 使用 get_symbols_overview 查看上下文
步骤 3: 使用 find_referencing_symbols 追踪调用链
步骤 4: 综合分析影响范围
```

### 4. Token 节省

| 操作 | Token 消耗 | 建议 |
|------|-----------|------|
| read_file(整个文件) | 高 (~5000) | 使用 get_symbols_overview |
| grep "pattern" | 高 | 使用 find_symbol 或 search_for_pattern |
| find_symbol + find_referencing_symbols | 低 (~500) | ✅ 首选 |

---

## 常见问题

### Q: 如何检查项目是否已索引?

A: 使用查询命令:

```
检查当前项目索引状态
```

### Q: 索引需要多久?

A:
- 首次全量索引: 2-5 分钟
- 后续增量更新: 10-30 秒 (自动)

### Q: 索引失败怎么办?

A: 检查项目是否可编译:

```bash
# Java 项目
mvn compile

# Python 项目
python -m compileall src/
```

### Q: 如何查看 Serena 可用工具?

A:

```
列出 Serena 的所有工具
```

---

## code-analyzer 集成清单

在实现 code-analyzer 时使用的 Serena 工具:

- [x] **find_symbol** - Step 3 缺陷检测, Step 4 需求验证
- [x] **find_referencing_symbols** - Step 5 影响范围分析
- [x] **get_symbols_overview** - Step 1 代码变更分析
- [x] **search_for_pattern** - Step 3 缺陷检测 (文本模式)
- [x] **项目索引** - 初始化阶段 (project index 命令)

---

## 参考资源

- Serena GitHub: https://github.com/oraios/serena
- LSP 协议: https://microsoft.github.io/language-server-protocol/

---

**版本**: 1.0.0
**创建**: 2025-10-27
**适用**: code-analyzer 项目
