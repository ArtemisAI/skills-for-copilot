# Step 5: 影响范围分析

## 目标

确定代码变更的影响范围,自动生成回归测试范围建议。

## 核心概念

### 直接影响

被修改的代码本身:

- 修改的类
- 修改的方法
- 修改的接口

### 间接影响

调用或依赖被修改代码的模块:

- 调用链上游 (谁调用了它)
- 依赖关系 (谁依赖它)
- 数据流传播 (数据如何流动)

## 分析流程

### 1. 识别变更的核心模块

从 Step 1 的变更文件中提取核心模块:

```json
{
  "changed_modules": [
    {
      "file": "UserController.java",
      "class": "UserController",
      "methods": ["loginByPhone", "sendSmsCode"]
    },
    {
      "file": "UserService.java",
      "class": "UserService",
      "methods": ["validatePhone", "verifySmsCode"]
    },
    {
      "file": "SmsService.java",
      "class": "SmsService",
      "methods": ["sendSmsCode"],
      "new": true
    }
  ]
}
```

### 2. 使用 Serena MCP 追踪调用链

#### 向上追踪 (谁调用了它)

**查询**: "查找调用 UserController.loginByPhone 的代码"

```
调用链:
API Gateway → UserController.loginByPhone()
```

**查询**: "查找调用 UserService 的所有代码"

```
调用链:
UserController → UserService
OrderController → UserService  # 间接影响!
AdminController → UserService  # 间接影响!
```

#### 向下追踪 (它调用了谁)

**查询**: "查找 UserService 调用的所有方法"

```
依赖链:
UserService → UserRepository
UserService → SmsService
UserService → RedisTemplate
```

### 3. 构建依赖图

使用 Serena MCP 构建完整的依赖关系图:

```
┌─────────────────┐
│  UserController │ ← 直接影响
└────────┬────────┘
         │ 调用
┌────────▼────────┐
│   UserService   │ ← 直接影响
└────────┬────────┘
         │ 调用
    ┌────┴────┬──────────┬─────────┐
    │         │          │         │
┌───▼──┐  ┌──▼───┐  ┌───▼────┐ ┌──▼──────┐
│ Repo │  │ SMS  │  │ Redis  │ │ Session │
└──────┘  └──┬───┘  └────────┘ └─────────┘
             │ ← 直接影响 (新增)
             │
       ┌─────┴──────┐
       │            │
┌──────▼────┐  ┌───▼──────────┐
│OrderCtrl  │  │ AdminCtrl    │ ← 间接影响
└───────────┘  └──────────────┘
```

### 4. 数据流分析

追踪数据的流向:

**场景**: 修改了 `User` 实体的字段

```
数据流:
UserController → UserService → UserRepository → Database
                     ↓
                OrderService (使用 User 数据) ← 间接影响!
```

### 5. 计算影响范围

#### 直接影响模块

```json
{
  "direct_impact": [
    {
      "module": "UserController",
      "reason": "修改了 loginByPhone 方法",
      "risk": "high"
    },
    {
      "module": "UserService",
      "reason": "修改了登录逻辑",
      "risk": "high"
    },
    {
      "module": "SmsService",
      "reason": "新增模块",
      "risk": "medium"
    }
  ]
}
```

#### 间接影响模块

```json
{
  "indirect_impact": [
    {
      "module": "OrderController",
      "reason": "调用了 UserService 获取用户信息",
      "impact_path": "OrderController → UserService",
      "risk": "medium"
    },
    {
      "module": "AdminController",
      "reason": "调用了 UserService 进行权限验证",
      "impact_path": "AdminController → UserService",
      "risk": "low"
    }
  ]
}
```

## 回归测试范围建议

### 1. 功能测试范围

根据影响范围生成测试建议:

```markdown
## 回归测试范围

### 🔴 必须测试 (直接影响)

1. **用户登录功能**
   - 手机号登录 (新增功能)
   - 验证码登录 (新增功能)
   - 用户名密码登录 (原有功能,确保不受影响)

2. **用户服务**
   - 用户信息查询
   - 用户状态管理

3. **短信服务**
   - 验证码发送
   - 验证码验证

### 🟡 建议测试 (间接影响)

4. **订单功能**
   - 订单创建 (依赖用户登录态)
   - 订单查询 (依赖用户信息)

5. **管理后台**
   - 管理员登录 (使用相同的 UserService)
   - 用户管理功能

### 🟢 可选测试 (低风险)

6. **用户相关报表**
   - 用户统计报表 (仅读取用户数据)
```

### 2. 测试优先级

按风险等级排序:

```json
{
  "regression_scope": [
    {
      "priority": 1,
      "risk": "high",
      "module": "用户登录",
      "test_cases": [
        "手机号登录 - 正常流程",
        "手机号登录 - 异常场景 (格式错误、验证码错误)",
        "用户名密码登录 - 确保原有功能正常"
      ]
    },
    {
      "priority": 2,
      "risk": "medium",
      "module": "订单创建",
      "test_cases": [
        "订单创建 - 验证登录态有效性"
      ]
    },
    {
      "priority": 3,
      "risk": "low",
      "module": "管理后台",
      "test_cases": [
        "管理员登录 - 确保不受影响"
      ]
    }
  ]
}
```

## 输出

影响范围分析报告:

```json
{
  "impact_analysis": {
    "direct_impact": {
      "modules": ["UserController", "UserService", "SmsService"],
      "count": 3
    },
    "indirect_impact": {
      "modules": ["OrderController", "AdminController"],
      "count": 2
    },
    "call_chains": [
      "API Gateway → UserController → UserService → UserRepository",
      "OrderController → UserService → UserRepository",
      "AdminController → UserService → UserRepository"
    ],
    "data_flow": [
      "User 实体 → OrderService (订单创建)",
      "User 实体 → ReportService (报表生成)"
    ]
  },
  "regression_scope": {
    "must_test": [
      {
        "module": "用户登录",
        "priority": 1,
        "reason": "核心变更,直接影响"
      }
    ],
    "should_test": [
      {
        "module": "订单创建",
        "priority": 2,
        "reason": "依赖用户登录态,间接影响"
      }
    ],
    "optional_test": [
      {
        "module": "管理后台",
        "priority": 3,
        "reason": "低风险,可择机测试"
      }
    ]
  }
}
```

## MCP 工具使用

### Serena MCP

**调用链追踪**:

```
"查找调用 UserService 的所有代码"
"查找 UserController 调用的所有方法"
"构建 UserService 的完整依赖图"
```

**依赖分析**:

```
"查找使用 User 实体的所有服务"
"查找依赖 SmsService 的模块"
```

**影响评估**:

```
"如果修改 UserService.validatePhone,会影响哪些模块?"
```

## 注意事项

1. **传递依赖**: 注意多层调用链的影响 (A → B → C)
2. **异步调用**: 消息队列、事件驱动的影响难以追踪
3. **动态调用**: 反射、动态代理的调用链难以静态分析
4. **本地分析**: 基于本地代码库分析,不依赖运行时数据

## 常见问题

**Q: 如何处理微服务的跨服务影响?**

A: 当前版本仅分析单体应用,微服务需要额外的服务依赖图。

**Q: 如何减少回归测试范围?**

A: 根据风险等级和优先级,聚焦高风险直接影响模块。

**Q: 如何验证影响分析的准确性?**

A: 结合 Serena MCP 的语义分析和静态代码扫描,交叉验证。

## 下一步

→ **Step 6**: 风险评估与报告生成 (@step6-report-generate.md)
