# Step 3: 缺陷检测

## 目标

基于技术栈规则,检测代码变更中的常见缺陷。

## 检测策略

### 1. 加载检测规则

根据 Step 2 识别的技术栈,加载对应规则:

```
templates/{techstack}/defect-rules.md
```

### 2. 静态分析 + 语义检测

**两层检测**:

- **Level 1**: Git diff 文本匹配 (快速,覆盖明显模式)
- **Level 2**: Serena MCP 语义分析 (深度,覆盖隐蔽问题)

## Java + SpringBoot 缺陷检测

### 🔴 Blocker (阻断级)

#### 1. SQL 注入风险

**检测模式**:

```java
// 危险: 字符串拼接 SQL
String sql = "SELECT * FROM user WHERE name = '" + name + "'";

// 危险: 使用 + 或 format 拼接
String sql = String.format("DELETE FROM %s WHERE id = %d", table, id);
```

**检测方法**:

```bash
# Level 1: 文本匹配
git diff HEAD~3..HEAD | grep -E '"\s*(SELECT|INSERT|UPDATE|DELETE).*\+|String\.format.*SELECT'

# Level 2: Serena MCP 语义分析
"查找所有字符串拼接构造 SQL 的代码"
```

**修复建议**:

```java
// 正确: 参数化查询
@Query("SELECT * FROM user WHERE name = :name")
User findByName(@Param("name") String name);
```

#### 2. 敏感信息泄露

**检测模式**:

```java
// 危险: 硬编码密码
String password = "admin123";
String apiKey = "sk-1234567890";
```

**检测方法**:

```bash
# 检测硬编码敏感信息
git diff HEAD~3..HEAD | grep -iE 'password\s*=\s*"[^"]+"'
git diff HEAD~3..HEAD | grep -iE 'apiKey|secretKey|token.*=.*"'
```

### 🟠 Critical (严重级)

#### 3. N+1 查询问题

**检测模式**:

```java
// 危险: 循环中查询数据库
for (Order order : orders) {
    User user = userRepository.findById(order.getUserId());
}
```

**检测方法**:

```bash
# Level 1: 文本匹配循环内的 repository 调用
git diff HEAD~3..HEAD | grep -A 5 "for.*:" | grep "Repository\."

# Level 2: Serena MCP 控制流分析
"查找循环内部调用 JPA Repository 方法的代码"
```

**修复建议**:

```java
// 正确: 批量查询
List<Long> userIds = orders.stream()
    .map(Order::getUserId)
    .collect(Collectors.toList());
List<User> users = userRepository.findAllById(userIds);
```

#### 4. 资源泄漏

**检测模式**:

```java
// 危险: 未关闭资源
FileInputStream fis = new FileInputStream("file.txt");
// ... 没有 finally 或 try-with-resources
```

**检测方法**:

```bash
# 检测未使用 try-with-resources 的流操作
git diff HEAD~3..HEAD | grep -E "new\s+(File|Socket|Connection)" | grep -v "try"
```

### 🟡 Major (重要级)

#### 5. 事务失效

**检测模式**:

```java
@Service
public class UserService {
    @Transactional
    public void updateUser() {
        // 危险: 同类内部调用,事务失效
        this.saveUser();
    }

    @Transactional
    public void saveUser() { }
}
```

**检测方法**:

```bash
# 检测同类中的 this 调用
git diff HEAD~3..HEAD | grep -E "this\.\w+\(" | grep -B 10 "@Transactional"
```

**修复建议**:

```java
// 方案1: 拆分到不同 Service
// 方案2: 注入自身代理
@Autowired
private UserService self;
```

#### 6. 异常吞没

**检测模式**:

```java
// 危险: catch 后仅打印,不处理
try {
    riskyOperation();
} catch (Exception e) {
    e.printStackTrace();  // 仅打印,不处理
}
```

**检测方法**:

