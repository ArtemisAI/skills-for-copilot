# Step 4: 需求验证

## 目标

对比需求文档和代码实现,识别:

- ✅ 已实现的需求
- ❌ 未实现的需求
- ⚠️ 多余实现(不在需求中的功能)

## 输入

**需求文档**: 用户提供的需求描述 (文本/Markdown)

**示例**:

```
需求: 用户登录优化

功能点:
1. 支持手机号登录
2. 支持验证码登录
3. 保留原有用户名密码登录
4. 添加登录失败次数限制
```

## 验证流程

### 1. 解析需求文档

提取需求点:

```json
{
  "requirement_id": "用户登录优化",
  "features": [
    {
      "id": "F1",
      "description": "支持手机号登录",
      "priority": "high"
    },
    {
      "id": "F2",
      "description": "支持验证码登录",
      "priority": "high"
    },
    {
      "id": "F3",
      "description": "保留原有用户名密码登录",
      "priority": "high"
    },
    {
      "id": "F4",
      "description": "添加登录失败次数限制",
      "priority": "medium"
    }
  ]
}
```

### 2. 匹配代码实现

#### 使用 Serena MCP 语义搜索

**F1: 支持手机号登录**

```
查询: "查找处理手机号登录的代码"

结果:
- UserController.java:loginByPhone()
- UserService.java:validatePhone()
```

**F2: 支持验证码登录**

```
查询: "查找发送或验证短信验证码的代码"

结果:
- SmsService.java:sendSmsCode()
- UserService.java:verifySmsCode()
```

**F3: 保留原有用户名密码登录**

```
查询: "查找用户名密码登录的代码"

结果:
- UserController.java:loginByPassword()  # 仍然存在
```

**F4: 添加登录失败次数限制**

```
查询: "查找记录登录失败次数的代码"

结果: 未找到相关代码
```

### 3. 识别多余实现

检查变更中是否有需求文档未提及的功能:

```
查询: "列出本次提交新增的所有 public 方法"

结果:
- loginByPhone() ✓ (需求中有)
- sendSmsCode() ✓ (需求中有)
- loginByThirdParty() ⚠️ (需求中没有)
```

### 4. 使用 Sequential MCP 推理验证

对于复杂需求,使用 Sequential MCP 进行多步推理:

**推理链示例**:

```
需求: "支持手机号登录"

推理步骤:
1. 是否有接收手机号的接口? → 是 (UserController.loginByPhone)
2. 是否验证手机号格式? → 是 (正则表达式验证)
3. 是否发送验证码? → 是 (SmsService.sendSmsCode)
4. 是否验证验证码? → 是 (UserService.verifySmsCode)
5. 是否创建登录会话? → 是 (sessionManager.createSession)

结论: ✅ 需求已完整实现
```

## 验证结果分类

### ✅ 已实现

需求点和代码实现完全匹配:

```json
{
  "feature_id": "F1",
  "description": "支持手机号登录",
  "status": "implemented",
  "evidence": [
    "UserController.loginByPhone() - 接收手机号",
    "UserService.validatePhone() - 验证格式",
    "SmsService.sendSmsCode() - 发送验证码",
    "UserService.verifySmsCode() - 验证验证码"
  ],
  "completeness": "100%"
}
```

### ❌ 未实现

需求点没有对应的代码实现:

```json
{
  "feature_id": "F4",
  "description": "添加登录失败次数限制",
  "status": "not_implemented",
  "reason": "未找到记录登录失败次数的代码",
  "impact": "无法防止暴力破解"
}
```

### ⚠️ 部分实现

需求点有部分实现,但不完整:

```json
{
  "feature_id": "F2",
  "description": "支持验证码登录",
  "status": "partially_implemented",
  "implemented": [
    "发送验证码 (SmsService.sendSmsCode)"
  ],
  "missing": [
    "验证码过期时间检查",
    "验证码重复发送限制"
  ],
  "completeness": "60%"
}
```

### 🔵 多余实现

代码中实现了需求文档未提及的功能:

```json
{
  "feature": "第三方登录 (微信、支付宝)",
  "status": "extra_implementation",
  "code": "UserController.loginByThirdParty()",
  "reason": "需求文档中未提及此功能",
  "suggestion": "确认是否为需求遗漏或过度实现"
}
```

## 输出

需求验证报告:

```json
{
  "requirement_id": "用户登录优化",
  "verification_result": {
    "implemented": [
      {
        "id": "F1",
        "description": "支持手机号登录",
        "completeness": "100%",
        "evidence": ["UserController.loginByPhone()"]
      },
      {
        "id": "F2",
        "description": "支持验证码登录",
        "completeness": "100%",
        "evidence": ["SmsService.sendSmsCode()"]
      },
      {
        "id": "F3",
        "description": "保留原有用户名密码登录",
        "completeness": "100%",
        "evidence": ["UserController.loginByPassword()"]
      }
    ],
    "not_implemented": [
      {
        "id": "F4",
        "description": "添加登录失败次数限制",
        "reason": "未找到相关代码"
      }
    ],
    "extra_features": [
      {
        "description": "第三方登录 (微信、支付宝)",
        "code": "UserController.loginByThirdParty()"
      }
    ]
  },
  "summary": {
    "total_requirements": 4,
    "implemented": 3,
    "not_implemented": 1,
    "extra_features": 1,
    "coverage": "75%"
  }
}
```

## MCP 工具使用

### Serena MCP

**语义搜索**:

```
"查找处理[需求关键词]的代码"
"查找调用[相关方法]的代码"
"列出本次提交新增的所有 public 方法"
```

### Sequential MCP

**复杂推理**:

```
需求: [需求描述]
代码: [相关代码片段]

推理任务:
1. 识别需求的核心功能点
2. 逐一验证代码是否实现
3. 评估实现的完整性
4. 给出验证结论
```

## 注意事项

1. **需求粒度**: 需求描述越详细,验证越准确
2. **隐式需求**: 注意识别隐式需求 (如"支持登录"隐含"登录态管理")
3. **版本兼容**: 验证是否影响现有功能 (如"保留原有登录方式")
4. **本地检查**: 基于本地代码库验证,提测前确认需求覆盖

## 常见问题

**Q: 如果没有需求文档怎么办?**

A: 跳过此步骤,仅进行缺陷检测和影响分析。

**Q: 如何处理需求变更?**

A: 要求用户提供最新需求文档,或明确变更部分。

**Q: 多余实现一定是问题吗?**

A: 不一定,可能是需求遗漏或开发者主动优化,需要与产品确认。

## 下一步

→ **Step 5**: 影响范围分析 (@step5-impact-analysis.md)