```bash
# 检测空 catch 块或仅 printStackTrace
git diff HEAD~3..HEAD | grep -A 3 "catch.*Exception" | grep -E "printStackTrace|^}"
```

#### 7. 空指针风险

**检测模式**:

```java
// 危险: 未判空直接调用
User user = userRepository.findById(id);
String name = user.getName();  // user 可能为 null
```

**检测方法**:

```bash
# Level 2: Serena MCP 数据流分析
"查找可能返回 null 的方法调用,且后续未进行空值检查"
```

### 🟢 Minor (次要级)

#### 8. 循环依赖

**检测模式**:

```java
@Service
public class UserService {
    @Autowired
    private OrderService orderService;  // 相互依赖
}

@Service
public class OrderService {
    @Autowired
    private UserService userService;
}
```

**检测方法**:

使用 Serena MCP 依赖图分析。

## 检测流程

### 1. 快速文本扫描 (Level 1)

对 Git diff 结果进行模式匹配:

```bash
# 提取新增和修改的代码
git diff HEAD~3..HEAD | grep "^+" | grep -v "^+++"

# 应用检测规则
grep -E "pattern1|pattern2|pattern3"
```

### 2. 深度语义分析 (Level 2)

使用 Serena MCP 进行:

- 控制流分析 (循环、条件)
- 数据流分析 (变量传递)
- 依赖图分析 (调用链)
- 符号执行 (路径分析)

### 3. 缺陷分级

按严重度分类:

- 🔴 Blocker: 必须修复,阻塞提测
- 🟠 Critical: 优先修复,高风险
- 🟡 Major: 计划修复,中风险
- 🟢 Minor: 择机修复,低风险

## 输出

缺陷清单:

```json
{
  "defects": [
    {
      "id": "SQL-001",
      "severity": "blocker",
      "type": "SQL注入",
      "file": "src/main/java/UserRepository.java",
      "line": 78,
      "code": "String sql = \"SELECT * FROM user WHERE name = '\" + name + \"'\";",
      "description": "使用字符串拼接构造 SQL,存在注入风险",
      "impact": "恶意输入可绕过认证,访问或篡改数据",
      "suggestion": "使用参数化查询: @Query(\"... WHERE name = :name\")",
      "reference": "OWASP A03:2021 - Injection"
    },
    {
      "id": "NPL-001",
      "severity": "major",
      "type": "N+1查询",
      "file": "src/main/java/OrderService.java",
      "line": 45,
      "code": "User user = userRepository.findById(order.getUserId());",
      "description": "循环中调用 Repository 方法,产生 N+1 查询",
      "impact": "性能严重下降,数据库连接池耗尽",
      "suggestion": "使用批量查询: findAllById(userIds)"
    }
  ],
  "summary": {
    "total": 5,
    "blocker": 2,
    "critical": 1,
    "major": 2,
    "minor": 0
  }
}
```

## MCP 工具使用

### Serena MCP

**索引检查**:

```bash
# 检查是否已索引
serena-cli status

# 如需索引
serena-cli index --incremental
```

**语义查询**:

```
查询: "查找循环内部调用 JPA Repository 方法的代码"
查询: "查找可能返回 null 的方法调用"
查询: "查找 @Transactional 方法内部的 this 调用"
```

## 注意事项

1. **误报处理**: 对于误报,提供"忽略"机制
2. **规则更新**: 缺陷规则需要定期更新
3. **性能优化**: Level 1 快速扫描,Level 2 按需深度分析
4. **本地检查**: 在本地执行,提测前发现问题

## 常见问题

**Q: 如何减少误报?**

A: 结合 Level 1 和 Level 2,Level 1 发现的可疑代码由 Level 2 确认。

**Q: 如何处理框架特定的安全模式?**

A: 在 best-practices.md 中记录框架的安全 API。

## 下一步

→ **Step 4**: 需求验证 (@step4-requirement-verify.md)
